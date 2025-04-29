"""main file."""

import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.common.config.settings import InfisicalSettings
from src.core.configs import Settings
from src.core.constants import CommonPaths
from src.core.logging_manager import LoggingManager
from src.services.routers.version import router as version_router

app = FastAPI()

# Include the version router
app.include_router(version_router, prefix="/api")


def main():
    """Main method represents entry point for start application.

    :return:
    """
    os.makedirs(CommonPaths.log_path, exist_ok=True)
    load_dotenv()
    settings = Settings()
    sys.path.append(str(CommonPaths.project_root))
    LoggingManager.setup_logger()

    logging.info("Setup Authentication...")
    infisical_settings = InfisicalSettings()
    infisical_settings.load_infisical_secrets()

    logging.info("Starting application...")
    uvicorn.run(
        app, host=settings.host, port=settings.port, log_config=None
    )  # log_config=None enable own custom logs for this lib


if __name__ == "__main__":
    main()
