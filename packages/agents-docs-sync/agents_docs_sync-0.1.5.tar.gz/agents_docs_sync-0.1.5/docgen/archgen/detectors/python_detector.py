"""
Python プロジェクト検出器
"""

from pathlib import Path
import tomllib

from ..models import Module, Service


class PythonDetector:
    """Python プロジェクトを検出"""

    def detect(self, project_root: Path) -> list[Service]:
        services = []

        # pyproject.toml の検出
        pyproject = project_root / "pyproject.toml"
        if pyproject.exists():
            service = self._parse_pyproject(pyproject)
            if service:
                # モジュール構造のスキャン
                service.modules = self._scan_modules(project_root)
                services.append(service)

        # requirements*.txt の検出
        if services:
            for req_file in project_root.glob("requirements*.txt"):
                deps = self._parse_requirements(req_file)
                services[0].dependencies.extend(deps)

        # 重複を除去
        if services:
            services[0].dependencies = sorted(set(services[0].dependencies))

        return services

    def _scan_modules(self, project_root: Path) -> list[Module]:
        """プロジェクト内のモジュールをスキャン"""

        modules = []
        # プロジェクトルート直下のディレクトリを探索（パッケージのみ）
        for path in project_root.iterdir():
            if path.is_dir() and (path / "__init__.py").exists():
                # 除外ディレクトリのチェック（簡易的）
                if path.name.startswith(".") or path.name in ["tests", "docs", "venv"]:
                    continue

                module = self._scan_package(path, project_root)
                if module:
                    modules.append(module)

        return modules

    def _scan_package(
        self, path: Path, project_root: Path, depth: int = 0, max_depth: int = 2
    ) -> Module:
        """パッケージを再帰的にスキャン（最大深度制限付き）"""

        submodules = []
        dependencies = set()

        # 最大深度に達したら、これ以上スキャンしない
        if depth >= max_depth:
            # 浅いパッケージでも依存関係を収集
            deps = self._collect_package_dependencies(path, project_root)
            return Module(
                name=path.name,
                path=path.relative_to(project_root),
                is_package=True,
                submodules=[],
                dependencies=sorted(deps),
            )

        # パッケージ内のサブパッケージのみをスキャン（個別ファイルは無視）
        for item in path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                if item.name == "__pycache__":
                    continue
                submodule = self._scan_package(item, project_root, depth + 1, max_depth)
                submodules.append(submodule)

        # このパッケージ全体の依存関係を収集
        # ただし、トップレベル（depth=0）では収集しない（冗長な矢印を避けるため）
        if depth > 0:
            pkg_deps = self._collect_package_dependencies(path, project_root)
            dependencies.update(pkg_deps)

        return Module(
            name=path.name,
            path=path.relative_to(project_root),
            is_package=True,
            submodules=submodules,
            dependencies=sorted(dependencies),
        )

    def _collect_package_dependencies(self, package_path: Path, project_root: Path) -> set[str]:
        """パッケージ内の全Pythonファイルから内部パッケージへの依存を収集"""
        dependencies = set()

        # 現在のパッケージ名を取得
        current_package_rel = package_path.relative_to(project_root)
        if current_package_rel.parts[0] == "docgen" and len(current_package_rel.parts) > 1:
            current_package = current_package_rel.parts[1]
        else:
            current_package = package_path.name

        # プロジェクトのトップレベルパッケージ（docgen）の直下にあるパッケージ一覧
        # これらが認識すべき内部パッケージ
        docgen_packages = {
            "collectors",
            "utils",
            "models",
            "archgen",
            "detectors",
            "generators",
            "rag",
        }

        # パッケージ内の全.pyファイルをスキャン
        for py_file in package_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            imports = self._parse_imports(py_file)
            for imp in imports:
                # パターン1: 絶対インポート "docgen.models" -> "models"
                if imp.startswith("docgen."):
                    parts = imp.split(".")
                    if len(parts) >= 2 and parts[1] in docgen_packages:
                        target_package = parts[1]
                        if target_package != current_package:
                            dependencies.add(target_package)
                # パターン2: 直接インポート "models" or "utils" (同じプロジェクト内)
                elif imp in docgen_packages and imp != current_package:
                    dependencies.add(imp)

        return dependencies

    def _parse_imports(self, path: Path) -> list[str]:
        """Pythonファイルからインポートを抽出"""
        import ast

        deps = set()
        try:
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        deps.add(name.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps.add(node.module.split(".")[0])
        except Exception:
            pass
        return list(deps)

    def _parse_pyproject(self, path: Path) -> Service | None:
        """pyproject.toml をパース"""
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)

            project = data.get("project", {})
            dependencies = []

            # project.dependencies
            if "dependencies" in project:
                deps = self._extract_package_names(project["dependencies"])
                dependencies.extend(deps)

            # dependency-groups (PEP 735 / uv)
            dep_groups = data.get("dependency-groups", {})
            for group_deps in dep_groups.values():
                dependencies.extend(self._extract_package_names(group_deps))

            # tool.poetry.dependencies (Poetry support)
            poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            if poetry_deps:
                dependencies.extend(poetry_deps.keys())

            return Service(
                name=project.get("name", "unknown"),
                type="python",
                description=project.get("description", ""),
                metadata={"version": project.get("version", "0.0.0")},
                dependencies=dependencies,
            )
        except Exception:
            return None

    def _parse_requirements(self, path: Path) -> list[str]:
        """requirements.txt から依存パッケージを抽出"""
        deps = []
        try:
            with open(path) as f:
                lines = f.readlines()
                deps = self._extract_package_names(lines)
        except Exception:
            pass
        return deps

    def _extract_package_names(self, lines: list[str | dict]) -> list[str]:
        """依存関係リストからパッケージ名を抽出"""
        deps = []
        for line in lines:
            # 辞書形式の場合（include-groupなど）はスキップ
            if isinstance(line, dict):
                continue

            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # バージョン指定などを除去
            # e.g., "package>=1.0.0" -> "package"
            # e.g., "package[extra]>=1.0.0" -> "package"
            pkg = (
                line.split(">=")[0]
                .split("==")[0]
                .split("<")[0]
                .split("~=")[0]
                .split("!=")[0]
                .strip()
            )
            pkg = pkg.split("[")[0].strip()  # extrasを除去

            if pkg and pkg != "python":  # python自体の指定を除外
                deps.append(pkg)
        return deps
