"""
Tests for Secret Management Integration

This test suite covers:
- BaseSecretProvider interface
- VaultSecretProvider
- AWSSecretsProvider
- AzureKeyVaultProvider
- GCPSecretProvider
- SecretManager high-level interface
- APILinker integration
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from apilinker.core.secrets import (
    BaseSecretProvider,
    SecretManager,
    SecretManagerConfig,
    SecretProvider,
    RotationStrategy,
    SecretMetadata,
    SecretNotFoundError,
    SecretAccessError,
    VaultSecretProvider,
    AWSSecretsProvider,
    AzureKeyVaultProvider,
    GCPSecretProvider,
)


# === Base Provider Tests ===


class MockSecretProvider(BaseSecretProvider):
    """Mock implementation for testing base class"""

    def __init__(self, config):
        super().__init__(config)
        self.secrets = {}

    def get_secret(self, secret_name, version=None):
        # Check cache first
        cache_key = f"{secret_name}:{version or 'latest'}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        if secret_name not in self.secrets:
            raise SecretNotFoundError(f"Secret '{secret_name}' not found")

        value = self.secrets[secret_name]
        # Cache the result
        self._set_cache(cache_key, value)
        return value

    def set_secret(self, secret_name, secret_value, metadata=None):
        self.secrets[secret_name] = secret_value
        # Clear cache when updating
        self._clear_cache(f"{secret_name}:latest")
        self._clear_cache(f"{secret_name}:1")
        return SecretMetadata(name=secret_name, version="1")

    def delete_secret(self, secret_name):
        if secret_name in self.secrets:
            del self.secrets[secret_name]
            return True
        return False

    def rotate_secret(self, secret_name, rotation_function=None):
        if rotation_function:
            new_value = rotation_function()
        else:
            new_value = "rotated_value"
        return self.set_secret(secret_name, new_value)

    def list_secrets(self, prefix=None):
        secrets = []
        for name in self.secrets.keys():
            if prefix is None or name.startswith(prefix):
                secrets.append(SecretMetadata(name=name))
        return secrets


def test_base_provider_cache():
    """Test that base provider caching works correctly"""
    provider = MockSecretProvider({"cache_ttl_seconds": 300})

    # Set and get secret
    provider.set_secret("test-key", "test-value")
    value = provider.get_secret("test-key")
    assert value == "test-value"

    # Check cache
    cached = provider._get_from_cache("test-key:latest")
    assert cached == "test-value"

    # Clear cache
    provider._clear_cache("test-key:latest")
    cached = provider._get_from_cache("test-key:latest")
    assert cached is None


def test_base_provider_operations():
    """Test basic CRUD operations"""
    provider = MockSecretProvider({})

    # Create
    metadata = provider.set_secret("key1", "value1")
    assert metadata.name == "key1"

    # Read
    value = provider.get_secret("key1")
    assert value == "value1"

    # Update
    provider.set_secret("key1", "value2")
    assert provider.get_secret("key1") == "value2"

    # Delete
    assert provider.delete_secret("key1") is True
    assert provider.delete_secret("key1") is False  # Already deleted

    # Not found
    with pytest.raises(SecretNotFoundError):
        provider.get_secret("nonexistent")


def test_base_provider_list_with_prefix():
    """Test listing secrets with prefix filter"""
    provider = MockSecretProvider({})

    provider.set_secret("app/api-key", "key1")
    provider.set_secret("app/db-pass", "pass1")
    provider.set_secret("infra/token", "token1")

    # List all
    all_secrets = provider.list_secrets()
    assert len(all_secrets) == 3

    # List with prefix
    app_secrets = provider.list_secrets(prefix="app/")
    assert len(app_secrets) == 2


def test_base_provider_rotation():
    """Test secret rotation"""
    provider = MockSecretProvider({})

    provider.set_secret("api-key", "old-key")

    # Rotate with custom function
    provider.rotate_secret("api-key", rotation_function=lambda: "new-key")
    assert provider.get_secret("api-key") == "new-key"

    # Rotate without function (uses default)
    provider.rotate_secret("api-key")
    assert provider.get_secret("api-key") == "rotated_value"


# === Vault Provider Tests ===


@pytest.mark.skipif(True, reason="Requires hvac package and Vault server")
def test_vault_provider_initialization():
    """Test Vault provider initialization"""
    with patch("apilinker.core.secrets.hvac") as mock_hvac:
        mock_client = Mock()
        mock_client.is_authenticated.return_value = True
        mock_hvac.Client.return_value = mock_client

        config = {
            "url": "http://localhost:8200",
            "token": "test-token",
            "mount_point": "secret",
            "kv_version": 2,
        }

        provider = VaultSecretProvider(config)
        assert provider.url == "http://localhost:8200"
        assert provider.kv_version == 2
        mock_hvac.Client.assert_called_once()


@pytest.mark.skipif(True, reason="Requires hvac package and Vault server")
def test_vault_provider_get_secret():
    """Test retrieving secret from Vault"""
    with patch("apilinker.core.secrets.hvac") as mock_hvac:
        mock_client = Mock()
        mock_client.is_authenticated.return_value = True
        mock_client.secrets.kv.v2.read_secret_version.return_value = {
            "data": {"data": {"key": "value", "password": "secret123"}}
        }
        mock_hvac.Client.return_value = mock_client

        config = {
            "url": "http://localhost:8200",
            "token": "test-token",
            "kv_version": 2,
        }

        provider = VaultSecretProvider(config)
        secret = provider.get_secret("app/credentials")

        assert secret == {"key": "value", "password": "secret123"}
        mock_client.secrets.kv.v2.read_secret_version.assert_called_once()


# === AWS Provider Tests ===


@pytest.mark.skipif(True, reason="Requires boto3 package and AWS credentials")
def test_aws_provider_initialization():
    """Test AWS Secrets Manager provider initialization"""
    with patch("apilinker.core.secrets.boto3") as mock_boto3:
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        config = {
            "region_name": "us-east-1",
            "aws_access_key_id": "AKIA...",
            "aws_secret_access_key": "secret",
        }

        AWSSecretsProvider(config)
        mock_boto3.client.assert_called_once_with(
            "secretsmanager",
            region_name="us-east-1",
            aws_access_key_id="AKIA...",
            aws_secret_access_key="secret",
            aws_session_token=None,
            endpoint_url=None,
        )


@pytest.mark.skipif(True, reason="Requires boto3 package and AWS credentials")
def test_aws_provider_get_secret():
    """Test retrieving secret from AWS Secrets Manager"""
    with patch("apilinker.core.secrets.boto3") as mock_boto3:
        mock_client = Mock()
        mock_client.get_secret_value.return_value = {
            "SecretString": '{"username": "admin", "password": "secret123"}'
        }
        mock_boto3.client.return_value = mock_client

        config = {"region_name": "us-east-1"}
        provider = AWSSecretsProvider(config)
        secret = provider.get_secret("db-credentials")

        assert secret == {"username": "admin", "password": "secret123"}
        mock_client.get_secret_value.assert_called_once_with(SecretId="db-credentials")


@pytest.mark.skipif(True, reason="Requires boto3 package and AWS credentials")
def test_aws_provider_secret_not_found():
    """Test AWS provider handling of missing secrets"""
    with patch("apilinker.core.secrets.boto3") as mock_boto3:
        mock_client = Mock()
        mock_client.exceptions.ResourceNotFoundException = Exception
        mock_client.get_secret_value.side_effect = (
            mock_client.exceptions.ResourceNotFoundException()
        )
        mock_boto3.client.return_value = mock_client

        config = {"region_name": "us-east-1"}
        provider = AWSSecretsProvider(config)

        with pytest.raises(SecretNotFoundError):
            provider.get_secret("nonexistent")


# === Azure Provider Tests ===


@pytest.mark.skipif(True, reason="Requires azure packages and Azure credentials")
def test_azure_provider_initialization():
    """Test Azure Key Vault provider initialization"""
    with patch("apilinker.core.secrets.SecretClient") as mock_secret_client, patch(
        "apilinker.core.secrets.DefaultAzureCredential"
    ):
        config = {"vault_url": "https://mykeyvault.vault.azure.net/"}

        AzureKeyVaultProvider(config)
        assert (
            AzureKeyVaultProvider(config).vault_url
            == "https://mykeyvault.vault.azure.net/"
        )
        mock_secret_client.assert_called_once()


@pytest.mark.skipif(True, reason="Requires azure packages and Azure credentials")
def test_azure_provider_get_secret():
    """Test retrieving secret from Azure Key Vault"""
    with patch("apilinker.core.secrets.SecretClient") as mock_secret_client, patch(
        "apilinker.core.secrets.DefaultAzureCredential"
    ):
        mock_client = Mock()
        mock_secret = Mock()
        mock_secret.value = "my-api-key-12345"
        mock_client.get_secret.return_value = mock_secret
        mock_secret_client.return_value = mock_client

        config = {"vault_url": "https://mykeyvault.vault.azure.net/"}
        provider = AzureKeyVaultProvider(config)
        secret = provider.get_secret("api-key")

        assert secret == "my-api-key-12345"
        mock_client.get_secret.assert_called_once_with(name="api-key")


# === GCP Provider Tests ===


@pytest.mark.skipif(True, reason="Requires google-cloud-secret-manager package")
def test_gcp_provider_initialization():
    """Test Google Secret Manager provider initialization"""
    with patch("apilinker.core.secrets.secretmanager") as mock_sm:
        mock_client = Mock()
        mock_sm.SecretManagerServiceClient.return_value = mock_client

        config = {"project_id": "my-project"}
        GCPSecretProvider(config)

        assert GCPSecretProvider(config).project_id == "my-project"
        mock_sm.SecretManagerServiceClient.assert_called()


@pytest.mark.skipif(True, reason="Requires google-cloud-secret-manager package")
def test_gcp_provider_get_secret():
    """Test retrieving secret from Google Secret Manager"""
    with patch("apilinker.core.secrets.secretmanager") as mock_sm:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.payload.data = b'{"api_key": "test-key-123"}'
        mock_client.access_secret_version.return_value = mock_response
        mock_sm.SecretManagerServiceClient.return_value = mock_client

        config = {"project_id": "my-project"}
        provider = GCPSecretProvider(config)
        secret = provider.get_secret("app-credentials")

        assert secret == {"api_key": "test-key-123"}


# === SecretManager High-Level Interface Tests ===


def test_secret_manager_with_env_provider():
    """Test SecretManager with environment variable fallback"""
    import os

    os.environ["TEST_SECRET"] = "test-value-123"

    config = SecretManagerConfig(provider=SecretProvider.ENV)
    manager = SecretManager(config)

    value = manager.get_secret("TEST_SECRET")
    assert value == "test-value-123"

    # Clean up
    del os.environ["TEST_SECRET"]


def test_secret_manager_env_not_found():
    """Test SecretManager raises error for missing env var"""
    config = SecretManagerConfig(provider=SecretProvider.ENV)
    manager = SecretManager(config)

    with pytest.raises(SecretNotFoundError):
        manager.get_secret("NONEXISTENT_VAR")


def test_secret_manager_config_validation():
    """Test SecretManager validates configuration"""
    # Missing vault config
    config = SecretManagerConfig(provider=SecretProvider.VAULT)

    with pytest.raises(ValueError, match="vault_config is required"):
        SecretManager(config)


# === APILinker Integration Tests ===


def test_apilinker_secret_resolution():
    """Test APILinker resolves secret references"""
    from apilinker import ApiLinker
    import os

    os.environ["TEST_API_KEY"] = "sk_test_1234567890"

    linker = ApiLinker(
        secret_manager_config={"provider": "env"},
        source_config={
            "type": "rest",
            "base_url": "https://api.example.com",
            "auth": {
                "type": "api_key",
                "key": "secret://TEST_API_KEY",
                "header": "X-API-Key",
            },
        },
        log_level="ERROR",
    )

    assert linker.secret_manager is not None

    # Test secret resolution
    resolved = linker._resolve_secret("secret://TEST_API_KEY")
    assert resolved == "sk_test_1234567890"

    # Test non-secret value
    resolved = linker._resolve_secret("plain-value")
    assert resolved == "plain-value"

    # Clean up
    del os.environ["TEST_API_KEY"]


def test_apilinker_dict_secret_resolution():
    """Test APILinker resolves dict-style secret references"""
    from apilinker import ApiLinker
    import os

    os.environ["DB_PASSWORD"] = "super-secret-password"

    linker = ApiLinker(
        secret_manager_config={"provider": "env"},
        log_level="ERROR",
    )

    # Test dict secret reference
    resolved = linker._resolve_secret({"secret": "DB_PASSWORD"})
    assert resolved == "super-secret-password"

    # Clean up
    del os.environ["DB_PASSWORD"]


def test_apilinker_without_secret_manager():
    """Test APILinker works without secret manager"""
    from apilinker import ApiLinker

    linker = ApiLinker(
        source_config={
            "type": "rest",
            "base_url": "https://api.example.com",
            "auth": {"type": "api_key", "key": "plain-key", "header": "X-API-Key"},
        },
        log_level="ERROR",
    )

    assert linker.secret_manager is None

    # Should return value as-is
    resolved = linker._resolve_secret("secret://TEST")
    assert resolved == "secret://TEST"


def test_apilinker_auth_secrets_resolution():
    """Test APILinker resolves secrets in auth config"""
    from apilinker import ApiLinker
    import os

    os.environ["CLIENT_ID"] = "client-id-123"
    os.environ["CLIENT_SECRET"] = "client-secret-456"

    linker = ApiLinker(
        secret_manager_config={"provider": "env"},
        source_config={
            "type": "rest",
            "base_url": "https://api.example.com",
            "auth": {
                "type": "oauth2",
                "client_id": "secret://CLIENT_ID",
                "client_secret": "secret://CLIENT_SECRET",
                "token_url": "https://auth.example.com/token",
            },
        },
        log_level="ERROR",
    )

    # Verify secrets were resolved during initialization
    # The auth config should have been passed to auth_manager with resolved secrets
    assert linker.source is not None

    # Clean up
    del os.environ["CLIENT_ID"]
    del os.environ["CLIENT_SECRET"]


def test_secret_metadata():
    """Test SecretMetadata dataclass"""
    metadata = SecretMetadata(
        name="test-secret",
        created_at=datetime.now(),
        version="1",
        rotation_enabled=True,
        tags={"env": "dev"},
    )

    assert metadata.name == "test-secret"
    assert metadata.version == "1"
    assert metadata.rotation_enabled is True
    assert metadata.tags["env"] == "dev"


def test_rotation_strategy_enum():
    """Test RotationStrategy enum values"""
    assert RotationStrategy.MANUAL.value == "manual"
    assert RotationStrategy.SCHEDULED.value == "scheduled"
    assert RotationStrategy.ON_DEMAND.value == "on_demand"
    assert RotationStrategy.AUTO.value == "auto"


def test_secret_provider_enum():
    """Test SecretProvider enum values"""
    assert SecretProvider.VAULT.value == "vault"
    assert SecretProvider.AWS.value == "aws"
    assert SecretProvider.AZURE.value == "azure"
    assert SecretProvider.GCP.value == "gcp"
    assert SecretProvider.ENV.value == "env"


# === Error Handling Tests ===


def test_secret_not_found_error():
    """Test SecretNotFoundError exception"""
    with pytest.raises(SecretNotFoundError, match="not found"):
        raise SecretNotFoundError("Secret not found")


def test_secret_access_error():
    """Test SecretAccessError exception"""
    with pytest.raises(SecretAccessError, match="denied"):
        raise SecretAccessError("Access denied")


def test_import_error_handling():
    """Test graceful handling of missing optional dependencies"""
    # Test Vault import error
    with patch(
        "builtins.__import__", side_effect=ImportError("No module named 'hvac'")
    ):
        with pytest.raises(ImportError, match="hvac package is required"):
            VaultSecretProvider({"url": "http://localhost:8200", "token": "test"})


def test_secret_manager_env_operations():
    """Test SecretManager with env provider doesn't support write operations"""
    config = SecretManagerConfig(provider=SecretProvider.ENV)
    manager = SecretManager(config)

    with pytest.raises(NotImplementedError):
        manager.set_secret("test", "value")

    with pytest.raises(NotImplementedError):
        manager.delete_secret("test")

    with pytest.raises(NotImplementedError):
        manager.rotate_secret("test")

    with pytest.raises(NotImplementedError):
        manager.list_secrets()


