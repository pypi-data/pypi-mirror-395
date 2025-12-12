"""
Test command collector module
Collects test commands from various configuration files.
"""

from pathlib import Path
from typing import Any

from ..utils.file_utils import safe_read_json
from ..utils.logger import get_logger
from .collector_utils import BuildCommandCollector


class TestingCommandScanner:
    """Test command scanner class"""

    SCRIPTS_DIR = "scripts"
    RUN_TESTS_SCRIPT = "run_tests.sh"
    MAKEFILE_NAMES = ["Makefile", "makefile"]
    PYTEST_INI = "pytest.ini"
    PACKAGE_JSON = "package.json"

    def __init__(
        self,
        project_root: Path,
        package_managers: dict[str, str] | None = None,
        logger: Any | None = None,
    ):
        """
        Initialize

        Args:
            project_root: Project root directory
            package_managers: Dictionary of detected package managers
            logger: Logger instance
        """
        self.project_root = project_root
        self.package_managers = package_managers or {}
        self.logger = logger or get_logger(__name__)
        self.build_collector = BuildCommandCollector(project_root, package_managers)

    def collect_test_commands(self) -> list[str]:
        """
        Collect test commands

        Returns:
            List of test commands
        """
        commands = []

        # Collect from scripts/run_tests.sh
        run_tests_script = self.project_root / self.SCRIPTS_DIR / self.RUN_TESTS_SCRIPT
        if run_tests_script.exists():
            # If the script exists, it's the primary test command
            # We can read it to see what it does, or just return the script execution
            # For now, let's return the content if it's a single line command, or the script itself
            try:
                content = run_tests_script.read_text(encoding="utf-8").strip()
                lines = [
                    line
                    for line in content.splitlines()
                    if line.strip() and not line.startswith("#")
                ]
                if len(lines) == 1:
                    command = lines[0]
                    command = self.build_collector._add_uv_run_if_needed(command)
                    commands.append(command)
                else:
                    # If it's a complex script, return the script execution command
                    commands.append(f"bash {self.SCRIPTS_DIR}/{self.RUN_TESTS_SCRIPT}")
            except Exception:
                pass

        # Collect from Makefile
        makefile = self.project_root / self.MAKEFILE_NAMES[0]
        if makefile.exists():
            content = makefile.read_text(encoding="utf-8")
            # Extract command line for test target
            in_test_target = False
            for line in content.split("\n"):
                if line.strip() == "test:":
                    in_test_target = True
                elif line.strip().endswith(":") and in_test_target:
                    break  # Next target
                elif in_test_target and line.startswith("\t") and line.strip():
                    command = line.lstrip("\t")
                    if command and not command.startswith("@"):
                        command = self.build_collector._add_uv_run_if_needed(command)
                        commands.append(command)

        # For Python projects
        if "python" in self.package_managers:
            pm = self.package_managers["python"]
            if pm == "uv":
                commands.append("uv run pytest tests/ -v --tb=short")
            elif pm == "poetry":
                commands.append("poetry run pytest tests/ -v --tb=short")
            else:  # pip
                commands.append("pytest tests/ -v --tb=short")
        # Collect from pytest.ini (if package manager is not specified)
        elif (self.project_root / self.PYTEST_INI).exists():
            command = "pytest tests/ -v --tb=short"
            command = self.build_collector._add_uv_run_if_needed(command)
            commands.append(command)

        # Collect from package.json
        if (self.project_root / self.PACKAGE_JSON).exists():
            package_data = safe_read_json(self.project_root / self.PACKAGE_JSON)
            if package_data and "scripts" in package_data and "test" in package_data["scripts"]:
                pm = self.package_managers.get("javascript", "npm")
                if pm == "pnpm":
                    commands.append("pnpm test")
                elif pm == "yarn":
                    commands.append("yarn test")
                else:  # npm
                    commands.append("npm test")

        # For Go projects
        if "go" in self.package_managers and (self.project_root / "go.mod").exists():
            pm = self.package_managers["go"]
            if pm == "go":
                commands.append("go test ./...")

        # Deduplicate preserving order
        seen = set()
        unique_commands = []
        for c in commands:
            if c not in seen:
                unique_commands.append(c)
                seen.add(c)
        return unique_commands
