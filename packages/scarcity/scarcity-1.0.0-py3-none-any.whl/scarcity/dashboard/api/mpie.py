"""MPIE related endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["mpie"])


@router.get("/operators", summary="List active MPIE operators")
async def list_operators() -> dict[str, object]:
    """Return placeholder operator info."""

    return {"operators": []}


