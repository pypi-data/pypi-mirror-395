from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import os

from .secret_provider import get_secret
from .verge_routes import router as verge_routes_router

REGISTERED_ROUTES = []


def add_central_auth(app: FastAPI):

    AUTH_INTROSPECT_URL = os.getenv("AUTH_INTROSPECT_URL")
    AUTH_LOGIN_URL = os.getenv("AUTH_LOGIN_URL")

    CLIENT_ID = os.getenv("VERGE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("VERGE_CLIENT_SECRET")

    SERVICE_NAME = os.getenv("SERVICE_NAME")
    SERVICE_BASE_URL = os.getenv("SERVICE_BASE_URL")
    AUTH_REGISTER_URL = os.getenv("AUTH_REGISTER_URL")

    VERGE_SECRET = get_secret("VERGE_SERVICE_SECRET")

    # ---------------------------------------
    # INTERNAL ROUTES (MUST LOAD FIRST)
    # ---------------------------------------
    app.include_router(verge_routes_router)

    # ---------------------------------------
    # STARTUP — ONLY COLLECT ROUTES (NO REGISTER)
    # ---------------------------------------
    @app.on_event("startup")
    async def collect_routes():
        print("🔥 Verge bootstrap started")
        REGISTERED_ROUTES.clear()

        for route in app.routes:
            path = getattr(route, "path", None)
            methods = getattr(route, "methods", [])

            if not path:
                continue

            if path.startswith(("/docs", "/openapi", "/__verge__")):
                continue

            for m in methods:
                if m in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                    REGISTERED_ROUTES.append({"path": path, "method": m})

        print("✅ Collected Routes:", REGISTERED_ROUTES)

    # ---------------------------------------
    # SUPER ADMIN TRIGGERED REGISTRATION
    # ---------------------------------------
    async def register_with_auth():
        print("🔧 Triggered register_with_auth()")
        print("📍 AUTH_REGISTER_URL =", AUTH_REGISTER_URL)
        print("📍 SERVICE_NAME =", SERVICE_NAME)
        print("📍 SERVICE_BASE_URL =", SERVICE_BASE_URL)
        print("📍 CLIENT_ID =", CLIENT_ID)
        print("📍 ROUTES =", REGISTERED_ROUTES)
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    AUTH_REGISTER_URL,
                    params={
                        "name": SERVICE_NAME,
                        "base_url": SERVICE_BASE_URL,
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET
                    },
                    headers={"X-Verge-Service-Secret": VERGE_SECRET}
                )

            print(f"📡 Registration: {resp.status_code}")
            print(resp.text)

        except Exception as e:
            print("❌ Registration failed:", e)

    # ---------------------------------------
    # MIDDLEWARE AUTH
    # ---------------------------------------
    @app.middleware("http")
    async def central_auth(request: Request, call_next):
        path = request.url.path

        # Whitelisted paths
        if path.startswith("/__verge__") or path in {"/docs", "/openapi.json", "/health"}:
            return await call_next(request)

        # Extract token
        token = None
        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            token = request.cookies.get("access_token")

        # redirect if HTML request
        if not token and "text/html" in request.headers.get("accept", ""):
            return RedirectResponse(
                f"{AUTH_LOGIN_URL}?redirect_url={request.url}"
            )

        if not token:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        # Validate token
        try:
            async with httpx.AsyncClient(timeout=4) as client:
                res = await client.post(
                    AUTH_INTROSPECT_URL,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "X-Client-Id": CLIENT_ID,
                        "X-Client-Secret": CLIENT_SECRET,
                    },
                )
                data = res.json()

        except Exception:
            return JSONResponse({"detail": "Auth service unreachable"}, status_code=503)

        if not data.get("active"):
            return JSONResponse({"detail": "Session expired"}, status_code=401)

        user = data.get("user", {})
        request.state.user = user

        # ----------------------------------------------
        # ⭐ ANY authenticated user triggers auto-registration
        # ----------------------------------------------
        print("🔐 Authenticated user → auto-registering service")
        await register_with_auth()
