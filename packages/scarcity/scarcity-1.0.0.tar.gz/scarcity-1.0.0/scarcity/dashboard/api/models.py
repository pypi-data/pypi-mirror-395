"""Model registry endpoints."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from .. import registry

router = APIRouter(tags=["models"])


@router.get("/versions", summary="List stored global models")
async def list_models() -> dict[str, object]:
    """Return model metadata from the registry."""

    return {"models": registry.list_models()}


@router.post("/push", summary="Upload and broadcast a new model revision")
async def push_model(
    revision: int = Form(...),
    file: UploadFile = File(...)
) -> dict[str, object]:
    """Accept a request to push a new model revision."""

    if file.content_type not in {"application/json", "text/json"}:
        raise HTTPException(status_code=415, detail="Only JSON model files are supported.")
    content = await file.read()
    path = registry.save_model(str(revision), content)
    return {"status": "stored", "revision": revision, "path": path}


@router.get("/{revision}", summary="Download a model revision")
async def download_model(revision: str) -> FileResponse:
    """Serve a stored model revision."""

    path = registry.get_model_path(revision)
    return FileResponse(path, media_type="application/json", filename=f"{revision}.json")


