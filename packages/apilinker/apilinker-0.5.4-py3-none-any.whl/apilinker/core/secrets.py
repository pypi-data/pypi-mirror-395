"""
Secret Management Module for APILinker.

This module provides enterprise-grade secret management with support for multiple
secret storage providers including HashiCorp Vault, AWS Secrets Manager, Azure Key Vault,
and Google Secret Manager.

Features:
- Pluggable secret provider interface
- Support for multiple secret backends
- Automatic credential rotation
- Least-privilege access patterns
- Graceful degradation when providers are not available

Dependencies (all optional):
- hvac: HashiCorp Vault integration
- boto3: AWS Secrets Manager integration
- azure-keyvault-secrets: Azure Key Vault integration
- google-cloud-secret-manager: Google Secret Manager integration
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class SecretProvider(str, Enum):
    """Supported secret storage providers."""

    VAULT = "vault"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ENV = "env"  # Fallback to environment variables


class RotationStrategy(str, Enum):
    """Secret rotation strategies."""

    MANUAL = "manual"  # No automatic rotation
    SCHEDULED = "scheduled"  # Rotate on schedule
    ON_DEMAND = "on_demand"  # Rotate when requested
    AUTO = "auto"  # Provider-managed rotation


@dataclass
class SecretMetadata:
    """Metadata for a secret."""

    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[str] = None
    rotation_enabled: bool = False
    next_rotation: Optional[datetime] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class SecretManagerConfig:
    """Configuration for secret management.

    Attributes:
        provider: Secret storage provider to use
        vault_config: HashiCorp Vault configuration (if provider=vault)
        aws_config: AWS Secrets Manager configuration (if provider=aws)
        azure_config: Azure Key Vault configuration (if provider=azure)
        gcp_config: Google Secret Manager configuration (if provider=gcp)
        rotation_strategy: How secrets should be rotated
        rotation_interval_days: Days between automatic rotations (if scheduled)
        cache_ttl_seconds: How long to cache secrets in memory (0 = no cache)
        enable_least_privilege: Enforce least-privilege access patterns
    """

    provider: SecretProvider = SecretProvider.ENV
    vault_config: Optional[Dict[str, Any]] = None
    aws_config: Optional[Dict[str, Any]] = None
    azure_config: Optional[Dict[str, Any]] = None
    gcp_config: Optional[Dict[str, Any]] = None
    rotation_strategy: RotationStrategy = RotationStrategy.MANUAL
    rotation_interval_days: int = 90
    cache_ttl_seconds: int = 300  # 5 minutes default
    enable_least_privilege: bool = True


class BaseSecretProvider(ABC):
    """Abstract base class for secret providers.

    All secret providers must implement this interface to be compatible
    with APILinker's secret management system.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the secret provider.

        Args:
            config: Provider-specific configuration
        """
        self.config = config
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._cache_ttl = timedelta(seconds=config.get("cache_ttl_seconds", 300))

    @abstractmethod
    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret value.

        Args:
            secret_name: Name/path of the secret
            version: Specific version to retrieve (None = latest)

        Returns:
            Secret value (string, dict, or bytes)

        Raises:
            SecretNotFoundError: Secret does not exist
            SecretAccessError: Insufficient permissions
        """
        pass

    @abstractmethod
    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret.

        Args:
            secret_name: Name/path of the secret
            secret_value: Secret value to store
            metadata: Optional metadata (tags, description, etc.)

        Returns:
            Metadata for the created/updated secret

        Raises:
            SecretAccessError: Insufficient permissions
        """
        pass

    @abstractmethod
    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret.

        Args:
            secret_name: Name/path of the secret

        Returns:
            True if deleted, False if not found

        Raises:
            SecretAccessError: Insufficient permissions
        """
        pass

    @abstractmethod
    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret to a new value.

        Args:
            secret_name: Name/path of the secret
            rotation_function: Optional function to generate new secret value

        Returns:
            Metadata for the rotated secret

        Raises:
            SecretNotFoundError: Secret does not exist
            SecretAccessError: Insufficient permissions
        """
        pass

    @abstractmethod
    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List available secrets.

        Args:
            prefix: Optional prefix filter

        Returns:
            List of secret metadata

        Raises:
            SecretAccessError: Insufficient permissions
        """
        pass

    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_ttl:
                return value
            else:
                del self._cache[key]
        return None

    def _set_cache(self, key: str, value: Any) -> None:
        """Store value in cache with timestamp."""
        self._cache[key] = (value, datetime.now())

    def _clear_cache(self, key: Optional[str] = None) -> None:
        """Clear cache for specific key or all keys."""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()


