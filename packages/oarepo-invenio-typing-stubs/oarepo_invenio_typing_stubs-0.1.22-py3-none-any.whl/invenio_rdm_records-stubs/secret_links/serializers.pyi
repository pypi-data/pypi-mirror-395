from typing import Any

from itsdangerous import Serializer

class TokenSerializerMixin(Serializer):
    def create_token(self, obj_id: Any, extra_data: dict[str, Any] = ...) -> str: ...
    def validate_token(
        self,
        token: str,
        expected_data: dict[str, Any] | None = ...,
        *,
        force: bool = ...,
    ) -> dict[str, Any] | None: ...
    def load_token(self, token: str, *, force: bool = ...) -> dict[str, Any]: ...

class TimedSecretLinkSerializer(TokenSerializerMixin):
    def __init__(self, expires_at: Any | None = ..., **kwargs: Any) -> None: ...

class SecretLinkSerializer(TokenSerializerMixin):
    def __init__(self, **kwargs: Any) -> None: ...
