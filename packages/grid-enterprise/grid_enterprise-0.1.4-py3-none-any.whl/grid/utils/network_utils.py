import ipaddress
import logging
import subprocess
from urllib import error, request

from .constants import HEALTH_CHECK_PATH, HEALTH_CHECK_PORT

logger = logging.getLogger("grid.utils.network")


def _health_endpoint_reachable(candidate_ip: str, timeout: int) -> bool:
    try:
        ip_obj = ipaddress.ip_address(candidate_ip)
    except ValueError:
        logger.debug("Invalid IP candidate %s from ifconfig.me", candidate_ip)
        return False

    host = candidate_ip if ip_obj.version == 4 else f"[{candidate_ip}]"
    url = f"http://{host}:{HEALTH_CHECK_PORT}{HEALTH_CHECK_PATH}"

    try:
        with request.urlopen(url, timeout=timeout) as resp:
            status = getattr(resp, "status", resp.getcode())
            return 200 <= status < 400
    except (error.URLError, error.HTTPError, TimeoutError) as exc:
        logger.debug("Health endpoint unreachable at %s: %s", url, exc)
    except Exception as exc:  # defensive catch for unexpected scenarios
        logger.debug("Unexpected error probing health endpoint %s: %s", url, exc)

    return False


def resolve_host_ip(timeout: int = 5) -> str:
    """
    Resolve the host IP by calling ifconfig.me and validating it against the local
    health endpoint. Falls back to 127.0.0.1 when validation fails.
    """
    try:
        output = subprocess.check_output(
            ["curl", "-s", "https://ifconfig.me"],
            text=True,
            timeout=timeout,
        ).strip()
        if output and _health_endpoint_reachable(output, timeout):
            return output
        if output:
            logger.debug("Discarding %s due to failing health check; using localhost", output)
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        logger.warning("Unable to resolve host IP via ifconfig.me: %s", exc)
    except Exception as exc:  # defensive catch for unexpected scenarios
        logger.debug("Unexpected error while resolving host IP: %s", exc)

    return "127.0.0.1"

