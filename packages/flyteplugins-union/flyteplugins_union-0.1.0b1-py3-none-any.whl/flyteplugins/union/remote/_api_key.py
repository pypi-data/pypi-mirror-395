from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import AsyncIterator

from flyte._initialize import ensure_client, get_client
from flyte.remote._common import ToJSONMixin
from flyte.syncify import syncify

# This service still lives under flyteidl
from flyteidl.service.identity_pb2 import UserInfoRequest

from flyteplugins.union.internal.common import list_pb2

# These proto definitions live in cloud idl and have just been copied over.
from flyteplugins.union.internal.identity.app_definition_pb2 import App
from flyteplugins.union.internal.identity.app_payload_pb2 import (
    CreateAppRequest,
    DeleteAppRequest,
    GetAppRequest,
    ListAppsRequest,
    UpdateAppRequest,
)
from flyteplugins.union.internal.identity.app_service_pb2_grpc import AppsServiceStub
from flyteplugins.union.internal.identity.enums_pb2 import (
    AUTHORIZATION_CODE,
    CLIENT_CREDENTIALS,
    CLIENT_SECRET_BASIC,
    CODE,
    CONSENT_METHOD_REQUIRED,
)
from flyteplugins.union.utils.auth import AppClientCredentials, encode_app_client_credentials, is_serverless_endpoint


@dataclass
class ApiKey(ToJSONMixin):
    """Represents a Union API Key (OAuth Application).

    API Keys in Union are OAuth 2.0 applications that can be used for
    headless authentication. They support client credentials flow for
    machine-to-machine authentication.

    Attributes:
        pb2: The underlying protobuf App message
        organization: The organization this API key belongs to (for serverless)
        encoded_credentials: Base64-encoded credentials for UNION_API_KEY env var

    Example:
        # Create a new API key
        api_key = ApiKey.create(name="ci-pipeline")
        print(f"export FLYTE_API_KEY=\"{api_key.encoded_credentials}\"")

        # List all API keys
        for key in ApiKey.listall():
            print(f"{key.client_id}: {key.client_name}")

        # Get a specific API key
        key = ApiKey.get(client_id="my-client-id")

        # Delete an API key
        ApiKey.delete(client_id="my-client-id")
    """

    pb2: App
    organization: str | None = field(default=None)
    encoded_credentials: str | None = field(default=None)

    @property
    def client_id(self) -> str:
        """The OAuth client ID."""
        return self.pb2.client_id

    @property
    def client_name(self) -> str:
        """The human-readable name of the API key."""
        return self.pb2.client_name

    @property
    def client_secret(self) -> str:
        """The OAuth client secret (only available on creation)."""
        return self.pb2.client_secret

    @syncify
    @classmethod
    async def create(
        cls,
        name: str,
        *,
        redirect_uris: list[str] | None = None,
    ) -> ApiKey:
        """Create a new API key.

        Args:
            name: Human-readable name for the API key
            redirect_uris: OAuth redirect URIs (defaults to localhost callback)

        Returns:
            ApiKey instance with client_secret populated

        Raises:
            Exception: If API key creation fails

        Example:
            api_key = ApiKey.create(name="ci-pipeline")
            print(f"Client ID: {api_key.client_id}")
            print(f"Client Secret: {api_key.client_secret}")
            print(f"Encoded: {api_key.encoded_credentials}")
        """
        ensure_client()
        client = get_client()
        endpoint = client.endpoint

        if not endpoint:
            raise ValueError("No endpoint configured")

        channel = client._channel
        stub = AppsServiceStub(channel)

        # Normalize the client name
        normalized_client_name = re.sub("[^0-9a-zA-Z]+", "-", name.lower())

        # Determine client_id and organization based on endpoint type
        if is_serverless_endpoint(endpoint):
            user_info = await client.identity_service.UserInfo(UserInfoRequest())
            user_handle = user_info.additional_claims.fields["userhandle"].string_value
            org = user_handle
            tenant = endpoint.split(".")[0]
            client_id = f"{tenant}-{user_handle}-{normalized_client_name}"
        else:
            org = None
            client_id = normalized_client_name

        # Create the request
        request = CreateAppRequest(
            organization=org or "",
            client_id=client_id,
            client_name=client_id,
            grant_types=[CLIENT_CREDENTIALS, AUTHORIZATION_CODE],
            redirect_uris=redirect_uris or ["http://localhost:8080/authorization-code/callback"],
            response_types=[CODE],
            token_endpoint_auth_method=CLIENT_SECRET_BASIC,
            consent_method=CONSENT_METHOD_REQUIRED,
        )

        response = await stub.Create(request)

        # Encode credentials for UNION_API_KEY environment variable
        encoded = encode_app_client_credentials(
            AppClientCredentials(
                endpoint=endpoint,
                client_id=response.app.client_id,
                client_secret=response.app.client_secret,
                org=org or "None",
            )
        )

        return cls(pb2=response.app, organization=org, encoded_credentials=encoded)

    @syncify
    @classmethod
    async def get(cls, client_id: str) -> ApiKey:
        """Get an API key by client ID.

        Args:
            client_id: The OAuth client ID

        Returns:
            ApiKey instance

        Raises:
            Exception: If API key not found

        Example:
            key = ApiKey.get(client_id="my-client-id")
            print(key.client_name)
        """
        ensure_client()
        client = get_client()
        channel = client._channel
        stub = AppsServiceStub(channel)

        request = GetAppRequest(client_id=client_id)
        response = await stub.Get(request)

        return cls(pb2=response.app)

    @syncify
    @classmethod
    async def listall(
        cls,
        *,
        limit: int = 100,
    ) -> AsyncIterator[ApiKey]:
        """List all API keys.

        Args:
            limit: Maximum number of keys to return

        Yields:
            ApiKey instances

        Example:
            for key in ApiKey.listall(limit=10):
                print(f"{key.client_id}: {key.client_name}")
        """
        ensure_client()
        client = get_client()
        channel = client._channel
        stub = AppsServiceStub(channel)

        list_request = list_pb2.ListRequest(
            limit=limit,
        )
        # todo: need to handle serverless
        request = ListAppsRequest(
            organization="",
            request=list_request,
        )

        response = await stub.List(request)

        for app in response.apps:
            yield cls(pb2=app)

    @syncify
    @classmethod
    async def delete(cls, client_id: str) -> None:
        """Delete an API key.

        Args:
            client_id: The OAuth client ID to delete

        Raises:
            Exception: If deletion fails

        Example:
            ApiKey.delete(client_id="old-ci-key")
        """
        ensure_client()
        client = get_client()
        channel = client._channel
        stub = AppsServiceStub(channel)

        request = DeleteAppRequest(client_id=client_id)
        await stub.Delete(request)

    @syncify
    @classmethod
    async def update(
        cls,
        client_id: str,
        *,
        client_name: str | None = None,
        redirect_uris: list[str] | None = None,
    ) -> ApiKey:
        """Update an API key.

        Args:
            client_id: The OAuth client ID to update
            client_name: New name for the API key
            redirect_uris: New redirect URIs

        Returns:
            Updated ApiKey instance

        Raises:
            Exception: If update fails

        Example:
            key = ApiKey.update(
                client_id="my-key",
                client_name="renamed-key"
            )
        """
        ensure_client()
        client = get_client()
        channel = client._channel
        stub = AppsServiceStub(channel)

        # Get current app first to preserve fields not being updated
        current = await cls.get.aio(client_id)

        request = UpdateAppRequest(
            client_id=client_id,
            client_name=client_name or current.client_name,
            redirect_uris=redirect_uris or list(current.pb2.redirect_uris),
            # Preserve other fields from current app
            grant_types=list(current.pb2.grant_types),
            response_types=list(current.pb2.response_types),
            token_endpoint_auth_method=current.pb2.token_endpoint_auth_method,
            consent_method=current.pb2.consent_method,
        )

        response = await stub.Update(request)

        return cls(pb2=response.app)
