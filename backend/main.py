import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .routers import clients, properties, showings # Add other routers as needed
from .exceptions import ApiException

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Replace with your allowed origins in production
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routers
app.include_router(clients.router)
app.include_router(properties.router)
app.include_router(showings.router) # Add other routers here

# Health Check
@app.get('/health')
def health_check():
    return {"status": "ok"}

# Static Files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{{"file_path:path}}")
    async def serve_frontend(file_path: str, request: Request):
        if file_path.startswith("api"):
            return None  # Let API routes handle it
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")

# Exception Handling
@app.exception_handler(ApiException)
def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    import logging
    logging.exception(exc)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
