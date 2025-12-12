"""
アーキテクチャマニフェストのデータモデル
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
import yaml


class Module(BaseModel):
    """モジュール/パッケージ"""

    name: str
    path: Path
    is_package: bool = False
    dependencies: list[str] = Field(default_factory=list)
    submodules: list["Module"] = Field(default_factory=list)


class Service(BaseModel):
    """個別サービス/コンポーネント"""

    name: str
    type: str  # "python", "docker", "database", "external", etc.
    description: str | None = None
    ports: list[int] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    modules: list[Module] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ArchitectureManifest(BaseModel):
    """アーキテクチャマニフェスト"""

    project_name: str
    version: str = "1.0"
    services: list[Service] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_yaml(self, path: Path) -> None:
        """YAML形式で保存"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.model_dump(), f, allow_unicode=True, sort_keys=False)

    @classmethod
    def from_yaml(cls, path: Path) -> "ArchitectureManifest":
        """YAML形式から読み込み"""
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
