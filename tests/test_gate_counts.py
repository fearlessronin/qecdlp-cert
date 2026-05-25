from verifier.gate_counts import count_gate_basis, summarize_gate_counts


def test_count_gate_basis():
    gates = [{"type": "CNOT"}, {"type": "CNOT"}, {"type": "TOFFOLI"}, {}]
    assert count_gate_basis(gates) == {"CNOT": 2, "TOFFOLI": 1, "UNKNOWN": 1}


def test_summarize_gate_counts():
    gates = [{"type": "NOT"}, {"type": "TOFFOLI"}]
    summary = summarize_gate_counts(gates)
    assert summary["total_gates"] == 2
    assert summary["by_type"]["NOT"] == 1