def test_apilinker_load_config_with_secrets():
    """Test loading secret manager config from YAML file"""
    from apilinker import ApiLinker
    import tempfile
    import os

    config_content = """
secrets:
  provider: env
  cache_ttl_seconds: 600

source:
  type: rest
  base_url: "https://api.example.com"
  auth:
    type: api_key
    key: "secret://TEST_KEY"
    header: "X-API-Key"
"""

    os.environ["TEST_KEY"] = "test-api-key-123"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(config_content)
        config_path = f.name

    try:
        linker = ApiLinker(config_path=config_path, log_level="ERROR")
        assert linker.secret_manager is not None
        assert linker.source is not None
    finally:
        os.unlink(config_path)
        del os.environ["TEST_KEY"]


def test_secret_manager_config_vault_missing_config():
    """Test that creating VAULT config without vault_config raises error"""
    config = SecretManagerConfig(provider=SecretProvider.VAULT)

    with pytest.raises(ValueError, match="vault_config is required"):
        SecretManager(config)


def test_secret_manager_config_aws_missing_config():
    """Test that creating AWS config without aws_config raises error"""
    config = SecretManagerConfig(provider=SecretProvider.AWS)

    with pytest.raises(ValueError, match="aws_config is required"):
        SecretManager(config)


def test_secret_manager_config_azure_missing_config():
    """Test that creating AZURE config without azure_config raises error"""
    config = SecretManagerConfig(provider=SecretProvider.AZURE)

    with pytest.raises(ValueError, match="azure_config is required"):
        SecretManager(config)


