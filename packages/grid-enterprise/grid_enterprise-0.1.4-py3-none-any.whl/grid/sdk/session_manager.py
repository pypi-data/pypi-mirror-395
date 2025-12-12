import asyncio
import json
import logging
import os
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

import httpx
import jwt
from tabulate import tabulate
from rich import print

from grid.sdk.resource_manager import GRIDResourceManager
from logging.handlers import RotatingFileHandler

from grid.utils.airgen_utils import AirGenUtils
from grid.utils.isaac_utils import IsaacUtils

__all__ = ["GRIDSessionManager"]

TOKEN_SECRET_PLATFORM = "aksdhiefrifhroihfoih4hfroihofirkshdueuhduihfr"
TOKEN_SECRET_USER = "aksdhiefrifhroihfoih4hfroihofirade"


def _log_path() -> Path:
    # Put session logs next to other GRID logs
    base = Path(os.environ.get("GRID_DATA_DIR", "~/.grid")).expanduser()
    path = base / "grid_session.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class GRIDSessionManager:
    """Async helper for starting/stopping/listing remote GRID sessions."""

    def __init__(self, resources: GRIDResourceManager, commander, username: str) -> None:
        self.resources = resources
        self.commander = commander
        self.user_id = username
        self.platform_auth_token = self._build_jwt(is_platform=True)
        self.session_nodes: Dict[str, str] = {}  # session_id → node_ip

        # logging -------------------------------------------------------- #
        self.logger = logging.getLogger("grid.session")
        if not self.logger.handlers:
            log_path = _log_path()
            # file handler: rotating, include extra 'arguments' field in log output
            fh = RotatingFileHandler(log_path, maxBytes=10_000_000, backupCount=5)
            # Include 'arguments' if passed via extra
            fmt = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s | arguments=%(arguments)s"
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)
            # console handler at INFO level
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(logging.Formatter("%(levelname)-8s | %(message)s"))
            self.logger.addHandler(ch)
            # log all events
            self.logger.setLevel(logging.DEBUG)
            # Prevent propagation to root logger to avoid duplicate or unintended console output
            self.logger.propagate = False

    @staticmethod
    def _build_jwt(is_platform: bool) -> str:
        secret = TOKEN_SECRET_PLATFORM if is_platform else TOKEN_SECRET_USER
        return jwt.encode({"user_id": "grid_user"}, secret, algorithm="HS512")

    # --------------------- session lifecycle --------------------------- #
    async def start_session(self, session_id: str, config_path: Path, node: str) -> bool | None:
        """Start remote session and stream progress."""
        ip = self.resources.get_ip(node)
        config = self._compose_config(session_id, config_path)
        self.logger.debug(f"Starting session {session_id} on node {node}", extra={"arguments": config})

        url = f"http://{ip}:8000/start_session"
        headers = {"Authorization": f"Bearer {self.platform_auth_token}"}
        timeout = httpx.Timeout(600.0)
        
        if config["session"]["sim"]["sim_type"] == "airgen":
            asset_url, rel_path = AirGenUtils.get_asset_spec(config["session"]["sim"]["scene_name"])
            print("Requesting asset download …")
            self.commander.download_asset(node, asset_url, rel_path)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                async with client.stream("POST", url, json={"session_config": config}, headers=headers) as resp:
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        data = json.loads(line)
                        print(f"[cyan]Status[/cyan]: {data['msg_content']}")
                        if data["msg_type"] == "response_end":
                            ok = bool(data["success"])
                            if ok:
                                self.session_nodes[session_id] = ip
                            return ok
            except httpx.RequestError as exc:
                self.logger.error("Request error: %s", exc)
                return None

    async def stop_session(self, node: str, session_id: str) -> bool:
        ip = self.resources.get_ip(node)
        
        self.logger.debug(f"Stopping session {session_id} on node {node}", extra={"arguments": {"session_id": session_id}})
        
        url = f"http://{ip}:8000/terminate_session"
        headers = {"Authorization": f"Bearer {self.platform_auth_token}"}

        async with httpx.AsyncClient(timeout=600.0) as client:
            try:
                resp = await client.post(url, json={"session_id": session_id, "user_id": self.user_id}, headers=headers)
                data = resp.json()
                if data.get("success"):
                    self.session_nodes.pop(session_id, None)
                    print("Session stopped.")
                else:
                    print("Failed to stop session.")
                return data.get("success", False)
            except httpx.RequestError as exc:
                print("Request error:", exc)
                return False

    # ------------------------- utilities ------------------------------- #
    def _compose_config(self, session_id: str, config_path: Path) -> Dict[str, Any]:
        try:
            cfg = json.loads(config_path.read_text())
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {config_path}: {e}")
        if "sim" not in cfg or "grid" not in cfg:
            raise ValueError("Config must contain 'sim' and 'grid' sections")
        return {
            "user": {"user_id": self.user_id},
            "session": {"session_id": session_id, **cfg},
        }

    async def list_sessions(self) -> List[Dict[str, str]]:
        tasks = [self.get_session_info(node) for node in self.resources.nodes]
        results = await asyncio.gather(*tasks)
        active = [r for r in results if r["session_id"] not in {None, "", "N/A"}]
        if active:
            print(tabulate([[r["session_id"], r["node"], r["last_active"]] for r in active], headers=["Session", "Node", "Last active"], tablefmt="grid"))
        else:
            print("No active sessions.")
        return results

    async def get_session_info(self, node: str) -> Dict[str, str]:
        ip = self.resources.get_ip(node)
        url = f"http://{ip}:8000/is_idle"
        headers = {"Authorization": f"Bearer {self.platform_auth_token}"}
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                data = (await client.get(url, headers=headers)).json()
                return {
                    "node": node,
                    "session_id": data.get("session_id", "N/A"),
                    "last_active": data.get("last_active_time", "N/A"),
                    "has_active_session": data.get("has_active_session", False),
                }
        except httpx.RequestError:
            return {"node": node, "session_id": "N/A", "last_active": "N/A", "has_active_session": False}

    async def get_session_id_by_node(self, node: str) -> Optional[str]:
        info = await self.get_session_info(node)
        return info.get("session_id") if info["session_id"] not in {None, "", "N/A"} else None
