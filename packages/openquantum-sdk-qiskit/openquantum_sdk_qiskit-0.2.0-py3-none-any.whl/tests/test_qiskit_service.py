import pytest
from openquantum_sdk_qiskit.oq_service import OpenQuantumService
from openquantum_sdk_qiskit.oq_backend import OpenQuantumBackend


def test_service_return_backend_hardcoded():
    with pytest.MonkeyPatch.context() as m:
        m.setenv("OPENQUANTUM_NO_AUTOLOAD", "1")
        service = OpenQuantumService(token="dummy")

        backend = service.return_backend("Rigetti Ankaa-3")

        assert isinstance(backend, OpenQuantumBackend)
        assert backend.name == "Rigetti Ankaa-3"
        assert backend.num_qubits == 84
        assert "rx" in backend.target.operation_names


def test_service_return_backend_ionq():
    with pytest.MonkeyPatch.context() as m:
        m.setenv("OPENQUANTUM_NO_AUTOLOAD", "1")
        service = OpenQuantumService(token="dummy")

        backend = service.return_backend("IonQ Aria-1")
        assert backend.num_qubits == 25
        assert "ms" in backend.target.operation_names
