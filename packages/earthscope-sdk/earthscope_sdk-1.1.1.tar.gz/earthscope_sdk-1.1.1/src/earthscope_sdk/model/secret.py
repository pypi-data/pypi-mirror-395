from typing import Annotated

from pydantic import PlainSerializer, SerializationInfo
from pydantic import SecretStr as _SecretStr


def _dump_secret_plaintext(secret: _SecretStr, info: SerializationInfo):
    """
    A special field serializer to dump the actual secret value.

    Only writes secret in plaintext when `info.context == "plaintext".

    See [Pydantic docs](https://docs.pydantic.dev/latest/concepts/serialization/#serialization-context)
    """

    if info.context == "plaintext":
        return secret.get_secret_value()

    return str(secret)


SecretStr = Annotated[
    _SecretStr,
    PlainSerializer(
        _dump_secret_plaintext,
        return_type=str,
        when_used="json-unless-none",
    ),
]