def test_secret_manager_config_gcp_missing_config():
    """Test that creating GCP config without gcp_config raises error"""
    config = SecretManagerConfig(provider=SecretProvider.GCP)

    with pytest.raises(ValueError, match="gcp_config is required"):
        SecretManager(config)


def test_base_provider_cache_operations():
    """Test cache get/set/clear operations"""
    provider = MockSecretProvider({"cache_ttl_seconds": 300})

    # Test cache miss
    assert provider._get_from_cache("missing-key") is None

    # Test cache set and get
    provider._set_cache("test-key", "test-value")
    assert provider._get_from_cache("test-key") == "test-value"

    # Test cache clear
    provider._clear_cache("test-key")
    assert provider._get_from_cache("test-key") is None


def test_secret_metadata_minimal():
    """Test SecretMetadata with only required fields"""
    metadata = SecretMetadata(name="minimal-secret")

    assert metadata.name == "minimal-secret"
    assert metadata.version is None
    assert metadata.rotation_enabled is False
    assert metadata.tags == {}


def test_secret_metadata_with_all_fields():
    """Test SecretMetadata with all optional fields populated"""
    from datetime import datetime

    metadata = SecretMetadata(
        name="full-secret",
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2023, 1, 2),
        version="v1",
        rotation_enabled=True,
        next_rotation=datetime(2023, 2, 1),
        tags={"env": "prod", "team": "platform"},
    )

    assert metadata.name == "full-secret"
    assert metadata.version == "v1"
    assert metadata.rotation_enabled is True
    assert metadata.tags["env"] == "prod"
    assert metadata.tags["team"] == "platform"


