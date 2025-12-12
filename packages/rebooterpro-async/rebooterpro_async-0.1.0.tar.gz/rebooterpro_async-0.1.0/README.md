# ConnectSense Rebooter Pro Client

Async Python client for the local HTTPS API exposed by the ConnectSense Rebooter Pro. It wraps the device endpoints so they can be reused from any project or packaged for PyPI.

## Installation

```bash
pip install rebooterpro-async
```

## Usage

```python
import asyncio
from rebooterpro_async import RebooterProClient


async def main():
    client = RebooterProClient("rebooter-pro.local")
    info = await client.get_info()
    await client.set_outlet_state(True)   # turn outlet on
    await client.push_webhook("https://example.com/ha-webhook", token="secret")
    await client.aclose()

asyncio.run(main())
```

### Features
- Async aiohttp transport with optional injected session.
- Bundled device CA for hostname validation; IP targets fall back to `ssl=False`.
- Helpers for `/info`, `/config`, `/control`, `/notify` endpoints.
- Simple helper to build the device webhook payload: `build_webhook_payload()`.
- MIT licensed; source and issues live at https://github.com/connectsense/rebooterpro-async.

### Notes
- The client is intentionally transport-only: it does not manage application state or option schemas.
- When you target the device by IP address, TLS verification is disabled (`ssl=False`) to avoid hostname mismatch errors.

### Home Assistant integration hint
If you want to swap direct aiohttp calls, initialize the client with session and SSL helper:

```python
session = async_get_clientsession(hass)
ssl_ctx = await get_aiohttp_ssl(hass, entry)
client = RebooterProClient(entry.data[CONF_HOST], session=session, ssl_context=ssl_ctx)
await client.set_outlet_state(True)
```

## Releases & automation
- Tagged releases (`v*`) trigger the GitHub Actions workflow in `.github/workflows/publish.yml` to build sdist/wheel and publish to PyPI using `PYPI_API_TOKEN`.
- Make sure the GitHub repository has Issues enabled (required for device/service libraries). Consider adding an issue template tailored to your consumers.
