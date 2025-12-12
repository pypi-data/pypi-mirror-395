from __future__ import annotations
from openquantum_sdk.models import JobRead
from openquantum_sdk.clients import SchedulerClient
from openquantum_sdk_qiskit.oq_backend import OpenQuantumBackend
from openquantum_sdk_qiskit.oq_sampler import OQSampler
from openquantum_sdk_qiskit.oq_target import build_target_from_capabilities
from qiskit.primitives import BackendSamplerV2
from qiskit import QuantumCircuit

import json
from typing import Dict

import pytest

qiskit = pytest.importorskip("qiskit")


def _caps_2q() -> Dict:
    return {
        "n_qubits": 2,
        "timing": {"dt": 2.0e-9, "durations": [{"op": "cx", "qubits": [0, 1], "value_s": 5.0e-7}]},
        "native_ops": [
            {"name": "x", "arity": 1},
            {"name": "h", "arity": 1},
            {"name": "cx", "arity": 2},
        ],
        "topology": {"directed_edges": False, "coupling_map": [[0, 1]]},
        "noise": {"gate_error": [{"op": "cx", "qubits": [0, 1], "prob": 0.01}]},
        "limits": {"max_circuits": 100},
    }


def test_target_builder_basic():
    cap = _caps_2q()
    target = build_target_from_capabilities(cap)
    assert target.num_qubits == 2
    # cx on (0,1) and (1,0)
    assert "cx" in target.operation_names
    assert (0, 1) in target["cx"].keys()
    assert (1, 0) in target["cx"].keys()


def test_sampler_scheduler_counts_json_to_primitive_result(requests_mock):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    output_url = "https://output.example.com/job-abc"
    counts = {"00": 50, "11": 50}
    requests_mock.get(output_url, text=json.dumps(counts))

    class _SchedulerStub(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def __init__(self, output_url: str, counts: Dict[str, int]):
            self._output_url = output_url
            self._counts = counts

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-adapter",
                status="Completed",
                input_data_url="https://input.example.com/job-adapter",
                job_preparation_id="prep",
                execution_plan_id="plan",
                queue_priority_id="prio",
                message=None,
                output_data_url=self._output_url,
                transaction_id=None,
                submitted_at=None,
            )

        def get_job_categories(self, limit=100):
            from unittest.mock import MagicMock
            cats = MagicMock()
            c = MagicMock()
            c.id = "cat-1"
            c.name = "Qiskit"
            cats.categories = [c]
            return cats

        def get_job_subcategories(self, category_id, limit=100):
            from unittest.mock import MagicMock
            subs = MagicMock()
            s = MagicMock()
            s.id = "sub-1"
            s.name = "sub-1"
            subs.categories = [s]
            return subs

    sampler = OQSampler(
        backend=object(),
        scheduler=_SchedulerStub(output_url, counts),
        config={
            "organization_id": "org-1",
            "backend_class_id": "bk-1",
            "job_subcategory_id": "sub-1",
        },
        export_format="qasm3",
    )
    job = sampler.run([(qc, None, 100)])
    res = job.result()
    assert len(res) == 1
    pub0 = res[0]
    # DataBin should have BitArray shots
    total = sum(pub0.data.m.get_counts().values())
    assert total == 100


def test_backend_run_parses_counts_to_memory(requests_mock):
    cap = _caps_2q()
    backend = OpenQuantumBackend(
        name="oq://test/backend",
        capabilities=cap,
        scheduler=None,
        config=None,
    )

    class _SchedulerStub(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def __init__(self):
            pass

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-xyz",
                status="Completed",
                input_data_url="https://input.example.com/job-xyz",
                job_preparation_id="prep-xyz",
                execution_plan_id="plan",
                queue_priority_id="prio",
                message=None,
                output_data_url="https://output.example.com/job-xyz",
                transaction_id=None,
                submitted_at=None,
            )

        def get_job_categories(self, limit=100):
            from unittest.mock import MagicMock
            cats = MagicMock()
            c = MagicMock()
            c.id = "cat-1"
            c.name = "Qiskit"
            cats.categories = [c]
            return cats

        def get_job_subcategories(self, category_id, limit=100):
            from unittest.mock import MagicMock
            subs = MagicMock()
            s = MagicMock()
            s.id = "sub-1"
            s.name = "sub-1"
            subs.categories = [s]
            return subs

    backend._scheduler = _SchedulerStub()
    backend._config = {
        "organization_id": "org-1",
        "backend_class_id": "bk-1",
        "job_subcategory_id": "sub-1",
    }

    counts = {"00": 60, "11": 40}
    requests_mock.get("https://output.example.com/job-xyz", text=json.dumps(counts))

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    job = backend.run([qc], shots=100, memory=True)
    result = job.result()
    assert hasattr(result, "results")
    assert len(result.results) == 1
    exp0 = result.results[0]
    assert exp0.shots == 100
    assert isinstance(exp0.data.memory, list)
    assert len(exp0.data.memory) == 100


