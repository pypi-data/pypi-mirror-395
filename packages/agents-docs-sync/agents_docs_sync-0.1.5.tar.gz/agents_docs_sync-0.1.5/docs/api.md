# API ドキュメント

自動生成日時: 2025-12-04 16:59:01

---

## docgen/archgen/cli.py

### generate_architecture

**型**: `function`

**シグネチャ**:
```
def generate_architecture(project_root: Path, output_dir: Path) -> bool:
```

**説明**:

アーキテクチャを生成

Args:
    project_root: プロジェクトルート
    output_dir: 出力ディレクトリ

*定義場所: docgen/archgen/cli.py:15*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

CLI エントリポイント

*定義場所: docgen/archgen/cli.py:52*

---


## docgen/archgen/detectors/docker_detector.py

### DockerDetector

**型**: `class`

**シグネチャ**:
```
class DockerDetector:
```

**説明**:

Docker 構成を検出

*定義場所: docgen/archgen/detectors/docker_detector.py:11*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self, project_root: Path) -> list[Service]:
```

*説明なし*

*定義場所: docgen/archgen/detectors/docker_detector.py:14*

---


## docgen/archgen/detectors/python_detector.py

### PythonDetector

**型**: `class`

**シグネチャ**:
```
class PythonDetector:
```

**説明**:

Python プロジェクトを検出

*定義場所: docgen/archgen/detectors/python_detector.py:11*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self, project_root: Path) -> list[Service]:
```

*説明なし*

*定義場所: docgen/archgen/detectors/python_detector.py:14*

---


## docgen/archgen/generators/mermaid_generator.py

### MermaidGenerator

**型**: `class`

**シグネチャ**:
```
class MermaidGenerator:
```

**説明**:

Mermaid.js形式でアーキテクチャ図を生成（依存なし）

*定義場所: docgen/archgen/generators/mermaid_generator.py:11*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, manifest: ArchitectureManifest, output_dir: Path) -> Path:
```

**説明**:

Mermaid形式のアーキテクチャ図を生成

*定義場所: docgen/archgen/generators/mermaid_generator.py:23*

---


## docgen/archgen/models.py

### Module

**型**: `class`

**シグネチャ**:
```
class Module:
```

**説明**:

モジュール/パッケージ

*定義場所: docgen/archgen/models.py:12*

---

### Service

**型**: `class`

**シグネチャ**:
```
class Service:
```

**説明**:

個別サービス/コンポーネント

*定義場所: docgen/archgen/models.py:22*

---

### ArchitectureManifest

**型**: `class`

**シグネチャ**:
```
class ArchitectureManifest:
```

**説明**:

アーキテクチャマニフェスト

*定義場所: docgen/archgen/models.py:34*

---

### to_yaml

**型**: `method`

**シグネチャ**:
```
def to_yaml(self, path: Path) -> None:
```

**説明**:

YAML形式で保存

*定義場所: docgen/archgen/models.py:42*

---

### from_yaml

**型**: `method`

**シグネチャ**:
```
def from_yaml(cls, path: Path) -> 'ArchitectureManifest':
```

**説明**:

YAML形式から読み込み

*定義場所: docgen/archgen/models.py:49*

---


## docgen/archgen/renderer.py

### ArchitectureRenderer

**型**: `class`

**シグネチャ**:
```
class ArchitectureRenderer:
```

**説明**:

アーキテクチャ図のレンダリングを管理

*定義場所: docgen/archgen/renderer.py:11*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, generator_type: str, image_formats: list[str] | None):
```

**説明**:

初期化

Args:
    generator_type: 生成器の種類 ("mermaid", "blockdiag", "matplotlib")
    image_formats: 画像出力形式のリスト

*定義場所: docgen/archgen/renderer.py:14*

---

### render

**型**: `method`

**シグネチャ**:
```
def render(self, manifest: ArchitectureManifest, output_dir: Path) -> dict[str, Path]:
```

**説明**:

図を生成

Args:
    manifest: アーキテクチャマニフェスト
    output_dir: 出力ディレクトリ

Returns:
    生成されたファイルのパス辞書

*定義場所: docgen/archgen/renderer.py:28*

---


## docgen/archgen/scanner.py

### ProjectScanner

**型**: `class`

**シグネチャ**:
```
class ProjectScanner:
```

**説明**:

プロジェクトをスキャンしてアーキテクチャを抽出

*定義場所: docgen/archgen/scanner.py:12*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

*説明なし*

*定義場所: docgen/archgen/scanner.py:15*

---

### scan

**型**: `method`

**シグネチャ**:
```
def scan(self) -> ArchitectureManifest:
```

**説明**:

プロジェクトをスキャン

*定義場所: docgen/archgen/scanner.py:22*

---


## docgen/cli_handlers.py

### InitHandler

**型**: `class`

**シグネチャ**:
```
class InitHandler:
```

**説明**:

Handler for the 'init' command

*定義場所: docgen/cli_handlers.py:18*

---

### handle

**型**: `method`

**シグネチャ**:
```
def handle(self, force: bool, project_root: Path, quiet: bool) -> int:
```

**説明**:

Initialize the project

Args:
    force: Force overwrite existing files
    project_root: Project root directory
    quiet: Suppress detailed messages

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli_handlers.py:21*

---

### BuildIndexHandler

**型**: `class`

**シグネチャ**:
```
class BuildIndexHandler:
```

**説明**:

Handler for the 'build-index' command

*定義場所: docgen/cli_handlers.py:126*

---

### handle

**型**: `method`

**シグネチャ**:
```
def handle(self, project_root: Path, config: dict) -> int:
```

**説明**:

Build RAG index

Args:
    project_root: Project root directory
    config: Configuration dictionary

Returns:
    Exit code

*定義場所: docgen/cli_handlers.py:129*

---

### HooksHandler

**型**: `class`

**シグネチャ**:
```
class HooksHandler:
```

**説明**:

Handler for the 'hooks' command

*定義場所: docgen/cli_handlers.py:212*

---

### handle

**型**: `method`

**シグネチャ**:
```
def handle(self, args, project_root: Path) -> int:
```

**説明**:

Handle Git hooks management actions

Args:
    args: Parsed arguments
    project_root: Project root directory

Returns:
    Exit code

*定義場所: docgen/cli_handlers.py:215*

---


## docgen/collectors/base_collector.py

### BaseCollector

**型**: `class`

**シグネチャ**:
```
class BaseCollector:
```

**説明**:

ベースコレクタークラス

*定義場所: docgen/collectors/base_collector.py:12*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    logger: ロガーインスタンス（Noneの場合はデフォルトロガーを使用）

*定義場所: docgen/collectors/base_collector.py:15*

---

### collect

**型**: `method`

**シグネチャ**:
```
def collect(self) -> Any:
```

**説明**:

情報を収集（サブクラスで実装）

Returns:
    収集した情報

*定義場所: docgen/collectors/base_collector.py:27*

---


## docgen/collectors/coding_standards_collector.py

### CodingStandardsCollector

**型**: `class`

**シグネチャ**:
```
class CodingStandardsCollector:
```

**説明**:

Coding standards collector class

*定義場所: docgen/collectors/coding_standards_collector.py:12*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    logger: Logger instance

*定義場所: docgen/collectors/coding_standards_collector.py:19*

---

### collect_coding_standards

**型**: `method`

**シグネチャ**:
```
def collect_coding_standards(self) -> dict[str, str | dict[str, Any] | bool]:
```

**説明**:

Collect coding standards

Returns:
    Dictionary of coding standards

*定義場所: docgen/collectors/coding_standards_collector.py:30*

---


## docgen/collectors/collector_utils.py

### ConfigReader

**型**: `class`

**シグネチャ**:
```
class ConfigReader:
```

**説明**:

Common utilities for reading various configuration files.

*定義場所: docgen/collectors/collector_utils.py:10*

---

### read_json_file

**型**: `method`

**シグネチャ**:
```
def read_json_file(file_path: Path) -> dict[str, Any] | None:
```

**説明**:

Read and parse JSON file.

*定義場所: docgen/collectors/collector_utils.py:14*

---

### read_makefile

**型**: `method`

**シグネチャ**:
```
def read_makefile(project_root: Path) -> str | None:
```

**説明**:

Read Makefile content.

*定義場所: docgen/collectors/collector_utils.py:25*

---

### read_package_json

**型**: `method`

**シグネチャ**:
```
def read_package_json(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read package.json file.

*定義場所: docgen/collectors/collector_utils.py:35*

---

### BuildCommandCollector

**型**: `class`

**シグネチャ**:
```
class BuildCommandCollector:
```

**説明**:

ビルドコマンド収集クラス

*定義場所: docgen/collectors/collector_utils.py:40*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None):
```

*説明なし*

*定義場所: docgen/collectors/collector_utils.py:43*

---

### collect_build_commands

**型**: `method`

**シグネチャ**:
```
def collect_build_commands(self) -> list[str]:
```

**説明**:

ビルドコマンドを収集

*定義場所: docgen/collectors/collector_utils.py:54*

---

### read_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def read_pyproject_toml(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read pyproject.toml file.

*定義場所: docgen/collectors/collector_utils.py:131*

---

### extract_scripts_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_scripts_from_package_json(package_data: dict[str, Any]) -> list[str]:
```

**説明**:

Extract scripts from package.json.

*定義場所: docgen/collectors/collector_utils.py:146*

---

### extract_dependencies_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_dependencies_from_package_json(package_data: dict[str, Any]) -> dict[str, list[str]]:
```

**説明**:

Extract dependencies from package.json.

*定義場所: docgen/collectors/collector_utils.py:152*

---

### parse_makefile_targets

**型**: `method`

**シグネチャ**:
```
def parse_makefile_targets(content: str) -> list[str]:
```

**説明**:

Parse Makefile targets.

*定義場所: docgen/collectors/collector_utils.py:169*

---

### detect_language_from_config

**型**: `method`

**シグネチャ**:
```
def detect_language_from_config(project_root: Path) -> str | None:
```

**説明**:

Detect programming language from configuration files.

*定義場所: docgen/collectors/collector_utils.py:181*

---


## docgen/collectors/command_help_extractor.py

### CommandHelpExtractor

**型**: `class`

**シグネチャ**:
```
class CommandHelpExtractor:
```

**説明**:

Extract help text from Python CLI entry points

*定義場所: docgen/collectors/command_help_extractor.py:16*

---

### extract_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_from_entry_point(entry_point: str, project_root: Path | None) -> str:
```

**説明**:

Extract description from a Python entry point

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    Description string, or empty string if extraction fails

*定義場所: docgen/collectors/command_help_extractor.py:20*

---

### extract_options_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_options_from_entry_point(entry_point: str, project_root: Path | None) -> list[dict[str, str]]:
```

**説明**:

Extract command options from a Python entry point

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    List of option dicts with 'name' and 'help' keys

*定義場所: docgen/collectors/command_help_extractor.py:115*

---

