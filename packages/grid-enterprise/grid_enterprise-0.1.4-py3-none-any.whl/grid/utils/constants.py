"""
Common constants shared across GRID utilities.
"""

# Session-related port assignments
SESSION_VIZ_HTTP_PORT = 9090
SESSION_VIZ_WS_PORT = 9877
SESSION_NOTEBOOK_HTTP_PORT = 8890
SESSION_UI_HTTP_PORT = 3000
SESSION_UI_LOCAL_HTTP_PORT = 3198

# Local health endpoint (used to validate host IP selection)
HEALTH_CHECK_HOST = "0.0.0.0"
HEALTH_CHECK_PORT = 9654
HEALTH_CHECK_PATH = "/health"
