from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.dashboard import router as dashboard_router
from routers.upload import router as upload_router


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="SmartRetail Automated Business Intelligence API",
    version="1.0.0",
    description="Backend API for automated ETL and analytics on retail sales data.",
    lifespan=app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(upload_router)
app.include_router(dashboard_router)
