from contextlib import suppress
from datetime import timedelta
from typing import TYPE_CHECKING, Optional

from earthscope_sdk.client.user._base import UserBaseService

if TYPE_CHECKING:
    from earthscope_sdk.client.user.models import AwsTemporaryCredentials
    from earthscope_sdk.common.context import SdkContext


class _UserService(UserBaseService):
    """
    L2 user/IDM service functionality
    """

    def __init__(self, ctx: "SdkContext"):
        super().__init__(ctx)

        self._aws_creds_by_role = dict[str, "AwsTemporaryCredentials"]()

    async def _get_aws_credentials(
        self,
        *,
        role: str = "s3-miniseed",
        force=False,
        ttl_threshold: Optional[timedelta] = None,
    ):
        """
        Retrieve temporary AWS credentials.

        Leverages a memory cache and disk cache in this profile's state directory
        (`~/.earthscope/<profile_name>/aws.<role>.json`)

        Args:
            role: Alias of the role to assume. Defaults to `s3-miniseed`.
            force: Ignore cache and fetch new credentials. Defaults to `False`.
            ttl_threshold: Time-to-live remaining on cached credentials after which new credentials are fetched. Defaults to 30s.

        Returns: Temporary AWS credentials for the selected role.
        """
        # lazy imports
        from pydantic import ValidationError

        from earthscope_sdk.client.user.models import AwsTemporaryCredentials

        aws_creds_file_path = self.ctx.settings.profile_dir / f"aws.{role}.json"

        if not force:
            # Check memory cache
            if aws_creds := self._aws_creds_by_role.get(role):
                if not aws_creds.is_expired(ttl_threshold):
                    return aws_creds

            # Check disk cache
            with suppress(FileNotFoundError, ValidationError):
                aws_creds_bytes = aws_creds_file_path.read_bytes()
                aws_creds = AwsTemporaryCredentials.model_validate_json(aws_creds_bytes)
                if not aws_creds.is_expired(ttl_threshold):
                    return aws_creds

        # Get new AWS creds
        # NOTE: this method will implicitly refresh our access token if necessary
        aws_creds = await super()._get_aws_credentials(role=role)

        # persist in memory and on disk
        self._aws_creds_by_role[role] = aws_creds
        aws_creds_file_path.parent.mkdir(parents=True, exist_ok=True)
        aws_creds_file_path.write_bytes(aws_creds.model_dump_json().encode())

        return aws_creds


class AsyncUserService(_UserService):
    """
    User and Identity Management functionality
    """

    def __init__(self, ctx: "SdkContext"):
        super().__init__(ctx)

        self.get_aws_credentials = self._get_aws_credentials
        self.get_profile = self._get_profile


class UserService(_UserService):
    """
    User and Identity Management functionality
    """

    def __init__(self, ctx: "SdkContext"):
        super().__init__(ctx)

        self.get_aws_credentials = ctx.syncify(self._get_aws_credentials)
        self.get_profile = ctx.syncify(self._get_profile)
