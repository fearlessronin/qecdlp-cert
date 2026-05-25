from verifier.gate_counts import count_gate_basis, summarize_gate_counts


def test_count_gate_basis():
    gates = [{"type": "CNOT"}, {"type": "TOFFOLI"}, {"type": "CNOT"}, {"other": "ignored"}]
    assert count_gate_basis(gates) == {"CNOT": 2, "TOFFOLI": 1}


def test_summarize_gate_counts_empty_and_nonempty():
    assert summarize_gate_counts([]) == {"total_gates": 0, "basis_counts": {}}
    summary = summarize_gate_counts([{"type": "NOT"}, {"type": "NOT"}])
    assert summary["total_gates"] == 2
    assert summary["basis_counts"] == {"NOT": 2}