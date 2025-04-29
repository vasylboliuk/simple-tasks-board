"""File stores Settings."""

from enum import StrEnum
from functools import cached_property
from typing import List, Optional

from infisical_sdk import BaseSecret, InfisicalSDKClient, ListSecretsResponse
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


class InfisicalSettings(BaseSettings):
    """Infisical settings used for managing configuration and secrets."""

    model_config = SettingsConfigDict(env_prefix="INFISICAL_", env_file=".env")

    host: str
    environment_slug: str
    client_id: SecretStr = Field(exclude=True, repr=False)
    client_secret: SecretStr = Field(exclude=True, repr=False)
    project_id: str
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 30

    _client: InfisicalSDKClient = None

    @cached_property
    def client(self) -> InfisicalSDKClient:
        """Get an Infisical SDK client instance."""
        if self._client:
            return self._client
        _client = InfisicalSDKClient(host=self.host)
        _client.auth.universal_auth.login(
            client_id=self.client_id.get_secret_value(),
            client_secret=self.client_secret.get_secret_value(),
        )
        self._client = _client
        return _client

    def get_secrets(self, secret_path: str) -> ListSecretsResponse:
        """Get a list of secrets from Infisical.

        :param secret_path: path to secret store
        :return: List of secrets in format: ListSecretsResponse
        """
        secrets_val: ListSecretsResponse = self.client.secrets.list_secrets(
            project_id=self.project_id,
            environment_slug=self.environment_slug,
            secret_path=secret_path,
        )
        return secrets_val

    def get_secret(self, secret_path: str, secret_name: str) -> BaseSecret:
        """Get secret from Infisical.

        :param secret_path: path to secret store
        :param secret_name: name of secret
        :return: BaseSecret
        """
        secret_val: BaseSecret = self.client.secrets.get_secret_by_name(
            project_id=self.project_id,
            environment_slug=self.environment_slug,
            secret_path=secret_path,
            secret_name=secret_name,
        )
        return secret_val

    def load_infisical_secrets(self) -> list[BaseSecret]:
        """Load infisical secrets."""
        # Initialize the client
        client = InfisicalSDKClient(
            host=self.host,
            cache_ttl=300,  # `None` to disable caching
        )
        client.auth.universal_auth.login(
            client_id=self.client_id.get_secret_value(), client_secret=self.client_secret.get_secret_value()
        )
        # Use the SDK to interact with Infisical
        path = "/"
        secrets = client.secrets.list_secrets(
            project_id=self.project_id, environment_slug=self.environment_slug, secret_path=path
        )
        secrets_res: List = secrets.secrets
        return secrets_res
