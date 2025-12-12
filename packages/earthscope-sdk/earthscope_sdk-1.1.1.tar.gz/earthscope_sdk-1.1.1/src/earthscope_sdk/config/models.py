import base64
import binascii
import datetime as dt
import fnmatch
import functools
from contextlib import suppress
from enum import Enum
from functools import cached_property
from typing import Annotated, Any, Optional, Type, Union

from annotated_types import Ge, Gt
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    HttpUrl,
    ValidationError,
    model_validator,
)

from earthscope_sdk import __version__
from earthscope_sdk.model.secret import SecretStr


def _try_float(v: Any):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


Timedelta = Annotated[dt.timedelta, BeforeValidator(_try_float)]


class AccessTokenBody(BaseModel):
    """
    Access token payload

    [See Auth0 docs](https://auth0.com/docs/secure/tokens/access-tokens/access-token-profiles)
    """

    audience: Annotated[Union[str, list[str]], Field(alias="aud")]
    issuer: Annotated[str, Field(alias="iss")]
    issued_at: Annotated[dt.datetime, Field(alias="iat")]
    expires_at: Annotated[dt.datetime, Field(alias="exp")]
    scope: Annotated[str, Field(alias="scope")] = ""
    subject: Annotated[str, Field(alias="sub")]
    grant_type: Annotated[Optional[str], Field(alias="gty")] = None
    token_id: Annotated[Optional[str], Field(alias="jti")] = None
    client_id: Annotated[
        str,
        Field(
            validation_alias=AliasChoices("client_id", "azp"),
            serialization_alias="client_id",
        ),
    ]

    @cached_property
    def ttl(self) -> dt.timedelta:
        """time to live (TTL) until expiration"""
        return self.expires_at - dt.datetime.now(dt.timezone.utc)

    model_config = ConfigDict(extra="allow", frozen=True, populate_by_name=True)


class AuthFlowType(Enum):
    DeviceCode = "device_code"
    MachineToMachine = "m2m"


class Tokens(BaseModel):
    """
    EarthScope SDK oauth2 tokens
    """

    access_token: Optional[SecretStr] = None
    id_token: Optional[SecretStr] = None
    refresh_token: Optional[SecretStr] = None

    model_config = ConfigDict(frozen=True)

    @cached_property
    def access_token_body(self):
        if self.access_token is None:
            return None

        with suppress(IndexError, binascii.Error, ValidationError):
            payload_b64 = self.access_token.get_secret_value().split(".", 2)[1]
            payload = base64.b64decode(payload_b64 + "==")  # extra padding
            return AccessTokenBody.model_validate_json(payload)

        raise ValueError("Unable to decode access token body")

    @model_validator(mode="after")
    def ensure_one_of(self):
        # allow all fields to be optional in subclasses
        if self.__class__ != Tokens:
            return self

        if self.access_token or self.refresh_token:
            return self

        raise ValueError("At least one of access token and refresh token is required.")


class RetrySettings(BaseModel):
    """
    Retry configuration for the [Stamina library](https://stamina.hynek.me/en/stable/index.html)
    """

    # same defaults as AWS SDK "standard" mode:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html#standard-retry-mode

    attempts: Annotated[int, Ge(0)] = 3
    timeout: Timedelta = dt.timedelta(seconds=20)

    wait_initial: Timedelta = dt.timedelta(milliseconds=100)
    wait_max: Timedelta = dt.timedelta(seconds=5)
    wait_jitter: Timedelta = dt.timedelta(seconds=1)
    wait_exp_base: Annotated[float, Gt(0)] = 2

    async def retry_context(self, *retry_exc: Type[Exception]):
        """
        Obtain a [Stamina](https://stamina.hynek.me/en/stable/index.html) retry iterator.
        """
        from stamina import retry_context

        retry_on = functools.partial(self.is_retriable, retry_exc=retry_exc)

        ctx = retry_context(
            on=retry_on,
            attempts=self.attempts,
            timeout=self.timeout,
            wait_initial=self.wait_initial,
            wait_jitter=self.wait_jitter,
            wait_max=self.wait_max,
            wait_exp_base=self.wait_exp_base,
        )
        async for attempt in ctx:
            yield attempt

    def is_retriable(
        self,
        exc: Exception,
        *args,
        retry_exc: tuple[Type[Exception]] = (),
        **kwargs,
    ) -> bool:
        """
        Check if the given exception can be retried
        """
        if retry_exc and isinstance(exc, retry_exc):
            return True

        return False


