from __future__ import annotations
from openquantum_sdk.qiskit import OpenQuantumService
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


def test_return_backend_and_run_counts_to_memory(requests_mock):
    svc = OpenQuantumService()
    backend = svc.return_backend(
        name="oq://test/backend",
        capabilities_source=_caps_2q(),
        config={
            "organization_id": "org-1",
            "backend_class_id": "bk-1",
            "job_subcategory_id": "sub-1",
        },
        export_format="qasm3",
    )

    counts = {"00": 60, "11": 40}
    output_url = "https://output.example.com/job-bkrun"

    from openquantum_sdk.clients import SchedulerClient
    from openquantum_sdk.models import JobRead
    from unittest.mock import MagicMock

    class _SchedulerStub(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-bkrun",
                status="Completed",
                input_data_url="",
                job_preparation_id="",
                execution_plan_id="",
                queue_priority_id="",
                message=None,
                output_data_url=output_url,
                transaction_id=None,
                submitted_at=None,
            )

        def get_job_categories(self, limit=100):
            cats = MagicMock()
            c = MagicMock()
            c.id = "cat-1"
            c.name = "Qiskit"
            cats.categories = [c]
            return cats

        def get_job_subcategories(self, category_id, limit=100):
            subs = MagicMock()
            s = MagicMock()
            s.id = "sub-1"
            s.name = "sub-1"
            subs.categories = [s]
            return subs

    backend._scheduler = _SchedulerStub()

    requests_mock.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
        "job_categories": [{"id": "cat-1", "name": "Qiskit", "job_subcategories": [{"id": "sub-1", "name": "sub-1"}]}]
    })

    requests_mock.get(output_url, text=json.dumps(counts))

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    job = backend.run([qc], shots=100, memory=True)
    result = job.result()
    assert len(result.results) == 1
    assert result.results[0].shots == 100
    assert isinstance(result.results[0].data.memory, list)
    assert len(result.results[0].data.memory) == 100


def test_create_sampler_wires_scheduler_and_runs(requests_mock):
    svc = OpenQuantumService()
    backend = svc.return_backend(
        name="oq://test/backend",
        capabilities_source=_caps_2q(),
        config={
            "organization_id": "org-1",
            "backend_class_id": "bk-1",
            "job_subcategory_id": "sub-1",
        },
    )

    from openquantum_sdk.clients import SchedulerClient
    from openquantum_sdk.models import JobRead

    output_url = "https://output.example.com/job-sampler"
    counts = {"00": 70, "11": 30}
    requests_mock.get(output_url, text=json.dumps(counts))

    class _SchedulerStub(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-sampler",
                status="Completed",
                input_data_url="",
                job_preparation_id="",
                execution_plan_id="",
                queue_priority_id="",
                message=None,
                output_data_url=output_url,
                transaction_id=None,
                submitted_at=None,
            )

        def get_job_categories(self, limit=100):
            from unittest.mock import MagicMock
            cats = MagicMock()
            c = MagicMock()
            c.id = "cat-1"
            c.name = "Qiskit"
            s = MagicMock()
            s.id = "sub-1"
            s.name = "Sampler"

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

    svc.scheduler = _SchedulerStub()
    backend._scheduler = svc.scheduler

    requests_mock.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
        "job_categories": [{"id": "cat-1", "name": "Qiskit", "job_subcategories": [{"id": "sub-1", "name": "Sampler"}]}]
    })

    sampler = svc.create_sampler(
        backend=backend,
        organization_id="org-1",
        backend_class_id="bk-1",
        job_subcategory_id="sub-1",
        export_format="qasm3",
    )

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    b_sampler = BackendSamplerV2(backend=backend)
    res_backend = b_sampler.run([(qc, None, 100)]).result()
    assert sum(res_backend[0].data.meas.get_counts().values()) == 100

    res = sampler.run([(qc, None, 100)]).result()
    assert sum(res[0].data.m.get_counts().values()) == 100