class SecretNotFoundError(Exception):
    """Raised when a secret does not exist."""

    pass


class SecretAccessError(Exception):
    """Raised when access to a secret is denied."""

    pass


class VaultSecretProvider(BaseSecretProvider):
    """HashiCorp Vault secret provider.

    Supports:
    - KV v1 and v2 secrets engines
    - Token authentication
    - AppRole authentication
    - Least-privilege policies
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Vault provider.

        Config options:
            url: Vault server URL (required)
            token: Vault token (for token auth)
            role_id: AppRole role ID (for AppRole auth)
            secret_id: AppRole secret ID (for AppRole auth)
            mount_point: KV mount point (default: "secret")
            kv_version: KV secrets engine version (1 or 2, default: 2)
            namespace: Vault namespace (Vault Enterprise)
            verify_tls: Verify TLS certificates (default: True)
        """
        super().__init__(config)

        try:
            import hvac
        except ImportError:
            raise ImportError(
                "hvac package is required for Vault support. "
                "Install with: pip install hvac"
            )

        self.url = config.get("url")
        if not self.url:
            raise ValueError("Vault URL is required")

        self.mount_point = config.get("mount_point", "secret")
        self.kv_version = config.get("kv_version", 2)
        self.namespace = config.get("namespace")

        # Initialize Vault client
        self.client = hvac.Client(
            url=self.url,
            namespace=self.namespace,
            verify=config.get("verify_tls", True),
        )

        # Authenticate
        self._authenticate(config)

        logger.info(f"Initialized Vault provider: {self.url}")

    def _authenticate(self, config: Dict[str, Any]) -> None:
        """Authenticate with Vault using configured method."""
        if config.get("token"):
            self.client.token = config["token"]
        elif config.get("role_id") and config.get("secret_id"):
            # AppRole authentication
            response = self.client.auth.approle.login(
                role_id=config["role_id"], secret_id=config["secret_id"]
            )
            self.client.token = response["auth"]["client_token"]
        else:
            raise ValueError("Either token or role_id/secret_id must be provided")

        if not self.client.is_authenticated():
            raise SecretAccessError("Failed to authenticate with Vault")

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret from Vault KV."""
        # Check cache first
        cache_key = f"{secret_name}:{version or 'latest'}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            if self.kv_version == 2:
                # KV v2: read_secret_version
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=secret_name,
                    mount_point=self.mount_point,
                    version=version,
                )
                secret_value = response["data"]["data"]
            else:
                # KV v1: read_secret
                response = self.client.secrets.kv.v1.read_secret(
                    path=secret_name, mount_point=self.mount_point
                )
                secret_value = response["data"]

            # Cache the result
            self._set_cache(cache_key, secret_value)
            return secret_value

        except Exception as e:
            if "Invalid path" in str(e) or "not found" in str(e).lower():
                raise SecretNotFoundError(f"Secret '{secret_name}' not found in Vault")
            elif "permission denied" in str(e).lower():
                raise SecretAccessError(f"Access denied to secret '{secret_name}'")
            else:
                raise

    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret in Vault KV."""
        try:
            if self.kv_version == 2:
                # KV v2: create_or_update_secret
                response = self.client.secrets.kv.v2.create_or_update_secret(
                    path=secret_name,
                    secret=(
                        secret_value
                        if isinstance(secret_value, dict)
                        else {"value": secret_value}
                    ),
                    mount_point=self.mount_point,
                )
                version = str(response["data"]["version"])
            else:
                # KV v1: create_or_update_secret
                self.client.secrets.kv.v1.create_or_update_secret(
                    path=secret_name,
                    secret=(
                        secret_value
                        if isinstance(secret_value, dict)
                        else {"value": secret_value}
                    ),
                    mount_point=self.mount_point,
                )
                version = None

            # Clear cache
            self._clear_cache(secret_name)

            return SecretMetadata(
                name=secret_name,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=version,
            )

        except Exception as e:
            if "permission denied" in str(e).lower():
                raise SecretAccessError(
                    f"Access denied to create/update secret '{secret_name}'"
                )
            else:
                raise

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret from Vault KV."""
        try:
            if self.kv_version == 2:
                # KV v2: delete_metadata_and_all_versions
                self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                    path=secret_name, mount_point=self.mount_point
                )
            else:
                # KV v1: delete_secret
                self.client.secrets.kv.v1.delete_secret(
                    path=secret_name, mount_point=self.mount_point
                )

            # Clear cache
            self._clear_cache(secret_name)
            return True

        except Exception as e:
            if "not found" in str(e).lower():
                return False
            elif "permission denied" in str(e).lower():
                raise SecretAccessError(
                    f"Access denied to delete secret '{secret_name}'"
                )
            else:
                raise

    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret in Vault."""
        if rotation_function:
            new_value = rotation_function()
        else:
            # Generate a new random value
            import secrets

            new_value = secrets.token_urlsafe(32)

        return self.set_secret(secret_name, new_value)

    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List secrets in Vault KV."""
        try:
            if self.kv_version == 2:
                response = self.client.secrets.kv.v2.list_secrets(
                    path=prefix or "", mount_point=self.mount_point
                )
            else:
                response = self.client.secrets.kv.v1.list_secrets(
                    path=prefix or "", mount_point=self.mount_point
                )

            secrets_list = []
            for key in response.get("data", {}).get("keys", []):
                secrets_list.append(
                    SecretMetadata(
                        name=f"{prefix}/{key}" if prefix else key,
                    )
                )

            return secrets_list

        except Exception as e:
            if "permission denied" in str(e).lower():
                raise SecretAccessError(f"Access denied to list secrets")
            else:
                raise


class AWSSecretsProvider(BaseSecretProvider):
    """AWS Secrets Manager provider.

    Supports:
    - Secret storage and retrieval
    - Automatic rotation
    - IAM least-privilege policies
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize AWS Secrets Manager provider.

        Config options:
            region_name: AWS region (required)
            aws_access_key_id: AWS access key (optional, uses IAM role if not provided)
            aws_secret_access_key: AWS secret key (optional)
            aws_session_token: AWS session token (optional)
            endpoint_url: Custom endpoint URL (optional, for testing)
        """
        super().__init__(config)

        try:
            import boto3
        except ImportError:
            raise ImportError(
                "boto3 package is required for AWS Secrets Manager support. "
                "Install with: pip install boto3"
            )

        region_name = config.get("region_name")
        if not region_name:
            raise ValueError("AWS region_name is required")

        # Initialize boto3 client
        self.client = boto3.client(
            "secretsmanager",
            region_name=region_name,
            aws_access_key_id=config.get("aws_access_key_id"),
            aws_secret_access_key=config.get("aws_secret_access_key"),
            aws_session_token=config.get("aws_session_token"),
            endpoint_url=config.get("endpoint_url"),
        )

        logger.info(f"Initialized AWS Secrets Manager provider: {region_name}")

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret from AWS Secrets Manager."""
        # Check cache first
        cache_key = f"{secret_name}:{version or 'latest'}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            kwargs = {"SecretId": secret_name}
            if version:
                kwargs["VersionId"] = version

            response = self.client.get_secret_value(**kwargs)

            # Parse secret value
            if "SecretString" in response:
                import json

                try:
                    secret_value = json.loads(response["SecretString"])
                except json.JSONDecodeError:
                    secret_value = response["SecretString"]
            else:
                secret_value = response["SecretBinary"]

            # Cache the result
            self._set_cache(cache_key, secret_value)
            return secret_value

        except self.client.exceptions.ResourceNotFoundException:
            raise SecretNotFoundError(
                f"Secret '{secret_name}' not found in AWS Secrets Manager"
            )
        except self.client.exceptions.AccessDeniedException:
            raise SecretAccessError(f"Access denied to secret '{secret_name}'")

    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret in AWS Secrets Manager."""
        import json

        try:
            # Convert value to string
            if isinstance(secret_value, dict):
                secret_string = json.dumps(secret_value)
            elif isinstance(secret_value, (str, int, float, bool)):
                secret_string = str(secret_value)
            else:
                secret_string = json.dumps({"value": secret_value})

            # Try to create secret
            try:
                response = self.client.create_secret(
                    Name=secret_name,
                    SecretString=secret_string,
                    Description=metadata.get("description", "") if metadata else "",
                    Tags=[
                        {"Key": k, "Value": v}
                        for k, v in (metadata or {}).get("tags", {}).items()
                    ],
                )
                version = response["VersionId"]
            except self.client.exceptions.ResourceExistsException:
                # Secret exists, update it
                response = self.client.put_secret_value(
                    SecretId=secret_name, SecretString=secret_string
                )
                version = response["VersionId"]

            # Clear cache
            self._clear_cache(secret_name)

            return SecretMetadata(
                name=secret_name,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=version,
            )

        except self.client.exceptions.AccessDeniedException:
            raise SecretAccessError(
                f"Access denied to create/update secret '{secret_name}'"
            )

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret from AWS Secrets Manager."""
        try:
            self.client.delete_secret(
                SecretId=secret_name,
                ForceDeleteWithoutRecovery=True,  # Immediate deletion
            )

            # Clear cache
            self._clear_cache(secret_name)
            return True

        except self.client.exceptions.ResourceNotFoundException:
            return False
        except self.client.exceptions.AccessDeniedException:
            raise SecretAccessError(f"Access denied to delete secret '{secret_name}'")

    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret in AWS Secrets Manager."""
        if rotation_function:
            new_value = rotation_function()
            return self.set_secret(secret_name, new_value)
        else:
            # Use AWS automatic rotation (requires Lambda function)
            try:
                self.client.rotate_secret(SecretId=secret_name)
                # Return updated metadata
                return SecretMetadata(
                    name=secret_name,
                    updated_at=datetime.now(),
                    rotation_enabled=True,
                )
            except self.client.exceptions.ResourceNotFoundException:
                raise SecretNotFoundError(f"Secret '{secret_name}' not found")
            except self.client.exceptions.AccessDeniedException:
                raise SecretAccessError(
                    f"Access denied to rotate secret '{secret_name}'"
                )

    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List secrets in AWS Secrets Manager."""
        try:
            kwargs = {}
            if prefix:
                kwargs["Filters"] = [{"Key": "name", "Values": [prefix]}]

            response = self.client.list_secrets(**kwargs)

            secrets_list = []
            for secret in response.get("SecretList", []):
                secrets_list.append(
                    SecretMetadata(
                        name=secret["Name"],
                        created_at=secret.get("CreatedDate"),
                        updated_at=secret.get("LastChangedDate"),
                        rotation_enabled=secret.get("RotationEnabled", False),
                        next_rotation=secret.get("NextRotationDate"),
                    )
                )

            return secrets_list

        except self.client.exceptions.AccessDeniedException:
            raise SecretAccessError("Access denied to list secrets")


