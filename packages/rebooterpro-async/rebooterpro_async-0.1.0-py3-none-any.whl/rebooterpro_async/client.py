from __future__ import annotations

import asyncio
import ipaddress
import json
import re
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

import aiohttp

try:
    from importlib.resources import files
except ImportError:  # Python <3.11 fallback
    from importlib import resources

    def files(package: str):
        return resources.files(package)

# Strip only a leading http/https scheme; the device always speaks https.
_SCHEME_RE = re.compile(r"^\s*https?://", re.IGNORECASE)


class RebooterError(Exception):
    """Base error for all client failures."""


class RebooterConnectionError(RebooterError):
    """Network, SSL, or timeout failure while talking to the device."""

    def __init__(self, message: str, *, cause: BaseException | None = None):
        super().__init__(message)
        self.__cause__ = cause


class RebooterHttpError(RebooterError):
    """HTTP status >=400 returned by the device."""

    def __init__(self, status: int, body: str, url: str):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status} from {url}: {body[:200]}")


class RebooterDecodeError(RebooterError):
    """Response was not valid JSON when JSON was expected."""


def _normalize_host(host: str) -> str:
    """Remove scheme/whitespace so we can safely build https://host URLs."""
    cleaned = _SCHEME_RE.sub("", (host or "").strip(), count=1)
    return cleaned.rstrip("/")


def _build_ssl_context(cafile: Path) -> ssl.SSLContext:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    ctx.load_verify_locations(cafile=str(cafile))
    return ctx


def _choose_ssl(host: str, ca_bundle: Path | None) -> ssl.SSLContext | bool | None:
    """
    Decide what to pass to aiohttp's ssl= parameter:
      - False for IP addresses (disables hostname verification but keeps TLS)
      - SSLContext using the bundled CA when available
      - None to defer to system defaults
    """
    try:
        if host:
            ipaddress.ip_address(host)
            return False
    except ValueError:
        pass

    if ca_bundle and ca_bundle.exists():
        return _build_ssl_context(ca_bundle)
    return None


def build_webhook_payload(webhook_url: str, *, token: str | None = None, port: int | None = None) -> dict[str, Any]:
    """Shape the payload expected by POST /notify on the device."""
    parsed = urlparse(webhook_url)
    resolved_port = port or parsed.port or (443 if parsed.scheme == "https" else 80)

    payload: dict[str, Any] = {"url": webhook_url, "port": resolved_port}
    if token:
        payload["headers"] = {"Authorization": f"Bearer {token}"}
    return payload


def _default_ca_bundle() -> Path | None:
    """Return the packaged device CA path if present."""
    try:
        path = files("rebooterpro_async.data") / "device_ca.pem"
    except Exception:
        return None
    return path if path.exists() else None


DEFAULT_CA_BUNDLE = _default_ca_bundle()


@dataclass
class RebooterProClient:
    """
    Async client for the local Rebooter Pro HTTPS API.

    This client is transport-only; it simply wraps the device endpoints with
    small helper methods.
    """

    host: str
    port: int = 443
    session: aiohttp.ClientSession | None = None
    ssl_context: ssl.SSLContext | bool | None = None
    request_timeout: float = 10.0
    ca_bundle: Path | None = DEFAULT_CA_BUNDLE

    def __post_init__(self):
        normalized = _normalize_host(self.host)
        self.host = normalized
        self.base_url = f"https://{normalized}:{self.port}"
        self._own_session: aiohttp.ClientSession | None = None
        if self.ssl_context is None:
            self.ssl_context = _choose_ssl(normalized, self.ca_bundle)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    async def aclose(self) -> None:
        if self._own_session and not self._own_session.closed:
            await self._own_session.close()
        self._own_session = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self.session:
            return self.session
        if not self._own_session or self._own_session.closed:
            self._own_session = aiohttp.ClientSession()
        return self._own_session

    async def _request_json(self, method: str, path: str, *, json_body: Mapping[str, Any] | None = None, timeout: float | None = None) -> Any:
        session = await self._ensure_session()
        url = f"{self.base_url}/{path.lstrip('/')}"
        client_timeout = aiohttp.ClientTimeout(total=timeout or self.request_timeout)
        try:
            async with session.request(
                method,
                url,
                json=json_body,
                ssl=self.ssl_context,
                timeout=client_timeout,
            ) as resp:
                text = await resp.text()
        except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as exc:
            raise RebooterConnectionError(f"Failed to talk to Rebooter Pro at {self.host}", cause=exc) from exc

        if resp.status >= 400:
            raise RebooterHttpError(resp.status, text, url)

        if not text:
            return None

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise RebooterDecodeError(f"Invalid JSON from {url}: {text[:200]}") from exc

    # ---- Device endpoints ----
    async def get_info(self) -> Mapping[str, Any] | None:
        """GET /info: returns device metadata (serial/model)."""
        return await self._request_json("GET", "/info")

    async def get_config(self) -> Mapping[str, Any] | None:
        """GET /config: fetch the full auto-reboot configuration."""
        return await self._request_json("GET", "/config")

    async def set_config(self, payload: Mapping[str, Any]) -> Mapping[str, Any] | None:
        """POST /config with the full device configuration."""
        return await self._request_json("POST", "/config", json_body=payload)

    async def set_partial_config(self, payload: Mapping[str, Any]) -> Mapping[str, Any] | None:
        """POST /config with a partial payload (device merges fields)."""
        return await self._request_json("POST", "/config", json_body=payload)

    async def get_control_state(self) -> Mapping[str, Any] | None:
        """GET /control: outlet state and reboot flag."""
        return await self._request_json("GET", "/control")

    async def set_outlet_state(self, enabled: bool) -> Mapping[str, Any] | None:
        """POST /control to turn the outlet on/off."""
        return await self._request_json("POST", "/control", json_body={"outlet_active": bool(enabled)})

    async def reboot_outlet(self) -> Mapping[str, Any] | None:
        """POST /control to reboot the outlet."""
        return await self._request_json("POST", "/control", json_body={"outlet_reboot": True})

    async def push_webhook(self, webhook_url: str, *, token: str | None = None, port: int | None = None) -> Mapping[str, Any] | None:
        """POST /notify to register a webhook endpoint."""
        payload = build_webhook_payload(webhook_url, token=token, port=port)
        return await self._request_json("POST", "/notify", json_body=payload)
