"""Common utilities for collecting project information."""

import json
from pathlib import Path
from typing import Any

from ..utils.file_utils import safe_read_file


class ConfigReader:
    """Common utilities for reading various configuration files."""

    @staticmethod
    def read_json_file(file_path: Path) -> dict[str, Any] | None:
        """Read and parse JSON file."""
        content = safe_read_file(file_path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def read_makefile(project_root: Path) -> str | None:
        """Read Makefile content."""
        makefile_paths = ["Makefile", "makefile"]
        for makefile in makefile_paths:
            content = safe_read_file(project_root / makefile)
            if content:
                return content
        return None

    @staticmethod
    def read_package_json(project_root: Path) -> dict[str, Any] | None:
        """Read package.json file."""
        return ConfigReader.read_json_file(project_root / "package.json")


class BuildCommandCollector:
    """ビルドコマンド収集クラス"""

    def __init__(self, project_root: Path, package_managers: dict[str, str] | None = None):
        self.project_root = project_root
        self.package_managers = package_managers or {}

    def _add_uv_run_if_needed(self, command: str) -> str:
        """uvパッケージマネージャを使用している場合、python/pytestコマンドにuv runを追加"""
        if "python" in self.package_managers and self.package_managers["python"] == "uv":
            if command.startswith("python") or command.startswith("pytest"):
                return f"uv run {command}"
        return command

    def collect_build_commands(self) -> list[str]:
        """ビルドコマンドを収集"""
        commands = []

        # Pythonプロジェクトの場合
        if "python" in self.package_managers:
            pm = self.package_managers["python"]
            if pm == "uv":
                commands.append("uv sync")
                commands.append("uv build")
            elif pm == "poetry":
                commands.append("poetry install")
                commands.append("poetry build")
            elif pm == "conda":
                commands.append("conda env create -f environment.yml")
            else:  # pip
                commands.append("pip install -e .")
                commands.append("python setup.py build")

        # scripts/run_pipeline.sh から収集
        pipeline_script = self.project_root / "scripts" / "run_pipeline.sh"
        if pipeline_script.exists():
            content = safe_read_file(pipeline_script)
            if content:
                for line in content.split("\n"):
                    if (
                        line.strip().startswith("python")
                        or line.strip().startswith("npm")
                        or line.strip().startswith("make")
                        or line.strip().startswith("go")
                    ):
                        command = line.strip()
                        command = self._add_uv_run_if_needed(command)
                        commands.append(command)

        # Makefile から収集
        content = ConfigReader.read_makefile(self.project_root)
        if content:
            for line in content.split("\n"):
                if line.startswith("\t") and line.strip():
                    command = line.lstrip("\t")
                    if command and not command.startswith("@"):
                        command = self._add_uv_run_if_needed(command)
                        commands.append(command)

        # package.json から収集
        package_data = ConfigReader.read_package_json(self.project_root)
        if package_data and "scripts" in package_data:
            pm = self.package_managers.get("javascript", "npm")
            for script_name, script_cmd in package_data["scripts"].items():
                if pm == "pnpm":
                    commands.append(f"pnpm run {script_name}")
                elif pm == "yarn":
                    commands.append(f"yarn run {script_name}")
                else:  # npm
                    commands.append(f"npm run {script_name}")

        # Goプロジェクトの場合
        if "go" in self.package_managers:
            pm = self.package_managers["go"]
            if pm == "go":
                commands.append("go build")
            elif pm == "dep":
                commands.append("dep ensure")
            elif pm == "glide":
                commands.append("glide install")

        # 重複を順序を保って排除
        seen = set()
        unique_commands = []
        for c in commands:
            if c not in seen:
                unique_commands.append(c)
                seen.add(c)
        return unique_commands

    @staticmethod
    def read_pyproject_toml(project_root: Path) -> dict[str, Any] | None:
        """Read pyproject.toml file."""
        try:
            import tomllib
        except ImportError:
            return None

        file_path = project_root / "pyproject.toml"
        try:
            with open(file_path, "rb") as f:
                return tomllib.load(f)
        except (OSError, ValueError):
            return None

    @staticmethod
    def extract_scripts_from_package_json(package_data: dict[str, Any]) -> list[str]:
        """Extract scripts from package.json."""
        scripts = package_data.get("scripts", {})
        return list(scripts.keys())

    @staticmethod
    def extract_dependencies_from_package_json(
        package_data: dict[str, Any],
    ) -> dict[str, list[str]]:
        """Extract dependencies from package.json."""
        deps = {}

        # Regular dependencies
        if "dependencies" in package_data:
            deps["npm"] = list(package_data["dependencies"].keys())

        # Dev dependencies
        if "devDependencies" in package_data:
            deps.setdefault("npm-dev", []).extend(package_data["devDependencies"].keys())

        return deps

    @staticmethod
    def parse_makefile_targets(content: str) -> list[str]:
        """Parse Makefile targets."""
        targets = []
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("\t") and not line.startswith("#") and ":" in line:
                target = line.split(":")[0].strip()
                if target and not target.startswith("."):
                    targets.append(target)
        return targets

    @staticmethod
    def detect_language_from_config(project_root: Path) -> str | None:
        """Detect programming language from configuration files."""
        # Python
        if (project_root / "pyproject.toml").exists() or (project_root / "setup.py").exists():
            return "python"

        # JavaScript/TypeScript
        package_json = ConfigReader.read_package_json(project_root)
        if package_json:
            return "javascript"  # Could be refined to detect TypeScript

        # Go
        if (project_root / "go.mod").exists():
            return "go"

        # Rust
        if (project_root / "Cargo.toml").exists():
            return "rust"

        return None
