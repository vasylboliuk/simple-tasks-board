"""Infisical client file."""

from functools import cached_property

from infisical_sdk import BaseSecret, InfisicalSDKClient, ListSecretsResponse

from src.core.settings import InfisicalSettings


class InfisicalClient:
    """Infisical client class wrapper used for managing configuration and secrets."""

    _client = None

    def __init__(
        self, host: str, client_id: str, client_secret: str, project_id: str, environment_slug: str, cache_ttl=300
    ):
        """InfisicalClient class constructor."""
        self.host = host
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_id = project_id
        self.environment_slug = environment_slug
        self.cache_ttl = cache_ttl

    @classmethod
    def load_from_settings(cls, settings: InfisicalSettings):
        """Load setting from InfisicalSettings class."""
        return cls(
            host=settings.host,
            client_id=settings.client_id.get_secret_value(),
            client_secret=settings.client_secret.get_secret_value(),
            project_id=settings.project_id,
            environment_slug=settings.environment_slug,
        )

    @cached_property
    def client(self) -> InfisicalSDKClient:
        """Get an Infisical SDK client instance."""
        if self._client:
            return self._client
        _client = InfisicalSDKClient(host=self.host, cache_ttl=self.cache_ttl)
        _client.auth.universal_auth.login(
            client_id=self.client_id,
            client_secret=self.client_secret,
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
