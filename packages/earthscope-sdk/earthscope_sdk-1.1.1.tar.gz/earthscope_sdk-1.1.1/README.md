# EarthScope SDK

An SDK for interacting with EarthScope's APIs

## Getting Started

### Installation

Install from PyPI

```shell
pip install earthscope-sdk
```

### Usage

For detailed usage info and examples, visit [our SDK docs](https://docs.earthscope.org/projects/SDK).

```py
# Import and create a client
from earthscope_sdk import EarthScopeClient

client = EarthScopeClient()

# Example client method usage; retrieve your user profile
profile = client.user.get_profile()
print(profile)

# Client cleanup
client.close()
```

#### Async Usage

There is also an `async` client available

```py
import asyncio
from earthscope_sdk import AsyncEarthScopeClient

async def main():
    client = AsyncEarthScopeClient()

    profile = await client.user.get_profile()
    print(profile)

    await client.close()

asyncio.run(main())
```

#### Context Managers

Client classes can also be used as context managers to ensure resource cleanup occurs.

```py
# sync
with EarthScopeClient() as client:
   client.user.get_profile()

# async
async with AsyncEarthScopeClient() as client:
   await client.user.get_profile()
```

## Bootstrapping Authentication

There are a few methods of bootstrapping authentication for the SDK.

Once refreshable credentials are available to the SDK, it will transparently handle access token refresh on your behalf.

### Same host

If you have the [EarthScope CLI](https://docs.earthscope.org/projects/CLI) installed on the same host that is running your application which uses `earthscope-sdk`, you can simply log in using the CLI. The CLI shares credentials and configuration with this SDK (when running on the same host).

Running `es login` will open your browser and prompt you to log in to your EarthScope account.

```console
$ es login
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://login.earthscope.org/activate?user_code=ABCD-EFGH

Successful login! Access token expires at 2024-12-27 18:50:37+00:00
```

Now when you run your application, `earthscope-sdk` will find your credentials.

### Different hosts

Sometimes your workload runs on different hosts than your main workstation and you cannot feasibly "log in" on all of them. For example, maybe you're running many containers in your workload.

You can still use the [EarthScope CLI](https://docs.earthscope.org/projects/CLI) to facilitate auth for applications on other machines.

1. Use the CLI on your primary workstation [as described above](#same-host) to log in.

1. Use the CLI to retrieve your refresh token.

   ```console
   $ es user get-refresh-token
   <your-refresh-token>
   ```

   > **Note: your refresh token should be treated as a secret credential. Anyone with a valid refresh token can use it to continually retrieve new access tokens on your behalf**.

1. Pass this refresh token to all the hosts needing auth for the `earthscope-sdk`. For example, inject the `ES_OAUTH2__REFRESH_TOKEN` environment variable on these hosts.

   ```shell
   export ES_OAUTH2__REFRESH_TOKEN="<your-refresh-token>"
   ```

## SDK Settings

SDK Settings are provided via the following methods (in order of precedence):

1. initialization arguments (e.g. via class constructors)
1. environment variables
1. dotenv file (.env) variables
1. user's home directory settings files
   1. `~/.earthscope/config.toml` (for configuration)
   1. `~/.earthscope/<profile-name>/tokens.json` (for tokens)
1. legacy EarthScope CLI v0 credentials
1. default settings

SDK configuration is managed by the `SdkSettings` class, and calling the constructor performs this settings loading chain.

```py
from earthscope_sdk.config.settings import SdkSettings

settings = SdkSettings()  # loads settings via loading chain
```

For more details on SDK configuration, including what options are available, see [our settings docs](docs/settings.md).

## Contributing

For details on contributing to the EarthScope SDK, please see:

- [design docs](docs/design.md)
- [development docs](docs/development.md)
