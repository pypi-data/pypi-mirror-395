"""
CLI Command Handlers
"""

from pathlib import Path
import shutil
import subprocess

from .utils.exceptions import ErrorMessages
from .utils.logger import get_logger

# Define constants locally to avoid circular import
DOCGEN_DIR = Path(__file__).parent.resolve()

logger = get_logger("docgen")


class InitHandler:
    """Handler for the 'init' command"""

    def handle(self, force: bool, project_root: Path, quiet: bool = False) -> int:
        """
        Initialize the project

        Args:
            force: Force overwrite existing files
            project_root: Project root directory
            quiet: Suppress detailed messages

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        docgen_dir = project_root / "docgen"
        config_file = docgen_dir / "config.toml"

        # Check existing files
        if config_file.exists() and not force:
            logger.warning(
                f"Config file already exists: {config_file}\nUse --force flag to overwrite."
            )
            return 1

        # Create docgen directory
        docgen_dir.mkdir(parents=True, exist_ok=True)

        # Source directory in package
        package_docgen_dir = DOCGEN_DIR

        try:
            # 1. Copy config.toml.sample to config.toml
            source_config = package_docgen_dir / "config.toml.sample"
            if source_config.exists():
                shutil.copy2(source_config, config_file)
                if not quiet:
                    logger.info(f"✓ Created config file: {config_file}")
            else:
                logger.error(f"Source file not found: {source_config}")
                return 1

            # 2. Copy templates directory
            self._copy_directory_contents(
                package_docgen_dir / "templates",
                docgen_dir / "templates",
                quiet=quiet,
                description="Templates",
            )

            # 3. Copy prompts directory
            self._copy_directory_contents(
                package_docgen_dir / "prompts",
                docgen_dir / "prompts",
                quiet=quiet,
                description="Prompts",
            )

            # 4. Copy hooks directory (with execution permissions)
            hooks_copied = self._copy_directory_contents(
                package_docgen_dir / "hooks",
                docgen_dir / "hooks",
                quiet=quiet,
                description="Git hooks",
            )

            # Grant execution permissions to hooks files
            if hooks_copied:
                hooks_dir = docgen_dir / "hooks"
                for hook_file in hooks_dir.iterdir():
                    if hook_file.is_file():
                        hook_file.chmod(0o755)

            if not quiet:
                logger.info("✓ Project initialization completed")

            return 0

        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            return 1

    def _copy_directory_contents(
        self, source_dir: Path, dest_dir: Path, quiet: bool = False, description: str = "Files"
    ) -> bool:
        """Copy directory contents"""
        if not source_dir.exists():
            logger.warning(f"Source directory not found: {source_dir}")
            return False

        dest_dir.mkdir(parents=True, exist_ok=True)

        try:
            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, dest_dir / item.name)

            if not quiet:
                file_count = len(list(dest_dir.iterdir()))
                logger.info(f"✓ Copied {description}: {file_count} files")

            return True

        except Exception as e:
            logger.error(f"Error copying {description}: {e}")
            return False


class BuildIndexHandler:
    """Handler for the 'build-index' command"""

    def handle(self, project_root: Path, config: dict) -> int:
        """
        Build RAG index

        Args:
            project_root: Project root directory
            config: Configuration dictionary

        Returns:
            Exit code
        """
        try:
            from .rag.chunker import CodeChunker
            from .rag.embedder import Embedder
            from .rag.indexer import VectorIndexer

            logger.info("Starting RAG index construction...")

            # Get RAG config
            rag_config = config.get("rag", {})

            # 1. Chunk codebase
            logger.info("Step 1/3: Chunking codebase...")
            chunker = CodeChunker(rag_config)
            chunks = chunker.chunk_codebase(project_root)

            if not chunks:
                logger.warning("No chunks found")
                return 1

            logger.info(f"✓ Created {len(chunks)} chunks")

            # 2. Generate embeddings
            logger.info("Step 2/3: Generating embeddings...")
            embedder = Embedder(rag_config)

            # Extract text from chunks
            texts = [chunk["text"] for chunk in chunks]

            # Generate embeddings in batch
            embeddings = embedder.embed_batch(texts, batch_size=32)

            logger.info(f"✓ Generated {len(embeddings)} embeddings")

            # 3. Build index
            logger.info("Step 3/3: Building index...")
            index_dir = project_root / "docgen" / "index"
            indexer = VectorIndexer(
                index_dir=index_dir,
                embedding_dim=embedder.embedding_dim,
                config=rag_config,
            )

            # Build index
            indexer.build(embeddings, chunks)

            # Save
            indexer.save()

            logger.info(f"✓ Saved index: {index_dir}")
            logger.info("=" * 60)
            logger.info("RAG index construction completed!")
            logger.info("=" * 60)
            logger.info(f"Index directory: {index_dir}")
            logger.info(f"Chunk count: {len(chunks)}")
            logger.info(f"Embedding dim: {embedder.embedding_dim}")
            logger.info("")
            logger.info("Generate docs with RAG using:")
            logger.info("  uv run python -m docgen.docgen --use-rag")

            return 0

        except ImportError as e:
            logger.error(
                f"Failed to import RAG modules: {e}\n"
                "Please install RAG dependencies: uv sync --extra rag"
            )
            return 1
        except Exception as e:
            logger.error(f"Error building index: {e}", exc_info=True)
            return 1


class HooksHandler:
    """Handler for the 'hooks' command"""

    def handle(self, args, project_root: Path) -> int:
        """
        Handle Git hooks management actions

        Args:
            args: Parsed arguments
            project_root: Project root directory

        Returns:
            Exit code
        """
        action = args.hooks_action

        if action == "run":
            return self._handle_run(args)

        git_hooks_dir = project_root / ".git" / "hooks"
        docgen_hooks_dir = project_root / "docgen" / "hooks"

        if not docgen_hooks_dir.exists():
            logger.error(ErrorMessages.HOOKS_DIR_NOT_FOUND)
            return 1

        if action == "list":
            return self._handle_list(project_root)

        elif action == "validate":
            return self._handle_validate(project_root)

        hook_names = ["pre-commit", "post-commit", "pre-push", "commit-msg"]
        target_hooks = [args.hook_name] if args.hook_name else hook_names

        if action == "enable":
            return self._enable_hooks(git_hooks_dir, docgen_hooks_dir, target_hooks)
        elif action == "disable":
            return self._disable_hooks(git_hooks_dir, target_hooks)
        else:
            logger.error(f"Unknown action: {action}")
            return 1

    def _handle_run(self, args) -> int:
        """Handle 'run' action"""
        try:
            from .hooks.orchestrator import HookOrchestrator

            orchestrator = HookOrchestrator(args.hook_name, args.hook_args)

            # Register tasks
            from .hooks.tasks.commit_msg_generator import CommitMsgGeneratorTask
            from .hooks.tasks.doc_generator import DocGeneratorTask
            from .hooks.tasks.file_stager import FileStagerTask
            from .hooks.tasks.rag_generator import RagGeneratorTask
            from .hooks.tasks.test_runner import TestRunnerTask
            from .hooks.tasks.version_checker import VersionCheckerTask

            orchestrator.register_task("run_tests", TestRunnerTask)
            orchestrator.register_task("generate_docs", DocGeneratorTask)
            orchestrator.register_task("generate_rag", RagGeneratorTask)
            orchestrator.register_task("stage_changes", FileStagerTask)
            orchestrator.register_task("generate_commit_message", CommitMsgGeneratorTask)
            orchestrator.register_task("check_version", VersionCheckerTask)

            return orchestrator.run()
        except ImportError as e:
            logger.error(f"Failed to load hook orchestrator: {e}")
            return 1

    def _handle_list(self, project_root: Path) -> int:
        """Handle 'list' action"""
        print("\nAvailable Git hooks:")
        print(f"  Config file: {project_root}/docgen/hooks.toml")
        print("-" * 40)

        try:
            from .hooks.config import ConfigLoader

            loader = ConfigLoader(str(project_root))
            hooks = loader.load_config()
            for name, hook_config in hooks.items():
                status = "Enabled" if hook_config.enabled else "Disabled"
                print(f"  {name}: {status}")
                for task in hook_config.tasks:
                    task_status = "Enabled" if task.enabled else "Disabled"
                    print(f"    - {task.name}: {task_status}")
        except Exception as e:
            print(f"  Config load error: {e}")
        print("-" * 40)
        return 0

    def _handle_validate(self, project_root: Path) -> int:
        """Handle 'validate' action"""
        print("Validating hook config...")
        try:
            from .hooks.config import ConfigLoader

            loader = ConfigLoader(str(project_root))
            config = loader.load_config()
            print("✓ Config file is valid TOML")
            print(f"✓ Found {len(config)} hook definitions")
            return 0
        except Exception as e:
            print(f"✗ Validation error: {e}")
            return 1

    def _enable_hooks(self, git_hooks_dir, docgen_hooks_dir, hook_names):
        """Enable hooks"""

        git_hooks_dir.mkdir(parents=True, exist_ok=True)

        for hook_name in hook_names:
            source_file = docgen_hooks_dir / hook_name
            hook_file = git_hooks_dir / hook_name

            if not source_file.exists():
                logger.warning(
                    ErrorMessages.HOOK_SOURCE_NOT_FOUND.format(
                        hook_name=hook_name, source_file=source_file
                    )
                )
                continue

            # Backup existing hook
            if hook_file.exists() and not self._is_docgen_hook(hook_file):
                backup_file = hook_file.with_suffix(
                    f"{hook_file.suffix}.backup.{subprocess.run(['date', '+%Y%m%d_%H%M%S'], capture_output=True, text=True).stdout.strip()}"
                )
                shutil.copy2(hook_file, backup_file)
                logger.info(f"Backed up existing {hook_name} hook: {backup_file}")

            # Add hook
            if not self._is_docgen_hook(hook_file):
                with open(hook_file, "a") as f:
                    if not hook_file.exists() or not self._has_shebang(hook_file):
                        f.write("#!/bin/bash\n")
                    f.write(f"\n# docgen - {hook_name} hook\n")
                    with open(source_file) as src:
                        f.write(src.read())
                hook_file.chmod(0o755)
                logger.info(f"✓ Installed {hook_name} hook")
            else:
                logger.info(f"✓ {hook_name} hook is already installed")

        logger.info("Enabled Git hooks")
        return 0

    def _disable_hooks(self, git_hooks_dir, hook_names):
        """Disable hooks"""

        for hook_name in hook_names:
            hook_file = git_hooks_dir / hook_name
            disabled_file = hook_file.with_suffix(f"{hook_file.suffix}.disabled")

            if hook_file.exists():
                if self._is_docgen_hook(hook_file):
                    shutil.move(hook_file, disabled_file)
                    logger.info(f"✓ Disabled {hook_name} hook")
                else:
                    logger.info(f"✓ {hook_name} hook is not a docgen hook (ignored)")
            else:
                logger.info(f"✓ {hook_name} hook does not exist")

        logger.info("Disabled Git hooks")
        return 0

    def _is_docgen_hook(self, hook_file):
        """Check if hook file is a docgen hook"""
        try:
            with open(hook_file) as f:
                return "# docgen" in f.read()
        except FileNotFoundError:
            return False

    def _has_shebang(self, hook_file):
        """Check if hook file has a shebang"""
        try:
            with open(hook_file) as f:
                first_line = f.readline().strip()
                return first_line.startswith("#!")
        except FileNotFoundError:
            return False
