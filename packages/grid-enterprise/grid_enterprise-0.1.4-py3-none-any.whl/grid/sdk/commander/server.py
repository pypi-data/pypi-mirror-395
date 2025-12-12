import asyncio
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import threading
import os
from grid.utils.storage_utils import init_data_dir

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from grid.sdk.commander.core import Commander
from grid.utils.auth_utils import get_sas_token, get_acr_password, get_username
from grid.sdk.commander.security import require_token
from fastapi import APIRouter
from fastapi import Depends

api = APIRouter(dependencies=[Depends(require_token)])

# --------------------------------------------------------------------------- #
# Logging – one rotating file + console                                       #
# --------------------------------------------------------------------------- #
def _setup_logging(log_path) -> None:
    logger = logging.getLogger("grid.commander")
    # Capture all levels on this logger
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    file_handler = RotatingFileHandler(log_path, maxBytes=10_000_000, backupCount=5)
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)-8s | %(message)s"))
    console.setLevel(logging.ERROR)
    logger.addHandler(console)

LOG_PATH = Path(os.environ.get("GRID_DATA_DIR", "~/.grid")).expanduser() / "grid_commander.log"
_setup_logging(LOG_PATH)
init_data_dir()

commander = Commander()

# Models -------------------------------------------------------------------- #
class LoginCredentials(BaseModel):
    username: str
    password: str

class NodeData(BaseModel):
    data: dict

class SimName(BaseModel):
    sim_name: str

class VolumeInfo(BaseModel):
    volume_info: dict

class DownloadFileRequest(BaseModel):
    url: str
    dest: str

# Helper – stream any commander generator ----------------------------------- #
async def _stream(generator):
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def _worker():
        try:
            for chunk in generator:
                loop.call_soon_threadsafe(queue.put_nowait, chunk)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

    threading.Thread(target=_worker, daemon=True).start()

    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk

# --------------------------------------------------------------------------- #
# Endpoints                                                                   #
# --------------------------------------------------------------------------- #
@api.post("/set_node_data/")
def set_node_data(data: NodeData):
    commander.set_node_data(data.data)
    return {"message": "Node data set successfully"}

@api.post("/set_sim/")
def set_sim(sim_name: SimName):
    commander.set_sim(sim_name.sim_name)
    return {"message": "Simulation profile set successfully"}

@api.get("/get_sim/")
def get_sim():
    return {"sim_name": commander.get_sim()}

@api.post("/init_containers/")
def init_containers(vol: VolumeInfo):
    gen = commander.init_containers(vol.volume_info)
    return StreamingResponse(_stream(gen), media_type="text/plain")

@api.post("/kill_containers/")
def kill_containers():
    return StreamingResponse(_stream(commander.kill_containers()),
                             media_type="text/plain")

@api.post("/update_containers/")
def update_containers():
    return StreamingResponse(_stream(commander.update_containers()),
                             media_type="text/plain")

@api.post("/login_registry/")
def login_registry():
    username = get_username()
    password = get_acr_password()
    if not password:
        commander.stop_containers_due_to_invalid_license()
        raise HTTPException(status_code=403, detail="Unable to retrieve ACR password")
    if not username:
        commander.stop_containers_due_to_invalid_license()
        raise HTTPException(status_code=403, detail="Unable to retrieve ACR username")
    return StreamingResponse(_stream(commander.login_registry(username, password)),
                             media_type="text/plain")

@api.get("/check_containers/")
def check_containers():
    return {"status": commander.check_grid_containers()}

@api.get("/check_sim_container/")
def check_sim_container():
    return {"sim_name": commander.check_sim_container()}

# server.py
from pathlib import Path

@api.post("/download_file/")
def download_file(req: DownloadFileRequest):

    # 2) Establish GRID root dir
    grid_root = Path(os.getenv("GRID_DATA_DIR", "~/.grid")).expanduser().resolve()

    # 3) Compute destination, disallow traversal
    dest = (grid_root / req.dest).resolve()
    if not str(dest).startswith(str(grid_root) + os.sep):
        raise HTTPException(status_code=400, detail="Invalid destination path")

    # 4) Ensure parent exists
    dest.parent.mkdir(parents=True, exist_ok=True)

    # 5) Stream download via your commander
    return StreamingResponse(
        commander.download_file(req.url, str(dest)),
        media_type="text/plain",
    )

@api.post("/init_assets/")
def init_assets():
    return StreamingResponse(_stream(commander.init_assets()),
                             media_type="text/plain")


# --------------------------------------------------------------------------- #
# Basic FastAPI scaffolding                                                   #
# --------------------------------------------------------------------------- #
app = FastAPI()
app.include_router(api)

# --------------------------------------------------------------------------- #
# Optional: lightweight wrapper to run as a subprocess or thread             #
# --------------------------------------------------------------------------- #
class CommanderServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8060):
        init_data_dir()
        self.host, self.port = host, port
        self.server: uvicorn.Server | None = None
        self.thread: threading.Thread | None = None

    def start(self, block: bool = False):
        if self.thread and self.thread.is_alive():
            logging.warning("CommanderServer already running")
            return

        self.server = uvicorn.Server(
            uvicorn.Config(app, host=self.host, port=self.port, log_level="critical")
        )

        if block:
            # Run in *this* thread – call blocks
            self.server.run()
        else:
            # Background thread for embedding in the REPL
            self.thread = threading.Thread(target=self.server.run, daemon=True)
            self.thread.start()
            logging.getLogger("grid.commander").info(
                "CommanderServer started on %s:%s", self.host, self.port
            )

    def stop(self, timeout: float = 10.0):
        log = logging.getLogger("grid.commander")
        if not self.server or not self.thread:
            log.warning("CommanderServer not running")
            return

        log.info("Stopping CommanderServer …")
        self.server.should_exit = True          # <— signals the loop in that thread
        try:
            self.thread.join(timeout=timeout)
        except KeyboardInterrupt:
            # If interrupted during shutdown, just log and continue
            log.debug("CommanderServer shutdown interrupted")

        if self.thread.is_alive():
            log.error("CommanderServer did not shut down within %.1fs", timeout)
        else:
            log.info("CommanderServer stopped")

def main():
    CommanderServer().start()

def cli():
    import argparse, sys
    p = argparse.ArgumentParser(description="GRID Commander FastAPI server")
    p.add_argument("--host", default=os.getenv("GRID_SERVER_HOST", "0.0.0.0"))
    p.add_argument("--port", type=int,
                   default=int(os.getenv("GRID_SERVER_PORT", 8060)))
    args = p.parse_args()
    # <-- This call blocks until Ctrl-C
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    cli()
