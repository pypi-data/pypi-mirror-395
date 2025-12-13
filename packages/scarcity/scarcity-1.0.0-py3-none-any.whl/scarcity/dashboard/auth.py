"""Authentication helpers and routes for SCIC."""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()

_bearer_scheme = HTTPBearer(auto_error=False)


def _issue_token(subject: str) -> dict[str, object]:
    """Return a dummy token payload."""

    expires = datetime.utcnow() + timedelta(hours=1)
    return {
        "access_token": f"dummy-token-for-{subject}",
        "token_type": "bearer",
        "expires_at": expires.isoformat() + "Z",
    }


@router.post("/login", summary="Obtain an access token")
async def login(username: str, password: str) -> dict[str, object]:
    """Placeholder login endpoint."""

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _issue_token(username)


async def authenticate(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
) -> str:
    """Simple dependency that validates the provided token."""

    if credentials is None or not credentials.credentials.startswith("dummy-token"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return credentials.credentials


