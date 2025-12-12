import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .constants import HEALTH_CHECK_HOST, HEALTH_CHECK_PATH, HEALTH_CHECK_PORT

logger = logging.getLogger("grid.repl")


class _HealthRequestHandler(BaseHTTPRequestHandler):
    """
    Minimal HTTP handler that exposes a single health endpoint.
    """

    def do_GET(self):  # noqa: N802 (BaseHTTPRequestHandler naming)
        if self.path == HEALTH_CHECK_PATH:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404)

    def log_message(self, format: str, *args):  # noqa: A003 (shadow builtin)
        # Suppress the default stdout logging from BaseHTTPRequestHandler
        logger.debug("Health server request: " + format, *args)


def start_health_server(
    host: str = HEALTH_CHECK_HOST, port: int = HEALTH_CHECK_PORT
) -> ThreadingHTTPServer | None:
    """
    Start the lightweight health server on a background thread.

    Returns the server instance so the caller can shut it down later.
    If the port is unavailable, returns None.
    """
    try:
        server = ThreadingHTTPServer((host, port), _HealthRequestHandler)
    except OSError as exc:
        logger.warning("Unable to start health server on %s:%s (%s)", host, port, exc)
        return None

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.debug("Health server started on %s:%s", host, port)
    return server


def stop_health_server(server: ThreadingHTTPServer | None) -> None:
    """
    Stop the health server if it was started.
    """
    if not server:
        return
    try:
        server.shutdown()
        server.server_close()
        logger.debug("Health server stopped")
    except KeyboardInterrupt:
        # If interrupted during shutdown, just log and continue
        logger.debug("Health server shutdown interrupted")

