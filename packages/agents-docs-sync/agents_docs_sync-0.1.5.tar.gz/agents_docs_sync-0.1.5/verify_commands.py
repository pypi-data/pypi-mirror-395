import importlib.metadata
import sys
from unittest.mock import MagicMock

importlib.metadata.version = MagicMock(return_value="0.0.0")

from pathlib import Path

sys.path.append("/home/user/projects/hamu/agents-docs-sync")

from docgen.collectors.project_info_collector import ProjectInfoCollector
from docgen.language_detector import LanguageDetector

project_root = Path("/home/user/projects/hamu/agents-docs-sync")
detector = LanguageDetector(project_root)
detector.detect_languages()
package_managers = detector.get_detected_package_managers()

collector = ProjectInfoCollector(project_root, package_managers)
project_info = collector.collect_all()

print("Build Commands:")
for cmd in project_info.build_commands:
    print(f"  - {cmd}")

print("\nTest Commands:")
for cmd in project_info.test_commands:
    print(f"  - {cmd}")

print("\nScripts:")
for name, cmd in project_info.scripts.items():
    print(f"  - {name}: {cmd}")
