from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import os
import asyncio

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

    # ------------------------------------------------------
    # INTERNAL ROUTER
    # ------------------------------------------------------
    app.include_router(verge_routes_router)

    # ------------------------------------------------------
    # COLLECT ROUTES
    # ------------------------------------------------------
    def collect_routes():
        print("\n********** [ROUTE COLLECTION STARTED] **********")

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

        print("🔥 Collected Routes:", REGISTERED_ROUTES)
        print("********** [ROUTE COLLECTION COMPLETED] **********\n")

    # ------------------------------------------------------
    # REGISTER SERVICE WITH AUTH
    # ------------------------------------------------------
    async def register_with_auth():
        print("\n********** [SERVICE REGISTRATION TRIGGERED] **********")
        print("📡 AUTH_REGISTER_URL:", AUTH_REGISTER_URL)
        print("📌 SERVICE_NAME:", SERVICE_NAME)
        print("📌 SERVICE_BASE_URL:", SERVICE_BASE_URL)
        print("📌 CLIENT_ID:", CLIENT_ID)
        print("📌 ROUTES:", REGISTERED_ROUTES)

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

            print("📡 REGISTRATION STATUS:", resp.status_code)
            print("📄 RESPONSE:", resp.text)

        except Exception as e:
            print("❌ REGISTRATION FAILED:", e)

        print("********** [SERVICE REGISTRATION COMPLETED] **********\n")

    # ------------------------------------------------------
    # MIDDLEWARE
    # ------------------------------------------------------
    @app.middleware("http")
    async def central_auth(request: Request, call_next):
        print("\n====================================")
        print("********** [MIDDLEWARE ENTERED] **********")
        print("➡ PATH:", request.url.path)
        print("====================================\n")

        path = request.url.path

        # ------------------------------------
        # WHITELIST CHECK
        # ------------------------------------
        if path.startswith("/__verge__") or path in {"/docs", "/openapi.json", "/health"}:
            print("✔ WHITELISTED PATH — SKIPPING AUTH")
            print("********** [MIDDLEWARE EXIT - WHITELIST] **********\n")
            return await call_next(request)

        print("🔎 NOT WHITELIST — Proceeding with Auth Check")

        # ------------------------------------
        # TOKEN EXTRACTION
        # ------------------------------------
        auth_header = request.headers.get("authorization")
        token = None

        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]
            print("✔ TOKEN FOUND IN HEADER")
        else:
            token = request.cookies.get("access_token")
            if token:
                print("✔ TOKEN FOUND IN COOKIE")

        if not token:
            print("❌ NO TOKEN FOUND")

            if "text/html" in request.headers.get("accept", ""):
                print("➡ HTML Request → Redirecting to Login Page")
                print("********** [MIDDLEWARE EXIT - REDIRECT] **********\n")
                return RedirectResponse(f"{AUTH_LOGIN_URL}?redirect_url={request.url}")

            print("❌ Returning 401 Unauthorized")
            print("********** [MIDDLEWARE EXIT - 401] **********\n")
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        # ------------------------------------
        # INTROSPECT TOKEN
        # ------------------------------------
        print("\n********** [TOKEN INTROSPECTION STARTED] **********")
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
            print("📡 Auth Response:", data)

        except Exception:
            print("❌ AUTH SERVICE UNREACHABLE")
            print("********** [MIDDLEWARE EXIT - 503] **********\n")
            return JSONResponse({"detail": "Auth service unreachable"}, status_code=503)

        if not data.get("active"):
            print("❌ SESSION EXPIRED / INVALID TOKEN")
            print("********** [MIDDLEWARE EXIT - EXPIRED] **********\n")
            return JSONResponse({"detail": "Session expired"}, status_code=401)

        print("✔ TOKEN VALID")
        print("********** [TOKEN INTROSPECTION COMPLETED] **********\n")

        # Store user
        request.state.user = data.get("user")
        print("👤 USER SET IN request.state")

        # ------------------------------------
        # ALWAYS COLLECT & REGISTER
        # ------------------------------------
        print("\n********** [START COLLECT + REGISTER] **********")
        collect_routes()
        asyncio.create_task(register_with_auth())
        print("********** [COLLECT + REGISTER TRIGGERED] **********\n")

        # ------------------------------------
        # CONTINUE REQUEST
        # ------------------------------------
        print("➡ Proceeding to actual endpoint handler")
        print("********** [MIDDLEWARE EXIT - SUCCESS] **********\n")
        return await call_next(request)
