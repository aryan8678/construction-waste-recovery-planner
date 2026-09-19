from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.session import Base, engine
from app.database.seed_data import seed_database
from app.routes.assessments import router as assessments_router
from app.routes.rules import router as rules_router
from app.routes.materials import router as materials_router
from app.routes.statistics import router as statistics_router
from app.routes.health import router as health_router
from app.routes.ml_status import router as ml_status_router

# Ensure tables and seed data exist at import time
Base.metadata.create_all(bind=engine)
seed_database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(
    title="Construction Waste Recovery Planner API",
    description="A Machine Learning Decision Support System for Sustainable Material Recovery and Circular Economy",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(assessments_router)
app.include_router(ml_status_router)
app.include_router(rules_router)
app.include_router(materials_router)
app.include_router(statistics_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Construction Waste Recovery Planner API",
        "docs": "/docs",
        "status": "online",
        "engine": "Machine Learning Model (with Civil Engineering Safety Constraints)"
    }
