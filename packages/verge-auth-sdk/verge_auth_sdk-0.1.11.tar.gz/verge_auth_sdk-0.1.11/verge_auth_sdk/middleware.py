from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import os

from .secret_provider import get_secret
from .verge_routes import router as verge_routes_router

REGISTERED_ROUTES = []


def add_central_auth(app: FastAPI):

    # ----------------------------
    # ENV CONFIG
    # ----------------------------
    AUTH_INTROSPECT_URL = os.getenv("AUTH_INTROSPECT_URL")
    AUTH_LOGIN_URL = os.getenv("AUTH_LOGIN_URL")
    CLIENT_ID = os.getenv("VERGE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("VERGE_CLIENT_SECRET")

    SERVICE_NAME = os.getenv("SERVICE_NAME")
    SERVICE_BASE_URL = os.getenv("SERVICE_BASE_URL")
    AUTH_REGISTER_URL = os.getenv("AUTH_REGISTER_URL")
    VERGE_SECRET = get_secret("VERGE_SERVICE_SECRET")

    # ========================================================
    #  SUPER ADMIN ONLY — SERVICE REGISTRATION + ROUTE SYNC
    # ========================================================
    async def sync_with_auth_service():
        payload = {
            "name": SERVICE_NAME,
            "base_url": SERVICE_BASE_URL,
            "routes": REGISTERED_ROUTES,
        }

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.post(
                    AUTH_REGISTER_URL,
                    json=payload,
                    headers={"X-Verge-Service-Secret": VERGE_SECRET}
                )
                print(f"🔄 SUPER ADMIN Triggered Sync: {resp.status_code}")
                print("Response:", resp.text)

        except Exception as e:
            print("❌ Super Admin Sync Failed:", e)

    # ========================================================
    # ATTACH INTERNAL VERGE ROUTES FIRST
    # ========================================================
    app.include_router(verge_routes_router)

    # ========================================================
    # STARTUP — COLLECT ROUTES ONLY (NO SYNC)
    # ========================================================
    @app.on_event("startup")
    async def verge_bootstrap():
        print("🔥 Verge bootstrap started")
        REGISTERED_ROUTES.clear()
        print("📌 Collecting routes...")

        for route in app.routes:
            try:
                path = getattr(route, "path", None)
                methods = getattr(route, "methods", [])

                if not path:
                    continue

                # Skip internal routes
                if path.startswith(("/__verge__", "/docs", "/openapi")):
                    continue

                # Collect allowed HTTP methods
                for m in methods:
                    if m in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                        REGISTERED_ROUTES.append({"path": path, "method": m})

            except Exception as e:
                print("❌ Error collecting route:", e)

        print("✅ Route Collection:", REGISTERED_ROUTES)

    # ========================================================
    # MIDDLEWARE — AUTH ENFORCEMENT + SUPER ADMIN SYNC
    # ========================================================
    @app.middleware("http")
    async def central_auth(request: Request, call_next):
        path = request.url.path

        # Skip special paths
        if path.startswith("/__verge__") or path in {"/health", "/docs", "/openapi.json"}:
            return await call_next(request)

        # ----------------------
        # Extract Token
        # ----------------------
        token = None

        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            token = request.cookies.get("access_token")

        # =======================================================
        # CASE 1: UNAUTHENTICATED HTML → REDIRECT (NO SYNC)
        # =======================================================
        if not token and "text/html" in request.headers.get("accept", ""):
            login_redirect = f"{AUTH_LOGIN_URL}?redirect_url={request.url}"
            return RedirectResponse(login_redirect)

        # =======================================================
        # CASE 2: UNAUTHENTICATED API → 401
        # =======================================================
        if not token:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        # =======================================================
        # CASE 3: VALIDATE TOKEN WITH AUTH SERVICE
        # =======================================================
        try:
            async with httpx.AsyncClient(timeout=3) as client:
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

        # Get user & roles
        user = data.get("user", {})
        roles = data.get("roles", [])

        request.state.user = user
        request.state.roles = roles

        # =======================================================
        # ⭐ CASE 4: SUPER ADMIN LOGGED IN → TRIGGER SYNC
        # =======================================================
        is_super_admin = user.get("is_super_admin", False)

        if is_super_admin:
            print("🔐 Super Admin logged in — triggering registration + sync")
            await sync_with_auth_service()

        # Continue processing request
        return await call_next(request)
