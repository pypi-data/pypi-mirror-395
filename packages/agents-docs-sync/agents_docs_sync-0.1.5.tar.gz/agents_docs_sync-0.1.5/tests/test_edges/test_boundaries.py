"""Detector boundary tests (self-contained helper)"""

from pathlib import Path

from docgen.detectors.unified_detector import UnifiedDetectorFactory


def _write(root: Path, relative_path: str, content: str) -> Path:
    path = Path(root) / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def test_boundary_language_order_and_all_detected(temp_project):
    _write(temp_project, "main.rs", "fn main() {}\n")
    _write(temp_project, "Main.java", "public class Main {}\n")

    # UnifiedDetector is per-language, but for this test which checks multiple languages,
    # we might need to use the factory or LanguageDetector.
    # However, to keep it simple and close to the original test intent (checking detection logic),
    # we can use the factory to create detectors for all languages and check them.

    from docgen.detectors.unified_detector import UnifiedDetectorFactory

    detectors = UnifiedDetectorFactory.create_all_detectors(temp_project)
    detected = []
    for d in detectors:
        if d.detect():
            detected.append(d.get_language())

    # The original test checked get_language() on a single instance, which implies GenericDetector
    # might have picked the "primary" language.
    # UnifiedDetector doesn't have a "primary" concept across languages, it's one per language.
    # We will adapt the test to check if the expected languages are in the detected list.

    assert "rust" in detected
    assert "java" in detected


def test_boundary_with_third_language(temp_project):
    _write(temp_project, "script.R", "# R code\n")
    _write(temp_project, "main.rs", "fn main() {}\n")
    _write(temp_project, "Main.java", "public class Main {}\n")
    detectors = UnifiedDetectorFactory.create_all_detectors(temp_project)
    detected = []
    for d in detectors:
        if d.detect():
            detected.append(d.get_language())

    langs = set(detected)
    assert {"rust", "java", "r"}.issubset(langs)
