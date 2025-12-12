from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class GRIDResourceManager:
    """Look up node information and decide whether the host should run containers."""

    def __init__(self, *, nodes: Dict[str, Dict[str, Any]], serve_locally: bool) -> None:
        self.nodes = nodes
        self._serve = serve_locally

    @classmethod
    def from_config(cls, raw_cfg: Dict[str, Any]) -> "GRIDResourceManager":
        """
        Accept either *modern* schema (``serve`` + ``servers`` array)
        or *legacy* flat-dict schema (``host_grid_local`` flag).
        """
        # 1. decide the flag
        serve = raw_cfg.pop("serve", raw_cfg.pop("host_grid_local", False))

        # 2. extract node map
        if "servers" in raw_cfg:                            # modern array
            nodes = {srv.pop("id"): srv for srv in raw_cfg.pop("servers")}
        else:                                               # legacy dict
            nodes = {k: v for k, v in raw_cfg.items()}

        # 3. synthesise 'local' when containers may be hosted here
        if serve and "local" not in nodes:
            nodes["local"] = {"ip": "127.0.0.1"}

        return cls(nodes=nodes, serve_locally=serve)

    @staticmethod
    def load(path: str | Path) -> "GRIDResourceManager":
        p = Path(path).expanduser()
        if not p.exists():
            raise FileNotFoundError(p)

        if p.suffix.lower() in {".yml", ".yaml"}:
            import yaml  # lazy import
            data = yaml.safe_load(p.read_text())
        else:
            data = json.loads(p.read_text())

        return GRIDResourceManager.from_config(data)

    def _ensure(self, name: str) -> None:
        if name == "local" and self._serve:
            return
        if name not in self.nodes:
            raise KeyError(f"Node '{name}' not found in resource config")

    def should_serve(self) -> bool:
        """True if this workstation is allowed to host GRID containers."""
        return self._serve

    def node_exists(self, name: str) -> bool:
        """Return True if *name* is valid (includes implicit ``local``)."""
        return (name == "local" and self._serve) or name in self.nodes

    def list_nodes(self) -> List[Dict[str, str]]:
        """Return rows ready for ``tabulate``."""
        rows = [
            {"Node Name": n, "IP Address": meta.get("ip", "N/A")}
            for n, meta in self.nodes.items()
        ]
        if self._serve and "local" not in self.nodes:
            rows.append({"Node Name": "local", "IP Address": "127.0.0.1"})
        return rows

    def get_ip(self, name: str) -> str:
        """Return IP address for *name* (``local`` ⇒ 127.0.0.1)."""
        self._ensure(name)
        return "127.0.0.1" if name == "local" else self.nodes[name]["ip"]

    def storage_mounts(self, name: str) -> Dict[str, str]:
        """Return storage volume mapping or ``{}``."""
        self._ensure(name)
        return {} if name == "local" else self.nodes[name].get("storage", {}) or {}