from pathlib import Path


def write_file(root: Path, relative_path: str, content: str) -> Path:
    path = Path(root) / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path