class HttpRetrySettings(RetrySettings):
    status_codes: set[int] = {429, 500, 502, 503, 504}

    def is_retriable(
        self,
        exc: Exception,
        *args,
        **kwargs,
    ) -> bool:
        from httpx import HTTPStatusError

        if isinstance(exc, HTTPStatusError):
            if exc.response.status_code in self.status_codes:
                return True

        return super().is_retriable(exc, *args, **kwargs)


class AuthFlowSettings(Tokens):
    """
    Auth flow configuration

    Not for direct use.
    """

    # Auth parameters
    audience: str = "https://api.earthscope.org"
    domain: HttpUrl = HttpUrl("https://login.earthscope.org")
    client_id: str = "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
    scope: str = "offline_access"
    client_secret: Optional[SecretStr] = None

    # Only inject bearer token for requests to these hosts
    allowed_hosts: set[str] = {
        "earthscope.org",
        "*.earthscope.org",
    }

    # Auth exchange retries
    retry: HttpRetrySettings = HttpRetrySettings(
        attempts=5,
        timeout=dt.timedelta(seconds=30),
        wait_initial=dt.timedelta(seconds=1),
        wait_jitter=dt.timedelta(seconds=3),
    )

    @cached_property
    def auth_flow_type(self) -> AuthFlowType:
        if self.client_secret is not None:
            return AuthFlowType.MachineToMachine

        return AuthFlowType.DeviceCode

    @cached_property
    def allowed_host_patterns(self) -> set[str]:
        """
        The subset of allowed hosts that are glob patterns.

        Use `is_host_allowed` to check if a host is allowed by any of these patterns.
        """
        return {h for h in self.allowed_hosts if "*" in h or "?" in h}

    def is_host_allowed(self, host: str) -> bool:
        """
        Check if a host matches any pattern in the allowed hosts set.

        Supports glob patterns with '?' and '*' characters (e.g., *.earthscope.org).

        Args:
            host: The hostname to check

        Returns:
            True if the host matches any allowed pattern, False otherwise
        """
        if host in self.allowed_hosts:
            return True

        for allowed_pattern in self.allowed_host_patterns:
            if fnmatch.fnmatch(host, allowed_pattern):
                self.allowed_hosts.add(host)
                return True

        return False


class HttpSettings(BaseModel):
    """
    HTTP client configuration
    """

    # httpx limits
    keepalive_expiry: Timedelta = dt.timedelta(seconds=5)
    max_connections: Optional[int] = None
    max_keepalive_connections: Optional[int] = None

    # httpx timeouts
    timeout_connect: Timedelta = dt.timedelta(seconds=5)
    timeout_read: Timedelta = dt.timedelta(seconds=5)

    # automatically retry requests
    retry: HttpRetrySettings = HttpRetrySettings()

    # Other
    user_agent: str = f"earthscope-sdk py/{__version__}"
    extra_headers: dict[str, str] = {}

    @cached_property
    def limits(self):
        """httpx Limits on client connection pool"""
        # lazy import
        import httpx

        return httpx.Limits(
            max_connections=self.max_connections,
            max_keepalive_connections=self.max_keepalive_connections,
            keepalive_expiry=self.keepalive_expiry.total_seconds(),
        )

    @cached_property
    def timeouts(self):
        """httpx Timeouts default behavior"""
        # lazy import
        import httpx

        return httpx.Timeout(
            connect=self.timeout_connect.total_seconds(),
            # reuse read timeout for others
            read=self.timeout_read.total_seconds(),
            write=self.timeout_read.total_seconds(),
            pool=self.timeout_read.total_seconds(),
        )


class ResourceRefs(BaseModel):
    """
    References to EarthScope resources
    """

    api_url: HttpUrl = HttpUrl("https://api.earthscope.org")
    """Base URL for api.earthscope.org"""


class SdkBaseSettings(BaseModel):
    """
    Common base class for SDK settings

    Not for direct use.
    """

    http: HttpSettings = HttpSettings()
    oauth2: AuthFlowSettings = AuthFlowSettings()
    resources: ResourceRefs = ResourceRefs()
