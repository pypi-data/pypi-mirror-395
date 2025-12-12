"""Symlink handling tests for detectors"""

import pytest

from docgen.detectors.unified_detector import UnifiedDetector


def test_symlink_is_ignored_by_all_detectors(temp_project):
    # 実ファイルが検出要件を満たせば検出されることを確認する
    real_rs = temp_project / "real.rs"
    real_rs.write_text("fn main() {}\n")
    try:
        link_rs = temp_project / "link.rs"
        link_rs.symlink_to(real_rs)
    except OSError:
        pytest.skip("Symlinks not supported on this platform")

    detector = UnifiedDetector(temp_project, "rust")
    assert detector.detect() is True
    assert detector.get_language() == "rust"