def test_backend_sampler_v2_integration_with_backend_run(requests_mock):
    cap = _caps_2q()
    backend = OpenQuantumBackend(
        name="oq://test/backend",
        capabilities=cap,
        scheduler=None,
        config=None,
    )

    class _SchedulerStub(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def __init__(self):
            pass

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-s2v",
                status="Completed",
                input_data_url="https://input.example.com/job-s2v",
                job_preparation_id="prep-s2v",
                execution_plan_id="plan",
                queue_priority_id="prio",
                message=None,
                output_data_url="https://output.example.com/job-s2v",
                transaction_id=None,
                submitted_at=None,
            )

        def get_job_categories(self, limit=100):
            from unittest.mock import MagicMock
            cats = MagicMock()
            c = MagicMock()
            c.id = "cat-1"
            c.name = "Qiskit"
            cats.categories = [c]
            return cats

        def get_job_subcategories(self, category_id, limit=100):
            from unittest.mock import MagicMock
            subs = MagicMock()
            s = MagicMock()
            s.id = "sub-1"
            s.name = "sub-1"
            subs.categories = [s]
            return subs

    backend._scheduler = _SchedulerStub()
    backend._config = {
        "organization_id": "org-1",
        "backend_class_id": "bk-1",
        "job_subcategory_id": "sub-1",
    }

    counts = {"00": 70, "11": 30}
    requests_mock.get("https://output.example.com/job-s2v", text=json.dumps(counts))

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    sampler = BackendSamplerV2(backend=backend)
    res = sampler.run([(qc, None, 100)]).result()
    assert len(res) == 1
    total = sum(res[0].data.meas.get_counts().values())
    assert total == 100


def test_backend_requires_scheduler():
    """Test that Backend.run raises RuntimeError if scheduler is missing."""
    cap = _caps_2q()
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.measure_all()

    backend = OpenQuantumBackend(name="test", capabilities=cap, scheduler=None, config=None)
    with pytest.raises(RuntimeError, match="provide scheduler and config"):
        backend.run([qc])

    backend = OpenQuantumBackend(
        name="test",
        capabilities=cap,
        scheduler=None,
        config={"backend_class_id": "test", "job_subcategory_id": "test"}
    )
    with pytest.raises(RuntimeError, match="provide scheduler and config"):
        backend.run([qc])


def test_backend_requires_config_keys():
    """Test that Backend.run raises ValueError if required config keys are missing."""
    cap = _caps_2q()
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.measure_all()

    mock_scheduler = object()

    backend = OpenQuantumBackend(name="test", capabilities=cap, scheduler=mock_scheduler, config={})
    with pytest.raises(ValueError, match="Missing config keys.*backend_class_id.*job_subcategory_id"):
        backend.run([qc])

    backend = OpenQuantumBackend(
        name="test",
        capabilities=cap,
        scheduler=mock_scheduler,
        config={"backend_class_id": "test:backend"}
    )
    with pytest.raises(ValueError, match="Missing config keys.*job_subcategory_id"):
        backend.run([qc])

    backend = OpenQuantumBackend(
        name="test",
        capabilities=cap,
        scheduler=mock_scheduler,
        config={"job_subcategory_id": "test:subcategory"}
    )
    with pytest.raises(ValueError, match="Missing config keys.*backend_class_id"):
        backend.run([qc])


def test_prx_gate_define_does_not_recurse():
    """Test that PRXGate._define() doesn't cause infinite recursion."""
    import numpy as np

    caps = {
        "n_qubits": 2,
        "native_ops": [
            {"name": "prx", "arity": 1, "params": ["theta", "phi"]},
            {"name": "cz", "arity": 2},
            {"name": "measure", "arity": 1},
        ],
        "topology": {"directed_edges": False, "coupling_map": [[0, 1]]},
    }

    target = build_target_from_capabilities(caps)
    assert "prx" in target.operation_names

    PRXGateClass = None
    for inst in target.operations:
        if inst.name == "prx":
            PRXGateClass = type(inst)
            break

    assert PRXGateClass is not None, "PRXGate not found in target"

    gate = PRXGateClass(np.pi / 2, np.pi / 4)

    defn = gate.definition
    assert defn is not None
    assert defn.num_qubits == 1
    assert len(defn.data) == 3


def test_prx_gate_transpilation_no_recursion():
    """Test that transpiling a circuit with PRX gates doesn't cause recursion."""
    from qiskit import transpile

    caps = {
        "n_qubits": 2,
        "native_ops": [
            {"name": "prx", "arity": 1, "params": ["theta", "phi"]},
            {"name": "cz", "arity": 2},
            {"name": "measure", "arity": 1},
        ],
        "topology": {"directed_edges": False, "coupling_map": [[0, 1]]},
    }

    backend = OpenQuantumBackend(name="test-prx", capabilities=caps)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    tqc = transpile(qc, backend=backend, optimization_level=1)
    assert tqc is not None
    assert tqc.num_qubits == 2
