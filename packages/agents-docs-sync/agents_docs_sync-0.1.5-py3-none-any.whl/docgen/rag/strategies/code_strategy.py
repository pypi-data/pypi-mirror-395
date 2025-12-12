"""
Code chunking strategy.
"""

import ast
from pathlib import Path
from typing import Any

from ...utils.logger import get_logger
from .base_strategy import BaseChunkStrategy

logger = get_logger(__name__)


class CodeChunkStrategy(BaseChunkStrategy):
    """Strategy for chunking code files (Python, YAML, TOML)."""

    def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """
        Chunk code content based on file extension.
        """
        if file_path.suffix == ".py":
            return self._chunk_python(content, file_path)
        elif file_path.suffix in {".yaml", ".yml"}:
            return self._chunk_yaml(content, file_path)
        elif file_path.suffix == ".toml":
            return self._chunk_toml(content, file_path)
        else:
            # Fallback to generic chunking if extension not explicitly handled but passed to this strategy
            # Ideally, this shouldn't happen if the dispatcher is correct, but good for safety.
            # However, since we have TextChunkStrategy, maybe we should return empty or raise error?
            # For now, let's return empty list or handle it if we want to support other code files generically?
            # But generic chunking is in TextChunkStrategy.
            return []

    def _chunk_python(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk Python files by function and class."""
        chunks = []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")
            # Fallback to treating as a single chunk (handled by caller or return single chunk here?)
            # Returning single chunk here seems appropriate as fallback
            return [
                {
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "File",
                    "name": file_path.name,
                    "text": content,
                    "start_line": 1,
                    "end_line": len(content.splitlines()),
                    "hash": self._hash_text(content),
                }
            ]

        lines = content.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1  # 0-indexed
                end_line = node.end_lineno if node.end_lineno else start_line + 1

                # Extract node content
                chunk_text = "\n".join(lines[start_line:end_line])

                chunks.append(
                    {
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": node.__class__.__name__,
                        "name": node.name,
                        "text": chunk_text,
                        "start_line": start_line + 1,  # 1-indexed for display
                        "end_line": end_line,
                        "hash": self._hash_text(chunk_text),
                    }
                )

        return chunks

    def _chunk_yaml(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk YAML files by top-level keys."""
        chunks = []
        lines = content.splitlines()

        current_section = []
        section_start = 0
        section_name = "preamble"

        for i, line in enumerate(lines):
            # Detect top-level keys (no indent)
            if line and not line.startswith(" ") and ":" in line:
                # Save previous section
                if current_section:
                    section_text = "\n".join(current_section)
                    chunks.append(
                        {
                            "file": str(file_path.relative_to(self.project_root)),
                            "type": "YAMLSection",
                            "name": section_name,
                            "text": section_text,
                            "start_line": section_start + 1,
                            "end_line": i,
                            "hash": self._hash_text(section_text),
                        }
                    )

                # Start new section
                section_name = line.split(":")[0].strip()
                section_start = i
                current_section = [line]
            else:
                current_section.append(line)

        # Save last section
        if current_section:
            section_text = "\n".join(current_section)
            chunks.append(
                {
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "YAMLSection",
                    "name": section_name,
                    "text": section_text,
                    "start_line": section_start + 1,
                    "end_line": len(lines),
                    "hash": self._hash_text(section_text),
                }
            )

        return chunks

    def _chunk_toml(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk TOML files by sections."""
        chunks = []
        lines = content.splitlines()

        current_section = []
        section_start = 0
        section_name = "header"

        for i, line in enumerate(lines):
            # Detect section headers ([section])
            if line.strip().startswith("[") and line.strip().endswith("]"):
                # Save previous section
                if current_section:
                    section_text = "\n".join(current_section)
                    chunks.append(
                        {
                            "file": str(file_path.relative_to(self.project_root)),
                            "type": "TOMLSection",
                            "name": section_name,
                            "text": section_text,
                            "start_line": section_start + 1,
                            "end_line": i,
                            "hash": self._hash_text(section_text),
                        }
                    )

                # Start new section
                section_name = line.strip("[").strip("]")
                section_start = i
                current_section = [line]
            else:
                current_section.append(line)

        # Save last section
        if current_section:
            section_text = "\n".join(current_section)
            chunks.append(
                {
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "TOMLSection",
                    "name": section_name,
                    "text": section_text,
                    "start_line": section_start + 1,
                    "end_line": len(lines),
                    "hash": self._hash_text(section_text),
                }
            )

        return chunks
