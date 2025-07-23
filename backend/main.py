import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.openapi.utils import get_openapi

from database import engine, Base
from routers import users, properties, showings # Add other routers as needed

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate Platform", version="1.0.0", openapi_url="/openapi.json", docs_url="/docs")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Router Registration
app.include_router(users.router)
app.include_router(properties.router)
app.include_router(showings.router) # Add other routers as needed

# Health Check
@app.get('/health')
def health_check():
    return {"status": "OK"}

# Custom Exception Handler
@app.exception_handler(Exception)
def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={'message': f'Internal Server Error: {exc}'})

# Static File Serving
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        if file_path.startswith("api/") or file_path.startswith("static/") or file_path == "openapi.json" or file_path == "docs":
            return None  # Let API routes and static files handle it
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")  # SPA routing

# OpenAPI Customization (Optional)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Real Estate Platform",
        version="1.0.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
