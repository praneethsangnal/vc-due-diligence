from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="VC Due Diligence API",
    description="Autonomous Multi-Agent Venture Capital Due Diligence Platform",
    version="1.0.0",
)

app.include_router(router)