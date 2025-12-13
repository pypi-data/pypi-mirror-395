"""Cloud mobile service for managing cloud-hosted mobile devices.

This module handles:
- Connecting to cloud mobiles on the Minitap platform via HTTP API
- Keep-alive polling to maintain the connection (prevents idle shutdown)
- Proper cleanup when the MCP server stops

API Endpoints used:
- GET  /api/daas/virtual-mobiles/{id} - Fetch device info by ID or reference name
- POST /api/daas/virtual-mobiles/{id}/keep-alive - Keep device alive (prevents billing timeout)
"""

import asyncio
import logging
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

import aiohttp

from minitap.mcp.core.config import settings

logger = logging.getLogger(__name__)

# Context variable to store cloud mobile ID accessible from any MCP tool
# This is server-wide (not request-scoped) as it persists for the MCP lifecycle
_cloud_mobile_id: ContextVar[str | None] = ContextVar("cloud_mobile_id", default=None)


def get_cloud_mobile_id() -> str | None:
    """Get the current cloud mobile ID (UUID) from context.

    Returns:
        The cloud mobile UUID if running in cloud mode, None otherwise.
    """
    return _cloud_mobile_id.get()


def set_cloud_mobile_id(mobile_id: str | None) -> None:
    """Set the cloud mobile ID in context.

    Args:
        mobile_id: The cloud mobile UUID or None to clear.
    """
    _cloud_mobile_id.set(mobile_id)


@dataclass
class VirtualMobileInfo:
    """Information about a virtual mobile from the API."""

    id: str  # UUID
    reference_name: str | None
    state: str  # Ready, Starting, Stopping, Stopped, Error
    uptime_seconds: int
    cost_micro_dollars: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "VirtualMobileInfo":
        """Create from API response."""
        return cls(
            id=data["id"],
            reference_name=data.get("referenceName"),
            state=data.get("state", {}).get("current", "Unknown"),
            uptime_seconds=data.get("uptimeSeconds", 0),
            cost_micro_dollars=data.get("costMicroDollars", 0),
        )