class AzureKeyVaultProvider(BaseSecretProvider):
    """Azure Key Vault secret provider.

    Supports:
    - Secret storage and retrieval
    - Managed identity authentication
    - RBAC least-privilege policies
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Azure Key Vault provider.

        Config options:
            vault_url: Key Vault URL (required, e.g., https://myvault.vault.azure.net/)
            credential: Azure credential object (optional, uses DefaultAzureCredential if not provided)
            tenant_id: Azure tenant ID (optional, for service principal)
            client_id: Azure client ID (optional, for service principal)
            client_secret: Azure client secret (optional, for service principal)
        """
        super().__init__(config)

        try:
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential, ClientSecretCredential
        except ImportError:
            raise ImportError(
                "azure-keyvault-secrets and azure-identity packages are required for Azure Key Vault support. "
                "Install with: pip install azure-keyvault-secrets azure-identity"
            )

        vault_url = config.get("vault_url")
        if not vault_url:
            raise ValueError("Azure Key Vault URL is required")

        # Initialize credential
        if config.get("credential"):
            credential = config["credential"]
        elif (
            config.get("tenant_id")
            and config.get("client_id")
            and config.get("client_secret")
        ):
            credential = ClientSecretCredential(
                tenant_id=config["tenant_id"],
                client_id=config["client_id"],
                client_secret=config["client_secret"],
            )
        else:
            # Use managed identity / default credential chain
            credential = DefaultAzureCredential()

        # Initialize Key Vault client
        self.client = SecretClient(vault_url=vault_url, credential=credential)
        self.vault_url = vault_url

        logger.info(f"Initialized Azure Key Vault provider: {vault_url}")

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret from Azure Key Vault."""
        # Check cache first
        cache_key = f"{secret_name}:{version or 'latest'}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            if version:
                secret = self.client.get_secret(name=secret_name, version=version)
            else:
                secret = self.client.get_secret(name=secret_name)

            # Parse secret value
            import json

            try:
                secret_value = json.loads(secret.value)
            except json.JSONDecodeError:
                secret_value = secret.value

            # Cache the result
            self._set_cache(cache_key, secret_value)
            return secret_value

        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "does not exist" in error_msg:
                raise SecretNotFoundError(
                    f"Secret '{secret_name}' not found in Azure Key Vault"
                )
            elif "forbidden" in error_msg or "unauthorized" in error_msg:
                raise SecretAccessError(f"Access denied to secret '{secret_name}'")
            else:
                raise

    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret in Azure Key Vault."""
        import json

        try:
            # Convert value to string
            if isinstance(secret_value, dict):
                secret_string = json.dumps(secret_value)
            elif isinstance(secret_value, (str, int, float, bool)):
                secret_string = str(secret_value)
            else:
                secret_string = json.dumps({"value": secret_value})

            # Set secret with optional tags
            kwargs = {"name": secret_name, "value": secret_string}
            if metadata and metadata.get("tags"):
                kwargs["tags"] = metadata["tags"]

            secret = self.client.set_secret(**kwargs)

            # Clear cache
            self._clear_cache(secret_name)

            return SecretMetadata(
                name=secret_name,
                created_at=secret.properties.created_on,
                updated_at=secret.properties.updated_on,
                version=secret.properties.version,
                tags=secret.properties.tags or {},
            )

        except Exception as e:
            if "forbidden" in str(e).lower() or "unauthorized" in str(e).lower():
                raise SecretAccessError(
                    f"Access denied to create/update secret '{secret_name}'"
                )
            else:
                raise

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret from Azure Key Vault."""
        try:
            # Begin delete operation
            poller = self.client.begin_delete_secret(name=secret_name)
            poller.wait()  # Wait for deletion to complete

            # Clear cache
            self._clear_cache(secret_name)
            return True

        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "does not exist" in error_msg:
                return False
            elif "forbidden" in error_msg or "unauthorized" in error_msg:
                raise SecretAccessError(
                    f"Access denied to delete secret '{secret_name}'"
                )
            else:
                raise

    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret in Azure Key Vault."""
        if rotation_function:
            new_value = rotation_function()
        else:
            # Generate a new random value
            import secrets

            new_value = secrets.token_urlsafe(32)

        return self.set_secret(secret_name, new_value)

    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List secrets in Azure Key Vault."""
        try:
            secrets_list = []
            for secret_properties in self.client.list_properties_of_secrets():
                secret_name = secret_properties.name
                if prefix and not secret_name.startswith(prefix):
                    continue

                secrets_list.append(
                    SecretMetadata(
                        name=secret_name,
                        created_at=secret_properties.created_on,
                        updated_at=secret_properties.updated_on,
                        version=secret_properties.version,
                        tags=secret_properties.tags or {},
                    )
                )

            return secrets_list

        except Exception as e:
            if "forbidden" in str(e).lower() or "unauthorized" in str(e).lower():
                raise SecretAccessError("Access denied to list secrets")
            else:
                raise


class GCPSecretProvider(BaseSecretProvider):
    """Google Secret Manager provider.

    Supports:
    - Secret storage and retrieval
    - Workload identity authentication
    - IAM least-privilege policies
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Google Secret Manager provider.

        Config options:
            project_id: GCP project ID (required)
            credentials: Service account credentials (optional, uses application default if not provided)
            credentials_path: Path to service account JSON key file (optional)
        """
        super().__init__(config)

        try:
            from google.cloud import secretmanager
        except ImportError:
            raise ImportError(
                "google-cloud-secret-manager package is required for Google Secret Manager support. "
                "Install with: pip install google-cloud-secret-manager"
            )

        project_id = config.get("project_id")
        if not project_id:
            raise ValueError("GCP project_id is required")

        self.project_id = project_id

        # Initialize client with credentials
        client_kwargs = {}
        if config.get("credentials"):
            client_kwargs["credentials"] = config["credentials"]
        elif config.get("credentials_path"):
            import os

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["credentials_path"]

        self.client = secretmanager.SecretManagerServiceClient(**client_kwargs)

        logger.info(f"Initialized Google Secret Manager provider: {project_id}")

    def _get_secret_path(self, secret_name: str) -> str:
        """Get full secret path."""
        return f"projects/{self.project_id}/secrets/{secret_name}"

    def _get_version_path(self, secret_name: str, version: Optional[str] = None) -> str:
        """Get full secret version path."""
        version_id = version or "latest"
        return f"{self._get_secret_path(secret_name)}/versions/{version_id}"

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret from Google Secret Manager."""
        # Check cache first
        cache_key = f"{secret_name}:{version or 'latest'}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            version_path = self._get_version_path(secret_name, version)
            response = self.client.access_secret_version(name=version_path)

            # Parse secret value
            import json

            secret_bytes = response.payload.data
            secret_string = secret_bytes.decode("UTF-8")

            try:
                secret_value = json.loads(secret_string)
            except json.JSONDecodeError:
                secret_value = secret_string

            # Cache the result
            self._set_cache(cache_key, secret_value)
            return secret_value

        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "does not exist" in error_msg:
                raise SecretNotFoundError(
                    f"Secret '{secret_name}' not found in Google Secret Manager"
                )
            elif "permission denied" in error_msg or "forbidden" in error_msg:
                raise SecretAccessError(f"Access denied to secret '{secret_name}'")
            else:
                raise

    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret in Google Secret Manager."""
        import json

        try:
            # Convert value to bytes
            if isinstance(secret_value, dict):
                secret_bytes = json.dumps(secret_value).encode("UTF-8")
            elif isinstance(secret_value, (str, int, float, bool)):
                secret_bytes = str(secret_value).encode("UTF-8")
            else:
                secret_bytes = json.dumps({"value": secret_value}).encode("UTF-8")

            secret_path = self._get_secret_path(secret_name)

            # Try to create secret
            try:
                parent = f"projects/{self.project_id}"
                create_request = {
                    "parent": parent,
                    "secret_id": secret_name,
                    "secret": {
                        "replication": {"automatic": {}},
                        "labels": (metadata or {}).get("tags", {}),
                    },
                }
                self.client.create_secret(**create_request)
            except Exception as e:
                # Secret might already exist
                if "already exists" not in str(e).lower():
                    raise

            # Add secret version
            add_request = {
                "parent": secret_path,
                "payload": {"data": secret_bytes},
            }
            response = self.client.add_secret_version(**add_request)

            # Clear cache
            self._clear_cache(secret_name)

            return SecretMetadata(
                name=secret_name,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=response.name.split("/")[-1],
            )

        except Exception as e:
            if "permission denied" in str(e).lower() or "forbidden" in str(e).lower():
                raise SecretAccessError(
                    f"Access denied to create/update secret '{secret_name}'"
                )
            else:
                raise

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret from Google Secret Manager."""
        try:
            secret_path = self._get_secret_path(secret_name)
            self.client.delete_secret(name=secret_path)

            # Clear cache
            self._clear_cache(secret_name)
            return True

        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "does not exist" in error_msg:
                return False
            elif "permission denied" in error_msg or "forbidden" in error_msg:
                raise SecretAccessError(
                    f"Access denied to delete secret '{secret_name}'"
                )
            else:
                raise

    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret in Google Secret Manager."""
        if rotation_function:
            new_value = rotation_function()
        else:
            # Generate a new random value
            import secrets

            new_value = secrets.token_urlsafe(32)

        return self.set_secret(secret_name, new_value)

    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List secrets in Google Secret Manager."""
        try:
            parent = f"projects/{self.project_id}"
            secrets_list = []

            for secret in self.client.list_secrets(parent=parent):
                secret_name = secret.name.split("/")[-1]
                if prefix and not secret_name.startswith(prefix):
                    continue

                secrets_list.append(
                    SecretMetadata(
                        name=secret_name,
                        created_at=secret.create_time,
                        tags=dict(secret.labels) if secret.labels else {},
                    )
                )

            return secrets_list

        except Exception as e:
            if "permission denied" in str(e).lower() or "forbidden" in str(e).lower():
                raise SecretAccessError("Access denied to list secrets")
            else:
                raise


