from pathlib import Path

from scripts.generate_certificate_report import EXAMPLES, generate_report, report_row


def test_certificate_report_generation_creates_md_and_csv():
    rows = [report_row(cert_path, circuit_path) for cert_path, circuit_path in EXAMPLES]
    md_path = Path("outputs/certificate_report.md")
    csv_path = Path("outputs/certificate_report.csv")

    generate_report(rows, md_path, csv_path)

    assert md_path.exists()
    assert csv_path.exists()
    assert "Certificate Verification Report" in md_path.read_text(encoding="utf-8")
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "certificate_id" in csv_text
    assert {row["status"] for row in rows} <= {"pass", "fail"}
    assert all(row["status"] == "pass" for row in rows)