"""
Language Info Collector Module
"""

import json
from pathlib import Path
import re
from typing import Any

from .base_collector import BaseCollector


class LanguageInfoCollector(BaseCollector):
    """言語固有情報収集クラス"""

    # ファイルパス定数
    SCRIPTS_DIR = "scripts"
    MAKEFILE_NAMES = ["Makefile", "makefile"]
    PACKAGE_JSON = "package.json"
    PYPROJECT_TOML = "pyproject.toml"
    SETUP_PY = "setup.py"
    README_FILES = ["README.md", "README.rst"]

    def __init__(self, project_root: Path, logger: Any | None = None):
        super().__init__(project_root, logger)

    def collect(self) -> dict[str, Any]:
        """
        言語固有情報を収集

        Returns:
            収集した情報の辞書
        """
        return {
            "scripts": self.collect_scripts(),
            "description": self.collect_project_description(),
        }

    def collect_scripts(self) -> dict[str, dict[str, str]]:
        """
        実行可能なスクリプトを収集

        Returns:
            スクリプト名と詳細情報の辞書 {name: {command: str, description: str}}
        """
        from .command_help_extractor import CommandHelpExtractor

        scripts = {}

        # 1. package.json scripts
        package_json = self.project_root / self.PACKAGE_JSON
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data:
                        for name, cmd in data["scripts"].items():
                            scripts[name] = {
                                "command": cmd,
                                "description": "",
                                "options": [],
                            }
            except Exception:
                pass

        # 2. Makefile targets
        for makefile_name in self.MAKEFILE_NAMES:
            makefile = self.project_root / makefile_name
            if makefile.exists():
                try:
                    content = makefile.read_text(encoding="utf-8")
                    from .collector_utils import ConfigReader

                    targets = ConfigReader.parse_makefile_targets(content)
                    for target in targets:
                        scripts[target] = {
                            "command": f"make {target}",
                            "description": "",
                            "options": [],
                        }
                except Exception:
                    pass
                break

        # 3. pyproject.toml scripts
        pyproject = self.project_root / self.PYPROJECT_TOML
        if pyproject.exists():
            try:
                import tomllib

                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)

                # Standard [project.scripts]
                if "project" in data and "scripts" in data["project"]:
                    for name, entry_point in data["project"]["scripts"].items():
                        description = CommandHelpExtractor.extract_from_entry_point(
                            entry_point, self.project_root
                        )
                        # Use structured command extraction for hierarchical display
                        structured = (
                            CommandHelpExtractor.extract_structured_commands_from_entry_point(
                                entry_point, self.project_root
                            )
                        )
                        scripts[name] = {
                            "command": entry_point,
                            "description": description,
                            "options": structured.get("options", []),
                            "subcommands": structured.get("subcommands", {}),
                        }

                # Poetry scripts
                if (
                    "tool" in data
                    and "poetry" in data["tool"]
                    and "scripts" in data["tool"]["poetry"]
                ):
                    for name, cmd in data["tool"]["poetry"]["scripts"].items():
                        scripts[name] = {
                            "command": f"poetry run {name}",
                            "description": "",
                            "options": [],
                        }

                # PDM scripts
                if "tool" in data and "pdm" in data["tool"] and "scripts" in data["tool"]["pdm"]:
                    for name, cmd in data["tool"]["pdm"]["scripts"].items():
                        if isinstance(cmd, str):
                            scripts[name] = {
                                "command": f"pdm run {name}",
                                "description": "",
                                "options": [],
                            }

            except Exception:
                pass

        return scripts

    def collect_project_description(self) -> str | None:
        """
        プロジェクトの説明を収集

        Returns:
            プロジェクトの説明文（見つからない場合はNone）
        """
        # 1. pyproject.toml
        pyproject = self.project_root / self.PYPROJECT_TOML
        if pyproject.exists():
            try:
                import tomllib

                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                if "project" in data and "description" in data["project"]:
                    return data["project"]["description"]
                if (
                    "tool" in data
                    and "poetry" in data["tool"]
                    and "description" in data["tool"]["poetry"]
                ):
                    return data["tool"]["poetry"]["description"]
            except Exception:
                try:
                    content = pyproject.read_text(encoding="utf-8")
                    desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                    if desc_match:
                        return desc_match.group(1)
                except Exception:
                    pass

        # 2. package.json
        package_json = self.project_root / self.PACKAGE_JSON
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "description" in data:
                        return data["description"]
            except Exception:
                pass

        # 3. setup.py
        setup_py = self.project_root / self.SETUP_PY
        if setup_py.exists():
            try:
                content = setup_py.read_text(encoding="utf-8")
                desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    return desc_match.group(1)
            except Exception:
                pass

        # 4. README
        for readme_file in self.README_FILES:
            readme_path = self.project_root / readme_file
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    lines = content.split("\n")
                    for line in lines:
                        line_stripped = line.strip()
                        if (
                            line_stripped
                            and not line_stripped.startswith("#")
                            and not line_stripped.startswith("<!--")
                            and not line_stripped.startswith(">")
                        ):
                            return line_stripped
                except Exception:
                    pass

        return None
