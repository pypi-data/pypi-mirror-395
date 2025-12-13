from dataclasses import dataclass


@dataclass(frozen=True)
class BearerAuth:
    """Result of parsing the Bearer HTTP Authorization header.

    Analogous to `aiohttp.helpers.BasicAuth`.
    """

    token: str

    @classmethod
    def decode(cls, header_value: str) -> "BearerAuth":
        try:
            auth_scheme, token = header_value.split(" ", 1)
        except ValueError:
            msg = "No credentials"
            raise ValueError(msg) from None
        if auth_scheme.lower() != "bearer":
            msg = "Unexpected authorization scheme"
            raise ValueError(msg)
        if not token:
            msg = "No credentials"
            raise ValueError(msg)
        return cls(token=token)

    def encode(self) -> str:
        return "Bearer " + self.token
