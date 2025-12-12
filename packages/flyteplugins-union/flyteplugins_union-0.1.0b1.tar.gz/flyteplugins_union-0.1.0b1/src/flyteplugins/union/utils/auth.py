import base64
from dataclasses import dataclass

_SERVERLESS_ENDPOINTS = {
    "serverless-1.us-east-2.s.union.ai",
    "serverless-gcp.cloud-staging.union.ai",
    "utt-srv-staging-1.cloud-staging.union.ai",
    "serverless-preview.canary.unionai.cloud",
    "utt-srv-canary-1.canary.unionai.cloud",
}


@dataclass
class AppClientCredentials:
    """Application client credentials for API key."""

    endpoint: str
    client_id: str
    client_secret: str
    org: str


def is_serverless_endpoint(endpoint: str) -> bool:
    """Check if endpoint is a Union serverless endpoint."""
    return endpoint in _SERVERLESS_ENDPOINTS


def encode_app_client_credentials(app_credentials: AppClientCredentials) -> str:
    """
    Encode app credentials as a base64 string for use as UNION_API_KEY.

    Args:
        app_credentials: The application credentials to encode

    Returns:
        Base64-encoded credential string
    """
    data = (
        f"{app_credentials.endpoint}:{app_credentials.client_id}:{app_credentials.client_secret}:{app_credentials.org}"
    )
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")
