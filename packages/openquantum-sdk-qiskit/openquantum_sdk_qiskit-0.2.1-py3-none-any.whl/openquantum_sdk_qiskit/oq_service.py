from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pathlib import Path
import json
import os

from openquantum_sdk.auth import ClientCredentials, ClientCredentialsAuth
from openquantum_sdk.clients import ManagementClient, SchedulerClient

if TYPE_CHECKING:
    from qiskit.providers import BackendV2


def _require_qiskit() -> None:
    try:
        import qiskit  # noqa: F401
    except Exception as e:
        raise RuntimeError(
            "Qiskit is required for this operation. Install: pip install 'openquantum-sdk[qiskit]'"
        ) from e


class OpenQuantumService:
    """service for auth and backend availability discovery"""

    def __init__(
        self,
        *,
        token: Optional[str] = None,
        creds: Optional[ClientCredentials] = None,
        keycloak_base: str = "https://id.openquantum.com",
        realm: str = "platform",
        scheduler_url: str = "https://scheduler.openquantum.com",
        management_url: str = "https://management.openquantum.com",
    ) -> None:

        auth_obj: Optional[ClientCredentialsAuth] = None
        if token is None and creds is None and os.getenv("OPENQUANTUM_NO_AUTOLOAD") != "1":
            try:
                acct_name = os.getenv("OPENQUANTUM_ACCOUNT_NAME", "default")
                path = self._accounts_path(filename=None)
                if path.exists():
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if acct_name in data:
                        entry = data[acct_name]
                        kr_used = bool(entry.get("keyring", False))
                        if (entry.get("auth_mode") == "token"):
                            token = entry.get("token")
                            if (not token) and kr_used:
                                try:
                                    import keyring
                                    token = keyring.get_password("openquantum", f"{acct_name}:token")
                                except Exception:
                                    pass
                        else:
                            c = (entry.get("creds") or {})
                            if c.get("client_id"):
                                secret = c.get("client_secret") or ""
                                if (not secret) and kr_used:
                                    try:
                                        import keyring
                                        maybe = keyring.get_password("openquantum", f"{acct_name}:client_secret")
                                        secret = maybe or secret
                                    except Exception:
                                        pass
                                creds = ClientCredentials(client_id=c.get("client_id"), client_secret=secret)
                        keycloak_base = entry.get("keycloak_base", keycloak_base)
                        realm = entry.get("realm", realm)
                        scheduler_url = entry.get("scheduler_url", scheduler_url)
                        management_url = entry.get("management_url", management_url)
            except Exception as e:
                import warnings as _warnings
                _warnings.warn(
                    f"OpenQuantumService autoload failed: {e!r}. Continuing unauthenticated.",
                    stacklevel=2,
                )
        if token and creds:
            raise ValueError("Provide either 'token' or 'creds', not both.")
        if creds is not None:
            auth_obj = ClientCredentialsAuth(
                creds=creds,
                keycloak_base=keycloak_base,
                realm=realm,
            )

        self.management = ManagementClient(base_url=management_url, token=token, auth=auth_obj)
        self.scheduler = SchedulerClient(base_url=scheduler_url, token=token, auth=auth_obj)

    def close(self) -> None:
        """Close underlying HTTP sessions."""
        self.management.close()
        self.scheduler.close()

    def backends(
        self,
        *,
        name: Optional[str] = None,
        online: Optional[bool] = None,
        device_type: Optional[str] = None,  # "QPU" or "SIMULATOR"
        vendor_id: Optional[str] = None,
        min_num_qubits: Optional[int] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List backend classes with availability info.

        Filters:
            - name: substring match against backend class name
            - online: if True, require status == "Online" and accepting_jobs == True
            - device_type: match ``type`` field from Management API
            - vendor_id: match ``provider_id``
            - min_num_qubits: DEPRECATED (ignored) - constraint_data removed in SDK v0.2.1
        """
        items: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            page = self.management.list_backend_classes(limit=limit, cursor=cursor)
            for bc in page.backend_classes:
                if name:
                    needle = name.lower()
                    hay_name = (bc.name or "").lower()
                    hay_short = (bc.short_code or "").lower()
                    if needle not in hay_name and needle not in hay_short:
                        continue
                if device_type and (bc.type or "").lower() != device_type.lower():
                    continue
                if vendor_id and (bc.provider_id or "") != vendor_id:
                    continue
                if online is True and (((bc.status or "").lower() != "online") or not bool(bc.accepting_jobs)):
                    continue
                # Note: min_num_qubits filter removed as constraint_data no longer exists in SDK v0.2.1

                items.append(
                    {
                        "id": bc.id,
                        "name": bc.name,
                        "description": bc.description,
                        "type": bc.type,
                        "provider_id": bc.provider_id,
                        "short_code": bc.short_code,
                        "queue_depth": bc.queue_depth,
                        "accepting_jobs": bc.accepting_jobs,
                        "status": bc.status,
                    }
                )
            cursor = page.pagination.next_cursor
            if not cursor:
                break
        return items

    def return_target(
        self,
        name: str,
        *,
        capabilities_source: Optional[Union[str, Path, Dict[str, Any]]] = None,
    ) -> Any:  # target primative

        _require_qiskit()
        from .oq_target import build_target_from_capabilities
        caps = self._load_capabilities(name, capabilities_source)

        return build_target_from_capabilities(caps)

    def return_backend(
        self,
        name: str,
        *,
        capabilities_source: Optional[Union[str, Path, Dict[str, Any]]] = None,
        config: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
    ) -> Any:  # BackendV2 object
        """
        Args:
            name: backend identifier (id/short_code/name) or label.
            capabilities_source: dict|path|URL to capabilities; if None, resolves via Management API.
            config: required IDs for platform submission (org, backend_class_id, subcategory).
            export_format: 'qasm2' or 'qasm3'.
        """
        _require_qiskit()
        from .oq_backend import OpenQuantumBackend

        caps = self._load_capabilities(name, capabilities_source)
        backend = OpenQuantumBackend(
            name=name,
            capabilities=caps,
            scheduler=self.scheduler,
            config=config,
            export_format=export_format,
        )
        return backend

    def create_sampler(
        self,
        *,
        backend: "BackendV2",
        organization_id: Optional[str] = None,
        backend_class_id: str,
        job_subcategory_id: str,
        name: Optional[str] = None,
        configuration_data: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
    ):
        """Create a SamplerV2 (OQSampler internally)

        Args:
            backend: A Qiskit BackendV2 to transpile/run against.
            organization_id: Optional organization UUID.
            backend_class_id: Target backend class (UUID or short code).
            job_subcategory_id: Workload subcategory (UUID or short code).
            name: Optional job name prefix.
            configuration_data: Optional provider-specific configuration.
            export_format: "qasm2" or "qasm3" for submission IR.

        Returns:
            An initialized SamplerV2 that submits jobs to OpenQuantum.
        """
        _require_qiskit()
        try:
            from .oq_sampler import OQSampler
        except ImportError as e:
            raise ImportError("Qiskit plugin not installed correctly") from e

        config = {
            "organization_id": organization_id,
            "backend_class_id": backend_class_id,
            "job_subcategory_id": job_subcategory_id,
            "name": name,
            "configuration_data": configuration_data,
        }

        return OQSampler(
            backend=backend,
            scheduler=self.scheduler,
            config=config,
            export_format=export_format,
        )

    def create_estimator(
        self,
        *,
        backend: "BackendV2",
        organization_id: Optional[str] = None,
        backend_class_id: str,
        job_subcategory_id: str,
        name: Optional[str] = None,
        configuration_data: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
    ):
        """Create an EstimatorV2 (OQEstimator internally)

        Args:
            backend: A Qiskit BackendV2 to transpile/run against.
            organization_id: Optional organization UUID.
            backend_class_id: Target backend class (UUID or short code).
            job_subcategory_id: Workload subcategory (UUID or short code).
            name: Optional job name prefix.
            configuration_data: Optional provider-specific configuration.
            export_format: "qasm3" (default) or "qasm2".

        Returns:
            An initialized EstimatorV2 that submits jobs to OpenQuantum.
        """
        _require_qiskit()
        try:
            from .oq_estimator import OQEstimator
        except ImportError as e:
            raise ImportError("Qiskit plugin not installed correctly") from e

        config = {
            "organization_id": organization_id,
            "backend_class_id": backend_class_id,
            "job_subcategory_id": job_subcategory_id,
            "name": name,
            "configuration_data": configuration_data,
        }

        return OQEstimator(
            backend=backend,
            scheduler=self.scheduler,
            config=config,
            export_format=export_format,
        )

    def _load_capabilities(
        self,
        name: str,
        src: Optional[Union[str, Path, Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """Capability loader (placeholder).
           TODO: Wire to a real capabilities endpoint.
        """
        from .backend_data import (
            RIGETTI_ANKAA_3_CAPS,
            IONQ_ARIA_1_CAPS,
            IQM_EMERALD_CAPS,
            IQM_GARNET_CAPS
        )

        n = name.lower()
        if "ankaa-3" in n or "rigetti" in n:
            return RIGETTI_ANKAA_3_CAPS
        if "aria-1" in n or "aria" in n:
            return IONQ_ARIA_1_CAPS
        if "emerald" in n:
            return IQM_EMERALD_CAPS
        if "garnet" in n:
            return IQM_GARNET_CAPS

        if isinstance(src, dict):
            return src

        if isinstance(src, (str, Path)):
            p = Path(src)
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))

            import requests
            r = requests.get(str(src), timeout=15)
            r.raise_for_status()

            return r.json()

        page = self.management.list_backend_classes(limit=100)
        match = next(
            (
                bc
                for bc in page.backend_classes
                if bc.id == name or (bc.short_code or "") == name or (bc.name or "") == name
            ),
            None,
        )
        # TODO: replace with real field
        if not match or not getattr(match, "extra", {}).get("capabilities_url"):
            raise ValueError(f"Capabilities for backend '{name}' not found")

        import requests
        url = match.extra["capabilities_url"]
        r = requests.get(url, timeout=15)
        r.raise_for_status()

        return r.json()

    @property
    def active_account(self) -> Dict[str, Any]:
        """Return a minimal description of the active auth context."""

        auth_mode = "unauthenticated"
        if getattr(self.management, "_fixed_token", None):
            auth_mode = "token"
        elif getattr(self.management, "_auth", None):
            auth_mode = "client_credentials"
        return {
            "management_url": self.management.base_url,
            "scheduler_url": self.scheduler.base_url,
            "auth_mode": auth_mode,
        }

    @staticmethod
    def _accounts_path(filename: Optional[str]) -> Path:
        if filename:
            return Path(filename).expanduser()
        cfg_dir = os.getenv("OPENQUANTUM_CONFIG_DIR")
        if cfg_dir:
            return Path(cfg_dir).expanduser() / "accounts.json"
        try:
            from platformdirs import PlatformDirs

            d = PlatformDirs(appname="OpenQuantum", appauthor=False)
            return Path(d.user_config_dir) / "accounts.json"
        except Exception:
            return Path(os.path.expanduser("~/.openquantum/accounts.json"))

    @classmethod
    def save_account(
        cls,
        *,
        name: str = "default",
        token: Optional[str] = None,
        creds: Optional[ClientCredentials] = None,
        keycloak_base: str = "https://id.openquantum.com",
        realm: str = "platform",
        scheduler_url: str = "https://scheduler.openquantum.com",
        management_url: str = "https://management.openquantum.com",
        filename: Optional[str] = None,
        overwrite: bool = True,
        use_keyring: bool = True,
    ) -> None:
        """alt to qiskit account manager

        for local dev
        """
        if token and creds:
            raise ValueError("Provide either 'token' or 'creds', not both.")
        path = cls._accounts_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        data: Dict[str, Any] = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                if not overwrite:
                    raise
                data = {}
        if not overwrite and name in data:
            raise ValueError(f"Account '{name}' already exists. Set overwrite=True to replace.")
        entry: Dict[str, Any] = {
            "auth_mode": "token" if token else "client_credentials",
            "token": token,
            "creds": {"client_id": creds.client_id, "client_secret": creds.client_secret} if creds else None,
            "keycloak_base": keycloak_base,
            "realm": realm,
            "scheduler_url": scheduler_url,
            "management_url": management_url,
        }
        if use_keyring:
            try:
                import keyring

                if token:
                    keyring.set_password("openquantum", f"{name}:token", token)
                    entry["token"] = None
                if creds and creds.client_secret:
                    keyring.set_password("openquantum", f"{name}:client_secret", creds.client_secret)
                    entry["creds"] = {"client_id": creds.client_id, "client_secret": None}
                entry["keyring"] = True
            except Exception:
                entry.setdefault("keyring", False)
        data[name] = entry

        tmp_txt = json.dumps(data, indent=2)
        from tempfile import NamedTemporaryFile as _NTF

        cls._ensure_cfg_dir(path)
        with _NTF("w", delete=False, encoding="utf-8", dir=str(path.parent)) as _tmp:
            _tmp.write(tmp_txt)
            _tmp.flush()

            os.fsync(_tmp.fileno())
            _tmp_path = Path(_tmp.name)
        _tmp_path.replace(path)
        try:
            os.chmod(path, 0o600)
        except Exception:
            pass

    @staticmethod
    def _ensure_cfg_dir(path: Path) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    @classmethod
    def saved_accounts(
        cls,
        *,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return all saved accounts"""
        path = cls._accounts_path(filename)
        if not path.exists():
            return {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            masked: Dict[str, Any] = {}

            for k, v in raw.items():
                v = dict(v)
                tok = v.get("token")

                if tok:
                    v["token"] = tok[:6] + "…" + tok[-4:]

                creds = v.get("creds") or {}
                if creds.get("client_secret"):
                    cs = creds["client_secret"]
                    creds["client_secret"] = cs[:4] + "…" + cs[-4:]

                v["creds"] = creds
                masked[k] = v
            return masked

        except Exception:
            return {}

    @classmethod
    def delete_account(
        cls,
        *,
        name: str = "default",
        filename: Optional[str] = None,
    ) -> bool:
        """Delete a saved account by name."""
        path = cls._accounts_path(filename)
        if not path.exists():
            return False
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return False
        if name not in data:
            return False
        try:
            import keyring

            keyring.delete_password("openquantum", f"{name}:token")
            keyring.delete_password("openquantum", f"{name}:client_secret")
        except Exception:
            pass
        del data[name]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True

    @classmethod
    def from_saved_account(
        cls,
        *,
        name: str = "default",
        filename: Optional[str] = None,
    ) -> "OpenQuantumService":
        """Instantiate service from a saved account configuration."""
        path = cls._accounts_path(filename)
        if not path.exists():
            raise ValueError(f"Saved account file not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            raise ValueError(f"Failed to load saved accounts from {path}: {e}") from e
        if name not in data:
            raise ValueError(f"Saved account '{name}' not found")
        entry = data[name]
        kr = bool(entry.get("keyring", False))
        if entry.get("auth_mode") == "token":
            tok = entry.get("token")
            if (not tok) and kr:
                try:
                    import keyring

                    tok = keyring.get_password("openquantum", f"{name}:token")
                except Exception:
                    pass
            return cls(
                token=tok,
                scheduler_url=entry.get("scheduler_url"),
                management_url=entry.get("management_url"),
            )
        creds_dict = entry.get("creds") or {}
        client_secret = creds_dict.get("client_secret", "")
        if (not client_secret) and kr:
            try:
                import keyring

                maybe = keyring.get_password("openquantum", f"{name}:client_secret")
                client_secret = maybe or client_secret
            except Exception:
                pass
        creds = ClientCredentials(
            client_id=creds_dict.get("client_id", ""),
            client_secret=client_secret,
        )
        return cls(
            creds=creds,
            keycloak_base=entry.get("keycloak_base", "https://id.openquantum.com"),
            realm=entry.get("realm", "platform"),
            scheduler_url=entry.get("scheduler_url"),
            management_url=entry.get("management_url"),
        )

    @classmethod
    def login(
        cls,
        *,
        token: Optional[str] = None,
        creds: Optional[ClientCredentials] = None,
        save: bool = False,
        name: str = "default",
        filename: Optional[str] = None,
        **kwargs: Any,
    ) -> "OpenQuantumService":

        svc = cls(token=token, creds=creds, **kwargs)

        if save:
            cls.save_account(
                name=name,
                token=token,
                creds=creds,
                keycloak_base=kwargs.get("keycloak_base", "https://id.openquantum.com"),
                realm=kwargs.get("realm", "platform"),
                scheduler_url=kwargs.get("scheduler_url", "https://scheduler.openquantum.com"),
                management_url=kwargs.get("management_url", "https://management.openquantum.com"),
                filename=filename,
                overwrite=True,
                use_keyring=True,
            )
        return svc

    def __enter__(self) -> "OpenQuantumService":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