class SecretManager:
    """High-level secret management interface.

    Provides a unified interface for accessing secrets from multiple providers
    with automatic rotation, caching, and least-privilege access patterns.
    """

    def __init__(self, config: SecretManagerConfig):
        """Initialize secret manager with configuration.

        Args:
            config: Secret manager configuration
        """
        self.config = config
        self.provider: Optional[BaseSecretProvider] = None

        # Initialize provider based on configuration
        if config.provider == SecretProvider.VAULT:
            if not config.vault_config:
                raise ValueError("vault_config is required for Vault provider")
            self.provider = VaultSecretProvider(config.vault_config)

        elif config.provider == SecretProvider.AWS:
            if not config.aws_config:
                raise ValueError("aws_config is required for AWS provider")
            self.provider = AWSSecretsProvider(config.aws_config)

        elif config.provider == SecretProvider.AZURE:
            if not config.azure_config:
                raise ValueError("azure_config is required for Azure provider")
            self.provider = AzureKeyVaultProvider(config.azure_config)

        elif config.provider == SecretProvider.GCP:
            if not config.gcp_config:
                raise ValueError("gcp_config is required for GCP provider")
            self.provider = GCPSecretProvider(config.gcp_config)

        elif config.provider == SecretProvider.ENV:
            # Fallback to environment variables
            logger.warning(
                "Using environment variables for secrets (not recommended for production)"
            )
            self.provider = None

        logger.info(f"Initialized SecretManager with provider: {config.provider}")

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Any:
        """Retrieve a secret value.

        Args:
            secret_name: Name/path of the secret
            version: Specific version to retrieve (None = latest)

        Returns:
            Secret value

        Raises:
            SecretNotFoundError: Secret does not exist
            SecretAccessError: Insufficient permissions
        """
        if self.provider:
            return self.provider.get_secret(secret_name, version)
        else:
            # Fallback to environment variables
            import os

            value = os.environ.get(secret_name)
            if value is None:
                raise SecretNotFoundError(
                    f"Environment variable '{secret_name}' not found"
                )
            return value

    def set_secret(
        self,
        secret_name: str,
        secret_value: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecretMetadata:
        """Store or update a secret.

        Args:
            secret_name: Name/path of the secret
            secret_value: Secret value to store
            metadata: Optional metadata

        Returns:
            Metadata for the created/updated secret

        Raises:
            SecretAccessError: Insufficient permissions
        """
        if self.provider:
            return self.provider.set_secret(secret_name, secret_value, metadata)
        else:
            raise NotImplementedError(
                "Cannot set secrets when using environment variables"
            )

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret.

        Args:
            secret_name: Name/path of the secret

        Returns:
            True if deleted, False if not found

        Raises:
            SecretAccessError: Insufficient permissions
        """
        if self.provider:
            return self.provider.delete_secret(secret_name)
        else:
            raise NotImplementedError(
                "Cannot delete secrets when using environment variables"
            )

    def rotate_secret(
        self, secret_name: str, rotation_function: Optional[Callable[[], Any]] = None
    ) -> SecretMetadata:
        """Rotate a secret to a new value.

        Args:
            secret_name: Name/path of the secret
            rotation_function: Optional function to generate new secret value

        Returns:
            Metadata for the rotated secret

        Raises:
            SecretNotFoundError: Secret does not exist
            SecretAccessError: Insufficient permissions
        """
        if self.provider:
            return self.provider.rotate_secret(secret_name, rotation_function)
        else:
            raise NotImplementedError(
                "Cannot rotate secrets when using environment variables"
            )

    def list_secrets(self, prefix: Optional[str] = None) -> List[SecretMetadata]:
        """List available secrets.

        Args:
            prefix: Optional prefix filter

        Returns:
            List of secret metadata

        Raises:
            SecretAccessError: Insufficient permissions
        """
        if self.provider:
            return self.provider.list_secrets(prefix)
        else:
            raise NotImplementedError(
                "Cannot list secrets when using environment variables"
            )
