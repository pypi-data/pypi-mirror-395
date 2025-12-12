"""
Authentication integrations for external providers.

Provides production-ready integrations with:
- Azure AD / Entra ID (azure_ad.py)
- Generic OAuth 2.0 providers (oauth.py)

All integrations include:
- Comprehensive security features (PKCE, token validation)
- Claims mapping to netrun-auth format
- Multi-tenant support
- FastAPI integration helpers

Author: Netrun Systems
Version: 1.0.0
Date: 2025-11-25
"""

from netrun_auth.integrations.azure_ad import (
    AzureADConfig,
    AzureADClient,
    AzureADMultiTenantClient,
    get_azure_ad_client,
    initialize_azure_ad,
    get_current_user_azure,
)
from netrun_auth.integrations.oauth import (
    OAuthProvider,
    OAuthConfig,
    OAuthClient,
    OAuthManager,
    get_oauth_manager,
    create_oauth_router,
)

__all__ = [
    # Azure AD
    "AzureADConfig",
    "AzureADClient",
    "AzureADMultiTenantClient",
    "get_azure_ad_client",
    "initialize_azure_ad",
    "get_current_user_azure",
    # OAuth
    "OAuthProvider",
    "OAuthConfig",
    "OAuthClient",
    "OAuthManager",
    "get_oauth_manager",
    "create_oauth_router",
]
