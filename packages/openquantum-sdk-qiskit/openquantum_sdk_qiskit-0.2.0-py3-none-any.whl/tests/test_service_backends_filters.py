from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from openquantum_sdk.qiskit import OpenQuantumService
from openquantum_sdk.models import (
    BackendClassRead,
    PaginatedBackendClasses,
    PaginationInfo,
)


@dataclass
class _Page:
    backend_classes: List[BackendClassRead]
    pagination: PaginationInfo


def _bk(idx: int, **kw) -> BackendClassRead:
    return BackendClassRead(
        id=f"bk-{idx}",
        name=kw.get("name", f"Backend {idx}"),
        description="",
        type=kw.get("type", "QPU"),
        provider_id=kw.get("provider_id", "prov-1"),
        short_code=kw.get("short_code", f"sc-{idx}"),
        queue_depth=kw.get("queue_depth", 0),
        accepting_jobs=kw.get("accepting_jobs", True),
        status=kw.get("status", "Online"),
    )


def test_service_backends_all_filters(monkeypatch):
    svc = OpenQuantumService()

    pages = [
        _Page(
            backend_classes=[
                _bk(1, name="Alpha", short_code="ALP", provider_id="prov-A", min_qubits=4),
                _bk(2, name="Bravo", type="SIMULATOR", provider_id="prov-B", min_qubits=8),
            ],
            pagination=PaginationInfo(next_cursor="cursor-2"),
        ),
        _Page(
            backend_classes=[
                _bk(3, name="Charlie", provider_id="prov-A", accepting_jobs=False, status="Offline", min_qubits=16),
                _bk(4, name="Delta", provider_id="prov-A", min_qubits=32),
            ],
            pagination=PaginationInfo(next_cursor=None),
        ),
    ]

    def _list_backend_classes(limit: int = 50, cursor: Optional[str] = None):
        if not cursor:
            p = pages[0]
        else:
            p = pages[1]
        return PaginatedBackendClasses(backend_classes=p.backend_classes, pagination=p.pagination)

    monkeypatch.setattr(svc.management, "list_backend_classes", _list_backend_classes)

    out_name = svc.backends(name="alp")
    assert {b["id"] for b in out_name} == {"bk-1"}

    out_online_qpu = svc.backends(online=True, device_type="QPU")
    assert {b["id"] for b in out_online_qpu} == {"bk-1", "bk-4"}

    out_vendor = svc.backends(device_type="QPU", vendor_id="prov-A")
    assert {b["id"] for b in out_vendor} == {"bk-1", "bk-4", "bk-3"}
