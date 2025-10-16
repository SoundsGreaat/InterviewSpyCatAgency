from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cats, missions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Cat Agency API",
    description="Management system for Spy Cat Agency - manage spy cats, missions, and targets",
    version="1.0.0",
)

app.include_router(cats.router)
app.include_router(missions.router)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Welcome to Spy Cat Agency API",
        "status": "operational"
    }
