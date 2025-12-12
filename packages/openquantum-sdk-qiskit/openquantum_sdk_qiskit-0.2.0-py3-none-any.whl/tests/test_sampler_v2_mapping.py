from __future__ import annotations
from openquantum_sdk.models import JobRead
from openquantum_sdk.clients import SchedulerClient
from openquantum_sdk_qiskit.oq_sampler import OQSampler
from qiskit import QuantumCircuit

import json
from typing import Dict

import pytest

qiskit = pytest.importorskip("qiskit")


def _simple_bell(shots: int = 100) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.metadata = {"foo": "fooo"}
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc


class _SchedulerStub(SchedulerClient):
    base_url = "https://scheduler.openquantum.com"

    def __init__(self, output_url: str, counts: Dict[str, int]):
        self._output_url = output_url
        self._counts = counts

    def submit_job(self, config, file_content=None, file_path=None):
        return JobRead(
            id="job-pub",
            status="Completed",
            input_data_url="https://input.example.com/job-pub",
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


def test_sampler_v2_maps_counts_to_pub_databin(requests_mock):
    qc = _simple_bell(100)
    requests_mock.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
        "job_categories": [{"id": "cat-1", "name": "Qiskit", "job_subcategories": [{"id": "sub-1", "name": "sub-1"}]}]
    })

    output_url = "https://output.example.com/job-pub"
    counts = {"0": 50, "1": 50}
    requests_mock.get(output_url, text=json.dumps(counts))

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

    total = sum(pub0.data.m.get_counts().values())
    assert total == 100
    assert pub0.metadata["shots"] == 100
    assert pub0.metadata["circuit_metadata"] == qc.metadata


def test_sampler_v2_validates_export_format_on_init_and_run():
    with pytest.raises(ValueError):
        OQSampler(backend=object(), scheduler=None, config=None, export_format="invalid")


def test_sampler_v2_requires_scheduler():
    """Test that Sampler raises RuntimeError if scheduler is missing."""
    qc = _simple_bell(10)
    sampler = OQSampler(backend=object(), scheduler=None, config=None, export_format="qasm3")
    with pytest.raises(RuntimeError, match="provide scheduler and config"):
        _ = sampler.run([(qc, None, 10)])


def test_sampler_v2_requires_config_keys():
    """Test that Sampler raises ValueError if required config keys are missing."""
    qc = _simple_bell(10)
    mock_scheduler = object()

    sampler = OQSampler(backend=object(), scheduler=mock_scheduler, config={}, export_format="qasm3")
    with pytest.raises(ValueError, match="Missing config keys.*backend_class_id.*job_subcategory_id"):
        _ = sampler.run([(qc, None, 10)])

    sampler = OQSampler(
        backend=object(),
        scheduler=mock_scheduler,
        config={"backend_class_id": "test:backend"},
        export_format="qasm3"
    )
    with pytest.raises(ValueError, match="Missing config keys.*job_subcategory_id"):
        _ = sampler.run([(qc, None, 10)])

    sampler = OQSampler(
        backend=object(),
        scheduler=mock_scheduler,
        config={"job_subcategory_id": "test:subcategory"},
        export_format="qasm3"
    )
    with pytest.raises(ValueError, match="Missing config keys.*backend_class_id"):
        _ = sampler.run([(qc, None, 10)])


def test_sampler_v2_uses_run_time_export_format_over_default(requests_mock):
    requests_mock.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
        "job_categories": [{"id": "cat-1", "name": "Qiskit", "job_subcategories": [{"id": "sub-1", "name": "sub-1"}]}]
    })

    output_url = "https://output.example.com/job-fmt"
    counts = {"0": 1}

    class _Scheduler(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-fmt",
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

    import requests_mock as rqm

    with rqm.Mocker() as m:
        m.get(output_url, text=json.dumps(counts))
        m.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
            "job_categories": [{"id": "cat-1", "name": "Qiskit", "job_subcategories": [{"id": "sub-1", "name": "sub-1"}]}]
        })
        sampler = OQSampler(
            backend=object(),
            scheduler=_Scheduler(),
            config={
                "organization_id": "org-1",
                "backend_class_id": "bk-1",
                "job_subcategory_id": "sub-1",
            },
            export_format="qasm3",
        )
        qc = _simple_bell(1)
        job = sampler.run([(qc, None, 1)], export_format="qasm2")
        assert job.metadata["export_format"] == "qasm2"
        _ = job.result()


def test_sampler_bitarray_uses_num_clbits_not_shots(requests_mock):
    """Test that BitArray.from_samples uses circuit.num_clbits, not shots.

    This prevents the bug where histograms show 100+ leading zeros when
    shots > num_clbits.
    """
    requests_mock.get("https://scheduler.openquantum.com/v1/jobs/categories?limit=200", json={
        "job_categories": []
    })

    output_url = "https://output.example.com/job-bits"
    counts = {"00": 500, "11": 500}

    class _Scheduler(SchedulerClient):
        base_url = "https://scheduler.openquantum.com"

        def submit_job(self, config, file_content=None, file_path=None):
            return JobRead(
                id="job-bits",
                status="Completed",
                input_data_url="https://input.example.com/job-bits",
                job_preparation_id="prep-bits",
                execution_plan_id="plan",
                queue_priority_id="prio",
                message=None,
                output_data_url=output_url,
                transaction_id=None,
                submitted_at=None,
            )

        def download_job_output(self, job):
            return counts

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    sampler = OQSampler(
        backend=object(),
        scheduler=_Scheduler(output_url, counts),
        config={
            "organization_id": "org-1",
            "backend_class_id": "bk-1",
            "job_subcategory_id": "sub-1",
        },
        export_format="qasm3",
    )

    job = sampler.run([(qc, None, 1000)])
    result = job.result()

    result_counts = result[0].data.m.get_counts()

    for key in result_counts.keys():
        assert len(key) == 2, f"Expected 2-bit keys, got {len(key)}-bit key: {key}"
