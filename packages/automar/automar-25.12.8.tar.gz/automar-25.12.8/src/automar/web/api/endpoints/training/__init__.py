"""Training-related endpoints."""

from fastapi import APIRouter

from . import crossval, train, tune

router = APIRouter()
router.include_router(tune.router)
router.include_router(train.router)
router.include_router(crossval.router)

__all__ = ["router"]
