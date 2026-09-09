import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from fastapi.staticfiles import StaticFiles
from routers import locations
from routers import risk
from routers import reports
from routers import alerts
from routers import hospitals



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Landslide Early Warning System",
    description="AI-Based Landslide Risk Monitoring System for North Eastern Region",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(locations.router)
app.include_router(risk.router)
app.include_router(reports.router)
app.include_router(alerts.router)
app.include_router(hospitals.router)


@app.get("/")
def root():
    return {
        "message": "Landslide Risk Monitoring API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }