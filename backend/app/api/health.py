from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "name": "VC Due Diligence API",
        "version": "1.0.0",
        "status": "running",
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
    }