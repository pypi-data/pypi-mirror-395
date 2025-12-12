class AuthFlowError(Exception):
    """Generic authentication flow error"""


class UnauthenticatedError(AuthFlowError):
    pass


class UnauthorizedError(AuthFlowError):
    pass


class NoTokensError(AuthFlowError):
    pass


class NoAccessTokenError(NoTokensError):
    pass


class NoIdTokenError(NoTokensError):
    pass


class NoRefreshTokenError(NoTokensError):
    pass


class InvalidRefreshTokenError(AuthFlowError):
    pass


class ClientCredentialsFlowError(AuthFlowError):
    pass


class DeviceCodeRequestDeviceCodeError(AuthFlowError):
    pass


class DeviceCodePollingError(AuthFlowError):
    pass


class DeviceCodePollingExpiredError(DeviceCodePollingError):
    pass
