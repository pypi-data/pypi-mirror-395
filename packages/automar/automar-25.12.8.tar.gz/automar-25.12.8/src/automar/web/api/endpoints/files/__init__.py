"""File management endpoints."""

from fastapi import APIRouter

from . import configs, datasets, models, pca

router = APIRouter()
router.include_router(datasets.router)
router.include_router(models.router)
router.include_router(configs.router)
router.include_router(pca.router)

__all__ = ["router"]
