"""File stores Settings."""

from enum import StrEnum
from typing import List, Optional

from infisical_sdk import BaseSecret, InfisicalSDKClient
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class EnvType(StrEnum):
    """Environment type where application is deployed."""

    LOCAL = "local"
    DEV = "development"


class EnvTarget(StrEnum):
    """Environment deployment type target."""

    LOCAL = "local"


class EnvSettings(BaseModel):
    """Environment details like deployment target and environment type."""

    type: EnvType
    target: EnvTarget


class DatabaseSettings(BaseSettings):
    """Database connection settings and variables."""

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env")
    host: str
    port: int
    database_name: str
    user: SecretStr = Field(exclude=True, repr=False)
    password: SecretStr | None = Field(
        default=None,
        exclude=True,
        repr=False,
        description="Database password may be empty in case if IAM role authentication is used on the environment",
    )
    driver: str
    debug: Optional[bool] = Field(default=False)

    def get_url(self, password: SecretStr | None = None) -> URL:
        """Get sqlalchemy URL."""
        password = password or self.password
        url = URL.create(
            drivername=self.driver,
            username=self.user.get_secret_value(),
            password=password.get_secret_value() if isinstance(password, SecretStr) else password,
            host=self.host,
            port=self.port,
            database=self.database_name,
        )
        return url


class AuthSettings(BaseSettings):
    """Authentication settings."""

    model_config = SettingsConfigDict(env_prefix="INFISICAL_", env_file=".env")
    host: str
    environment_slug: str
    token: SecretStr = Field(exclude=True, repr=False)
    project_id: str
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 30

    def load_infisical_secrets(self) -> list[BaseSecret]:
        """Load infisical secrets."""
        # Initialize the client
        client = InfisicalSDKClient(
            host=self.host,
            token=self.token.get_secret_value(),
            cache_ttl=300,  # `None` to disable caching
        )
        # Use the SDK to interact with Infisical
        path = "/"
        secrets = client.secrets.list_secrets(
            project_id=self.project_id, environment_slug=self.environment_slug, secret_path=path
        )
        secrets_res: List = secrets.secrets
        return secrets_res
