from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import asdict
from typing import Any, TypeVar

import aiohttp
from aiohttp.hdrs import AUTHORIZATION
from jose import jwt
from jose.exceptions import JWTError
from multidict import CIMultiDict
from typing_extensions import Self
from yarl import URL

from neuro_admin_client.bearer_auth import BearerAuth
from neuro_admin_client.entities import (
    Permission,
    User,
)

from .admin_client import AdminClient
from .security import JWT_IDENTITY_CLAIM_OPTIONS


T = TypeVar("T")


class AuthClient:
    def __init__(
        self,
        url: URL | None,
        token: str,
        trace_configs: list[aiohttp.TraceConfig] | None = None,
    ) -> None:
        if url is not None and not url:
            msg = (
                "url argument should be http URL or None for secure-less configurations"
            )
            raise ValueError(msg)
        self._token = token
        self._admin_client = AdminClient(
            base_url=url,
            service_token=token,
            trace_configs=trace_configs or [],
        )
        self._url = url

    async def connect(self) -> None:
        await self._admin_client.connect()

    async def close(self) -> None:
        await self._admin_client.close()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    def _make_url(self, path: str) -> URL:
        assert self._url
        if path.startswith("/"):
            path = path[1:]
        return self._url / path

    @property
    def is_anonymous_access_allowed(self) -> bool:
        return self._url is None

    def get_unverified_username(self, token: str) -> str | None:
        try:
            claims = jwt.get_unverified_claims(token)
            for identity_claim in JWT_IDENTITY_CLAIM_OPTIONS:
                if claim := claims.get(identity_claim):
                    return str(claim)
            return None
        except JWTError:
            return None

    async def check_user_permissions(
        self,
        name: str,
        permissions: Sequence[Permission | Sequence[Permission]],
    ) -> bool:
        if self._url is None:
            return True
        missing = await self.get_missing_permissions(name, permissions)
        return not missing

    async def get_missing_permissions(
        self,
        name: str,
        permissions: Sequence[Permission | Sequence[Permission]],
    ) -> Sequence[Permission]:
        assert permissions, "No permissions passed"
        if self._url is None:
            return []

        flat_permissions: list[Permission] = []
        for p in permissions:
            if isinstance(p, Permission):
                flat_permissions.append(p)
            else:
                flat_permissions.extend(p)

        payload: list[dict[str, Any]] = [
            {
                **(d := asdict(p)),
                "uri": str(d["uri"]) if isinstance(d.get("uri"), URL) else d["uri"],
            }
            for p in flat_permissions
        ]
        return await self._admin_client.get_missing_permissions(
            name=name, payload=payload
        )

    async def verify_token(self, name: str, token: str) -> None:
        if self._url is None:
            return
        headers = AdminClient.generate_auth_headers(token)
        await self._admin_client.verify_token(name, headers=headers)

    def _generate_headers(self, token: str | None = None) -> CIMultiDict[str]:
        headers: CIMultiDict[str] = CIMultiDict()
        if token:
            headers[AUTHORIZATION] = BearerAuth(token).encode()
        return headers

    async def ping(self) -> None:
        if self._url is None:
            return
        await self._admin_client.ping()

    def _serialize_user(self, user: User) -> dict[str, Any]:
        return {"name": user.name, "email": user.email}

    async def add_user(self, user: User) -> User:
        payload = self._serialize_user(user)
        return await self._admin_client.add_user(payload=payload)

    async def get_user_token(
        self,
        name: str,
        new_token_uri: str | None = None,
        job_id: str | None = None,
        token: str | None = None,
    ) -> str:
        if self._url is None:
            return ""
        payload = {}
        if new_token_uri:
            payload["uri"] = new_token_uri
        if job_id:
            payload["job_id"] = job_id

        return await self._admin_client.get_user_token(name, payload, token)

    async def get_authorized_entities(
        self,
        user_name: str,
        entities: Iterable[T],
        per_entity_perms: Callable[[T], Sequence[Permission]],
        global_perm: Permission | None = None,
    ) -> list[T]:
        entities = list(entities)
        all_perms: list[Permission] = []
        if global_perm is not None:
            all_perms.append(global_perm)
        for e in entities:
            all_perms.extend(per_entity_perms(e))
        missing = set(await self.get_missing_permissions(user_name, all_perms))
        if global_perm is not None and global_perm not in missing:
            return entities

        # per-entity OR
        allowed: list[T] = []
        for e in entities:
            perms = per_entity_perms(e)
            if any(p not in missing for p in perms):
                allowed.append(e)
        return allowed
