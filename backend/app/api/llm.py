from fastapi import APIRouter

from app.core.config import settings
from app.schemas.llm import LLMRequest, LLMResponse
from app.services.llm_service import LLMService

router = APIRouter()

llm_service = LLMService()


@router.post("/test-llm", response_model=LLMResponse)
def test_llm(request: LLMRequest) -> LLMResponse:
    response = llm_service.generate_response(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        model=settings.MODEL_SPECIALIST,
    )

    return LLMResponse(response=response)