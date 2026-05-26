from pathlib import Path

from scripts.generate_paper_artifact_summary import main


def test_paper_artifact_summary_generation_creates_files():
    assert main() == 0
    md_path = Path("outputs/paper_artifact_summary.md")
    tex_path = Path("outputs/paper_artifact_summary.tex")

    assert md_path.exists()
    assert tex_path.exists()

    markdown = md_path.read_text(encoding="utf-8")
    tex = tex_path.read_text(encoding="utf-8")

    assert "## Modular inversion certificates" in markdown
    assert "## Toy exhaustive certificates" in markdown
    assert "## Resource-count verification fields" in markdown
    assert "## Notes on limitations" in markdown
    assert "Modular inversion certificate rows" in tex
    assert "Toy exhaustive certificate rows" in tex