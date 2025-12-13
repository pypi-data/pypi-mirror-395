# -*- coding: utf-8 -*-
"""Metadata endpoints for listing available options."""
from fastapi import APIRouter, HTTPException

from automar.shared.persistence.library import VALID_INDUSTRY, Periods, ValidFormats
from automar.shared.config.schemas import SCALERS_KEYS
from automar.web.api.preload import preload_torch, _torch_preloaded

router = APIRouter(tags=["metadata"])


@router.get("/industries")
async def list_industries():
    """Get list of valid industries"""
    return {"industries": list(VALID_INDUSTRY)}


@router.get("/periods")
async def list_periods():
    """Get list of valid time periods"""
    return {"periods": [p.value for p in Periods]}


@router.get("/formats")
async def list_formats():
    """Get list of valid output formats"""
    return {"formats": list(ValidFormats)}


@router.get("/models")
async def list_models():
    """Get list of available models"""
    return {"models": ["GRU", "transformer", "log-reg"]}


@router.get("/scalers")
async def list_scalers():
    """Get list of available scalers"""
    return {"scalers": SCALERS_KEYS}


@router.get("/devices")
async def list_devices():
    """Get list of available compute devices"""
    from automar.shared.services.device_utils import _available_device_types

    devices = _available_device_types()
    return {"devices": devices, "default": devices[0] if devices else "cpu"}


@router.post("/preload-torch")
async def trigger_torch_preload():
    """
    Trigger torch preloading in background when user navigates to ML tab.
    Runs in separate subprocess for zero blocking on other API requests.
    """
    if _torch_preloaded:
        return {"status": "already_loading"}

    preload_torch()
    return {"status": "preloading_torch"}
