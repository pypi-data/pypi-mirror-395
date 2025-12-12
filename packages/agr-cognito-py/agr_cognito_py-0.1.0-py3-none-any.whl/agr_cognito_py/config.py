"""Configuration for Cognito authentication."""
import os
from typing import Optional, List


class CognitoConfig:
    """Cognito configuration settings for token validation.

    Attributes:
        region: AWS region (default: us-east-1)
        user_pool_id: Cognito User Pool ID
        client_id: Cognito Client ID
        allowed_client_ids: List of allowed client IDs for audience validation
        issuer: Token issuer URL
        jwks_url: JSON Web Key Set URL
    """

    def __init__(
        self,
        region: Optional[str] = None,
        user_pool_id: Optional[str] = None,
        client_id: Optional[str] = None,
        allowed_client_ids: Optional[List[str]] = None
    ):
        """Initialize Cognito configuration.

        Args:
            region: AWS region. Defaults to COGNITO_REGION env var or 'us-east-1'.
            user_pool_id: User Pool ID. Defaults to COGNITO_USER_POOL_ID env var.
            client_id: Client ID. Defaults to COGNITO_CLIENT_ID env var.
            allowed_client_ids: Additional allowed client IDs for multi-client setups.

        Raises:
            ValueError: If client_id is not set.
        """
        self.region = region or os.getenv("COGNITO_REGION", "us-east-1")
        self.user_pool_id = user_pool_id or os.getenv("COGNITO_USER_POOL_ID")
        self.client_id = client_id or os.getenv("COGNITO_CLIENT_ID")

        if not self.user_pool_id:
            raise ValueError(
                "COGNITO_USER_POOL_ID must be set in environment or passed to CognitoConfig"
            )
        if not self.client_id:
            raise ValueError(
                "COGNITO_CLIENT_ID must be set in environment or passed to CognitoConfig"
            )

        # Build list of allowed client IDs for audience validation
        # Supports multiple clients from the same user pool (e.g., UI + API clients)
        self.allowed_client_ids = self._build_allowed_client_ids(allowed_client_ids)

        self.issuer = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}"
        self.jwks_url = f"{self.issuer}/.well-known/jwks.json"

    def _build_allowed_client_ids(self, allowed_client_ids: Optional[List[str]]) -> List[str]:
        """Build list of allowed client IDs from parameter and environment."""
        if allowed_client_ids:
            return allowed_client_ids

        # Start with the primary client ID (validated as non-None before this is called)
        assert self.client_id is not None
        client_ids: List[str] = [self.client_id]

        # Add additional allowed client IDs from environment (comma-separated)
        # e.g., COGNITO_ALLOWED_CLIENT_IDS=client1,client2,client3
        additional_ids = os.getenv("COGNITO_ALLOWED_CLIENT_IDS", "")
        if additional_ids:
            client_ids.extend([cid.strip() for cid in additional_ids.split(",") if cid.strip()])

        return list(set(client_ids))  # Remove duplicates


class CognitoAdminConfig:
    """Configuration for Cognito admin/machine-to-machine authentication.

    Used for API tests and service-to-service communication using
    the client_credentials OAuth flow.

    Attributes:
        client_id: Admin client ID
        client_secret: Admin client secret
        token_url: OAuth token endpoint URL
        scope: OAuth scope for the admin token
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_url: Optional[str] = None,
        scope: Optional[str] = None
    ):
        """Initialize Cognito admin configuration.

        Args:
            client_id: Admin client ID. Defaults to COGNITO_ADMIN_CLIENT_ID env var.
            client_secret: Admin client secret. Defaults to COGNITO_ADMIN_CLIENT_SECRET env var.
            token_url: OAuth token URL. Defaults to COGNITO_TOKEN_URL env var.
            scope: OAuth scope. Defaults to COGNITO_ADMIN_SCOPE env var.

        Raises:
            ValueError: If client_id or client_secret is not set.
        """
        self.client_id = client_id or os.getenv("COGNITO_ADMIN_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("COGNITO_ADMIN_CLIENT_SECRET")
        self.token_url = token_url or os.getenv("COGNITO_TOKEN_URL")
        self.scope = scope or os.getenv("COGNITO_ADMIN_SCOPE", "")

        if not self.client_id:
            raise ValueError(
                "COGNITO_ADMIN_CLIENT_ID must be set in environment or passed to CognitoAdminConfig"
            )
        if not self.client_secret:
            raise ValueError(
                "COGNITO_ADMIN_CLIENT_SECRET must be set in environment or passed to CognitoAdminConfig"
            )
