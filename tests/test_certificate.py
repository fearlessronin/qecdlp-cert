from pathlib import Path

from verifier.certificate import load_certificate, validate_certificate


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "reversible_arithmetic_certificate.schema.json"


def test_example_certificates_validate():
    for name in ["inv_8bit.json", "inv_16bit.json"]:
        cert = load_certificate(ROOT / "examples" / name)
        assert validate_certificate(cert, SCHEMA) is True
