from fastapi import APIRouter, Request, HTTPException
from .secret_provider import get_secret
import os

router = APIRouter()

SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_BASE_URL = os.getenv("SERVICE_BASE_URL")


@router.get("/__verge__/routes", include_in_schema=False)
async def verge_internal_routes(request: Request):

    expected_secret = get_secret("VERGE_SERVICE_SECRET")
    received_secret = request.headers.get("X-Verge-Service-Secret")

    # Enforce exact secret match
    if not expected_secret or expected_secret != received_secret:
        raise HTTPException(status_code=403, detail="Forbidden")

    collected = []

    # FastAPI auto-generated system paths you DON'T want to sync
    INTERNAL_PREFIXES = (
        "/__verge__",
        "/openapi",
        "/docs",
        "/redoc"
    )

    for route in request.app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", [])

        if not path:
            continue

        # Skip internal/system routes
        if path.startswith(INTERNAL_PREFIXES):
            continue

        # Filter HTTP methods
        for method in methods:
            if method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                collected.append({
                    "path": path,
                    "method": method
                })

    # Sort for consistency (helps prevent duplicate entries in DB)
    collected.sort(key=lambda r: (r["path"], r["method"]))

    return collected


@router.post("/sync/service-routes", include_in_schema=False)
async def sync_service_routes(request: Request):

    expected_secret = get_secret("VERGE_SERVICE_SECRET")
    received_secret = request.headers.get("X-Verge-Service-Secret")

    if not expected_secret or expected_secret != received_secret:
        raise HTTPException(status_code=403, detail="Forbidden")

    collected = []

    INTERNAL_PREFIXES = (
        "/__verge__",
        "/openapi",
        "/docs",
        "/redoc"
    )

    # Collect routes from the app
    for route in request.app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", [])

        if not path:
            continue

        if path.startswith(INTERNAL_PREFIXES):
            continue

        for method in methods:
            if method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                collected.append({
                    "path": path,
                    "method": method
                })

    collected.sort(key=lambda r: (r["path"], r["method"]))

    return {
        "service": SERVICE_NAME,
        "base_url": SERVICE_BASE_URL,
        "routes": collected
    }