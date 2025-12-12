from earthscope_sdk.common.service import SdkService


class UserBaseService(SdkService):
    """
    L1 user/IDM endpoints
    """

    async def _get_aws_credentials(self, *, role: str = "s3-miniseed"):
        """
        Retrieve temporary AWS credentials
        """

        from earthscope_sdk.client.user.models import AwsTemporaryCredentials

        req = self.ctx.httpx_client.build_request(
            method="GET",
            url=f"{self.resources.api_url}beta/user/credentials/aws/{role}",
        )

        resp = await self._send_with_retries(req)

        return AwsTemporaryCredentials.model_validate_json(resp.content)

    async def _get_profile(self):
        """
        Retrieve your EarthScope user profile
        """

        from earthscope_sdk.client.user.models import UserProfile

        req = self.ctx.httpx_client.build_request(
            method="GET",
            url=f"{self.resources.api_url}beta/user/profile",
        )

        resp = await self._send_with_retries(req)

        return UserProfile.model_validate_json(resp.content)
