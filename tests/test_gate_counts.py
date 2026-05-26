from verifier.gate_counts import (
    circuit_hash_from_gate_list,
    count_gate_basis,
    load_gate_list,
    summarize_gate_counts,
    validate_gate_indices,
)


def test_count_gate_basis():
    gates = [{"type": "CNOT"}, {"type": "TOFFOLI"}, {"type": "CNOT"}, {"other": "ignored"}]
    assert count_gate_basis(gates) == {"CNOT": 2, "TOFFOLI": 1}


def test_summarize_gate_counts_empty_and_nonempty():
    assert summarize_gate_counts([])["total_gates"] == 0
    summary = summarize_gate_counts({"qubit_count": 2, "gates": [{"type": "NOT"}, {"type": "NOT"}]})
    assert summary["logical_qubits"] == 2
    assert summary["total_gates"] == 2
    assert summary["gate_counts_by_type"] == {"NOT": 2}


def test_toy_toffoli_identity_counts():
    circuit = load_gate_list("circuits/toy_toffoli_identity.json")
    summary = summarize_gate_counts(circuit)
    assert summary["toffoli_count"] == 2
    assert summary["cnot_count"] == 0
    assert summary["total_gates"] == 2
    assert summary["logical_qubits"] == 3
    assert validate_gate_indices(circuit) == []
    assert circuit_hash_from_gate_list(circuit)


def test_toy_modinv_stub_counts():
    circuit = load_gate_list("circuits/toy_modinv_stub_8bit.json")
    summary = summarize_gate_counts(circuit)
    assert summary["logical_qubits"] == 24
    assert summary["not_count"] == 1
    assert summary["cnot_count"] == 1
    assert summary["toffoli_count"] == 2
    assert summary["swap_count"] == 1
    assert summary["total_gates"] == 5
    assert summary["serial_depth"] == 5
    assert summary["depth"] == 5  # legacy compatibility alias


def test_validate_gate_indices_reports_out_of_range():
    circuit = {"qubit_count": 2, "gates": [{"type": "CNOT", "controls": [0], "targets": [2]}]}
    errors = validate_gate_indices(circuit)
    assert errors
    assert "outside" in errors[0]