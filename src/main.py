"""main file."""

import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.common.constants import CommonPaths
from src.core.configs import Settings
from src.core.infisical_client import InfisicalClient
from src.core.logging_manager import LoggingManager
from src.core.settings import InfisicalSettings
from src.services.routers.version import router as version_router

app = FastAPI()

# Include the version router
app.include_router(version_router, prefix="/api")


def load_infisical_secrets():
    """Load Infisical secrets."""
    logging.info("Setup Authentication...")
    infisical_settings = InfisicalSettings()
    path = "/"
    infisical_client = InfisicalClient.load_from_settings(infisical_settings)
    infisical_client.get_secrets(path)


def setup_logger():
    """Setup logger."""
    sys.path.append(str(CommonPaths.project_root))
    LoggingManager.setup_logger()


def start_application(settings: Settings):
    """Start application."""
    logging.info("Starting application...")
    uvicorn.run(
        app, host=settings.host, port=settings.port, log_config=None
    )  # log_config=None enable own custom logs for this lib


def main():
    """Main method represents entry point for start application.

    :return:
    """
    os.makedirs(CommonPaths.log_path, exist_ok=True)
    load_dotenv()
    settings = Settings()

    setup_logger()
    load_infisical_secrets()
    start_application(settings)


if __name__ == "__main__":
    main()
