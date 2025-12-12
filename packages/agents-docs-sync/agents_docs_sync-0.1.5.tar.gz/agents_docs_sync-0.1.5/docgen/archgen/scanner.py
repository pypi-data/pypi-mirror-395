"""
プロジェクトスキャナー
"""

from pathlib import Path

from .detectors.docker_detector import DockerDetector
from .detectors.python_detector import PythonDetector
from .models import ArchitectureManifest


class ProjectScanner:
    """プロジェクトをスキャンしてアーキテクチャを抽出"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.detectors = [
            PythonDetector(),
            DockerDetector(),
        ]

    def scan(self) -> ArchitectureManifest:
        """プロジェクトをスキャン"""
        services = []
        for detector in self.detectors:
            detected = detector.detect(self.project_root)
            services.extend(detected)

        return ArchitectureManifest(project_name=self.project_root.name, services=services)
