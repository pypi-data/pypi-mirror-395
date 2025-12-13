from __future__ import annotations

import json
from collections.abc import Sequence
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
)

from aiohttp import ClientError, web
from aiohttp.hdrs import AUTHORIZATION, SEC_WEBSOCKET_PROTOCOL
from aiohttp.helpers import BasicAuth
from aiohttp.web import Application, Request, StreamResponse
from aiohttp_security import (
    AbstractAuthorizationPolicy,
    AbstractIdentityPolicy,
    check_authorized,
    setup,
)
from aiohttp_security.api import AUTZ_KEY
from jose import jwt
from jose.exceptions import JWTError


if TYPE_CHECKING:
    from . import AuthClient

from aiohttp.client_exceptions import ClientResponseError

from .bearer_auth import BearerAuth
from .entities import Permission


JWT_IDENTITY_CLAIM = "https://platform.neuromation.io/user"
JWT_IDENTITY_CLAIM_OPTIONS = ("identity", JWT_IDENTITY_CLAIM)
JWT_KIND_CLAIM = "https://platform.neuromation.io/kind"
JWT_JOB_ID_CLAIM = "https://platform.neuromation.io/job-id"

NEURO_AUTH_TOKEN_QUERY_PARAM = "neuro-auth-token"
WS_BEARER = "bearer.apolo.us-"


def _extract_claim(identity: str | None, claim_name: str) -> str | None:
    if not identity:
        return None
    try:
        claims = jwt.get_unverified_claims(identity)
        value: Any = claims.get(claim_name)
        if isinstance(value, str):
            return value
        if value is not None:
            return str(value)
        return None
    except JWTError:
        return None


def get_untrusted_user_name(identity: str | None) -> str | None:
    if identity is None:
        return "user"

    for claim in JWT_IDENTITY_CLAIM_OPTIONS:
        value = _extract_claim(identity, claim)
        if value:
            return value
    return None


def get_job_id_from_identity(identity: str | None) -> str | None:
    return _extract_claim(identity, JWT_JOB_ID_CLAIM)


def get_kind(identity: str) -> Kind:
    kind_str = _extract_claim(identity, JWT_KIND_CLAIM)
    try:
        return Kind(kind_str) if kind_str else Kind.USER
    except ValueError:
        return Kind.USER


async def check_permissions(
    request: web.Request, permissions: Sequence[Permission | Sequence[Permission]]
) -> None:
    user_name = await check_authorized(request)  # current implementation uses
    # get_untrusted_user_name function
    auth_policy = request.config_dict.get(AUTZ_KEY)
    if not auth_policy:
        msg = "Auth policy not configured"
        raise RuntimeError(msg)
    assert isinstance(auth_policy, AuthPolicy)

    try:
        missing = await auth_policy.get_missing_permissions(user_name, permissions)
    except ClientError as e:
        # re-wrap in order not to expose the client
        raise RuntimeError(e) from e

    if missing:
        payload = {"missing": [p.to_payload() for p in missing]}
        raise web.HTTPForbidden(
            text=json.dumps(payload), content_type="application/json"
        )


class AuthScheme(str, Enum):
    BASIC = "basic"
    BEARER = "bearer"


class Kind(str, Enum):
    CONTROL_PLANE = "control_plane"
    CLUSTER = "cluster"
    USER = "user"


class IdentityPolicy(AbstractIdentityPolicy):
    def __init__(
        self,
        auth_scheme: AuthScheme = AuthScheme.BEARER,
        default_identity: str | None = None,
    ) -> None:
        self._auth_scheme = auth_scheme
        self._default_identity = default_identity

    async def identify(self, request: Request) -> str | None:
        header_identity = request.headers.get(AUTHORIZATION)

        if header_identity is None:
            ws_identity = self._extract_ws_identity(request)
            query_identity = request.query.get(NEURO_AUTH_TOKEN_QUERY_PARAM)
            return ws_identity or query_identity or self._default_identity

        if self._auth_scheme == AuthScheme.BASIC:
            identity = cast(str, BasicAuth.decode(header_identity).password)
        else:
            identity = BearerAuth.decode(header_identity).token

        return identity

    async def remember(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        pass

    async def forget(
        self, request: Request, response: StreamResponse
    ) -> None:  # pragma: no cover
        pass

    def _extract_ws_identity(self, request: Request) -> str | None:
        ws_subprotocol = request.headers.get(SEC_WEBSOCKET_PROTOCOL)
        if ws_subprotocol is not None:
            for part in ws_subprotocol.strip().split(" "):
                if part.lower().startswith(WS_BEARER):
                    return part[len(WS_BEARER) :]
        return None


class AuthPolicy(AbstractAuthorizationPolicy):
    def __init__(self, auth_client: AuthClient) -> None:
        self._auth_client = auth_client

    async def authorized_userid(self, identity: str) -> str | None:
        name = get_untrusted_user_name(identity)
        if not name:
            return None
        try:
            # NOTE: here we make a call to the auth service on behalf of the
            # actual user, not a service.
            await self._auth_client.verify_token(name, token=identity)
            return name
        except ClientResponseError:
            return None

    async def permits(
        self,
        identity: str | None,
        permission: str | Enum,
        context: Any = None,
    ) -> bool:
        name = get_untrusted_user_name(identity)
        if not name:
            return False
        return await self._auth_client.check_user_permissions(name, context)

    async def get_missing_permissions(
        self,
        user_name: str,
        permissions: Sequence[Permission | Sequence[Permission]],
    ) -> Sequence[Permission]:
        return await self._auth_client.get_missing_permissions(user_name, permissions)


async def setup_security(
    app: Application,
    auth_client: AuthClient,
    auth_scheme: AuthScheme = AuthScheme.BEARER,
) -> None:  # pragma: no cover
    if auth_client.is_anonymous_access_allowed:
        identity_policy = IdentityPolicy(
            auth_scheme=auth_scheme, default_identity="user"
        )
    else:
        identity_policy = IdentityPolicy(auth_scheme=auth_scheme)
    auth_policy = AuthPolicy(auth_client=auth_client)
    setup(app, identity_policy, auth_policy)
