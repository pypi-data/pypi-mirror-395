from typing import Optional, Dict, Any, Iterable
import copy

from qiskit.primitives import BackendEstimatorV2, BaseEstimatorV2, PrimitiveResult, PubResult, EstimatorPubLike
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit.providers import BackendV2
from openquantum_sdk.clients import SchedulerClient


class OQEstimator(BaseEstimatorV2):
    """OpenQuantum Estimator.

    This implementation uses Qiskit's BackendEstimatorV2 logic to compute
    expectation values from shots execution on the OpenQuantum backend.
    """

    def __init__(
        self,
        *,
        backend: BackendV2,
        options: Optional[dict] = None,
        scheduler: Optional[SchedulerClient] = None,
        config: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
    ):
        """Initialize the Estimator.

        Args:
            backend: The backend to run circuits on.
            options: Primitive options.
            scheduler: (Optional) Explicit scheduler client (usually passed to backend).
            config: (Optional) Explicit config (usually passed to backend).
            export_format: (Optional) Export format.
        """
        self._backend = backend
        self._scheduler = scheduler
        self._config = config or {}
        self._export_format = export_format
        self._default_precision = 0.01
        backend_proxy = copy.copy(backend)

        if self._config and hasattr(backend_proxy, "_config"):
            current = getattr(backend_proxy, "_config", {}) or {}
            merged = {**current, **self._config}
            backend_proxy._config = merged

        if self._scheduler and hasattr(backend_proxy, "_scheduler"):
            backend_proxy._scheduler = self._scheduler

        self._backend_estimator = BackendEstimatorV2(backend=backend_proxy, options=options)

    @property
    def backend(self) -> BackendV2:
        return self._backend

    @property
    def options(self):
        """Return the options for the estimator."""
        return self._backend_estimator.options

    def run(
        self, pubs: Iterable[EstimatorPubLike], *, precision: float | None = None
    ) -> PrimitiveJob[PrimitiveResult[PubResult]]:
        return self._backend_estimator.run(pubs, precision=precision)
