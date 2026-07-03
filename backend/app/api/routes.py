from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.llm import router as llm_router

router = APIRouter()

router.include_router(health_router)
router.include_router(llm_router)