### extract_structured_commands_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_structured_commands_from_entry_point(entry_point: str, project_root: Path | None) -> dict[str, Any]:
```

**説明**:

Extract structured command hierarchy from a Python entry point.

Returns a structured dict with:
- options: list of main CLI options (e.g., --config, --detect-only)
- subcommands: dict of subcommand name -> {help, options, subcommands}

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    Structured command hierarchy dict

*定義場所: docgen/collectors/command_help_extractor.py:230*

---


## docgen/collectors/dependency_collector.py

### DependencyCollector

**型**: `class`

**シグネチャ**:
```
class DependencyCollector:
```

**説明**:

Dependency collector class

*定義場所: docgen/collectors/dependency_collector.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    logger: Logger instance

*定義場所: docgen/collectors/dependency_collector.py:20*

---

### collect_dependencies

**型**: `method`

**シグネチャ**:
```
def collect_dependencies(self) -> dict[str, list[str]]:
```

**説明**:

Collect dependencies

Returns:
    Dictionary of dependencies per language

*定義場所: docgen/collectors/dependency_collector.py:31*

---


## docgen/collectors/language_info_collector.py

### LanguageInfoCollector

**型**: `class`

**シグネチャ**:
```
class LanguageInfoCollector:
```

**説明**:

言語固有情報収集クラス

*定義場所: docgen/collectors/language_info_collector.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

*説明なし*

*定義場所: docgen/collectors/language_info_collector.py:24*

---

### collect

**型**: `method`

**シグネチャ**:
```
def collect(self) -> dict[str, Any]:
```

**説明**:

言語固有情報を収集

Returns:
    収集した情報の辞書

*定義場所: docgen/collectors/language_info_collector.py:27*

---

### collect_scripts

**型**: `method`

**シグネチャ**:
```
def collect_scripts(self) -> dict[str, dict[str, str]]:
```

**説明**:

実行可能なスクリプトを収集

Returns:
    スクリプト名と詳細情報の辞書 {name: {command: str, description: str}}

*定義場所: docgen/collectors/language_info_collector.py:39*

---

### collect_project_description

**型**: `method`

**シグネチャ**:
```
def collect_project_description(self) -> str | None:
```

**説明**:

プロジェクトの説明を収集

Returns:
    プロジェクトの説明文（見つからない場合はNone）

*定義場所: docgen/collectors/language_info_collector.py:141*

---


## docgen/collectors/project_info_collector.py

### ProjectInfoCollector

**型**: `class`

**シグネチャ**:
```
class ProjectInfoCollector:
```

**説明**:

プロジェクト情報収集クラス

プロジェクトのビルド/テスト手順、依存関係、コーディング規約などを収集する。

*定義場所: docgen/collectors/project_info_collector.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None, logger: Any | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    package_managers: 言語ごとのパッケージマネージャ辞書
    logger: ロガーインスタンス

*定義場所: docgen/collectors/project_info_collector.py:23*

---

### collect_all

**型**: `method`

**シグネチャ**:
```
def collect_all(self) -> ProjectInfo:
```

**説明**:

すべてのプロジェクト情報を収集

Returns:
    プロジェクト情報の辞書

*定義場所: docgen/collectors/project_info_collector.py:57*

---

### collect_key_features

**型**: `method`

**シグネチャ**:
```
def collect_key_features(self) -> list[str]:
```

**説明**:

主要機能を収集（プレースホルダー）

Returns:
    主要機能のリスト

*定義場所: docgen/collectors/project_info_collector.py:93*

---

### collect_test_commands

**型**: `method`

**シグネチャ**:
```
def collect_test_commands(self) -> list[str]:
```

**説明**:

テストコマンドを収集

Returns:
    テストコマンドのリスト

*定義場所: docgen/collectors/project_info_collector.py:103*

---

### collect_dependencies

**型**: `method`

**シグネチャ**:
```
def collect_dependencies(self) -> dict[str, list[str]]:
```

**説明**:

依存関係を収集

Returns:
    依存関係の辞書（言語ごと）

*定義場所: docgen/collectors/project_info_collector.py:112*

---

### collect_coding_standards

**型**: `method`

**シグネチャ**:
```
def collect_coding_standards(self) -> dict[str, str | dict[str, Any] | bool]:
```

**説明**:

コーディング規約を収集

Returns:
    コーディング規約の辞書

*定義場所: docgen/collectors/project_info_collector.py:121*

---

### collect_ci_cd_info

**型**: `method`

**シグネチャ**:
```
def collect_ci_cd_info(self) -> dict[str, Any]:
```

**説明**:

CI/CD情報を収集

Returns:
    CI/CD情報の辞書

*定義場所: docgen/collectors/project_info_collector.py:130*

---

### collect_project_structure

**型**: `method`

**シグネチャ**:
```
def collect_project_structure(self) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を収集

StructureAnalyzerに委譲して詳細な構造分析を実行

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/project_info_collector.py:151*

---


## docgen/collectors/structure_analyzer.py

### StructureAnalyzer

**型**: `class`

**シグネチャ**:
```
class StructureAnalyzer:
```

**説明**:

プロジェクト構造分析クラス

*定義場所: docgen/collectors/structure_analyzer.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    logger: ロガーインスタンス

*定義場所: docgen/collectors/structure_analyzer.py:51*

---

### count_symbols_in_file

**型**: `method`

**シグネチャ**:
```
def count_symbols_in_file(self, file_path: Path) -> int:
```

**説明**:

Pythonファイルのシンボル数をカウント

Args:
    file_path: Pythonファイルのパス

Returns:
    シンボル数（クラス、関数、非同期関数の合計）

*定義場所: docgen/collectors/structure_analyzer.py:62*

---

### collect_directory_structure

**型**: `method`

**シグネチャ**:
```
def collect_directory_structure(self, directory: Path, max_depth: int, current_depth: int) -> dict[str, Any] | str:
```

**説明**:

ディレクトリ構造を再帰的に収集

Args:
    directory: 対象ディレクトリ
    max_depth: 最大探索深度
    current_depth: 現在の深度

Returns:
    ディレクトリ構造の辞書、またはネストしないディレクトリの場合は "directory"

*定義場所: docgen/collectors/structure_analyzer.py:85*

---

### analyze

**型**: `method`

