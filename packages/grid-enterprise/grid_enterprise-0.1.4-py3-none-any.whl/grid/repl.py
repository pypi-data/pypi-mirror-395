from pathlib import Path
import asyncio
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import shlex
import subprocess
import sys
import webbrowser
from cmd import Cmd
from typing import Tuple, List
try:
    import readline
except ImportError:  # pragma: no cover - Windows without readline
    readline = None
import time
import requests
from importlib.metadata import version as pkg_version
import importlib.resources as pkg_resources
from packaging import version
from art import tprint
from rich import print  # rich-style coloured prints
from tabulate import tabulate

from grid.sdk.commander.client import CommanderClient
from grid.sdk.resource_manager import GRIDResourceManager
from grid.sdk.session_manager import GRIDSessionManager
from grid.utils.config_handler import ConfigHandler
from grid.utils.airgen_utils import AirGenUtils
from grid.utils.isaac_utils import IsaacUtils
from grid.utils.network_utils import resolve_host_ip
from grid.utils.constants import (
    SESSION_NOTEBOOK_HTTP_PORT,
    SESSION_UI_LOCAL_HTTP_PORT,
    SESSION_VIZ_HTTP_PORT,
    SESSION_VIZ_WS_PORT,
)
from grid.utils.health_server import start_health_server, stop_health_server

REQUEST_TIMEOUT = 5  # HTTP timeout for PyPI check (s)
SIM_OPTIONS = {1: "airgen", 2: "isaac"}
SIM_UTILS = {"airgen": AirGenUtils, "isaac": IsaacUtils}
LOG_PATH = Path.home() / ".grid" / "grid_repl.log"

def get_logger() -> logging.Logger:
    """Return module logger with rotating file + console handlers (idempotent)."""
    logger = logging.getLogger("grid.repl")
    if logger.handlers:
        return logger

    # Emit all levels to handlers
    logger.setLevel(logging.DEBUG)

    # File handler: rotate at 10MB, keep 5 backups
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(LOG_PATH, maxBytes=10_000_000, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fmt_file = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    fh.setFormatter(fmt_file)
    logger.addHandler(fh)

    # Console handler: INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt_console = logging.Formatter("%(levelname)-8s | %(message)s")
    ch.setFormatter(fmt_console)
    logger.addHandler(ch)

    return logger


logger = get_logger()

class GRIDRepl(Cmd):
    """Interactive shell for GRID Enterprise users."""

    # wrap ANSI color codes in readline zero-length markers so history navigation works
    prompt = 'GRID \001\033[91m\002#\001\033[0m\002 '
    intro = tprint("\nGRID", "colossal")

    # ---------------------------- INITIALISATION ------------------------ #
    def __init__(self) -> None:
        super().__init__()
        if readline:
            current_delims = readline.get_completer_delims()
            if "/" in current_delims:
                readline.set_completer_delims(" \t\n")
        print("General Robot Intelligence Development Platform - Enterprise version \nGeneral Robotics Technology, Inc.\n")
        self.sim_name: str | None = None
        self.default_node_name = "local"

        # managers / clients -------------------------------------------- #
        raw_cfg          = ConfigHandler.load_resource_config()
        self.resource_manager = GRIDResourceManager.from_config(raw_cfg)
        self.commander = CommanderClient(self.resource_manager)
        self.session_manager  = GRIDSessionManager(self.resource_manager,
                                                 self.commander, username="grid-user")

        self.health_server = start_health_server()
        self._start_local_server_if_needed()

        resolved_host_ip = resolve_host_ip()
        if not resolved_host_ip:
            resolved_host_ip = "127.0.0.1"

        self.local_url = "127.0.0.1"
        self.vm_url = f"{resolved_host_ip}"

        self.loop = asyncio.get_event_loop()
        self._check_for_updates()

        print("Type [cyan]help[/cyan] for list of commands.\n")

        
    def _parse_line(self, line: str) -> Tuple[List[str], str, bool]:
        """Return (positional_tokens, node_name, verbose_flag)."""
        node, verbose, pos = self.default_node_name, False, []
        node_specified = False
        try:
            tokens = shlex.split(line)
        except ValueError as exc:
            print(f"[red]Invalid input:[/red] {exc}")
            return [], node, verbose

        for tok in tokens:
            if tok.startswith("@"):
                node = tok[1:]
                node_specified = True
            elif tok == "--verbose":
                verbose = True
            else:
                pos.append(tok)

        if not node_specified:
            print(f"[yellow]No node specified; using {self.default_node_name}.[/yellow]")
        return pos, node, verbose

    def _start_local_server_if_needed(self) -> None:
        # 1. If containers are *not* meant to run on this machine, skip.
        if not self.resource_manager.should_serve():
            self.commander_server = None
            return

        # 2. Lazy-import the FastAPI server (keeps client-only installs light).
        try:
            from grid.sdk.commander.server import CommanderServer
        except ImportError:                       # user installed client-only wheel
            print(
                "[red]Local CommanderServer unavailable — "
                "install extras: pip install 'grid-enterprise[server]'[/red]"
            )
            self.commander_server = None
            return

        # 3. Start the server in a background thread so the REPL stays interactive.
        host = os.getenv("GRID_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("GRID_SERVER_PORT", 8060))
        self.commander_server = CommanderServer(host, port)

        # suppress CommanderServer / FastAPI / Uvicorn logs in this REPL
        import logging
        for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
            lg = logging.getLogger(name)
            lg.setLevel(logging.WARNING)
            lg.propagate = False

        # now start without polluting the REPL stdout
        self.commander_server.start(block=False)

    def _check_for_updates(self) -> None:
        try:
            cur = pkg_version("grid-enterprise")
            data = requests.get("https://pypi.org/pypi/grid-enterprise/json", timeout=REQUEST_TIMEOUT).json()
            latest = data["info"]["version"]
            if version.parse(latest) > version.parse(cur):
                print(f"[yellow]Update available:[/yellow] {latest} (current {cur}) — pip install -U grid-enterprise")
        except Exception as exc:
            logger.debug("Update check failed: %s", exc)

    @staticmethod
    def _choose_sim() -> str:
        while True:
            print("Select simulator:")
            for k, v in SIM_OPTIONS.items():
                print(f"  {k}: {v}")
            try:
                idx = int(input("> ").strip())
                if idx in SIM_OPTIONS:
                    return SIM_OPTIONS[idx]
            except ValueError:
                pass
            print("Invalid choice, try again.")

    def _ensure_sim(self, candidate: str | None) -> str:
        if candidate and candidate in SIM_UTILS:
            return candidate
        if candidate:
            print(f"[yellow]Unknown simulator:[/yellow] {candidate}")
        return self._choose_sim()
    
    def _require_node(self, node: str) -> bool:
        """Return True if node is valid; otherwise print error + suggestion."""
        if self.resource_manager.node_exists(node):
            return True
        print(f"[red]Unknown node: {node}[/red]")
        print("Run [bold]node list[/bold] to see configured nodes.")
        return False


    def _safe(self, fn, *args, **kw):
        """Run commander call, catch KeyError/ValueError, show concise message."""
        try:
            return fn(*args, **kw)
        except (KeyError, ValueError) as exc:
            print(f"[red]{exc}[/red]")
        except requests.RequestException as exc:
            print(f"[red]Cannot reach Commander server[/red]. Please ensure it is running and reachable.")

        return None

    def _path_completions(self, text: str) -> List[str]:
        """Return filesystem path completions honoring relative and user paths."""
        text = text or ""
        if text.startswith("@"):  # do not attempt path completion for node selectors
            return []

        quote_char = ""
        if text.startswith(("'", '"')):
            quote_char = text[0]
            text = text[1:]

        if text and text.endswith(os.sep):
            dir_part = text
            prefix = ""
        else:
            dir_part = os.path.dirname(text)
            prefix = os.path.basename(text)

        if dir_part:
            expanded_dir = os.path.expanduser(dir_part)
            display_dir = dir_part
        else:
            if text.startswith("~"):
                expanded_dir = os.path.expanduser("~")
                display_dir = "~"
            else:
                expanded_dir = os.path.expanduser(".")
                display_dir = ""
        if not os.path.isdir(expanded_dir):
            return []

        try:
            entries = os.listdir(expanded_dir)
        except OSError:
            return []

        completions: List[str] = []
        for entry in entries:
            if not entry.startswith(prefix):
                continue
            candidate_base = display_dir if display_dir else ""
            candidate = os.path.join(candidate_base, entry) if candidate_base else entry
            full_path = os.path.join(expanded_dir, entry)
            if os.path.isdir(full_path):
                candidate = candidate + os.sep
            if quote_char:
                candidate = quote_char + candidate
            elif any(ch.isspace() for ch in candidate):
                candidate = shlex.quote(candidate)
            completions.append(candidate)

        completions.sort()
        return completions

    def complete_session(self, text, line, begidx, endidx):
        """Provide tab completions for the session command."""
        options = ["start", "stop", "list"]
        try:
            lexer = shlex.shlex(line[:begidx], posix=True)
            lexer.whitespace_split = True
            lexer.commenters = ""
            tokens = list(lexer)
        except ValueError:
            return []

        if not tokens:
            return [opt for opt in options if opt.startswith(text)]

        if tokens[0] != "session":
            return []

        if len(tokens) == 1:
            return [opt for opt in options if opt.startswith(text)]

        subcmd = tokens[1]

        if subcmd != "start":
            return []

        # session start <session_id> [config]
        args = tokens[2:]
        if not args:
            return []

        if text:
            if args and args[-1] == text:
                arg_index = len(args) - 1
            else:
                arg_index = len(args)
        else:
            arg_index = len(args)

        if arg_index == 1:
            target_text = text
            if not target_text and len(args) >= 2:
                target_text = ""
            return self._path_completions(target_text)  

        return []
    
    def do_exit(self, _line: str) -> bool:  # noqa: D401, ANN001
        """Terminate the REPL (alias: Ctrl-D/Eof)."""
        self._shutdown()
        return True

    # Alias so Ctrl-D triggers the same shutdown path
    do_EOF = do_exit  # type: ignore[misc]
    def _shutdown(self):
        if getattr(self, "commander_server", None):
            self.commander_server.stop()
        if getattr(self, "health_server", None):
            stop_health_server(self.health_server)
        print("Goodbye!")

    def default(self, line: str):  # noqa: D401
        print(f"Unknown command: {line}. Try 'help'.")

    def do_clear(self, _):
        """Clear the terminal output."""
        os.system("clear")

    def do_init(self, line: str):
        """Spin up containers on the server (downloads if containers do not exist)
        
           Usage: init [sim] [--verbose] [@nodename]."""
        pos, node, verbose = self._parse_line(line)
        if not self._require_node(node):
            return                                  # early exit

        sim = self._ensure_sim(pos[0] if pos else None)

        running_sim = self._safe(self.commander.check_sim_container, node)
        if running_sim and running_sim != sim:
            print(
                "[red]Conflicting simulator detected:[/red] "
                f"[yellow]{running_sim}[/yellow] is already running on {node}. "
                "Terminate it before starting "
                f"[cyan]{sim}[/cyan]."
            )
            return

        self.sim_name = sim

        if self._safe(self.commander.set_sim, node, sim) is None:
            return                                  # error already shown

        if self.commander.check_grid_containers(node):
            print(f"[green]Containers already running on {node}[/green]")
            return

        print("Initializing assets …")
        self.commander.init_assets(node)
        print(f"Starting {sim} on {node} …")
        self.commander.init_containers(node, verbose)

    def do_terminate(self, line: str):
        _, node, verbose = self._parse_line(line)
        if not self._require_node(node):
            return
        self._safe(self.commander.kill_containers, node, verbose)

    def do_update(self, line: str):
        """Update containers on the server.
        
           Usage: update [sim] [--verbose] [@nodename]"""
        pos, node, verbose = self._parse_line(line)
        if not self._require_node(node):
            return
        
        sim = self._ensure_sim(pos[0] if pos else None)
        self.sim_name = sim
        
        if self._safe(self.commander.set_sim, node, sim) is None:
            return                                  
        
        print("Checking for updates …")
        self.commander.update_containers(node, verbose)
        print("Updating assets …")
        self.commander.init_assets(node)

    def _login_registry(self, node: str) -> bool:
        """Attempt registry login and return True on success."""
        try:
            success = self.commander.login_registry(node)
        except Exception as exc:  # noqa: BLE001
            logger.debug("Registry login failed: %s", exc)
            success = False
        if not success:
            print("[red]Invalid or expired license.[/red] You will not be able to run this software until you update/renew your license. Please check the validity of your license file or contact General Robotics.")
        return success

    def do_login(self, line: str):
        """login [@node] — docker login to ACR on server."""
        _, node, _ = self._parse_line(line)
        self._login_registry(node)
        return False

    def do_node(self, line: str):
        """List available nodes and select default.

           node list — list all available server nodes.
           node select <name> — set default node.
        """
        parts = shlex.split(line)
        if not parts:
            print("Usage: node list/select <nodename>")
            return

        cmd = parts[0]
        if cmd == "list":
            if len(parts) != 1:
                print("Usage: node list")
                return
            rows = self.resource_manager.list_nodes()
            print(tabulate(rows, headers="keys", tablefmt="grid"))

        elif cmd == "select":
            if len(parts) != 2:
                print("Usage: node select <node>")
                return
            node = parts[1]
            if not self.resource_manager.node_exists(node):
                print(f"[red]Unknown node: {node}[/red]")
                print("Run 'node list' to see configured nodes.")
                return
            self.default_node_name = node
            print(f"[green]Default node set to {node}[/green]")

        else:
            print("Usage: node list|select <node>")

    def do_session(self, line: str):
        """Manage remote sessions.

        session start <id> [config] [@nodename]
        session stop <id>/@nodename
        session list
        """
        pos, node, _ = self._parse_line(line)  
        
        if not pos:
            print("Usage: session start/stop/list …")
            return
        cmd = pos[0]
        if cmd == "list":
            self.loop.run_until_complete(self.session_manager.list_sessions())
            return
        if cmd == "start" and len(pos) >= 2:
            if not self._require_node(node):
                return             
            session_id = pos[1]
            if not self.commander.check_grid_containers(node):
                print("[yellow]Containers not running; run init first.[/yellow]")
                return
            
            sim_name = self.commander.get_sim(node)
            cfg = pos[2] if len(pos) >= 3 else self._create_sample_config(sim_name)
            config_path = Path(cfg).expanduser()
            if not config_path.exists():
                print(f"[red]Config file {config_path} does not exist.[/red]")
                return
            
            print(f"Starting session [cyan]{session_id}[/cyan] on node [green]{node}[/green] …")
            self.loop.run_until_complete(self.session_manager.start_session(session_id, config_path, node))
        elif cmd == "stop":
            target = pos[1] if len(pos) >= 2 else ""
            self.loop.run_until_complete(self._stop_session(target, node))
        else:
            print("Invalid session command.")

    def do_open(self, line: str):
        """Open interface for the active session on the specified node.

           Usage: open [interface] [@nodename]
           
           Interfaces:
           - ui (default): Open the web UI
           - nb: Open Jupyter notebook interface
           - viz: Open visualization interface
           - sim: Open simulation interface
           - code: Open VS Code interface
           
           Examples:
           - open @local          -> Opens UI
           - open nb @local       -> Opens notebook
           - open code @local     -> Opens VS Code
        """
        pos, node, _ = self._parse_line(line)
        if not self._require_node(node):
            return
            
        VALID_ENTITIES = {"nb", "sim", "viz", "code", "ui", "dc"}
        if len(pos) == 1 and pos[0] in VALID_ENTITIES:
            entity = pos[0]
        else:
            print(f"[red] Invalid or missing interface.[/red]")
            return

        if entity == "dc":
            self._open_entity(entity, node, None)
            time.sleep(1)
            return False

        # Get session ID (async call)
        session_id = self.loop.run_until_complete(self.session_manager.get_session_id_by_node(node))
        if not session_id:
            print(f"[yellow]No active sessions on node {node}.[/yellow]")
            return
            
        self._open_entity(entity, node, session_id)
        # Add a small delay to allow the browser to open and display the message
        time.sleep(1)
        
        return False  # Explicitly return to continue the REPL
    
    def _create_sample_config(self, sim_name) -> str:
        sim_util = SIM_UTILS[sim_name]
        sample = sim_util.create_sample_config()
        config_dir = Path.home() / ".grid"
        config_dir.mkdir(exist_ok=True)
        path = config_dir / f"sample_session_{self.sim_name}.json"
        path.write_text(json.dumps(sample, indent=2))
        print(f"Using sample config at {path}")
        return str(path)

    async def _stop_session(self, target: str, node: str):
        """Stop a session by ID or by @node handle."""
        print(f"Stopping session [cyan]{target}[/cyan] on node [green]{node}[/green] …")
        if not target:
            session_id = await self.session_manager.get_session_id_by_node(node)
            if not session_id:
                print(f"No active sessions on node {node}.")
                return
        else:
            session_id = target
            ip = self.session_manager.session_nodes.get(session_id)
            if not ip:
                ip = self.resource_manager.get_ip(node)

        await self.session_manager.stop_session(node, session_id)
    
    def _open_entity(self, entity: str, node: str, session_id: str | None):
        if entity == "dc":
            compose_resource = pkg_resources.files("grid.utils") / "docker-compose.yml"
            compose_path = Path(compose_resource)
            if not compose_path.exists():
                print("[red]docker-compose.yml resource not found.[/red]")
                return

            compose_url = compose_path.as_uri()
            print(f"Docker Compose file → [link={compose_url}]docker-compose.yml[/link]")
            #webbrowser.open(compose_url)
            return

        ip = self.resource_manager.get_ip(node)
        
        # Handle VS Code separately
        if entity == "code":
            try:
                folder_uri = f"vscode-remote://attached-container%2B677269645f636f7265/workspace"
                subprocess.run(["code", "--folder-uri", folder_uri], check=True)
                print(f"Opening VSCode remote container on node {node}")
            except subprocess.SubprocessError as exc:
                logger.error("VSCode launch failed: %s", exc)
                print("VSCode not available. Ensure the 'code' CLI is installed.")

            return

        # Build URLs for other entities
        local_urls = {
            "viz": f"http://{self.local_url}:{SESSION_VIZ_HTTP_PORT}/?url=ws://{self.local_url}:{SESSION_VIZ_WS_PORT}",
            "nb": f"http://{self.local_url}:{SESSION_NOTEBOOK_HTTP_PORT}",
            "ui": f"http://{self.local_url}:{SESSION_UI_LOCAL_HTTP_PORT}?sessionId={session_id}"
        }

        vm_urls = {
            "viz": f"http://{self.vm_url}:{SESSION_VIZ_HTTP_PORT}/?url=ws://{self.vm_url}:{SESSION_VIZ_WS_PORT}",
            "nb": f"http://{self.vm_url}:{SESSION_NOTEBOOK_HTTP_PORT}",
            "ui": f"http://{self.vm_url}:{SESSION_UI_LOCAL_HTTP_PORT}?sessionId={session_id}"
        }

        # Handle sim entity - need to check if sim_name is available
        if entity == "sim":
            if self.sim_name and self.sim_name in SIM_UTILS:
                local_urls["sim"] = SIM_UTILS[self.sim_name].sim_streaming_url(self.local_url)
                vm_urls["sim"] = SIM_UTILS[self.sim_name].sim_streaming_url(self.vm_url)
            else:
                print(f"[red]No simulator configured. Run 'init <sim>' first.[/red]")
                return

        local_url = local_urls.get(entity)
        vm_url = vm_urls.get(entity)

        if vm_url and local_url:
                
            print(f"If you are running the setup in your machine - {local_url}")
            print(f"If you are running this setup from a VM - {vm_url}")
            webbrowser.open(vm_url)
        else:
            print(f"[red]Unknown entity: {entity}[/red]")
            print("Available entities: ui, nb, viz, sim, code")
            
    def do_logs(self, line: str):
        """Show last N lines of the specified log.

           Usage: logs <commander|session|repl> [[N]]"""
        parts = shlex.split(line)
        if not parts or parts[0] not in ("commander", "session", "repl", "server", "core", "sim"):
            print("Usage: logs <commander|session|repl> [[n]]")
            return
        which = parts[0]
        # parse count
        if len(parts) > 1:
            try:
                n = int(parts[1])
            except ValueError:
                print("Usage: logs <commander|session|repl> [[n]]  # n must be an integer")
                return
        else:
            n = 100
        # determine logger
        if which == "commander":
            if not self.resource_manager.should_serve():
                print("Commander logs available only when serving on local.")
                return
            logger_name = "grid.commander"
        elif which == "session":
            logger_name = "grid.session"
        elif which in ("core", "server", "sim"):  # repl
            container_map = {
                "core": "grid_core",
                "server": "grid_server", 
                "sim": f"grid_sim_{self.sim_name}" if self.sim_name else "grid_sim_airgen"
            }
            container = container_map.get(which, "grid_core")
            
            try:
                result = subprocess.run(
                    ["docker", "logs", "--tail", str(n), container],
                    capture_output=True, text=True, check=True
                )
                print(f"--- Last {n} lines from {container} ---")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return
            except subprocess.CalledProcessError as e:
                print(f"Error getting docker logs for {container}: {e}")
                return
            except FileNotFoundError:
                print("Docker command not found. Please ensure Docker is installed.")
                return
        # locate file handler
        handlers = logging.getLogger(logger_name).handlers
        log_file = None
        for h in handlers:
            if hasattr(h, "baseFilename"):
                log_file = h.baseFilename
                break
        if not log_file:
            print(f"No '{which}' log file handler found.")
            return
        from pathlib import Path
        path = Path(log_file)
        if not path.exists():
            print(f"Log file not found: {path}")
            return
        # read last n lines
        from collections import deque

        with path.open() as f:
            lines = deque(f, maxlen=n)
        print(f"--- Last {n} lines from {which} log ({path}) ---")
        for l in lines:
            print(l.rstrip())


def repl() -> None:  # noqa: D401
    """Run the GRID interactive shell."""
    shell = GRIDRepl()
    try:
        if not shell._login_registry(shell.default_node_name):
            shell._shutdown()
            sys.exit(1)
        shell.cmdloop()
    except KeyboardInterrupt:
        shell._shutdown()


if __name__ == "__main__":
    repl()
