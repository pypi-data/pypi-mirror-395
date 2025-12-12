import logging
import requests
from grid.sdk.resource_manager import GRIDResourceManager

from contextlib import contextmanager
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
logger = logging.getLogger(__name__)

@contextmanager
def _live_spinner(title: str):
    """
    Context manager yielding an `update(text)` callable that refreshes a single line.
    """
    prog = Progress(
        SpinnerColumn(style="bold cyan"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,            # clear on exit
    )
    tid = prog.add_task(title, start=False)
    with Live(prog, console=console, refresh_per_second=12):
        yield lambda txt: prog.update(tid, description=txt)

def _stream_with_spinner(response, title: str, *,
                         verbose: bool = False,
                         logfile: str | None = None):
    """
    Stream server output to a Rich spinner. If `verbose` is True, also echo full
    lines to the console; otherwise they are suppressed. If `logfile` is given,
    *all* lines are appended there.
    """
    logf = open(logfile, "a") if logfile else None
    try:
        with _live_spinner(title) as update:
            for raw in response.iter_lines(chunk_size=1, decode_unicode=True):
                if not raw:
                    continue
                line = raw.rstrip()
                update(line)          # live one-liner

                if verbose:
                    console.log(line)
                if logf:
                    print(line, file=logf)
    finally:
        if logf:
            logf.close()

class CommanderClient:
    def __init__(self, resource_manager: GRIDResourceManager):
        self.resource_manager = resource_manager
        self.api_token = "grid-enterprise-token"
        self.headers   = {"Authorization": f"Bearer {self.api_token}"}

    def check_grid_containers(self, node_name):
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.get(f"{base_url}/check_containers/", headers=self.headers)
        response.raise_for_status()
        containers_status = response.json()
        all_up = containers_status.get("status", False)
        return all_up
    
    def check_sim_container(self, node_name):
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.get(f"{base_url}/check_sim_container/", headers=self.headers)
        response.raise_for_status()
        containers_status = response.json()
        sim_name = containers_status.get("sim_name")
        return sim_name

    def set_sim(self, node_name, sim_name):
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/set_sim/", headers=self.headers, json={"sim_name": sim_name})
        response.raise_for_status()
        return response.json()
    
    def get_sim(self, node_name):
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.get(f"{base_url}/get_sim/", headers=self.headers)
        response.raise_for_status()
        sim_data = response.json()
        return sim_data.get("sim_name", "")

    def init_containers(self, node_name, verbose=False):
        node_ip = self.resource_manager.get_ip(node_name)
        volume_info = self.resource_manager.storage_mounts(node_name)
        base_url = f"http://{node_ip}:8060"

        resp = requests.post(
            f"{base_url}/init_containers/", headers=self.headers,
            json={"volume_info": volume_info},
            stream=True,
        )
        resp.raise_for_status()

        _stream_with_spinner(resp, "Starting containers…",
                            verbose=verbose,
                            logfile="grid_client.log")

    def login_registry(self, node_name) -> bool:
        """Trigger registry login on the server using server-side license credentials."""
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        try:
            response = requests.post(
                f"{base_url}/login_registry/", headers=self.headers, stream=True
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.debug("Registry login request failed: %s", exc)
            return False

        success = True
        for line in response.iter_lines():
            if not line:
                continue
            decoded_line = line.decode("utf-8")
            if "login failed" in decoded_line.lower():
                success = False

        return success

    def kill_containers(self, node_name, verbose=False):
        node_ip = self.resource_manager.get_ip(node_name)
        resp = requests.post(
            f"http://{node_ip}:8060/kill_containers/", headers=self.headers,
            stream=True,
        )
        resp.raise_for_status()
        _stream_with_spinner(resp, "Stopping containers…",
                             verbose=verbose,
                             logfile="grid_client.log")

    def update_containers(self, node_name, verbose=False):
        node_ip = self.resource_manager.get_ip(node_name)
        resp = requests.post(
            f"http://{node_ip}:8060/update_containers/", headers=self.headers,
            stream=True,
        )
        resp.raise_for_status()
        _stream_with_spinner(resp, "Updating containers…",
                             verbose=verbose,
                             logfile="grid_client.log")

    def download_asset(self, node: str, url: str, rel_path: str):
        node_ip = self.resource_manager.get_ip(node)
        resp = requests.post(
            f"http://{node_ip}:8060/download_file/", headers=self.headers,
            json={"url": url, "dest": rel_path},      # note: rel_path
            stream=True,
        )
        resp.raise_for_status()
        _stream_with_spinner(resp, "Downloading asset …")
                
    def init_assets(self, node_name):
        node_ip = self.resource_manager.get_ip(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/init_assets/", headers=self.headers)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
                
