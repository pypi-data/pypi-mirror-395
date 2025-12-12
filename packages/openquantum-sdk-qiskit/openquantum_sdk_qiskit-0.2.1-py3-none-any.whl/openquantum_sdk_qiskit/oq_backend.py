from __future__ import annotations

import datetime
from typing import Any, Dict, Iterable, List, Optional

from qiskit.providers import BackendV2, Options
from qiskit.result import Result

from .oq_target import build_target_from_capabilities
from ._qasm import export_circuit_to_qasm
from openquantum_sdk.clients import SchedulerClient, JobSubmissionConfig
from .backend_data import (
    RIGETTI_ANKAA_3_CAPS,
    IONQ_ARIA_1_CAPS,
    IQM_EMERALD_CAPS,
    IQM_GARNET_CAPS
)


class OpenQuantumBackend(BackendV2):
    """Qiskit Backend for the OpenQuantum platform.
    """

    def __init__(
        self,
        name: str,
        *,
        capabilities: Optional[Dict[str, Any]] = None,
        scheduler: Optional[SchedulerClient] = None,
        config: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
        **kwargs
    ) -> None:
        super().__init__(name=name, **kwargs)

        self._scheduler = scheduler
        self._config = config or {}
        fmt = (export_format or "qasm3").lower()
        if fmt not in {"qasm2", "qasm3"}:
            raise ValueError("export_format must be 'qasm2' or 'qasm3'")
        self._export_format = fmt

        if capabilities is None:
            name_lower = name.lower()
            if "ankaa" in name_lower:
                capabilities = RIGETTI_ANKAA_3_CAPS
            elif "aria" in name_lower:
                capabilities = IONQ_ARIA_1_CAPS
            elif "emerald" in name_lower:
                capabilities = IQM_EMERALD_CAPS
            elif "garnet" in name_lower:
                capabilities = IQM_GARNET_CAPS
            else:
                capabilities = {
                    "n_qubits": 1,
                    "native_ops": [{"name": "measure", "arity": 1}],
                    "topology": {"directed_edges": False, "coupling_map": []}
                }

        self._cap = capabilities
        self._target = build_target_from_capabilities(capabilities)
        self._max_circuits = (self._cap.get("limits", {}) or {}).get("max_circuits", 1024)

        self.description = f"OpenQuantum Backend: {self.name}"
        self.online_date = datetime.datetime.now()
        self.backend_version = "0.0.1"

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return self._max_circuits

    @classmethod
    def _default_options(cls):
        return Options(shots=1024)

    def run(self, circuits: Iterable[Any], /, **run_options):
        """Submit circuits to platform and return a Qiskit Job-like object.

        BackendSamplerV2 compatibility - yields a Result with
        experiment data.memory as list[str] bitstrings.
        """
        if not self._scheduler:
            raise RuntimeError(
                "Scheduler submission is required: provide scheduler and config when constructing backend."
            )

        required = ("backend_class_id", "job_subcategory_id")
        missing = [k for k in required if not self._config.get(k)]
        if missing:
            raise ValueError(f"Missing config keys: {', '.join(missing)}")

        shots = run_options.get("shots") or getattr(self.options, "shots", None) or 100
        memory = run_options.get("memory", True)
        export_format = (run_options.get("export_format") or self._export_format).lower()

        if not isinstance(circuits, list):
            circuits = [circuits]

        results_payload: List[Dict[str, Any]] = []
        sub_id = str(self._config["job_subcategory_id"])

        for idx, circ in enumerate(circuits):
            payload = export_circuit_to_qasm(circ, export_format)

            job_config = JobSubmissionConfig(
                organization_id=self._config.get("organization_id"),
                backend_class_id=self._config["backend_class_id"],
                name=self._config.get("name", f"OQ Backend Run {idx}"),
                job_subcategory_id=sub_id,
                shots=shots,
                configuration_data=self._config.get("configuration_data", {}),
            )
            job = self._scheduler.submit_job(job_config, file_content=payload)
            counts: Dict[str, int] = self._scheduler.download_job_output(job)

            bit_width = max((len(k) for k in counts.keys()), default=0)
            memory_hex = self._counts_to_memory_hex(counts, bit_width)
            counts_hex = self._counts_bits_to_hex_keys(counts)

            results_payload.append(
                {
                    "shots": shots,
                    "success": True,
                    "data": {
                        "memory": memory_hex if memory and memory_hex is not None else None,
                        "counts": counts_hex,
                    },
                }
            )

        return _ImmediateResultJob(
            Result.from_dict(
                {
                    "results": results_payload,
                    "backend_name": self.name,
                    "success": True,
                    "backend_version": "0.1.0",
                    "job_id": "oq_job_id_placeholder",
                }
            )
        )

    # TODO: Job batching support

    def _counts_to_memory_hex(self, counts: Dict[str, int], bit_width: int) -> List[str]:
        """Expand counts of bitstrings into a list of hex memory strings."""
        memory: List[str] = []
        for bitstr, c in counts.items():
            s = bitstr.strip()
            if bit_width and len(s) < bit_width:
                s = s.zfill(bit_width)
            try:
                h = hex(int(s, 2))
                memory.extend([h] * int(c))
            except ValueError:
                pass
        return memory

    def _counts_bits_to_hex_keys(self, counts: Dict[str, int]) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for bitstr, c in counts.items():
            try:
                h = hex(int(bitstr, 2))
                out[h] = int(c)
            except ValueError:
                pass
        return out


class _ImmediateResultJob:
    def __init__(self, result: Result):
        self._result = result

    def result(self) -> Result:
        return self._result

    def status(self):
        from qiskit.providers import JobStatus
        return JobStatus.DONE

    def job_id(self):
        return self._result.job_id