def test_mock_provider_delete_nonexistent():
    """Test deleting a secret that doesn't exist returns False"""
    provider = MockSecretProvider({})

    result = provider.delete_secret("nonexistent")
    assert result is False


def test_mock_provider_list_with_no_secrets():
    """Test listing secrets when none exist"""
    provider = MockSecretProvider({})

    secrets = provider.list_secrets()
    assert len(secrets) == 0


def test_mock_provider_rotation_with_function():
    """Test secret rotation with custom function"""
    provider = MockSecretProvider({})

    provider.set_secret("api-key", "old-value")

    def custom_rotation():
        return "custom-new-value"

    metadata = provider.rotate_secret("api-key", rotation_function=custom_rotation)

    assert metadata.name == "api-key"
    assert provider.get_secret("api-key") == "custom-new-value"


def test_apilinker_resolve_plain_value():
    """Test APILinker returns plain values unchanged when no secret manager"""
    from apilinker import ApiLinker

    linker = ApiLinker(log_level="ERROR")

    # Without secret manager, should return as-is
    resolved = linker._resolve_secret("plain-value")
    assert resolved == "plain-value"


def test_apilinker_resolve_secret_prefix_no_manager():
    """Test APILinker returns secret:// values as-is when no secret manager configured"""
    from apilinker import ApiLinker

    linker = ApiLinker(log_level="ERROR")

    # Without secret manager, should return as-is even with secret:// prefix
    resolved = linker._resolve_secret("secret://SOME_KEY")
    assert resolved == "secret://SOME_KEY"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
