from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigHandler:
    """Utility for reading ~/.grid/resource_config.json (creates default if absent)."""

    _FILE = Path.home() / ".grid" / "resource_config.json"

    @staticmethod
    def load_resource_config() -> Dict[str, Any]:
        if not ConfigHandler._FILE.exists():
            ConfigHandler._create_default()

        try:
            with ConfigHandler._FILE.open("r") as fp:
                data: Dict[str, Any] = json.load(fp)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {ConfigHandler._FILE}") from exc

        if "servers" in data and isinstance(data["servers"], list):
            pass
        else:
            raise ValueError(
                f"{ConfigHandler._FILE} does not match expected schema "
                "(missing 'servers' array or 'host_grid_local' flag)."
            )

        return data

    @staticmethod
    def _create_default() -> None:
        """Write a minimal modern config with local hosting to ~/.grid/."""
        ConfigHandler._FILE.parent.mkdir(parents=True, exist_ok=True)
        default: Dict[str, Any] = {
            "serve": True,
            "servers": [{"id": "local", "ip": "127.0.0.1"}],
        }
        with ConfigHandler._FILE.open("w") as fp:
            json.dump(default, fp, indent=4)

        print(f"[yellow]Created default resource config at {ConfigHandler._FILE}[/yellow]")