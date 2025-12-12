import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserProfile(BaseModel):
    """
    EarthScope user profile
    """

    first_name: str
    last_name: str
    country_code: str
    region_code: Optional[str]
    institution: str
    work_sector: str
    user_id: str
    primary_email: str
    created_at: dt.datetime
    updated_at: dt.datetime


class AwsTemporaryCredentials(BaseModel):
    """
    AWS temporary credentials
    """

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    expiration: dt.datetime

    model_config = ConfigDict(frozen=True)

    @property
    def ttl(self):
        """
        Time to live
        """
        return self.expiration - dt.datetime.now(dt.timezone.utc)

    def is_expired(self, ttl_threshold: Optional[dt.timedelta] = None):
        """
        Check if these credentials are past or near expiration

        Args:
            ttl_threshold: remaining time-to-live before considering the temporary AWS creds expired (Default: 30s)
        """
        if ttl_threshold is None:
            ttl_threshold = dt.timedelta(seconds=30)

        return self.ttl <= ttl_threshold
