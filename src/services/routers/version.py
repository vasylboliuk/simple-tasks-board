"""version endpoint file."""

import logging

from fastapi import APIRouter

from src.core.__version__ import VERSION
from src.models.version import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse)
async def get_version():
    """Returns the current version of the API."""
    logging.info("GET /version")
    return VersionResponse(version=VERSION)