class CloudMobileService:
    """Service for managing cloud mobile connections via HTTP API.

    This service handles:
    1. Fetching cloud mobile info by name/UUID
    2. Sending keep-alive pings to prevent idle shutdown
    3. Proper cleanup on MCP server shutdown

    The keep-alive is CRITICAL for billing - the platform will shut down
    idle VMs after a timeout. The MCP server must send keep-alives while
    waiting for user commands.
    """

    KEEP_ALIVE_INTERVAL_SECONDS = 30
    API_TIMEOUT_SECONDS = 30

    def __init__(self, cloud_mobile_name: str, api_key: str):
        """Initialize the cloud mobile service.

        Args:
            cloud_mobile_name: The reference name or UUID of the cloud mobile.
            api_key: The Minitap API key for authentication.
        """
        self.cloud_mobile_name = cloud_mobile_name
        self.api_key = api_key
        self._base_url = settings.MINITAP_DAAS_API.rstrip("/")
        self._mobile_id: str | None = None  # UUID, resolved from name
        self._mobile_info: VirtualMobileInfo | None = None
        self._keep_alive_task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()
        self._session: aiohttp.ClientSession | None = None

    def _get_headers(self) -> dict[str, str]:
        """Get HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.API_TIMEOUT_SECONDS)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def _close_session(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _fetch_virtual_mobile(self) -> VirtualMobileInfo:
        """Fetch virtual mobile info from API.

        GET /api/daas/virtual-mobiles/{id}

        Args:
            id can be UUID or reference name.

        Returns:
            VirtualMobileInfo with device details.

        Raises:
            RuntimeError: If device not found or API error.
        """
        session = await self._ensure_session()
        url = f"{self._base_url}/virtual-mobiles/{self.cloud_mobile_name}"

        logger.debug(f"Fetching virtual mobile: {url}")

        async with session.get(url, headers=self._get_headers()) as response:
            if response.status == 404:
                raise RuntimeError(
                    f"Cloud mobile '{self.cloud_mobile_name}' not found. "
                    "Please verify the name/UUID exists in your Minitap Platform account."
                )
            if response.status == 401:
                raise RuntimeError(
                    "Authentication failed. Please verify your MINITAP_API_KEY is valid."
                )
            if response.status == 403:
                raise RuntimeError(
                    f"Access denied to cloud mobile '{self.cloud_mobile_name}'. "
                    "Please verify your API key has access to this device."
                )
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(
                    f"Failed to fetch cloud mobile: HTTP {response.status} - {error_text}"
                )

            data = await response.json()
            return VirtualMobileInfo.from_api_response(data)

    async def _send_keep_alive(self) -> bool:
        """Send keep-alive ping to prevent idle shutdown.

        POST /api/daas/virtual-mobiles/{id}/keep-alive

        Returns:
            True if successful, False otherwise.
        """
        if not self._mobile_id:
            logger.warning("Cannot send keep-alive: no mobile ID")
            return False

        session = await self._ensure_session()
        url = f"{self._base_url}/virtual-mobiles/{self._mobile_id}/keep-alive"

        try:
            async with session.post(url, headers=self._get_headers()) as response:
                if response.status == 204:
                    logger.debug(f"Keep-alive sent successfully for {self._mobile_id}")
                    return True
                else:
                    error_text = await response.text()
                    logger.warning(f"Keep-alive failed: HTTP {response.status} - {error_text}")
                    return False
        except Exception as e:
            logger.error(f"Keep-alive request failed: {e}")
            return False

    async def connect(self) -> None:
        """Connect to the cloud mobile and start keep-alive polling.

        1. Fetches device info to verify it exists
        2. Stores the UUID for keep-alive calls
        3. Starts background keep-alive polling

        Raises:
            RuntimeError: If no cloud mobile is found with the given name.
        """
        logger.info(f"Connecting to cloud mobile: {self.cloud_mobile_name}")

        try:
            # Fetch device info to verify it exists and get UUID
            self._mobile_info = await self._fetch_virtual_mobile()
            self._mobile_id = self._mobile_info.id

            logger.info(
                f"Connected to cloud mobile: {self.cloud_mobile_name} "
                f"(id={self._mobile_id}, state={self._mobile_info.state})"
            )

            # Check if device is in a usable state
            if self._mobile_info.state not in ("Ready", "Starting"):
                logger.warning(
                    f"Cloud mobile state is '{self._mobile_info.state}'. "
                    "Device may not be ready for use."
                )

            # Store the mobile ID in context for access from MCP tools
            set_cloud_mobile_id(self._mobile_id)

            # Send initial keep-alive
            await self._send_keep_alive()

            # Start keep-alive polling
            self._stop_event.clear()
            self._keep_alive_task = asyncio.create_task(
                self._keep_alive_loop(),
                name=f"cloud_mobile_keep_alive_{self._mobile_id}",
            )

        except Exception as e:
            logger.error(f"Failed to connect to cloud mobile '{self.cloud_mobile_name}': {e}")
            await self._close_session()
            raise RuntimeError(
                f"Failed to connect to cloud mobile '{self.cloud_mobile_name}'. "
                "Please verify:\n"
                "  1. The cloud mobile exists in your Minitap Platform account\n"
                "  2. The CLOUD_MOBILE_NAME matches exactly (case-sensitive)\n"
                "  3. Your MINITAP_API_KEY has access to this cloud mobile\n"
                f"Original error: {e}"
            ) from e

    async def _keep_alive_loop(self) -> None:
        """Background task that sends periodic keep-alive pings.

        This maintains the connection to the cloud mobile and prevents
        idle shutdown (which would stop billing but also lose the session).
        """
        logger.info(
            f"Starting cloud mobile keep-alive polling "
            f"(interval={self.KEEP_ALIVE_INTERVAL_SECONDS}s)"
        )

        consecutive_failures = 0
        max_failures = 3

        while not self._stop_event.is_set():
            try:
                # Wait for the interval, but check stop_event frequently
                for _ in range(self.KEEP_ALIVE_INTERVAL_SECONDS * 10):
                    if self._stop_event.is_set():
                        break
                    await asyncio.sleep(0.1)

                if self._stop_event.is_set():
                    break

                # Send keep-alive ping
                success = await self._send_keep_alive()

                if success:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        logger.error(
                            f"Keep-alive failed {max_failures} times consecutively. "
                            "Cloud mobile may have been shut down."
                        )
                        # Don't stop the loop - keep trying in case it recovers

            except asyncio.CancelledError:
                logger.info("Cloud mobile keep-alive task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in cloud mobile keep-alive: {e}")
                consecutive_failures += 1
                # Don't break on errors, try to continue
                await asyncio.sleep(5)

        logger.info("Cloud mobile keep-alive polling stopped")

    async def disconnect(self) -> None:
        """Disconnect from the cloud mobile and stop keep-alive polling.

        This MUST be called when the MCP server shuts down to:
        1. Stop keep-alive polling (allows VM to idle-shutdown if not used)
        2. Clean up HTTP session

        Note: We intentionally do NOT call a "stop" endpoint here.
        Stopping keep-alive will let the VM idle-shutdown naturally
        after its configured timeout, which is the expected behavior.
        """
        logger.info(f"Disconnecting from cloud mobile: {self.cloud_mobile_name}")

        # Signal the keep-alive loop to stop
        self._stop_event.set()

        # Cancel and wait for keep-alive task
        if self._keep_alive_task and not self._keep_alive_task.done():
            self._keep_alive_task.cancel()
            try:
                await asyncio.wait_for(self._keep_alive_task, timeout=5.0)
            except TimeoutError:
                logger.warning("Keep-alive task did not stop in time")
            except asyncio.CancelledError:
                pass

        # Close HTTP session
        await self._close_session()

        # Clear the context
        set_cloud_mobile_id(None)
        self._mobile_id = None
        self._mobile_info = None

        logger.info("Cloud mobile disconnected (keep-alive stopped)")

    @property
    def mobile_id(self) -> str | None:
        """Get the cloud mobile UUID."""
        return self._mobile_id

    @property
    def mobile_info(self) -> VirtualMobileInfo | None:
        """Get the cloud mobile info."""
        return self._mobile_info

    @property
    def is_connected(self) -> bool:
        """Check if connected to a cloud mobile."""
        return self._mobile_id is not None


async def get_cloud_screenshot(mobile_id: str | None = None) -> bytes:
    """Get a screenshot from a cloud mobile device.

    GET /api/daas/virtual-mobiles/{id}/screenshot

    Args:
        mobile_id: The cloud mobile UUID. If None, uses the current context.

    Returns:
        Screenshot image bytes (PNG format).

    Raises:
        RuntimeError: If no cloud mobile is connected or screenshot fails.
    """
    target_id = mobile_id or get_cloud_mobile_id()

    if not target_id:
        raise RuntimeError(
            "No cloud mobile connected. "
            "Either provide a mobile_id or ensure CLOUD_MOBILE_NAME is set."
        )

    api_key = settings.MINITAP_API_KEY.get_secret_value() if settings.MINITAP_API_KEY else None
    if not api_key:
        raise RuntimeError("MINITAP_API_KEY is required for cloud screenshot.")

    base_url = settings.MINITAP_DAAS_API.rstrip("/")
    url = f"{base_url}/virtual-mobiles/{target_id}/screenshot"

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 404:
                raise RuntimeError(f"Cloud mobile '{target_id}' not found.")
            if response.status == 401:
                raise RuntimeError("Authentication failed for cloud screenshot.")
            if response.status == 403:
                raise RuntimeError(f"Access denied to cloud mobile '{target_id}'.")
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(
                    f"Failed to get cloud screenshot: HTTP {response.status} - {error_text}"
                )

            return await response.read()
