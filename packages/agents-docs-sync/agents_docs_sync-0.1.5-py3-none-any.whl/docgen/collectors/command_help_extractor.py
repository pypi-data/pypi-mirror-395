"""
Command help text extractor utility
Extracts help text and descriptions from Python CLI entry points
"""

import importlib
from pathlib import Path
import sys
from typing import Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


class CommandHelpExtractor:
    """Extract help text from Python CLI entry points"""

    @staticmethod
    def extract_from_entry_point(entry_point: str, project_root: Path | None = None) -> str:
        """
        Extract description from a Python entry point

        Args:
            entry_point: Entry point string in format "module.path:function"
            project_root: Project root directory to add to sys.path

        Returns:
            Description string, or empty string if extraction fails
        """
        try:
            # Parse entry point format: "module.path:function"
            if ":" not in entry_point:
                logger.debug(f"Invalid entry point format: {entry_point}")
                return ""

            module_path, _ = entry_point.split(":", 1)

            # Add project root to sys.path if provided
            original_path = sys.path.copy()
            if project_root:
                sys.path.insert(0, str(project_root))

            try:
                # Import the module
                module = importlib.import_module(module_path)

                # Try to find argparse parser in the module
                description = CommandHelpExtractor._extract_argparse_description(module)

                return description

            finally:
                # Restore original sys.path
                sys.path = original_path

        except Exception as e:
            logger.debug(f"Failed to extract description from {entry_point}: {e}")
            return ""

    @staticmethod
    def _extract_argparse_description(module: Any) -> str:
        """
        Extract description from argparse parser in a module

        Args:
            module: Imported module to search for argparse parser

        Returns:
            Parser description or empty string
        """
        try:
            # Look for common patterns in the module
            # 1. Check if module has a CommandLineInterface class with a run method
            if hasattr(module, "CommandLineInterface"):
                cli_class = module.CommandLineInterface
                if hasattr(cli_class, "run"):
                    # Try to extract from the run method source
                    import inspect

                    source = inspect.getsource(cli_class.run)

                    # Look for argparse.ArgumentParser(description="...")
                    import re

                    match = re.search(
                        r'argparse\.ArgumentParser\s*\([^)]*description\s*=\s*["\']([^"\']+)["\']',
                        source,
                    )
                    if match:
                        return match.group(1)

            # 2. Check for main() function
            if hasattr(module, "main"):
                import inspect

                source = inspect.getsource(module.main)

                import re

                match = re.search(
                    r'argparse\.ArgumentParser\s*\([^)]*description\s*=\s*["\']([^"\']+)["\']',
                    source,
                )
                if match:
                    return match.group(1)

            return ""

        except Exception as e:
            logger.debug(f"Failed to extract argparse description: {e}")
            return ""

    @staticmethod
    def extract_options_from_entry_point(
        entry_point: str, project_root: Path | None = None
    ) -> list[dict[str, str]]:
        """
        Extract command options from a Python entry point

        Args:
            entry_point: Entry point string in format "module.path:function"
            project_root: Project root directory to add to sys.path

        Returns:
            List of option dicts with 'name' and 'help' keys
        """
        try:
            # Parse entry point format: "module.path:function"
            if ":" not in entry_point:
                logger.debug(f"Invalid entry point format: {entry_point}")
                return []

            module_path, _ = entry_point.split(":", 1)

            # Add project root to sys.path if provided
            original_path = sys.path.copy()
            if project_root:
                sys.path.insert(0, str(project_root))

            try:
                # Import the module
                module = importlib.import_module(module_path)

                # Try to find argparse options in the module
                options = CommandHelpExtractor._extract_argparse_options(module)

                return options

            finally:
                # Restore original sys.path
                sys.path = original_path

        except Exception as e:
            logger.debug(f"Failed to extract options from {entry_point}: {e}")
            return []

    @staticmethod
    def _extract_argparse_options(module: Any) -> list[dict[str, str]]:
        """
        Extract options from argparse parser in a module

        Args:
            module: Imported module to search for argparse parser

        Returns:
            List of option dicts with 'name' and 'help' keys
        """
        try:
            options = []
            seen_names = set()
            source = None

            # Look for common patterns in the module
            # 1. Check if module has a CommandLineInterface class with a run method
            if hasattr(module, "CommandLineInterface"):
                cli_class = module.CommandLineInterface
                if hasattr(cli_class, "run"):
                    import inspect

                    source = inspect.getsource(cli_class.run)

            # 2. Check for main() function
            if source is None and hasattr(module, "main"):
                import inspect

                source = inspect.getsource(module.main)

            if source is None:
                return options

            import re

            # Pattern to match: any_parser.add_argument("--option", ..., help="description", ...)
            # This matches parser, enable_parser, disable_parser, run_parser, etc.
            argument_pattern = r'\w*parser\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
            matches = re.findall(argument_pattern, source)

            for option_name, help_text in matches:
                # Skip version action as it's auto-handled
                if "version" in option_name:
                    continue
                # Skip duplicates (same option may appear in multiple subparsers)
                if option_name in seen_names:
                    continue
                seen_names.add(option_name)
                options.append({"name": option_name, "help": help_text})

            # Also extract subcommands from add_subparsers and add_parser calls
            # Pattern to match: subparsers.add_parser("name", help="description")
            subparser_pattern = (
                r'\w+\.add_parser\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
            )
            subparser_matches = re.findall(subparser_pattern, source)

            for cmd_name, help_text in subparser_matches:
                # Skip duplicates
                if cmd_name in seen_names:
                    continue
                seen_names.add(cmd_name)
                options.append({"name": cmd_name, "help": help_text})

            return options

        except Exception as e:
            logger.debug(f"Failed to extract argparse options: {e}")
            return []

    @staticmethod
    def extract_structured_commands_from_entry_point(
        entry_point: str, project_root: Path | None = None
    ) -> dict[str, Any]:
        """
        Extract structured command hierarchy from a Python entry point.

        Returns a structured dict with:
        - options: list of main CLI options (e.g., --config, --detect-only)
        - subcommands: dict of subcommand name -> {help, options, subcommands}

        Args:
            entry_point: Entry point string in format "module.path:function"
            project_root: Project root directory to add to sys.path

        Returns:
            Structured command hierarchy dict
        """
        result = {"options": [], "subcommands": {}}

        try:
            if ":" not in entry_point:
                logger.debug(f"Invalid entry point format: {entry_point}")
                return result

            module_path, _ = entry_point.split(":", 1)

            original_path = sys.path.copy()
            if project_root:
                sys.path.insert(0, str(project_root))

            try:
                module = importlib.import_module(module_path)
                return CommandHelpExtractor._extract_structured_argparse(module)
            finally:
                sys.path = original_path

        except Exception as e:
            logger.debug(f"Failed to extract structured commands from {entry_point}: {e}")
            return result

    @staticmethod
    def _extract_structured_argparse(module: Any) -> dict[str, Any]:
        """
        Extract structured command hierarchy from argparse in a module.

        Args:
            module: Imported module to search for argparse parser

        Returns:
            Structured command hierarchy dict with options and subcommands
        """
        result = {"options": [], "subcommands": {}}

        try:
            source = None

            if hasattr(module, "CommandLineInterface"):
                cli_class = module.CommandLineInterface
                if hasattr(cli_class, "run"):
                    import inspect

                    source = inspect.getsource(cli_class.run)

            if source is None and hasattr(module, "main"):
                import inspect

                source = inspect.getsource(module.main)

            if source is None:
                return result

            import re

            # Extract main parser options (parser.add_argument only, not *_parser)
            main_option_pattern = r'(?<!\w)parser\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
            main_matches = re.findall(main_option_pattern, source)

            seen_options = set()
            for option_name, help_text in main_matches:
                if "version" in option_name:
                    continue
                if option_name in seen_options:
                    continue
                seen_options.add(option_name)
                result["options"].append({"name": option_name, "help": help_text})

            # Extract subparsers variable name: subparsers = parser.add_subparsers(...)
            # e.g., subparsers = parser.add_subparsers(dest="command", ...)
            subparsers_pattern = r"(\w+)\s*=\s*parser\.add_subparsers\("
            subparsers_match = re.search(subparsers_pattern, source)

            if subparsers_match:
                subparsers_var = subparsers_match.group(1)

                # First, collect all nested subparsers variable names to exclude them
                nested_vars = set()
                all_nested_pattern = r"(\w+)\s*=\s*\w+_parser\.add_subparsers\("
                for nested in re.findall(all_nested_pattern, source):
                    nested_vars.add(nested)

                # Extract top-level subcommands: subparsers.add_parser("name", help="...")
                # and capture their variable name if assigned
                # Use exact match for subparsers_var to avoid matching nested subparsers
                subcommand_pattern = rf'(\w+_parser)?\s*=?\s*(?<!\w){re.escape(subparsers_var)}\.add_parser\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                subcommand_matches = re.findall(subcommand_pattern, source)

                for parser_var, cmd_name, help_text in subcommand_matches:
                    subcommand_info = {
                        "help": help_text,
                        "options": [],
                        "subcommands": {},
                    }

                    if parser_var:
                        # Extract options for this subcommand: parser_var.add_argument(...)
                        subcmd_option_pattern = rf'{parser_var}\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                        subcmd_options = re.findall(subcmd_option_pattern, source)

                        for opt_name, opt_help in subcmd_options:
                            if "version" not in opt_name:
                                subcommand_info["options"].append(
                                    {"name": opt_name, "help": opt_help}
                                )

                        # Check for nested subparsers: var_subparsers = parser_var.add_subparsers(...)
                        nested_subparsers_pattern = rf"(\w+)\s*=\s*{parser_var}\.add_subparsers\("
                        nested_match = re.search(nested_subparsers_pattern, source)

                        if nested_match:
                            nested_var = nested_match.group(1)
                            # Extract nested subcommands
                            nested_subcmd_pattern = rf'(\w+_parser)?\s*=?\s*{nested_var}\.add_parser\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                            nested_matches = re.findall(nested_subcmd_pattern, source)

                            for nested_parser_var, nested_cmd, nested_help in nested_matches:
                                nested_info = {
                                    "help": nested_help,
                                    "options": [],
                                    "subcommands": {},
                                }

                                if nested_parser_var:
                                    # Extract options for nested subcommand
                                    nested_opt_pattern = rf'{nested_parser_var}\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                                    nested_opts = re.findall(nested_opt_pattern, source)

                                    for nopt_name, nopt_help in nested_opts:
                                        if "version" not in nopt_name:
                                            nested_info["options"].append(
                                                {"name": nopt_name, "help": nopt_help}
                                            )

                                subcommand_info["subcommands"][nested_cmd] = nested_info

                    result["subcommands"][cmd_name] = subcommand_info

            return result

        except Exception as e:
            logger.debug(f"Failed to extract structured argparse: {e}")
            return result
