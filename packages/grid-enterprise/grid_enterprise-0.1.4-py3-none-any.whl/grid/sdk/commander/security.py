# server/security.py
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

TOKEN = os.getenv("GRID_API_TOKEN", "grid-enterprise-token")
_auth_scheme = HTTPBearer(auto_error=False)   # don’t raise automatically

def require_token(
    creds: HTTPAuthorizationCredentials = Depends(_auth_scheme),
):
    """Raise 401 if the bearer token is missing or doesn’t match TOKEN."""
    if not creds or creds.scheme.lower() != "bearer" or creds.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )