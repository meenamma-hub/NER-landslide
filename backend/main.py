from fastapi import FastAPI

from database import engine, Base

from routers import locations
from routers import risk
from routers import reports


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Landslide Early Warning System",
    description="AI-Based Landslide Risk Monitoring System for North Eastern Region",
    version="1.0.0"
)


app.include_router(locations.router)
app.include_router(risk.router)
app.include_router(reports.router)


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