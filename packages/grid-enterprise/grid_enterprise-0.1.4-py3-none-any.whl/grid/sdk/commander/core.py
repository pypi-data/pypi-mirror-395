import logging
import os
from pathlib import Path
import shlex
import subprocess
import yaml
import paramiko
import importlib.resources as pkg_resources
from typing import Generator, Dict, Any

from grid.utils.azcopy_downloader import AzCopyDownloader
from grid.utils.grid_asset_downloader import GRIDAssetDownloader
from grid.utils.airgen_utils import AirGenUtils
from grid.utils.isaac_utils import IsaacUtils
from grid.utils.network_utils import resolve_host_ip

from grid.utils.auth_utils import is_license_valid, get_client_datastore_name
import sys

logger = logging.getLogger("grid.commander")        # configured in server.py

class Commander:
    """
    Provides helper methods to manage GRID containers and remote commands.
    Progress suitable for the *client* is yielded, while full diagnostics are
    sent to the logger.
    """

    def __init__(self) -> None:
        self.node_data: Dict[str, Any] | None = None
        self.sim_profile: str | None = None
        self.docker_container_names = ["grid_core", "grid_server", "grid_sim"]
        self.sims = ["airgen", "isaac"]
        self.sim_utils_mapping = {
            "airgen": AirGenUtils,
            "isaac": IsaacUtils,
        }

        with pkg_resources.files("grid.utils").joinpath("docker-compose.yml") as p:
            self.docker_compose_file_path = str(p)

        self.azcopy_downloader = AzCopyDownloader()
        self.azcopy_downloader.ensure_azcopy_exists()
        
        # Check if the license is valid
        if not is_license_valid():
            logger.error(f"Invalid or non existing license. Please check your license file is present at {os.path.join(os.environ.get('GRID_DATA_DIR'), 'license.json')} and valid.")
            
            sys.exit(1)

        self.client_datastore = get_client_datastore_name()

    # --------------------------------------------------------------------- #
    # Public helpers                                                         #
    # --------------------------------------------------------------------- #
    def set_node_data(self, data: Dict[str, Any]) -> None:
        self.node_data = data
        logger.debug("Node data set: %s", data)

    # (unchanged) ---------------------------------------------------------- #
    def get_sim(self) -> str | None:
        return self.sim_profile
    # --------------------------------------------------------------------- #
    def set_sim(self, sim_name: str) -> None:
        self.sim_profile = sim_name
        self.docker_container_names[2] = f"grid_sim_{sim_name}"
        logger.info("Simulation profile set to %s", sim_name)

    # --------------------------------------------------------------------- #
    # Container lifecycle                                                    #
    # --------------------------------------------------------------------- #
    def init_containers(self, volume_info: Dict[str, str] | None) -> Generator[str, None, None]:
        """
        Build + up the docker-compose stack and stream progress lines.
        """
        try:
            if self.sim_profile:
                yield "Downloading pre-init assets\n"
                GRIDAssetDownloader.download_sim_assets(self.sim_profile, self.client_datastore)
                yield "Pre-init assets downloaded\n"
                
            if volume_info:
                logger.debug("Applying volume mappings: %s", volume_info)
                with open(self.docker_compose_file_path) as fp:
                    compose = yaml.safe_load(fp)

                for container_path, host_path in volume_info.items():
                    compose["services"].setdefault("core", {}) \
                        .setdefault("volumes", []).append(f"{host_path}:/workspace/{container_path}")
                    compose["services"].setdefault("sim-airgen", {}) \
                        .setdefault("volumes", []).append(f"{host_path}:/mnt/{container_path}")

                with open(self.docker_compose_file_path, "w") as fp:
                    yaml.safe_dump(compose, fp)
                logger.info("docker-compose file updated with volume mappings")

            resolved_host_ip = resolve_host_ip()
            compose_cmd = (
                f"HOST_IP={resolved_host_ip} docker compose -f "
                f"{self.docker_compose_file_path} --profile {self.sim_profile} up -d"
            )
            logger.debug("Running compose command: %s", compose_cmd)

            # run compose up detached; suppress container startup logs at info level
            for line in self._run_shell_iter(compose_cmd):
                # only log detailed compose output at debug level
                logger.debug(line.strip())

            yield "Checking container statuses...\n"
            statuses = {c: self.check_docker_container(c) for c in self.docker_container_names}
            for c, ok in statuses.items():
                line = f"{c}: {'✓' if ok else '✗'}\n"
                yield line
                logger.debug(line.strip())

            if not all(statuses.values()):
                err = "Error: one or more GRID containers failed to start."
                yield err + "\n"
                logger.error(err)
            else:
                yield "Containers are active.\n"
                logger.info("All containers up and running")

        except Exception as exc:
            logger.exception("init_containers failed: %s", exc)
            yield f"Exception: {exc}\n"

    def kill_containers(self) -> Generator[str, None, None]:
        compose_cmd = f"docker compose -f {self.docker_compose_file_path} --profile '*' down"
        logger.debug("Stopping containers with: %s", compose_cmd)

        # run compose down; suppress detailed shutdown logs at info level
        for line in self._run_shell_iter(compose_cmd):
            # only log detailed compose output at debug level
            logger.debug(line.strip())

        # status summary -------------------------------------------------- #
        statuses = {c: self.check_docker_container(c) for c in self.docker_container_names}
        for c, ok in statuses.items():
            line = f"{c}: {'✓' if not ok else '✗'}\n"
            yield line
            logger.debug(line.strip())

        if any(statuses.values()):
            err = "Error: one or more containers are still running."
            yield err + "\n"
            logger.error(err)
        else:
            yield "Containers stopped successfully.\n"
            logger.info("All containers stopped")

    def update_containers(self) -> Generator[str, None, None]:
        compose_cmd = f"docker compose -f {self.docker_compose_file_path} --profile {self.sim_profile} pull"
        logger.debug("Updating containers with: %s", compose_cmd)
        for line in self._run_shell_iter(compose_cmd):
            yield line
            logger.info(line.strip())

    # ------------------------------------------------------------------ #
    # Container status                                                   #
    # ------------------------------------------------------------------ #
    def check_grid_containers(self) -> bool:
        """
        Return **True only if *all* GRID containers are *running***.

        Keeps the status map on `self._last_status` so callers that need
        per-container information can still retrieve it.
        """
        self._last_status: dict[str, bool] = {
            name: self.check_docker_container(name)
            for name in self.docker_container_names
        }
        logger.debug("Container status: %s", self._last_status)
        return all(self._last_status.values())

    # --------------------------------------------------------------------- #
    # Registry login                                                        #
    # --------------------------------------------------------------------- #
    def login_registry(self, username: str, password: str) -> Generator[str, None, None]:
        yield "Logging in to General Robotics – GRID registry...\n"
        logger.info("Attempting ACR login for user %s", username)

        process = subprocess.run(
            ["docker", "login", "sfgrid.azurecr.io", "-u", username, "--password-stdin"],
            input=(password + "\n").encode(),
            capture_output=True,
        )

        if process.returncode == 0:
            msg = "Login successful!\n"
            yield msg
            logger.info(msg.strip())
        else:
            err = process.stderr.decode()
            yield f"Login failed:\n{err}"
            logger.debug("Docker login failed: %s", err.strip())
            self._stop_containers_due_to_invalid_license()

    def _stop_containers_due_to_invalid_license(self) -> None:
        """
        Stop running GRID containers when license validation fails so they cannot be used.
        """
        try:
            for _ in self.kill_containers():
                pass
        except Exception as exc:  # noqa: BLE001
            logger.debug("Failed to stop containers after license failure: %s", exc)

    def stop_containers_due_to_invalid_license(self) -> None:
        """Public wrapper for stopping containers on license failure."""
        self._stop_containers_due_to_invalid_license()

    # --------------------------------------------------------------------- #
    # File download                                                         #
    # --------------------------------------------------------------------- #
    def download_file(self, url: str, dest: str) -> Generator[str, None, None]:
        """
        Download a file or directory via AzCopyDownloader.
        """
        try:
            yield "Downloading …\n"
            logger.debug("Initiating azcopy to download asset: %s -> %s", url, dest)

            # delegate to AzCopyDownloader (handles SAS token internally)
            success, response = self.azcopy_downloader.download_az_file(url, dest)
            if success:
                if response=="exists":
                    yield "File already exists. Skipped download.\n"
                    logger.info("File already exists at destination: %s", dest)
                else:
                    yield "File download completed.\n"
                    logger.info("File download completed: %s", dest)
            else:
                err = f"Download failed for {url}"
                logger.error(err)
                logger.debug("AzCopy response: %s", response)

        except Exception as exc:
            logger.exception("download_file failed: %s", exc)
            yield f"Exception: {exc}\n"

    # --------------------------------------------------------------------- #
    # Asset initialisation                                                  #
    # --------------------------------------------------------------------- #
    def init_assets(self) -> Generator[str, None, None]:
        try:
            logger.info("Downloading model weights...")
            GRIDAssetDownloader.download_model_weights()
            logger.info("Model weights downloaded")

            logger.info("Downloading sample notebooks...")
            GRIDAssetDownloader.download_sample_notebooks()
            logger.info("Sample notebooks downloaded")

            yield "Assets initialized.\n"
        except Exception as exc:
            logger.exception("init_assets failed: %s", exc)
            yield f"Exception: {exc}\n"

    # --------------------------------------------------------------------- #
    # Helpers                                                               #
    # --------------------------------------------------------------------- #
    def check_docker_container(self, name: str) -> bool:
        cmd = "docker ps --format {{.Names}}"
        out = self._run_shell(cmd, quiet=True)
        return name in (out.splitlines() if out else [])
    
    def check_sim_container(self) -> str:
        """Return the name of the active simulation container, if any."""
        cmd = "docker ps --format {{.Names}}"
        out = self._run_shell(cmd, quiet=True)
        if out:
            running = set(out.splitlines())
            for sim in self.sims:
                if f"grid_sim_{sim}" in running:
                    return sim
        return ""

    def _run_shell_iter(self, command: str):
        with os.popen(command) as proc:
            for line in proc:
                yield line

    def _run_shell(self, command: str, quiet: bool = False) -> str | None:
        proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()
        if stderr:
            logger.error("Shell error (%s): %s", command, stderr.strip())
        if not quiet and stdout:
            logger.info("Shell output (%s): %s", command, stdout.strip())
        return stdout or None
