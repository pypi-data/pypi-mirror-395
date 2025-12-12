from openquantum_sdk_qiskit.oq_backend import OpenQuantumBackend


def test_rigetti_ankaa_3_backend():
    backend = OpenQuantumBackend(name="Rigetti Ankaa-3")
    assert backend.num_qubits == 84
    ops = backend.target.operation_names
    assert "rx" in ops
    assert "rz" in ops
    assert "iswap" in ops
    assert "measure" in ops
    assert "cz" not in ops
    assert "cx" not in ops


def test_ionq_aria_1_backend():
    backend = OpenQuantumBackend(name="IonQ Aria-1")
    assert backend.num_qubits == 25
    ops = backend.target.operation_names
    assert "gpi" in ops
    assert "gpi2" in ops
    assert "ms" in ops
    assert "measure" in ops
    assert "cx" not in ops


def test_iqm_emerald_backend():
    backend = OpenQuantumBackend(name="IQM Emerald")
    assert backend.num_qubits == 54
    target = backend.target
    ops = target.operation_names
    assert target.num_qubits == 54
    assert "measure" in ops
    assert "cz" in ops
    assert "prx" in ops
    assert target.instruction_supported("cz", (0, 1)) or target.instruction_supported("cz", (1, 0))


def test_iqm_garnet_backend():
    backend = OpenQuantumBackend(name="IQM Garnet")
    assert backend.num_qubits == 20
    target = backend.target
    assert target.num_qubits == 20
    assert "measure" in target.operation_names
    assert "cz" in target.operation_names
    assert "prx" in target.operation_names
    assert target.instruction_supported("cz", (0, 1)) or target.instruction_supported("cz", (1, 0))