**シグネチャ**:
```
def analyze(self, max_depth: int) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を分析

Args:
    max_depth: ディレクトリの最大探索深度

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/structure_analyzer.py:142*

---


## docgen/collectors/test_command_collector.py

### TestingCommandScanner

**型**: `class`

**シグネチャ**:
```
class TestingCommandScanner:
```

**説明**:

Test command scanner class

*定義場所: docgen/collectors/test_command_collector.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    package_managers: Dictionary of detected package managers
    logger: Logger instance

*定義場所: docgen/collectors/test_command_collector.py:23*

---

### collect_test_commands

**型**: `method`

**シグネチャ**:
```
def collect_test_commands(self) -> list[str]:
```

**説明**:

Collect test commands

Returns:
    List of test commands

*定義場所: docgen/collectors/test_command_collector.py:42*

---


## docgen/config/config_accessor.py

### ConfigKeys

**型**: `class`

**シグネチャ**:
```
class ConfigKeys:
```

**説明**:

Configuration key constants to avoid hardcoding.

*定義場所: docgen/config/config_accessor.py:10*

---

### ConfigAccessor

**型**: `class`

**シグネチャ**:
```
class ConfigAccessor:
```

**説明**:

Type-safe configuration accessor.
Wraps the raw configuration dictionary and provides typed properties.

*定義場所: docgen/config/config_accessor.py:26*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:32*

---

### raw_config

**型**: `method`

**シグネチャ**:
```
def raw_config(self) -> dict[str, Any]:
```

**説明**:

Get raw configuration dictionary

*定義場所: docgen/config/config_accessor.py:36*

---

### generation

**型**: `method`

**シグネチャ**:
```
def generation(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:44*

---

### generate_api_doc

**型**: `method`

**シグネチャ**:
```
def generate_api_doc(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:48*

---

### update_readme

**型**: `method`

**シグネチャ**:
```
def update_readme(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:52*

---

### generate_agents_doc

**型**: `method`

**シグネチャ**:
```
def generate_agents_doc(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:56*

---

### preserve_manual_sections

**型**: `method`

**シグネチャ**:
```
def preserve_manual_sections(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:60*

---

### llm

**型**: `method`

**シグネチャ**:
```
def llm(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:67*

---

### llm_provider

**型**: `method`

**シグネチャ**:
```
def llm_provider(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:71*

---

### llm_model

**型**: `method`

**シグネチャ**:
```
def llm_model(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:75*

---

### llm_temperature

**型**: `method`

**シグネチャ**:
```
def llm_temperature(self) -> float:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:79*

---

### output

**型**: `method`

**シグネチャ**:
```
def output(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:86*

---

### output_dir

**型**: `method`

**シグネチャ**:
```
def output_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:90*

---

### api_doc_dir

**型**: `method`

**シグネチャ**:
```
def api_doc_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:94*

---

### readme_path

**型**: `method`

**シグネチャ**:
```
def readme_path(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:98*

---

### agents_doc_path

**型**: `method`

**シグネチャ**:
```
def agents_doc_path(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:102*

---

### rag

**型**: `method`

**シグネチャ**:
```
def rag(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:109*

---

### rag_enabled

**型**: `method`

**シグネチャ**:
```
def rag_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:113*

---

### rag_auto_build_index

**型**: `method`

**シグネチャ**:
```
def rag_auto_build_index(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:117*

---

### rag_embedding

**型**: `method`

**シグネチャ**:
```
def rag_embedding(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:121*

---

### rag_retrieval

**型**: `method`

**シグネチャ**:
```
def rag_retrieval(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:125*

---

### cache

**型**: `method`

**シグネチャ**:
```
def cache(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:132*

---

### cache_enabled

**型**: `method`

**シグネチャ**:
```
def cache_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:136*

---

### debug

**型**: `method`

**シグネチャ**:
```
def debug(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:143*

---

### debug_enabled

**型**: `method`

**シグネチャ**:
```
def debug_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:147*

---

### agents

**型**: `method`

**シグネチャ**:
```
def agents(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:154*

---

### agents_llm_mode

**型**: `method`

**シグネチャ**:
```
def agents_llm_mode(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:158*

---

### agents_generation

**型**: `method`

**シグネチャ**:
```
def agents_generation(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:162*

---

### architecture

**型**: `method`

**シグネチャ**:
```
def architecture(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:169*

---

### architecture_enabled

**型**: `method`

**シグネチャ**:
```
def architecture_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:173*

---

### architecture_output_dir

**型**: `method`

**シグネチャ**:
```
def architecture_output_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:177*

---

### architecture_generator

**型**: `method`

**シグネチャ**:
```
def architecture_generator(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:181*

---

### exclude

**型**: `method`

**シグネチャ**:
```
def exclude(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:188*

---

### exclude_directories

**型**: `method`

**シグネチャ**:
```
def exclude_directories(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:192*

---

### exclude_patterns

**型**: `method`

**シグネチャ**:
```
def exclude_patterns(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:196*

---

### hooks

**型**: `method`

**シグネチャ**:
```
def hooks(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:203*

---

### hooks_enabled

**型**: `method`

**シグネチャ**:
```
def hooks_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:207*

---

### languages

**型**: `method`

**シグネチャ**:
```
def languages(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:214*

---

### languages_auto_detect

**型**: `method`

**シグネチャ**:
```
def languages_auto_detect(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:218*

---

### languages_preferred

**型**: `method`

**シグネチャ**:
```
def languages_preferred(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:222*

---


## docgen/config_manager.py

### ConfigManager

**型**: `class`

**シグネチャ**:
```
class ConfigManager:
```

**説明**:

設定ファイルの管理クラス

*定義場所: docgen/config_manager.py:44*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, docgen_dir: Path, config_path: Path | None, package_config_sample: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    docgen_dir: .docgenディレクトリパス
    config_path: 設定ファイルのパス（Noneの場合はデフォルト）
    package_config_sample: パッケージ内のサンプル設定ファイルパス

*定義場所: docgen/config_manager.py:47*

---

### get_config

**型**: `method`

**シグネチャ**:
```
def get_config(self) -> dict[str, Any]:
```

**説明**:

現在の設定を取得

*定義場所: docgen/config_manager.py:123*

---

### accessor

**型**: `method`

**シグネチャ**:
```
def accessor(self) -> ConfigAccessor:
```

**説明**:

型安全な設定アクセサを取得（遅延初期化）

*定義場所: docgen/config_manager.py:128*

---

### update_config

**型**: `method`

**シグネチャ**:
```
def update_config(self, updates: dict[str, Any]) -> None:
```

**説明**:

設定を動的に更新

Args:
    updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）

*定義場所: docgen/config_manager.py:162*

---

### load_detector_defaults

**型**: `method`

**シグネチャ**:
```
def load_detector_defaults(self) -> dict[str, Any]:
```

**説明**:

Detectorのデフォルト設定を読み込み

*定義場所: docgen/config_manager.py:187*

---

### load_detector_user_overrides

**型**: `method`

**シグネチャ**:
```
def load_detector_user_overrides(self) -> dict[str, Any]:
```

**説明**:

ユーザー設定ファイルを読み込み

*定義場所: docgen/config_manager.py:191*

---

### merge_detector_configs

**型**: `method`

**シグネチャ**:
```
def merge_detector_configs(self, defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
```

**説明**:

Detectorのデフォルト設定とユーザー設定をマージ

*定義場所: docgen/config_manager.py:195*

---


## docgen/detector_config_loader.py

### DetectorConfigLoader

**型**: `class`

**シグネチャ**:
```
class DetectorConfigLoader:
```

**説明**:

Loader for detector configurations

*定義場所: docgen/detector_config_loader.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

*説明なし*

*定義場所: docgen/detector_config_loader.py:16*

---

### load_defaults

**型**: `method`

**シグネチャ**:
```
def load_defaults(self) -> dict[str, Any]:
```

**説明**:

Load default detector configurations

Returns:
    Dictionary of language configurations

*定義場所: docgen/detector_config_loader.py:19*

---

### load_user_overrides

**型**: `method`

**シグネチャ**:
```
def load_user_overrides(self) -> dict[str, Any]:
```

**説明**:

Load detector configuration from config.toml

Returns:
    Detector configuration dictionary

*定義場所: docgen/detector_config_loader.py:46*

---

### merge_configs

**型**: `method`

**シグネチャ**:
```
def merge_configs(self, defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
```

**説明**:

Merge default and user configurations

Args:
    defaults: Default configurations
    overrides: User configurations

Returns:
    Merged configurations

*定義場所: docgen/detector_config_loader.py:74*

---


## docgen/detectors/base_detector.py

### BaseDetector

**型**: `class`

**シグネチャ**:
```
class BaseDetector:
```

**説明**:

言語検出のベースクラス

*定義場所: docgen/detectors/base_detector.py:11*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/detectors/base_detector.py:14*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

言語が使用されているか検出

Returns:
    検出された場合True

*定義場所: docgen/detectors/base_detector.py:24*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

検出された言語名を返す

Returns:
    言語名（例: 'python', 'javascript'）

*定義場所: docgen/detectors/base_detector.py:34*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名（例: 'pip', 'npm', 'yarn'）またはNone

*定義場所: docgen/detectors/base_detector.py:44*

---


## docgen/detectors/detector_patterns.py

### DetectorPatterns

**型**: `class`

**シグネチャ**:
```
class DetectorPatterns:
```

**説明**:

Common file detection patterns used by language detectors.

*定義場所: docgen/detectors/detector_patterns.py:6*

---

### get_package_files

**型**: `method`

**シグネチャ**:
```
def get_package_files(cls, language: str) -> list[str]:
```

**説明**:

Get package manager files for a language.

*定義場所: docgen/detectors/detector_patterns.py:185*

---

### get_source_extensions

**型**: `method`

**シグネチャ**:
```
def get_source_extensions(cls, language: str) -> list[str]:
```

**説明**:

Get source file extensions for a language.

*定義場所: docgen/detectors/detector_patterns.py:190*

---

### detect_by_package_files

**型**: `method`

**シグネチャ**:
```
def detect_by_package_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for package manager files.

*定義場所: docgen/detectors/detector_patterns.py:195*

---

### detect_by_source_files

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files.

*定義場所: docgen/detectors/detector_patterns.py:201*

---

### detect_by_source_files_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files_with_exclusions(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files, excluding common directories.

*定義場所: docgen/detectors/detector_patterns.py:213*

---

### detect_by_extensions_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_extensions_with_exclusions(cls, project_root: Path, extensions: list[str]) -> bool:
```

**説明**:

Detect files by extensions, excluding common directories.

*定義場所: docgen/detectors/detector_patterns.py:227*

---

### is_excluded_path

**型**: `method`

**シグネチャ**:
```
def is_excluded_path(cls, path: Path, project_root: Path) -> bool:
```

**説明**:

Check if a path should be excluded from detection.

*定義場所: docgen/detectors/detector_patterns.py:242*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(cls, language: str, file_exists_func) -> str | None:
```

**説明**:

Detect package manager for a language using file existence checks.

Args:
    language: Language name
    file_exists_func: Function that takes file patterns (str or tuple) and returns bool

Returns:
    Package manager name or None

*定義場所: docgen/detectors/detector_patterns.py:252*

---

### is_js_config_or_test

**型**: `method`

**シグネチャ**:
```
def is_js_config_or_test(cls, file_path: Path) -> bool:
```

**説明**:

Check if a file is likely a JavaScript config or test file.

*定義場所: docgen/detectors/detector_patterns.py:273*

---

### detect_python_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_python_package_manager(cls, project_root: Path) -> str | None:
```

**説明**:

Detect Python package manager with special handling for pyproject.toml.

*定義場所: docgen/detectors/detector_patterns.py:279*

---


## docgen/detectors/plugin_registry.py

### PluginRegistry

**型**: `class`

**シグネチャ**:
```
class PluginRegistry:
```

**説明**:

カスタムdetectorプラグインのレジストリ

*定義場所: docgen/detectors/plugin_registry.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

**説明**:

初期化

*定義場所: docgen/detectors/plugin_registry.py:18*

---

### discover_plugins

**型**: `method`

**シグネチャ**:
```
def discover_plugins(self, project_root: Path):
```

**説明**:

プロジェクトのプラグインディレクトリからdetectorを発見

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/detectors/plugin_registry.py:22*

---

### register

**型**: `method`

**シグネチャ**:
```
def register(self, detector_class: type[BaseDetector]):
```

**説明**:

Detectorクラスを登録

Args:
    detector_class: BaseDetectorを継承したクラス

*定義場所: docgen/detectors/plugin_registry.py:44*

---

### get_detector

**型**: `method`

**シグネチャ**:
```
def get_detector(self, language: str, project_root: Path) -> BaseDetector | None:
```

**説明**:

指定された言語のdetectorインスタンスを取得

Args:
    language: 言語名
    project_root: プロジェクトルート

Returns:
    Detectorインスタンスまたは None

*定義場所: docgen/detectors/plugin_registry.py:60*

---

### get_all_languages

**型**: `method`

**シグネチャ**:
```
def get_all_languages(self) -> list[str]:
```

**説明**:

登録されている全ての言語名を取得

Returns:
    言語名のリスト

*定義場所: docgen/detectors/plugin_registry.py:76*

---


## docgen/detectors/unified_detector.py

### UnifiedDetector

**型**: `class`

**シグネチャ**:
```
class UnifiedDetector:
```

**説明**:

パターンベースの統一言語検出クラス

DetectorPatterns で定義されたすべての言語を検出します。

*定義場所: docgen/detectors/unified_detector.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, language: str):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 検出対象の言語名

*定義場所: docgen/detectors/unified_detector.py:20*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

指定された言語が使用されているか検出

Returns:
    検出された場合True

*定義場所: docgen/detectors/unified_detector.py:32*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

検出された言語名を返す

Returns:
    言語名（例: 'python', 'javascript'）

*定義場所: docgen/detectors/unified_detector.py:55*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名（例: 'pip', 'npm', 'yarn'）またはNone

*定義場所: docgen/detectors/unified_detector.py:64*

---

### UnifiedDetectorFactory

**型**: `class`

**シグネチャ**:
```
class UnifiedDetectorFactory:
```

**説明**:

UnifiedDetector のファクトリークラス

サポートされているすべての言語の detector を生成します。

*定義場所: docgen/detectors/unified_detector.py:87*

---

### get_all_languages

**型**: `method`

**シグネチャ**:
```
def get_all_languages(cls) -> list[str]:
```

**説明**:

サポートされているすべての言語を取得

Returns:
    言語名のリスト

*定義場所: docgen/detectors/unified_detector.py:94*

---

### create_detector

**型**: `method`

**シグネチャ**:
```
def create_detector(cls, project_root: Path, language: str) -> UnifiedDetector:
```

**説明**:

指定された言語の detector を作成

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 言語名

Returns:
    UnifiedDetector インスタンス

*定義場所: docgen/detectors/unified_detector.py:107*

---

### create_all_detectors

**型**: `method`

**シグネチャ**:
```
def create_all_detectors(cls, project_root: Path) -> list[UnifiedDetector]:
```

**説明**:

すべての言語の detector を作成

Args:
    project_root: プロジェクトのルートディレクトリ

Returns:
    UnifiedDetector インスタンスのリスト

*定義場所: docgen/detectors/unified_detector.py:121*

---


## docgen/docgen.py

### DocGen

**型**: `class`

**シグネチャ**:
```
class DocGen:
```

**説明**:

ドキュメント自動生成メインクラス

*定義場所: docgen/docgen.py:30*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path | None, config_path: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ（Noneの場合は現在の作業ディレクトリ）
    config_path: 設定ファイルのパス（Noneの場合はデフォルト）

*定義場所: docgen/docgen.py:33*

---

### detect_languages

**型**: `method`

**シグネチャ**:
```
def detect_languages(self, use_parallel: bool) -> list[str]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語のリスト

*定義場所: docgen/docgen.py:67*

---

### update_config

**型**: `method`

**シグネチャ**:
```
def update_config(self, updates: dict[str, Any]) -> None:
```

**説明**:

設定を動的に更新

Args:
    updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）

*定義場所: docgen/docgen.py:81*

---

### generate_documents

**型**: `method`

**シグネチャ**:
```
def generate_documents(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/docgen.py:91*

---

### CommandLineInterface

**型**: `class`

**シグネチャ**:
```
class CommandLineInterface:
```

**説明**:

コマンドラインインターフェースクラス

*定義場所: docgen/docgen.py:111*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

*説明なし*

*定義場所: docgen/docgen.py:114*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self) -> int:
```

**説明**:

メイン実行メソッド

*定義場所: docgen/docgen.py:120*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メインエントリーポイント

*定義場所: docgen/docgen.py:268*

---


## docgen/document_generator.py

### DocumentGenerator

**型**: `class`

**シグネチャ**:
```
class DocumentGenerator:
```

**説明**:

ドキュメント生成クラス

*定義場所: docgen/document_generator.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, detected_languages: list[str], config: dict[str, Any], detected_package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    detected_languages: 検出された言語リスト
    config: 設定辞書
    detected_package_managers: 検出されたパッケージマネージャ辞書

*定義場所: docgen/document_generator.py:17*

---

### generate_documents

**型**: `method`

**シグネチャ**:
```
def generate_documents(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/document_generator.py:38*

---


## docgen/generator_factory.py

### GeneratorFactory

**型**: `class`

**シグネチャ**:
```
class GeneratorFactory:
```

**説明**:

ジェネレーターのファクトリークラス

*定義場所: docgen/generator_factory.py:12*

---

### create_generator

**型**: `method`

**シグネチャ**:
```
def create_generator(cls, generator_type: str, project_root: Path, detected_languages: list[str], config: dict[str, Any], detected_package_managers: dict[str, str] | None) -> BaseGenerator:
```

**説明**:

指定されたタイプのジェネレーターを作成

*定義場所: docgen/generator_factory.py:24*

---

### get_available_generators

**型**: `method`

**シグネチャ**:
```
def get_available_generators(cls) -> list[str]:
```

**説明**:

利用可能なジェネレーターのリストを取得

*定義場所: docgen/generator_factory.py:52*

---


## docgen/generators/agents_generator.py

### AgentsGenerator

**型**: `class`

**シグネチャ**:
```
class AgentsGenerator:
```

**説明**:

AGENTS.md生成クラス（OpenAI仕様準拠）

*定義場所: docgen/generators/agents_generator.py:20*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書
    **kwargs: BaseGeneratorに渡す追加引数（サービスなど）

*定義場所: docgen/generators/agents_generator.py:23*

---

### agents_path

**型**: `method`

**シグネチャ**:
```
def agents_path(self):
```

*説明なし*

*定義場所: docgen/generators/agents_generator.py:44*

---


## docgen/generators/api_generator.py

### APIGenerator

**型**: `class`

**シグネチャ**:
```
class APIGenerator:
```

**説明**:

APIドキュメント生成クラス

*定義場所: docgen/generators/api_generator.py:26*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書

*定義場所: docgen/generators/api_generator.py:29*

---


## docgen/generators/base_generator.py

### BaseGenerator

**型**: `class`

**シグネチャ**:
```
class BaseGenerator:
```

**説明**:

ベースジェネレータークラス（AGENTS.mdとREADME.mdの共通部分）

DI対応: コンストラクタでサービスを注入可能。

*定義場所: docgen/generators/base_generator.py:23*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書
    llm_service: LLMサービス（DI）
    template_service: テンプレートサービス（DI）
    rag_service: RAGサービス（DI）
    formatting_service: フォーマットサービス（DI）
    manual_section_service: 手動セクションサービス（DI）

*定義場所: docgen/generators/base_generator.py:29*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    生成に成功した場合True

*定義場所: docgen/generators/base_generator.py:182*

---


## docgen/generators/commit_message_generator.py

### CommitMessageGenerator

**型**: `class`

**シグネチャ**:
```
class CommitMessageGenerator:
```

**説明**:

コミットメッセージ生成クラス

*定義場所: docgen/generators/commit_message_generator.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, config: dict[str, Any]):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    config: 設定辞書

*定義場所: docgen/generators/commit_message_generator.py:19*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self) -> str | None:
```

**説明**:

コミットメッセージを生成

Returns:
    生成されたコミットメッセージ（エラー時はNone）

*定義場所: docgen/generators/commit_message_generator.py:32*

---


## docgen/generators/contributing_generator.py

### ContributingGenerator

**型**: `class`

**シグネチャ**:
```
class ContributingGenerator:
```

**説明**:

CONTRIBUTING.md generation class

*定義場所: docgen/generators/contributing_generator.py:12*

---


## docgen/generators/parsers/base_parser.py

### BaseParser

**型**: `class`

**シグネチャ**:
```
class BaseParser:
```

**説明**:

コード解析のベースクラス

Template Methodパターンにより、解析フローの共通部分を定義します。
サブクラスでは以下の抽象メソッドを実装します：
- `_parse_to_ast`: コンテンツをASTにパース
- `_extract_elements`: ASTからAPI要素を抽出
- `get_supported_extensions`: サポートする拡張子を返す

Attributes:
    PARSER_TYPE: パーサーの種類を示すクラス変数

*定義場所: docgen/generators/parsers/base_parser.py:24*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/generators/parsers/base_parser.py:39*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

ファイルを解析してAPI情報を抽出 (Template Method)

Args:
    file_path: 解析するファイルのパス

Returns:
    API情報のリスト

*定義場所: docgen/generators/parsers/base_parser.py:48*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートするファイル拡張子を返す

Returns:
    拡張子のリスト（例: ['.py', '.pyw']）

*定義場所: docgen/generators/parsers/base_parser.py:93*

---

### get_parser_type

**型**: `method`

**シグネチャ**:
```
def get_parser_type(self) -> str:
```

**説明**:

パーサーの種類を返す（キャッシュキーの生成に使用）

Returns:
    パーサーの種類（例: 'python', 'javascript'）

*定義場所: docgen/generators/parsers/base_parser.py:102*

---

### parse_project

**型**: `method`

**シグネチャ**:
```
def parse_project(self, exclude_dirs: list[str] | None, use_parallel: bool, max_workers: int | None, use_cache: bool, cache_manager: 'CacheManager | None') -> list[APIInfo]:
```

**説明**:

プロジェクト全体を解析

Args:
    exclude_dirs: 除外するディレクトリ（例: ['.git', 'node_modules']）
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）
    max_workers: 並列処理の最大ワーカー数（Noneの場合は自動）
    use_cache: キャッシュを使用するかどうか（デフォルト: True）
    cache_manager: キャッシュマネージャー（Noneの場合はキャッシュを使用しない）

Returns:
    全API情報のリスト

*定義場所: docgen/generators/parsers/base_parser.py:111*

---


## docgen/generators/parsers/generic_parser.py

### GenericParser

**型**: `class`

**シグネチャ**:
```
class GenericParser:
```

**説明**:

汎用コード解析クラス

*定義場所: docgen/generators/parsers/generic_parser.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, language: str):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 言語名（'rust', 'java', 'c', 'cpp', 'go', 'ruby', 'php'など）

*定義場所: docgen/generators/parsers/generic_parser.py:31*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

Returns:
    言語に応じた拡張子のリスト

*定義場所: docgen/generators/parsers/generic_parser.py:143*

---


## docgen/generators/parsers/js_parser.py

### JSParser

**型**: `class`

**シグネチャ**:
```
class JSParser:
```

**説明**:

JavaScript/TypeScriptコード解析クラス

*定義場所: docgen/generators/parsers/js_parser.py:13*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/js_parser.py:212*

---


## docgen/generators/parsers/parser_patterns.py

### ParserPatterns

**型**: `class`

**シグネチャ**:
```
class ParserPatterns:
```

**説明**:

Common patterns and utilities for code parsing.

*定義場所: docgen/generators/parsers/parser_patterns.py:9*

---

### extract_docstring

**型**: `method`

**シグネチャ**:
```
def extract_docstring(cls, content: str, language: str, start_pos: int) -> str | None:
```

**説明**:

Extract docstring/comment from content starting at a position.

Args:
    content: Source code content
    language: Programming language
    start_pos: Position to start searching from

Returns:
    Extracted docstring or None

*定義場所: docgen/generators/parsers/parser_patterns.py:53*

---

### find_functions_and_classes

**型**: `method`

**シグネチャ**:
```
def find_functions_and_classes(cls, content: str, language: str) -> list[tuple[str, str, int]]:
```

**説明**:

Find all functions and classes in content.

Args:
    content: Source code content
    language: Programming language

Returns:
    List of (name, type, position) tuples

*定義場所: docgen/generators/parsers/parser_patterns.py:74*

---

### create_api_info

**型**: `method`

**シグネチャ**:
```
def create_api_info(cls, name: str, entity_type: str, file_path: Path, project_root: Path, line_number: int | None, signature: str | None, docstring: str | None) -> APIInfo:
```

**説明**:

Create APIInfo object with common fields.

Args:
    name: Function/class name
    entity_type: Type ('function', 'class', etc.)
    file_path: Source file path
    project_root: Project root path
    line_number: Line number (optional)
    signature: Function signature (optional)
    docstring: Documentation string (optional)

Returns:
    APIInfo object

*定義場所: docgen/generators/parsers/parser_patterns.py:98*

---

### clean_docstring

**型**: `method`

**シグネチャ**:
```
def clean_docstring(cls, docstring: str, language: str) -> str:
```

**説明**:

Clean and normalize docstring content.

Args:
    docstring: Raw docstring
    language: Programming language

Returns:
    Cleaned docstring

*定義場所: docgen/generators/parsers/parser_patterns.py:135*

---


## docgen/generators/parsers/python_parser.py

### PythonParser

**型**: `class`

**シグネチャ**:
```
class PythonParser:
```

**説明**:

Pythonコード解析クラス

*定義場所: docgen/generators/parsers/python_parser.py:30*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/python_parser.py:51*

---

### PythonASTVisitor

**型**: `class`

**シグネチャ**:
```
class PythonASTVisitor:
```

**説明**:

Python AST訪問クラス

*定義場所: docgen/generators/parsers/python_parser.py:58*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, file_path: Path, project_root: Path):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:61*

---

### visit_ClassDef

**型**: `method`

**シグネチャ**:
```
def visit_ClassDef(self, node: ast.ClassDef):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:67*

---

### visit_FunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_FunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:90*

---

### visit_AsyncFunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_AsyncFunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:93*

---


## docgen/generators/readme_generator.py

### ReadmeGenerator

**型**: `class`

**シグネチャ**:
```
class ReadmeGenerator:
```

**説明**:

README generation class

*定義場所: docgen/generators/readme_generator.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    languages: List of detected languages
    config: Configuration dictionary
    package_managers: Dictionary of detected package managers
    **kwargs: Additional arguments passed to BaseGenerator (services, etc.)

*定義場所: docgen/generators/readme_generator.py:19*

---

### readme_path

**型**: `method`

**シグネチャ**:
```
def readme_path(self):
```

*説明なし*

*定義場所: docgen/generators/readme_generator.py:47*

---


## docgen/generators/service_factory.py

### GeneratorServiceFactory

**型**: `class`

**シグネチャ**:
```
class GeneratorServiceFactory:
```

**説明**:

ジェネレーターサービスファクトリ

*定義場所: docgen/generators/service_factory.py:19*

---

### create_services

**型**: `method`

**シグネチャ**:
```
def create_services(project_root: Path, config: dict[str, Any], logger: Logger | None) -> dict[str, Any]:
```

**説明**:

全サービスを生成して返す

Args:
    project_root: プロジェクトルートディレクトリ
    config: 設定辞書
    logger: ロガー（各サービスに渡される）

Returns:
    サービスインスタンスの辞書

*定義場所: docgen/generators/service_factory.py:23*

---

### create_llm_service

**型**: `method`

**シグネチャ**:
```
def create_llm_service(config: dict[str, Any], logger: Logger | None) -> LLMService:
```

**説明**:

LLMServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:50*

---

### create_template_service

**型**: `method`

**シグネチャ**:
```
def create_template_service(template_dir: Path | None) -> TemplateService:
```

**説明**:

TemplateServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:55*

---

### create_rag_service

**型**: `method`

**シグネチャ**:
```
def create_rag_service(project_root: Path, config: dict[str, Any], logger: Logger | None) -> RAGService:
```

**説明**:

RAGServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:60*

---

### create_formatting_service

**型**: `method`

**シグネチャ**:
```
def create_formatting_service() -> FormattingService:
```

**説明**:

FormattingServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:67*

---

### create_manual_section_service

**型**: `method`

**シグネチャ**:
```
def create_manual_section_service() -> ManualSectionService:
```

**説明**:

ManualSectionServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:72*

---


## docgen/generators/services/formatting_service.py

### FormattingService

**型**: `class`

**シグネチャ**:
```
class FormattingService:
```

**説明**:

フォーマット・マークダウン処理サービス

*定義場所: docgen/generators/services/formatting_service.py:15*

---

### format_languages

**型**: `method`

**シグネチャ**:
```
def format_languages(self, languages: list[str]) -> str:
```

**説明**:

言語リストをフォーマット

Args:
    languages: 言語のリスト

Returns:
    フォーマットされた言語リスト

*定義場所: docgen/generators/services/formatting_service.py:36*

---

### format_commands

**型**: `method`

**シグネチャ**:
```
def format_commands(self, commands: list[str] | None) -> str:
```

**説明**:

コマンドリストをフォーマット

Args:
    commands: コマンドのリスト

Returns:
    フォーマットされたコマンド

*定義場所: docgen/generators/services/formatting_service.py:55*

---

### format_project_structure

**型**: `method`

**シグネチャ**:
```
def format_project_structure(self, structure: dict | None) -> str:
```

**説明**:

プロジェクト構造をツリー形式でフォーマット

Args:
    structure: プロジェクト構造の辞書

Returns:
    フォーマットされたプロジェクト構造

*定義場所: docgen/generators/services/formatting_service.py:69*

---

### clean_llm_output

**型**: `method`

**シグネチャ**:
```
def clean_llm_output(self, content: str) -> str:
```

**説明**:

LLMの出力をクリーニング

Args:
    content: LLM出力

Returns:
    クリーニングされたコンテンツ

*定義場所: docgen/generators/services/formatting_service.py:114*

---

### validate_output

**型**: `method`

**シグネチャ**:
```
def validate_output(self, content: str) -> bool:
```

**説明**:

生成されたコンテンツを検証

Args:
    content: 生成されたコンテンツ

Returns:
    検証に成功した場合True

*定義場所: docgen/generators/services/formatting_service.py:134*

---

### generate_footer

**型**: `method`

**シグネチャ**:
```
def generate_footer(self, document_type: str) -> str:
```

**説明**:

フッターを生成

Args:
    document_type: ドキュメントタイプ

Returns:
    フッター文字列

*定義場所: docgen/generators/services/formatting_service.py:150*

---

### extract_description_section

**型**: `method`

**シグネチャ**:
```
def extract_description_section(self, content: str) -> str:
```

**説明**:

コンテンツから説明セクションを抽出

Args:
    content: ドキュメントコンテンツ

Returns:
    説明セクションのテキスト

*定義場所: docgen/generators/services/formatting_service.py:162*

---


## docgen/generators/services/llm_service.py

### LLMService

**型**: `class`

**シグネチャ**:
```
class LLMService:
```

**説明**:

LLM生成サービス

*定義場所: docgen/generators/services/llm_service.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any], logger: Logger | None):
```

**説明**:

初期化

Args:
    config: 設定辞書（agents設定を含む）
    logger: ロガー

*定義場所: docgen/generators/services/llm_service.py:18*

---

### agents_config

**型**: `method`

**シグネチャ**:
```
def agents_config(self) -> dict[str, Any]:
```

**説明**:

agents設定を取得

*定義場所: docgen/generators/services/llm_service.py:35*

---

### get_client

**型**: `method`

**シグネチャ**:
```
def get_client(self) -> Any:
```

**説明**:

LLMクライアントを取得（フォールバック付き）

Returns:
    LLMクライアント（取得できない場合はNone）

*定義場所: docgen/generators/services/llm_service.py:39*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str) -> str:
```

**説明**:

LLMを使用してテキストを生成

Args:
    prompt: 入力プロンプト

Returns:
    生成されたテキスト

Raises:
    RuntimeError: LLMクライアントが利用できない場合

*定義場所: docgen/generators/services/llm_service.py:57*

---

### should_use_outlines

**型**: `method`

**シグネチャ**:
```
def should_use_outlines(self) -> bool:
```

**説明**:

Outlinesを使用するかどうかを判定

Returns:
    Outlinesを使用するかどうか

*定義場所: docgen/generators/services/llm_service.py:76*

---

### create_outlines_model

**型**: `method`

**シグネチャ**:
```
def create_outlines_model(self, client: Any) -> Any:
```

**説明**:

Outlinesモデルを作成

Args:
    client: LLMクライアント

Returns:
    Outlinesモデル（サポートされない場合はNone）

*定義場所: docgen/generators/services/llm_service.py:87*

---

### format_project_info

**型**: `method`

**シグネチャ**:
```
def format_project_info(self, project_info: Any, languages: list[str], package_managers: dict[str, str] | None) -> str:
```

**説明**:

プロジェクト情報をプロンプト用に整形

Args:
    project_info: プロジェクト情報
    languages: 言語リスト
    package_managers: パッケージマネージャ辞書

Returns:
    整形された文字列

*定義場所: docgen/generators/services/llm_service.py:101*

---

### generate_content

**型**: `method`

**シグネチャ**:
```
def generate_content(self, prompt_file: str, prompt_name: str, project_info_str: str, rag_context: str) -> str:
```

**説明**:

LLMを使用して特定のコンテンツを生成

Args:
    prompt_file: プロンプトファイル名
    prompt_name: プロンプト名
    project_info_str: 整形済みプロジェクト情報
    rag_context: RAGコンテキスト

Returns:
    生成されたコンテンツ

*定義場所: docgen/generators/services/llm_service.py:143*

---


## docgen/generators/services/manual_section_service.py

### ManualSectionService

**型**: `class`

**シグネチャ**:
```
class ManualSectionService:
```

**説明**:

手動セクション管理サービス

*定義場所: docgen/generators/services/manual_section_service.py:11*

---

### extract

**型**: `method`

**シグネチャ**:
```
def extract(self, content: str) -> dict[str, str]:
```

**説明**:

既存のコンテンツから手動セクションを抽出

Args:
    content: 既存のドキュメントコンテンツ

Returns:
    セクションIDとコンテンツの辞書

*定義場所: docgen/generators/services/manual_section_service.py:14*

---

### merge

**型**: `method`

**シグネチャ**:
```
def merge(self, generated_content: str, manual_sections: dict[str, str]) -> str:
```

**説明**:

生成されたコンテンツに手動セクションをマージ

Args:
    generated_content: 自動生成されたコンテンツ
    manual_sections: 抽出された手動セクションの辞書

Returns:
    マージされたコンテンツ

*定義場所: docgen/generators/services/manual_section_service.py:53*

---


## docgen/generators/services/rag_service.py

### RAGService

**型**: `class`

**シグネチャ**:
```
class RAGService:
```

**説明**:

RAGコンテキスト取得サービス

*定義場所: docgen/generators/services/rag_service.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, config: dict[str, Any], logger: Logger | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートディレクトリ
    config: 設定辞書
    logger: ロガー

*定義場所: docgen/generators/services/rag_service.py:18*

---

### is_enabled

**型**: `method`

**シグネチャ**:
```
def is_enabled(self) -> bool:
```

**説明**:

RAGが有効かどうか

*定義場所: docgen/generators/services/rag_service.py:37*

---

### get_context

**型**: `method`

**シグネチャ**:
```
def get_context(self, query: str, top_k: int | None) -> str:
```

**説明**:

RAGコンテキストを取得してフォーマット

Args:
    query: 検索クエリ
    top_k: 取得するチャンク数（Noneの場合は設定ファイルから読み取る）

Returns:
    フォーマット済みのコンテキスト文字列（RAG無効時は空文字列）

*定義場所: docgen/generators/services/rag_service.py:41*

---


## docgen/generators/services/template_service.py

### TemplateService

**型**: `class`

**シグネチャ**:
```
class TemplateService:
```

**説明**:

テンプレートレンダリングサービス

*定義場所: docgen/generators/services/template_service.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, template_dir: Path | None):
```

**説明**:

初期化

Args:
    template_dir: テンプレートディレクトリのパス（Noneの場合は自動検出）

*定義場所: docgen/generators/services/template_service.py:17*

---

### render

**型**: `method`

**シグネチャ**:
```
def render(self, template_name: str, context: dict[str, Any]) -> str:
```

**説明**:

テンプレートをレンダリング

Args:
    template_name: テンプレートファイル名
    context: テンプレート変数

Returns:
    レンダリングされた文字列

*定義場所: docgen/generators/services/template_service.py:47*

---

### format_commands

**型**: `method`

**シグネチャ**:
```
def format_commands(self, commands: list[str]) -> str:
```

**説明**:

コマンドリストをマークダウンのコードブロックとしてフォーマット

Args:
    commands: コマンドのリスト

Returns:
    フォーマットされたマークダウン文字列

*定義場所: docgen/generators/services/template_service.py:62*

---

### format_custom_instructions

**型**: `method`

**シグネチャ**:
```
def format_custom_instructions(self, custom_instructions: str | dict[str, Any]) -> list[str]:
```

**説明**:

カスタム指示セクションを生成

Args:
    custom_instructions: カスタム指示の内容（文字列または辞書）

Returns:
    生成された行のリスト

*定義場所: docgen/generators/services/template_service.py:82*

---


## docgen/hooks/config.py

### TaskConfig

**型**: `class`

**シグネチャ**:
```
class TaskConfig:
```

**説明**:

タスク設定

*定義場所: docgen/hooks/config.py:20*

---

### HookConfig

**型**: `class`

**シグネチャ**:
```
class HookConfig:
```

**説明**:

フック設定

*定義場所: docgen/hooks/config.py:31*

---

### ConfigLoader

**型**: `class`

**シグネチャ**:
```
class ConfigLoader:
```

**説明**:

フック設定ローダー

*定義場所: docgen/hooks/config.py:39*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: str):
```

*説明なし*

*定義場所: docgen/hooks/config.py:42*

---

### load_config

**型**: `method`

**シグネチャ**:
```
def load_config(self) -> dict[str, HookConfig]:
```

**説明**:

設定を読み込む

*定義場所: docgen/hooks/config.py:47*

---


## docgen/hooks/orchestrator.py

### HookOrchestrator

**型**: `class`

**シグネチャ**:
```
class HookOrchestrator:
```

**説明**:

Git hook実行のオーケストレーター

*定義場所: docgen/hooks/orchestrator.py:19*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, hook_name: str, args: list[str]):
```

*説明なし*

*定義場所: docgen/hooks/orchestrator.py:22*

---

### register_task

**型**: `method`

**シグネチャ**:
```
def register_task(self, name: str, task_class: type):
```

**説明**:

タスクを登録する

*定義場所: docgen/hooks/orchestrator.py:40*

---

### run_async

**型**: `method`

**シグネチャ**:
```
async def run_async(self) -> int:
```

**説明**:

フックを非同期実行する

*定義場所: docgen/hooks/orchestrator.py:44*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self) -> int:
```

**説明**:

同期実行ラッパー

*定義場所: docgen/hooks/orchestrator.py:122*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

エントリーポイント

*定義場所: docgen/hooks/orchestrator.py:127*

---


## docgen/hooks/registry.py

### TaskRegistry

**型**: `class`

**シグネチャ**:
```
class TaskRegistry:
```

**説明**:

フックタスクのレジストリ

*定義場所: docgen/hooks/registry.py:4*

---

### register

**型**: `method`

**シグネチャ**:
```
def register(cls, name: str):
```

**説明**:

タスクを登録するデコレータ

*定義場所: docgen/hooks/registry.py:10*

---

### get_task

**型**: `method`

**シグネチャ**:
```
def get_task(cls, name: str) -> type[HookTask] | None:
```

**説明**:

タスククラスを取得

*定義場所: docgen/hooks/registry.py:20*

---

### get_all_tasks

**型**: `method`

**シグネチャ**:
```
def get_all_tasks(cls) -> dict[str, type[HookTask]]:
```

**説明**:

全タスクを取得

*定義場所: docgen/hooks/registry.py:25*

---


## docgen/hooks/tasks/base.py

### TaskStatus

**型**: `class`

**シグネチャ**:
```
class TaskStatus:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:9*

---

### TaskResult

**型**: `class`

**シグネチャ**:
```
class TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:16*

---

### HookContext

**型**: `class`

**シグネチャ**:
```
class HookContext:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:23*

---

### HookTask

**型**: `class`

**シグネチャ**:
```
class HookTask:
```

**説明**:

フックタスクの基底クラス

*定義場所: docgen/hooks/tasks/base.py:29*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: TaskConfig):
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:32*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

**説明**:

タスクを実行

*定義場所: docgen/hooks/tasks/base.py:36*

---

### should_run

**型**: `method`

**シグネチャ**:
```
def should_run(self, context: HookContext) -> bool:
```

**説明**:

タスクを実行すべきか判定

*定義場所: docgen/hooks/tasks/base.py:40*

---

### run_async

**型**: `method`

**シグネチャ**:
```
async def run_async(self, context: HookContext) -> TaskResult:
```

**説明**:

タスクを非同期実行（デフォルトは同期実行をラップ）

*定義場所: docgen/hooks/tasks/base.py:44*

---


## docgen/hooks/tasks/commit_msg_generator.py

### CommitMsgGeneratorTask

**型**: `class`

**シグネチャ**:
```
class CommitMsgGeneratorTask:
```

**説明**:

コミットメッセージ生成タスク

*定義場所: docgen/hooks/tasks/commit_msg_generator.py:9*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/commit_msg_generator.py:12*

---


## docgen/hooks/tasks/doc_generator.py

### DocGeneratorTask

**型**: `class`

**シグネチャ**:
```
class DocGeneratorTask:
```

**説明**:

ドキュメント生成タスク

*定義場所: docgen/hooks/tasks/doc_generator.py:7*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/doc_generator.py:10*

---


## docgen/hooks/tasks/file_stager.py

### FileStagerTask

**型**: `class`

**シグネチャ**:
```
class FileStagerTask:
```

**説明**:

ファイルステージングタスク

*定義場所: docgen/hooks/tasks/file_stager.py:9*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/file_stager.py:12*

---


## docgen/hooks/tasks/rag_generator.py

### RagGeneratorTask

**型**: `class`

**シグネチャ**:
```
class RagGeneratorTask:
```

**説明**:

RAG生成タスク

*定義場所: docgen/hooks/tasks/rag_generator.py:7*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/rag_generator.py:10*

---


## docgen/hooks/tasks/test_runner.py

### TestRunnerTask

**型**: `class`

**シグネチャ**:
```
class TestRunnerTask:
```

**説明**:

テスト実行タスク

*定義場所: docgen/hooks/tasks/test_runner.py:9*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/test_runner.py:12*

---


## docgen/hooks/tasks/version_checker.py

### VersionCheckerTask

**型**: `class`

**シグネチャ**:
```
class VersionCheckerTask:
```

**説明**:

バージョンチェック＆リリースタグ作成タスク

*定義場所: docgen/hooks/tasks/version_checker.py:10*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/version_checker.py:13*

---


## docgen/hooks/utils.py

### get_python_command

**型**: `function`

**シグネチャ**:
```
def get_python_command() -> str:
```

**説明**:

利用可能なPythonコマンドを取得する（uv優先）

*定義場所: docgen/hooks/utils.py:4*

---

### run_command

**型**: `function`

**シグネチャ**:
```
def run_command(command: list[str], cwd: str | None, capture_output: bool) -> tuple[int, str, str]:
```

**説明**:

コマンドを実行する

*定義場所: docgen/hooks/utils.py:23*

---

### get_changed_files

**型**: `function`

**シグネチャ**:
```
def get_changed_files(staged: bool) -> list[str]:
```

**説明**:

変更されたファイルを取得する

*定義場所: docgen/hooks/utils.py:36*

---

### is_git_repo

**型**: `function`

**シグネチャ**:
```
def is_git_repo(path: str) -> bool:
```

**説明**:

Gitリポジトリか確認する

*定義場所: docgen/hooks/utils.py:49*

---


## docgen/language_detector.py

### LanguageDetector

**型**: `class`

**シグネチャ**:
```
class LanguageDetector:
```

**説明**:

言語検出クラス

*定義場所: docgen/language_detector.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, config_manager):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    config_manager: 設定マネージャー（Noneの場合は新規作成）

*定義場所: docgen/language_detector.py:17*

---

### detect_languages

**型**: `method`

**シグネチャ**:
```
def detect_languages(self, use_parallel: bool) -> list[str]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語のリスト

*定義場所: docgen/language_detector.py:54*

---

### get_detected_languages

**型**: `method`

**シグネチャ**:
```
def get_detected_languages(self) -> list[str]:
```

**説明**:

検出された言語を取得

*定義場所: docgen/language_detector.py:127*

---

### get_detected_package_managers

**型**: `method`

**シグネチャ**:
```
def get_detected_package_managers(self) -> dict[str, str]:
```

**説明**:

検出されたパッケージマネージャを取得

*定義場所: docgen/language_detector.py:131*

---


## docgen/models/agents.py

### LLMConfig

**型**: `class`

**シグネチャ**:
```
class LLMConfig:
```

**説明**:

LLM設定モデル

*定義場所: docgen/models/agents.py:8*

---

### ProjectOverview

**型**: `class`

**シグネチャ**:
```
class ProjectOverview:
```

**説明**:

Project overview model.

*定義場所: docgen/models/agents.py:26*

---

### LLMSetup

**型**: `class`

**シグネチャ**:
```
class LLMSetup:
```

**説明**:

LLM setup model.

*定義場所: docgen/models/agents.py:34*

---

### SetupInstructions

**型**: `class`

**シグネチャ**:
```
class SetupInstructions:
```

**説明**:

Setup instructions model.

*定義場所: docgen/models/agents.py:41*

---

### BuildTestInstructions

**型**: `class`

**シグネチャ**:
```
class BuildTestInstructions:
```

**説明**:

Build and test instructions model.

*定義場所: docgen/models/agents.py:49*

---

### CodingStandards

**型**: `class`

**シグネチャ**:
```
class CodingStandards:
```

**説明**:

Coding standards model.

*定義場所: docgen/models/agents.py:57*

---

### PRGuidelines

**型**: `class`

**シグネチャ**:
```
class PRGuidelines:
```

**説明**:

PR guidelines model.

*定義場所: docgen/models/agents.py:64*

---

### AgentsConfig

**型**: `class`

**シグネチャ**:
```
class AgentsConfig:
```

**説明**:

Configuration model for agents documentation.

*定義場所: docgen/models/agents.py:72*

---

### AgentsGenerationConfig

**型**: `class`

**シグネチャ**:
```
class AgentsGenerationConfig:
```

**説明**:

Agents generation configuration model.

*定義場所: docgen/models/agents.py:89*

---

### AgentsConfigSection

**型**: `class`

**シグネチャ**:
```
class AgentsConfigSection:
```

**説明**:

Agents configuration section model.

*定義場所: docgen/models/agents.py:97*

---

### AgentsDocument

**型**: `class`

**シグネチャ**:
```
class AgentsDocument:
```

**説明**:

AGENTS.mdドキュメントの構造化データモデル

*定義場所: docgen/models/agents.py:110*

---


## docgen/models/api.py

### APIParameter

**型**: `class`

**シグネチャ**:
```
class APIParameter:
```

**説明**:

APIパラメータモデル

*定義場所: docgen/models/api.py:8*

---

### APIInfo

**型**: `class`

**シグネチャ**:
```
class APIInfo:
```

**説明**:

API情報モデル

*定義場所: docgen/models/api.py:18*

---


## docgen/models/cache.py

### CacheEntry

**型**: `class`

**シグネチャ**:
```
class CacheEntry:
```

**説明**:

キャッシュエントリーモデル

*定義場所: docgen/models/cache.py:10*

---

### CacheMetadata

**型**: `class`

**シグネチャ**:
```
class CacheMetadata:
```

**説明**:

キャッシュメタデータモデル

*定義場所: docgen/models/cache.py:19*

---


## docgen/models/config.py

### LanguagesConfig

**型**: `class`

**シグネチャ**:
```
class LanguagesConfig:
```

**説明**:

Languages configuration model.

*定義場所: docgen/models/config.py:10*

---

### OutputConfig

**型**: `class`

**シグネチャ**:
```
class OutputConfig:
```

**説明**:

Output configuration model.

*定義場所: docgen/models/config.py:17*

---

### GenerationConfig

**型**: `class`

**シグネチャ**:
```
class GenerationConfig:
```

**説明**:

Generation configuration model.

*定義場所: docgen/models/config.py:25*

---

### ExcludeConfig

**型**: `class`

**シグネチャ**:
```
class ExcludeConfig:
```

**説明**:

Exclude configuration model.

*定義場所: docgen/models/config.py:34*

---

### CacheConfig

**型**: `class`

**シグネチャ**:
```
class CacheConfig:
```

**説明**:

Cache configuration model.

*定義場所: docgen/models/config.py:41*

---

### DebugConfig

**型**: `class`

**シグネチャ**:
```
class DebugConfig:
```

**説明**:

Debug configuration model.

*定義場所: docgen/models/config.py:47*

---

### EmbeddingConfig

**型**: `class`

**シグネチャ**:
```
class EmbeddingConfig:
```

**説明**:

Embedding configuration model.

*定義場所: docgen/models/config.py:53*

---

### IndexConfig

**型**: `class`

**シグネチャ**:
```
class IndexConfig:
```

**説明**:

Index configuration model.

*定義場所: docgen/models/config.py:60*

---

### RetrievalConfig

**型**: `class`

**シグネチャ**:
```
class RetrievalConfig:
```

**説明**:

Retrieval configuration model.

*定義場所: docgen/models/config.py:68*

---

### ChunkingConfig

**型**: `class`

**シグネチャ**:
```
class ChunkingConfig:
```

**説明**:

Chunking configuration model.

*定義場所: docgen/models/config.py:75*

---

### RagExcludeConfig

**型**: `class`

**シグネチャ**:
```
class RagExcludeConfig:
```

*説明なし*

*定義場所: docgen/models/config.py:82*

---

### RagConfig

**型**: `class`

**シグネチャ**:
```
class RagConfig:
```

**説明**:

RAG configuration model.

*定義場所: docgen/models/config.py:94*

---

### ArchitecturePythonConfig

**型**: `class`

**シグネチャ**:
```
class ArchitecturePythonConfig:
```

**説明**:

Python architecture configuration.

*定義場所: docgen/models/config.py:106*

---

### ArchitectureJavascriptConfig

**型**: `class`

**シグネチャ**:
```
class ArchitectureJavascriptConfig:
```

**説明**:

JavaScript architecture configuration.

*定義場所: docgen/models/config.py:113*

---

### ArchitectureConfig

**型**: `class`

**シグネチャ**:
```
class ArchitectureConfig:
```

**説明**:

Architecture diagram generation configuration.

*定義場所: docgen/models/config.py:119*

---

### DocgenConfig

**型**: `class`

**シグネチャ**:
```
class DocgenConfig:
```

**説明**:

Main configuration model for docgen.

*定義場所: docgen/models/config.py:130*

---


## docgen/models/detector.py

### PackageManagerRule

**型**: `class`

**シグネチャ**:
```
class PackageManagerRule:
```

**説明**:

Package manager detection rule.

*定義場所: docgen/models/detector.py:9*

---

### validate_files

**型**: `method`

**シグネチャ**:
```
def validate_files(cls, v: tuple[str, ...]) -> tuple[str, ...]:
```

*説明なし*

*定義場所: docgen/models/detector.py:21*

---

### validate_manager

**型**: `method`

**シグネチャ**:
```
def validate_manager(cls, v: str) -> str:
```

*説明なし*

*定義場所: docgen/models/detector.py:28*

---

### LanguageConfig

**型**: `class`

**シグネチャ**:
```
class LanguageConfig:
```

**説明**:

Language detection configuration.

*定義場所: docgen/models/detector.py:34*

---

### validate_name

**型**: `method`

**シグネチャ**:
```
def validate_name(cls, v: str) -> str:
```

*説明なし*

*定義場所: docgen/models/detector.py:54*

---

### get_sorted_package_manager_rules

**型**: `method`

**シグネチャ**:
```
def get_sorted_package_manager_rules(self) -> list[PackageManagerRule]:
```

**説明**:

Return package manager rules sorted by priority.

*定義場所: docgen/models/detector.py:59*

---


## docgen/models/llm.py

### LLMConfig

**型**: `class`

**シグネチャ**:
```
class LLMConfig:
```

**説明**:

LLM設定モデル

*定義場所: docgen/models/llm.py:6*

---

### LLMClientConfig

**型**: `class`

**シグネチャ**:
```
class LLMClientConfig:
```

**説明**:

LLMクライアント設定モデル

*定義場所: docgen/models/llm.py:24*

---


## docgen/models/project.py

### ProjectInfo

**型**: `class`

**シグネチャ**:
```
class ProjectInfo:
```

**説明**:

Project information model.

*定義場所: docgen/models/project.py:8*

---


## docgen/models/readme.py

### Dependencies

**型**: `class`

**シグネチャ**:
```
class Dependencies:
```

**説明**:

Dependencies model.

*定義場所: docgen/models/readme.py:6*

---

### ReadmeSetupInstructions

**型**: `class`

**シグネチャ**:
```
class ReadmeSetupInstructions:
```

**説明**:

Setup instructions for README.

*定義場所: docgen/models/readme.py:14*

---

### ReadmeConfig

**型**: `class`

**シグネチャ**:
```
class ReadmeConfig:
```

**説明**:

Configuration model for README documentation.

*定義場所: docgen/models/readme.py:21*

---

### ReadmeDocument

**型**: `class`

**シグネチャ**:
```
class ReadmeDocument:
```

**説明**:

READMEドキュメントの構造化データモデル

*定義場所: docgen/models/readme.py:40*

---


## docgen/rag/chunker.py

### CodeChunker

**型**: `class`

**シグネチャ**:
```
class CodeChunker:
```

**説明**:

コードベースをチャンク化するクラス

*定義場所: docgen/rag/chunker.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | None):
```

**説明**:

初期化

Args:
    config: RAG設定（config.toml の rag セクション）

*定義場所: docgen/rag/chunker.py:44*

---

### should_process_file

**型**: `method`

**シグネチャ**:
```
def should_process_file(self, file_path: Path) -> bool:
```

**説明**:

ファイルを処理すべきかどうかを判定

Args:
    file_path: ファイルパス

Returns:
    処理すべき場合True

*定義場所: docgen/rag/chunker.py:62*

---

### chunk_file

**型**: `method`

**シグネチャ**:
```
def chunk_file(self, file_path: Path, project_root: Path) -> list[dict[str, Any]]:
```

**説明**:

ファイルをチャンク化

Args:
    file_path: ファイルパス
    project_root: プロジェクトルート

Returns:
    チャンクのリスト

*定義場所: docgen/rag/chunker.py:130*

---

### chunk_codebase

**型**: `method`

**シグネチャ**:
```
def chunk_codebase(self, project_root: Path) -> list[dict[str, Any]]:
```

**説明**:

プロジェクト全体をチャンク化

Args:
    project_root: プロジェクトルート

Returns:
    すべてのチャンクのリスト

*定義場所: docgen/rag/chunker.py:165*

---


## docgen/rag/embedder.py

### Embedder

**型**: `class`

**シグネチャ**:
```
class Embedder:
```

**説明**:

テキスト埋め込み生成クラス

*定義場所: docgen/rag/embedder.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    config: RAG設定（config.toml の rag セクション）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/embedder.py:19*

---

### model

**型**: `method`

**シグネチャ**:
```
def model(self):
```

**説明**:

埋め込みモデルをLazy load

*定義場所: docgen/rag/embedder.py:40*

---

### embedding_dim

**型**: `method`

**シグネチャ**:
```
def embedding_dim(self) -> int:
```

**説明**:

埋め込みベクトルの次元数

*定義場所: docgen/rag/embedder.py:58*

---

### embed_text

**型**: `method`

**シグネチャ**:
```
def embed_text(self, text: str) -> np.ndarray:
```

**説明**:

テキストを埋め込みベクトルに変換

Args:
    text: 入力テキスト

Returns:
    埋め込みベクトル（numpy配列）

*定義場所: docgen/rag/embedder.py:62*

---

### embed_batch

**型**: `method`

**シグネチャ**:
```
def embed_batch(self, texts: list[str], batch_size: int) -> np.ndarray:
```

**説明**:

複数のテキストをバッチ処理で埋め込み

Args:
    texts: 入力テキストのリスト
    batch_size: バッチサイズ

Returns:
    埋め込みベクトルの配列（shape: [len(texts), embedding_dim]）

*定義場所: docgen/rag/embedder.py:88*

---


## docgen/rag/indexer.py

### VectorIndexer

**型**: `class`

**シグネチャ**:
```
class VectorIndexer:
```

**説明**:

ベクトルインデックス管理クラス

*定義場所: docgen/rag/indexer.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, index_dir: Path, embedding_dim: int, config: dict[str, Any] | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    index_dir: インデックス保存ディレクトリ
    embedding_dim: 埋め込みベクトルの次元数
    config: RAG設定（config.toml の rag セクション）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/indexer.py:19*

---

### build

**型**: `method`

**シグネチャ**:
```
def build(self, embeddings: np.ndarray, metadata: list[dict[str, Any]]):
```

**説明**:

インデックスを構築

Args:
    embeddings: 埋め込みベクトルの配列（shape: [n_samples, embedding_dim]）
    metadata: 各埋め込みに対応するメタデータのリスト

*定義場所: docgen/rag/indexer.py:50*

---

### save

**型**: `method`

**シグネチャ**:
```
def save(self):
```

**説明**:

インデックスとメタデータを保存

*定義場所: docgen/rag/indexer.py:101*

---

### load

**型**: `method`

**シグネチャ**:
```
def load(self):
```

**説明**:

インデックスとメタデータを読み込み

*定義場所: docgen/rag/indexer.py:130*

---

### search

**型**: `method`

**シグネチャ**:
```
def search(self, query_embedding: np.ndarray, k: int) -> list[tuple[dict[str, Any], float]]:
```

**説明**:

類似ベクトルを検索

Args:
    query_embedding: クエリの埋め込みベクトル
    k: 取得する件数

Returns:
    (メタデータ, スコア) のタプルのリスト

*定義場所: docgen/rag/indexer.py:169*

---

### incremental_update

**型**: `method`

**シグネチャ**:
```
def incremental_update(self, new_embeddings: np.ndarray, new_metadata: list[dict[str, Any]]):
```

**説明**:

インデックスに新しいデータを追加（増分更新）

Args:
    new_embeddings: 新しい埋め込みベクトル
    new_metadata: 新しいメタデータ

*定義場所: docgen/rag/indexer.py:199*

---


## docgen/rag/retriever.py

### DocumentRetriever

**型**: `class`

**シグネチャ**:
```
class DocumentRetriever:
```

**説明**:

ドキュメント検索クラス

*定義場所: docgen/rag/retriever.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any], project_root: Path | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    config: 設定辞書（config.toml全体）
    project_root: プロジェクトルート（指定しない場合は現在のディレクトリ）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/retriever.py:18*

---

### embedder

**型**: `method`

**シグネチャ**:
```
def embedder(self) -> Embedder:
```

**説明**:

Embedderインスタンスを取得（Lazy loading）

*定義場所: docgen/rag/retriever.py:50*

---

### indexer

**型**: `method`

**シグネチャ**:
```
def indexer(self) -> VectorIndexer:
```

**説明**:

VectorIndexerインスタンスを取得（Lazy loading）

*定義場所: docgen/rag/retriever.py:57*

---

### retrieve

**型**: `method`

**シグネチャ**:
```
def retrieve(self, query: str, top_k: int | None) -> list[dict[str, Any]]:
```

**説明**:

クエリに類似するチャンクを検索

Args:
    query: 検索クエリ
    top_k: 取得する件数（Noneの場合はデフォルト値）

Returns:
    チャンクのリスト（スコア付き）

*定義場所: docgen/rag/retriever.py:83*

---

### format_context

**型**: `method`

**シグネチャ**:
```
def format_context(self, chunks: list[dict[str, Any]]) -> str:
```

**説明**:

チャンクをコンテキスト文字列にフォーマット

Args:
    chunks: チャンクのリスト

Returns:
    フォーマット済みのコンテキスト文字列

*定義場所: docgen/rag/retriever.py:118*

---

### retrieve_with_rerank

**型**: `method`

**シグネチャ**:
```
def retrieve_with_rerank(self, query: str, top_k: int, rerank_k: int) -> list[dict[str, Any]]:
```

**説明**:

再ランキング付き検索（将来の拡張用）

Args:
    query: 検索クエリ
    top_k: 最終的に取得する件数
    rerank_k: 初期検索で取得する件数（再ランク対象）

Returns:
    再ランク済みのチャンクのリスト

*定義場所: docgen/rag/retriever.py:150*

---


## docgen/rag/strategies/base_strategy.py

### BaseChunkStrategy

**型**: `class`

**シグネチャ**:
```
class BaseChunkStrategy:
```

**説明**:

Base class for chunking strategies.

*定義場所: docgen/rag/strategies/base_strategy.py:10*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

*説明なし*

*定義場所: docgen/rag/strategies/base_strategy.py:13*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk the content.

Args:
    content: File content
    file_path: Path to the file

Returns:
    List of chunks

*定義場所: docgen/rag/strategies/base_strategy.py:17*

---


## docgen/rag/strategies/code_strategy.py

### CodeChunkStrategy

**型**: `class`

**シグネチャ**:
```
class CodeChunkStrategy:
```

**説明**:

Strategy for chunking code files (Python, YAML, TOML).

*定義場所: docgen/rag/strategies/code_strategy.py:15*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk code content based on file extension.

*定義場所: docgen/rag/strategies/code_strategy.py:18*

---


## docgen/rag/strategies/markdown_strategy.py

### MarkdownChunkStrategy

**型**: `class`

**シグネチャ**:
```
class MarkdownChunkStrategy:
```

**説明**:

Strategy for chunking Markdown files.

*定義場所: docgen/rag/strategies/markdown_strategy.py:11*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk Markdown files by headers.

*定義場所: docgen/rag/strategies/markdown_strategy.py:14*

---


## docgen/rag/strategies/text_strategy.py

### TextChunkStrategy

**型**: `class`

**シグネチャ**:
```
class TextChunkStrategy:
```

**説明**:

Strategy for chunking generic text files.

*定義場所: docgen/rag/strategies/text_strategy.py:11*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk generic files as a single chunk.

*定義場所: docgen/rag/strategies/text_strategy.py:14*

---


## docgen/rag/validator.py

### DocumentValidator

**型**: `class`

**シグネチャ**:
```
class DocumentValidator:
```

**説明**:

ドキュメント検証クラス

*定義場所: docgen/rag/validator.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルート

*定義場所: docgen/rag/validator.py:56*

---

### validate_citations

**型**: `method`

**シグネチャ**:
```
def validate_citations(self, document: str, strict: bool) -> list[str]:
```

**説明**:

ドキュメント内の出典を検証

Args:
    document: 検証対象のドキュメント
    strict: 厳格モード（技術的主張に出典がない場合もエラー）

Returns:
    エラーメッセージのリスト

*定義場所: docgen/rag/validator.py:65*

---

### detect_secrets

**型**: `method`

**シグネチャ**:
```
def detect_secrets(self, document: str) -> list[str]:
```

**説明**:

ドキュメント内の機密情報を検出

Args:
    document: 検証対象のドキュメント

Returns:
    警告メッセージのリスト

*定義場所: docgen/rag/validator.py:145*

---

### validate

**型**: `method`

**シグネチャ**:
```
def validate(self, document: str, check_citations: bool, check_secrets: bool, strict: bool) -> dict[str, Any]:
```

**説明**:

ドキュメントの総合検証

Args:
    document: 検証対象のドキュメント
    check_citations: 出典チェックを行うか
    check_secrets: 機密情報チェックを行うか
    strict: 厳格モード

Returns:
    検証結果の辞書

*定義場所: docgen/rag/validator.py:180*

---

### print_report

**型**: `method`

**シグネチャ**:
```
def print_report(self, validation_result: dict[str, Any]):
```

**説明**:

検証結果をコンソールに出力

*定義場所: docgen/rag/validator.py:226*

---


## docgen/utils/cache.py

### CacheManager

**型**: `class`

**シグネチャ**:
```
class CacheManager:
```

**説明**:

キャッシュ管理クラス

*定義場所: docgen/utils/cache.py:20*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, cache_dir: Path | None, enabled: bool):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    cache_dir: キャッシュディレクトリ（Noneの場合は`docgen/.cache/`）
    enabled: キャッシュを有効にするかどうか

*定義場所: docgen/utils/cache.py:23*

---

### get_file_hash

**型**: `method`

**シグネチャ**:
```
def get_file_hash(self, file_path: Path) -> str:
```

**説明**:

ファイルのハッシュを計算

Args:
    file_path: ファイルパス

Returns:
    ファイルのSHA256ハッシュ（16進数文字列）

*定義場所: docgen/utils/cache.py:78*

---

### get_cache_key

**型**: `method`

**シグネチャ**:
```
def get_cache_key(self, file_path: Path, parser_type: str) -> str:
```

**説明**:

キャッシュキーを生成

Args:
    file_path: ファイルパス（相対パスまたは絶対パス）
    parser_type: パーサーの種類（例: 'python', 'javascript'）

Returns:
    キャッシュキー

*定義場所: docgen/utils/cache.py:99*

---

### get_cached_result

**型**: `method`

**シグネチャ**:
```
def get_cached_result(self, file_path: Path, parser_type: str) -> list[APIInfo] | None:
```

**説明**:

キャッシュから結果を取得

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類

Returns:
    キャッシュされた結果（存在する場合）、またはNone

*定義場所: docgen/utils/cache.py:124*

---

### set_cached_result

**型**: `method`

**シグネチャ**:
```
def set_cached_result(self, file_path: Path, parser_type: str, result: list[APIInfo]) -> None:
```

**説明**:

結果をキャッシュに保存

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類
    result: 解析結果

*定義場所: docgen/utils/cache.py:164*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(self) -> None:
```

**説明**:

キャッシュをクリア

*定義場所: docgen/utils/cache.py:194*

---

### invalidate_file

**型**: `method`

**シグネチャ**:
```
def invalidate_file(self, file_path: Path, parser_type: str | None) -> None:
```

**説明**:

特定のファイルのキャッシュを無効化

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類（Noneの場合はすべてのパーサータイプ）

*定義場所: docgen/utils/cache.py:201*

---

### save

**型**: `method`

**シグネチャ**:
```
def save(self) -> None:
```

**説明**:

キャッシュを保存（明示的に保存する場合）

*定義場所: docgen/utils/cache.py:237*

---

### get_cache_stats

**型**: `method`

**シグネチャ**:
```
def get_cache_stats(self) -> dict[str, Any]:
```

**説明**:

キャッシュの統計情報を取得

Returns:
    統計情報の辞書

*定義場所: docgen/utils/cache.py:241*

---


## docgen/utils/config_utils.py

### get_nested_config

**型**: `function`

**シグネチャ**:
```
def get_nested_config(config: dict[str, Any]) -> Any:
```

**説明**:

ネストされた設定値を安全に取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    設定値。存在しない場合はdefault

Examples:
    >>> config = {"a": {"b": {"c": "value"}}}
    >>> get_nested_config(config, "a", "b", "c")
    'value'
    >>> get_nested_config(config, "a", "x", "y", default="default")
    'default'

*定義場所: docgen/utils/config_utils.py:8*

---

### get_config_bool

**型**: `function`

**シグネチャ**:
```
def get_config_bool(config: dict[str, Any]) -> bool:
```

**説明**:

設定値をブール値として取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    ブール値

*定義場所: docgen/utils/config_utils.py:36*

---

### get_config_list

**型**: `function`

**シグネチャ**:
```
def get_config_list(config: dict[str, Any]) -> list:
```

**説明**:

設定値をリストとして取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    リスト

*定義場所: docgen/utils/config_utils.py:56*

---

### get_config_str

**型**: `function`

**シグネチャ**:
```
def get_config_str(config: dict[str, Any]) -> str:
```

**説明**:

設定値を文字列として取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    文字列

*定義場所: docgen/utils/config_utils.py:81*

---


## docgen/utils/exceptions.py

### ErrorMessages

**型**: `class`

**シグネチャ**:
```
class ErrorMessages:
```

**説明**:

共通エラーメッセージ定数

*定義場所: docgen/utils/exceptions.py:9*

---

### DocGenError

**型**: `class`

**シグネチャ**:
```
class DocGenError:
```

**説明**:

ドキュメント生成システムの基本例外クラス

*定義場所: docgen/utils/exceptions.py:24*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, details: str | None, error_code: str | None, context: dict[str, Any] | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:27*

---

### __str__

**型**: `method`

**シグネチャ**:
```
def __str__(self) -> str:
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:39*

---

### ConfigError

**型**: `class`

**シグネチャ**:
```
class ConfigError:
```

**説明**:

設定関連のエラー

*定義場所: docgen/utils/exceptions.py:49*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, config_path: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:52*

---

### LLMError

**型**: `class`

**シグネチャ**:
```
class LLMError:
```

**説明**:

LLM関連のエラー

*定義場所: docgen/utils/exceptions.py:64*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, provider: str | None, model: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:67*

---

### ParseError

**型**: `class`

**シグネチャ**:
```
class ParseError:
```

**説明**:

解析関連のエラー

*定義場所: docgen/utils/exceptions.py:81*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, file_path: str | None, language: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:84*

---

### CacheError

**型**: `class`

**シグネチャ**:
```
class CacheError:
```

**説明**:

キャッシュ関連のエラー

*定義場所: docgen/utils/exceptions.py:100*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, cache_key: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:103*

---

### FileOperationError

**型**: `class`

**シグネチャ**:
```
class FileOperationError:
```

**説明**:

ファイル操作関連のエラー

*定義場所: docgen/utils/exceptions.py:115*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, file_path: str | None, operation: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:118*

---

### GenerationError

**型**: `class`

**シグネチャ**:
```
class GenerationError:
```

**説明**:

ドキュメント生成関連のエラー

*定義場所: docgen/utils/exceptions.py:134*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, doc_type: str | None, generator: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:137*

---

### HookError

**型**: `class`

**シグネチャ**:
```
class HookError:
```

**説明**:

フック関連のエラー

*定義場所: docgen/utils/exceptions.py:157*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, hook_name: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:160*

---

### TemplateError

**型**: `class`

**シグネチャ**:
```
class TemplateError:
```

**説明**:

テンプレート関連のエラー

*定義場所: docgen/utils/exceptions.py:171*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, template_name: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:174*

---


## docgen/utils/file_utils.py

### safe_read_file

**型**: `function`

**シグネチャ**:
```
def safe_read_file(file_path: Path, encoding: str) -> str | None:
```

**説明**:

ファイルを安全に読み込む

Args:
    file_path: 読み込むファイルのパス
    encoding: 文字エンコーディング

Returns:
    ファイルの内容。読み込み失敗時はNone

*定義場所: docgen/utils/file_utils.py:20*

---

### save_yaml_file

**型**: `function`

**シグネチャ**:
```
def save_yaml_file(file_path: Path, data: dict[str, Any]) -> bool:
```

**説明**:

YAMLファイルを保存

Args:
    file_path: 保存先ファイルパス
    data: 保存するデータ

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:39*

---

### save_toml_file

**型**: `function`

**シグネチャ**:
```
def save_toml_file(file_path: Path, content: str) -> bool:
```

**説明**:

TOMLファイルを保存

Args:
    file_path: 保存先ファイルパス
    content: TOML形式の文字列

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:61*

---

### safe_write_file

**型**: `function`

**シグネチャ**:
```
def safe_write_file(file_path: Path, content: str, encoding: str) -> bool:
```

**説明**:

ファイルを安全に書き込む

Args:
    file_path: 書き込むファイルのパス
    content: 書き込む内容
    encoding: 文字エンコーディング

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:80*

---

### safe_read_json

**型**: `function`

**シグネチャ**:
```
def safe_read_json(file_path: Path) -> Any | None:
```

**説明**:

JSONファイルを安全に読み込む

Args:
    file_path: JSONファイルのパス

Returns:
    パースされたJSONデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:100*

---

### find_files_with_extensions

**型**: `function`

**シグネチャ**:
```
def find_files_with_extensions(root_dir: Path, extensions: list[str]) -> list[Path]:
```

**説明**:

指定された拡張子のファイルを検索

Args:
    root_dir: 検索するルートディレクトリ
    extensions: 拡張子のリスト（例: ['.py', '.js']）

Returns:
    見つかったファイルのリスト

*定義場所: docgen/utils/file_utils.py:119*

---

### safe_read_yaml

**型**: `function`

**シグネチャ**:
```
def safe_read_yaml(file_path: Path) -> Any | None:
```

**説明**:

YAMLファイルを安全に読み込む

Args:
    file_path: YAMLファイルのパス

Returns:
    パースされたYAMLデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:136*

---

### safe_read_toml

**型**: `function`

**シグネチャ**:
```
def safe_read_toml(file_path: Path) -> Any | None:
```

**説明**:

TOMLファイルを安全に読み込む

Args:
    file_path: TOMLファイルのパス

Returns:
    パースされたTOMLデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:157*

---


## docgen/utils/llm/anthropic_client.py

### AnthropicClient

**型**: `class`

**シグネチャ**:
```
class AnthropicClient:
```

**説明**:

Anthropic APIクライアント

*定義場所: docgen/utils/llm/anthropic_client.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/anthropic_client.py:16*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

Anthropic APIを使用してテキストを生成

*定義場所: docgen/utils/llm/anthropic_client.py:35*

---


## docgen/utils/llm/base.py

### LLMClientInitializer

**型**: `class`

**シグネチャ**:
```
class LLMClientInitializer:
```

**説明**:

Common initialization patterns for LLM clients.

*定義場所: docgen/utils/llm/base.py:25*

---

### setup_provider_config

**型**: `method`

**シグネチャ**:
```
def setup_provider_config(config: dict[str, Any], provider: str) -> dict[str, Any]:
```

**説明**:

Set up provider-specific configuration.

Args:
    config: Configuration dictionary
    provider: Provider name ('openai', 'anthropic', etc.)

Returns:
    Updated configuration dictionary

*定義場所: docgen/utils/llm/base.py:29*

---

### get_api_key

**型**: `method`

**シグネチャ**:
```
def get_api_key(config, env_var: str, default_env: str) -> str:
```

**説明**:

Get API key from config or environment.

Args:
    config: LLMConfig object
    env_var: Environment variable name from config
    default_env: Default environment variable name

Returns:
    API key string

*定義場所: docgen/utils/llm/base.py:46*

---

### initialize_client_with_fallback

**型**: `method`

**シグネチャ**:
```
def initialize_client_with_fallback(client_class, config: dict[str, Any], import_name: str, package_name: str, error_prefix: str):
```

**説明**:

Initialize LLM client with common error handling.

Args:
    client_class: Client class to instantiate
    config: Configuration dictionary
    import_name: Module name to import
    package_name: Package name for error messages
    error_prefix: Prefix for error messages

Returns:
    Initialized client instance

Raises:
    ImportError: If required package is not installed
    ConfigError: If initialization fails

*定義場所: docgen/utils/llm/base.py:63*

---

### BaseLLMClient

**型**: `class`

**シグネチャ**:
```
class BaseLLMClient:
```

**説明**:

LLMクライアントの抽象基底クラス

*定義場所: docgen/utils/llm/base.py:100*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | LLMConfig):
```

**説明**:

初期化

Args:
    config: LLM設定辞書またはLLMConfigオブジェクト

*定義場所: docgen/utils/llm/base.py:103*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

テキストを生成

Args:
    prompt: プロンプト
    system_prompt: システムプロンプト（オプション）
    **kwargs: その他のパラメータ

Returns:
    生成されたテキスト（エラー時はNone）

*定義場所: docgen/utils/llm/base.py:120*

---

### create_outlines_model

**型**: `method`

**シグネチャ**:
```
def create_outlines_model(self):
```

**説明**:

Outlinesモデルを作成

Returns:
    Outlinesモデルインスタンス（Outlinesが利用できない場合はNone）

*定義場所: docgen/utils/llm/base.py:134*

---


## docgen/utils/llm/factory.py

### LLMClientFactory

**型**: `class`

**シグネチャ**:
```
class LLMClientFactory:
```

**説明**:

LLMクライアントのファクトリークラス

*定義場所: docgen/utils/llm/factory.py:18*

---

### create_client

**型**: `method`

**シグネチャ**:
```
def create_client(config: dict[str, Any] | LLMClientConfig, mode: str) -> BaseLLMClient | None:
```

**説明**:

LLMクライアントを作成

Args:
    config: LLM設定辞書またはLLMClientConfigオブジェクト
    mode: 'api' または 'local'

Returns:
    LLMクライアントインスタンス（エラー時はNone）

*定義場所: docgen/utils/llm/factory.py:22*

---

### create_client_with_fallback

**型**: `method`

**シグネチャ**:
```
def create_client_with_fallback(config: dict[str, Any], preferred_mode: str) -> BaseLLMClient | None:
```

**説明**:

LLMクライアントを作成（フォールバック付き）

Args:
    config: LLM設定辞書
    preferred_mode: 優先するモード（'api' または 'local'）

Returns:
    LLMクライアントインスタンス（エラー時はNone）

*定義場所: docgen/utils/llm/factory.py:81*

---


## docgen/utils/llm/local_client.py

### LocalLLMClient

**型**: `class`

**シグネチャ**:
```
class LocalLLMClient:
```

**説明**:

ローカルLLMクライアント（Ollama、LM Studio対応）

*定義場所: docgen/utils/llm/local_client.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/local_client.py:17*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

ローカルLLMを使用してテキストを生成

*定義場所: docgen/utils/llm/local_client.py:43*

---


## docgen/utils/llm/openai_client.py

### OpenAIClient

**型**: `class`

**シグネチャ**:
```
class OpenAIClient:
```

**説明**:

OpenAI APIクライアント

*定義場所: docgen/utils/llm/openai_client.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/openai_client.py:16*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

OpenAI APIを使用してテキストを生成

*定義場所: docgen/utils/llm/openai_client.py:36*

---


## docgen/utils/logger.py

### setup_logger

**型**: `function`

**シグネチャ**:
```
def setup_logger(name: str, level: str | None, log_file: Path | None) -> logging.Logger:
```

**説明**:

ロガーを設定して返す

Args:
    name: ロガー名
    level: ログレベル（'DEBUG', 'INFO', 'WARNING', 'ERROR'）
            Noneの場合は環境変数DOCGEN_LOG_LEVELから取得、それもなければ'INFO'
    log_file: ログファイルのパス（Noneの場合は標準出力のみ）

Returns:
    設定済みのロガー

*定義場所: docgen/utils/logger.py:11*

---

### get_logger

**型**: `function`

**シグネチャ**:
```
def get_logger(name: str | None) -> logging.Logger:
```

**説明**:

ロガーを取得する（既に設定されている場合はそれを返す）

Args:
    name: ロガー名（Noneの場合は'docgen'）

Returns:
    ロガー

*定義場所: docgen/utils/logger.py:70*

---


## docgen/utils/markdown_utils.py

### get_current_timestamp

**型**: `function`

**シグネチャ**:
```
def get_current_timestamp() -> str:
```

**説明**:

Get current timestamp in standard format.

*定義場所: docgen/utils/markdown_utils.py:31*

---

### extract_project_description

**型**: `function`

**シグネチャ**:
```
def extract_project_description(project_root: Path, project_info_description: str | None, exclude_readme_path: Path | None) -> str:
```

**説明**:

Extract project description from README.md or project info.

Args:
    project_root: Project root directory
    project_info_description: Description from project info (fallback)
    exclude_readme_path: README path to exclude (to prevent circular reference)

Returns:
    Project description text

*定義場所: docgen/utils/markdown_utils.py:38*

---

### clean_llm_output_advanced

**型**: `function`

**シグネチャ**:
```
def clean_llm_output_advanced(text: str) -> str:
```

**説明**:

Advanced LLM output cleaning with thinking process removal and code block handling.

Args:
    text: LLM generated text to clean

Returns:
    Cleaned text with thinking processes removed

*定義場所: docgen/utils/markdown_utils.py:79*

---


## docgen/utils/outlines_utils.py

### should_use_outlines

**型**: `function`

**シグネチャ**:
```
def should_use_outlines(config: dict[str, Any]) -> bool:
```

**説明**:

Outlinesを使用するかどうかを判定

Args:
    config: 設定辞書

Returns:
    Outlinesを使用するかどうか

*定義場所: docgen/utils/outlines_utils.py:19*

---

### create_outlines_model

**型**: `function`

**シグネチャ**:
```
def create_outlines_model(client, provider: str):
```

**説明**:

Outlinesモデルを作成

Args:
    client: LLMクライアント
    provider: プロバイダー名 ('openai', 'anthropic', 'local')

Returns:
    Outlinesモデルインスタンス（作成できない場合はNone）

*定義場所: docgen/utils/outlines_utils.py:37*

---

### get_llm_client_with_fallback

**型**: `function`

**シグネチャ**:
```
def get_llm_client_with_fallback(config: dict[str, Any], agents_config: dict[str, Any]):
```

**説明**:

LLMクライアントを取得（フォールバック付き）

Args:
    config: メイン設定
    agents_config: AGENTS設定

Returns:
    LLMクライアントインスタンス

*定義場所: docgen/utils/outlines_utils.py:84*

---

### validate_output

**型**: `function`

**シグネチャ**:
```
def validate_output(text: str) -> bool:
```

**説明**:

LLMの出力を検証して、不適切な内容が含まれていないかチェック

Args:
    text: 検証するテキスト

Returns:
    検証に合格したかどうか

*定義場所: docgen/utils/outlines_utils.py:103*

---


## docgen/utils/prompt_loader.py

### PromptLoader

**型**: `class`

**シグネチャ**:
```
class PromptLoader:
```

**説明**:

プロンプトをTOMLファイルから読み込むクラス

*定義場所: docgen/utils/prompt_loader.py:25*

---

### load_prompt

**型**: `method`

**シグネチャ**:
```
def load_prompt(cls, file_name: str, key: str) -> str:
```

**説明**:

プロンプトを読み込む

Args:
    file_name: TOMLファイル名（例: 'agents_prompts.toml'）
    key: プロンプトのキー（例: 'overview', 'full'）
    **kwargs: テンプレート変数の置換用パラメータ

Returns:
    読み込んだプロンプト文字列（テンプレート変数が置換済み）

Raises:
    FileNotFoundError: ファイルが見つからない場合
    KeyError: 指定されたキーが見つからない場合

*定義場所: docgen/utils/prompt_loader.py:98*

---

### load_system_prompt

**型**: `method`

**シグネチャ**:
```
def load_system_prompt(cls, file_name: str, key: str) -> str:
```

**説明**:

システムプロンプトを読み込む

Args:
    file_name: TOMLファイル名（例: 'agents_prompts.toml'）
    key: システムプロンプトのキー（例: 'overview', 'generate'）
    **kwargs: テンプレート変数の置換用パラメータ

Returns:
    読み込んだシステムプロンプト文字列（テンプレート変数が置換済み）

Raises:
    FileNotFoundError: ファイルが見つかりません場合
    KeyError: 指定されたキーが見つからない場合

*定義場所: docgen/utils/prompt_loader.py:133*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(cls):
```

**説明**:

キャッシュをクリア（主にテスト用）

*定義場所: docgen/utils/prompt_loader.py:168*

---


## scripts/generate_requirements.py

### generate_requirements_file

**型**: `function`

**シグネチャ**:
```
def generate_requirements_file(extras: list[str], output_file: Path, include_base: bool) -> None:
```

**説明**:

pyproject.tomlからrequirementsファイルを生成

Args:
    extras: オプショナル依存関係のリスト（例: ['docgen', 'test']）
    output_file: 出力ファイルのパス
    include_base: 基本依存関係を含めるかどうか

*定義場所: scripts/generate_requirements.py:12*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メイン処理

*定義場所: scripts/generate_requirements.py:74*

---
