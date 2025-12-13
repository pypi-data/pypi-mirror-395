"""MCP server for mobile-use with screen analysis capabilities."""

import argparse
import os
import sys
import threading
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

# Fix Windows console encoding for Unicode characters (emojis in logs)
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    os.environ["PYTHONIOENCODING"] = "utf-8"

    try:
        import colorama

        colorama.init(strip=False, convert=True, wrap=True)
    except ImportError:
        pass


from fastmcp import FastMCP  # noqa: E402
from minitap.mobile_use.config import settings as sdk_settings

from minitap.mcp.core.config import settings  # noqa: E402
from minitap.mcp.core.device import (
    DeviceInfo,  # noqa: E402
    list_available_devices,
)
from minitap.mcp.core.logging_config import (
    configure_logging,  # noqa: E402
    get_logger,
)
from minitap.mcp.server.cloud_mobile import CloudMobileService
from minitap.mcp.server.middleware import LocalDeviceHealthMiddleware
from minitap.mcp.server.poller import device_health_poller

configure_logging(log_level=os.getenv("LOG_LEVEL", "INFO"))


def main() -> None:
    """Main entry point for the MCP server."""

    parser = argparse.ArgumentParser(description="Mobile Use MCP Server")
    parser.add_argument(
        "--api-key",
        type=str,
        required=False,
        default=None,
        help="Minitap API key for authentication",
    )
    parser.add_argument(
        "--cloud-mobile-name",
        type=str,
        required=False,
        default=None,
        help="Name of the cloud mobile device to connect to (enables cloud mode)",
    )
    parser.add_argument("--llm-profile", type=str, required=False, default=None)
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run as network server (uses MCP_SERVER_HOST and MCP_SERVER_PORT from env)",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=False,
        default=None,
        help="Port to run the server on (overrides MCP_SERVER_PORT env variable)",
    )

    args = parser.parse_args()

    if args.api_key:
        os.environ["MINITAP_API_KEY"] = args.api_key
        settings.__init__()
        sdk_settings.__init__()

    if args.cloud_mobile_name:
        os.environ["CLOUD_MOBILE_NAME"] = args.cloud_mobile_name
        settings.__init__()
        sdk_settings.__init__()

    if args.llm_profile:
        os.environ["MINITAP_LLM_PROFILE_NAME"] = args.llm_profile
        settings.__init__()
        sdk_settings.__init__()

    if args.port:
        os.environ["MCP_SERVER_PORT"] = str(args.port)
        settings.__init__()
        sdk_settings.__init__()

    if not settings.MINITAP_API_KEY:
        raise ValueError("Minitap API key is required to run the MCP")

    # Run MCP server with optional host/port for remote access
    if args.server:
        logger.info(f"Starting MCP server on {settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}")
        run_mcp_server(
            transport="http",
            host=settings.MCP_SERVER_HOST,
            port=settings.MCP_SERVER_PORT,
        )
    else:
        logger.info("Starting MCP server in local mode")
        run_mcp_server()


logger = get_logger(__name__)


@dataclass
class MCPLifespanContext:
    """Context for MCP server lifespan.

    Stores references to services that need cleanup on shutdown.
    """

    cloud_mobile_service: CloudMobileService | None = None
    local_poller_stop_event: threading.Event | None = None
    local_poller_thread: threading.Thread | None = None


@asynccontextmanager
async def mcp_lifespan(server: FastMCP) -> AsyncIterator[MCPLifespanContext]:
    """Lifespan context manager for MCP server.

    Handles startup/shutdown for both cloud and local modes.

    Cloud mode (CLOUD_MOBILE_NAME set):
    - Connects to cloud mobile on startup
    - Maintains keep-alive polling
    - Disconnects on shutdown (critical for billing!)

    Local mode (CLOUD_MOBILE_NAME not set):
    - Starts device health poller
    - Monitors local device connection

    Args:
        server: The FastMCP server instance.

    Yields:
        MCPLifespanContext with references to running services.

    Raises:
        RuntimeError: If cloud mobile connection fails
            (crashes MCP to prevent false "connected" state).
    """
    from minitap.mcp.core.sdk_agent import get_mobile_use_agent  # noqa: E402

    context = MCPLifespanContext()
    api_key = settings.MINITAP_API_KEY.get_secret_value() if settings.MINITAP_API_KEY else None

    # Check if running in cloud mode
    if settings.CLOUD_MOBILE_NAME:
        # ==================== CLOUD MODE ====================
        logger.info(f"Starting MCP in CLOUD mode with mobile: {settings.CLOUD_MOBILE_NAME}")

        if not api_key:
            logger.error("MINITAP_API_KEY is required")
            raise RuntimeError(
                "MINITAP_API_KEY is required when CLOUD_MOBILE_NAME is set. "
                "Please set your API key via --api-key or MINITAP_API_KEY environment variable."
            )

        # Create and connect cloud mobile service
        cloud_service = CloudMobileService(
            cloud_mobile_name=settings.CLOUD_MOBILE_NAME,
            api_key=api_key,
        )

        try:
            await cloud_service.connect()
        except Exception as e:
            # CRITICAL: If cloud mobile not found, crash the MCP!
            # This prevents the IDE from showing the server as "connected"
            # when it actually can't do anything useful.
            logger.error(f"Failed to connect to cloud mobile: {e}")
            raise RuntimeError(
                f"Cloud mobile connection failed. The MCP server cannot start.\n{e}"
            ) from e

        context.cloud_mobile_service = cloud_service
        logger.info("Cloud mobile connected, MCP server ready")

    else:
        # ==================== LOCAL MODE ====================
        logger.info("Starting MCP in LOCAL mode (no CLOUD_MOBILE_NAME set)")

        agent = get_mobile_use_agent()
        server.add_middleware(LocalDeviceHealthMiddleware(agent))

        # Start device health poller in background
        stop_event = threading.Event()
        poller_thread = threading.Thread(
            target=device_health_poller,
            args=(stop_event, agent),
            daemon=True,
        )
        poller_thread.start()

        context.local_poller_stop_event = stop_event
        context.local_poller_thread = poller_thread
        logger.info("Device health poller started")

    try:
        yield context
    finally:
        # ==================== SHUTDOWN ====================
        logger.info("MCP server shutting down, cleaning up resources...")

        if context.cloud_mobile_service:
            # CRITICAL: Stop cloud mobile connection to stop billing!
            logger.info("Disconnecting cloud mobile (stopping billing)...")
            try:
                await context.cloud_mobile_service.disconnect()
                logger.info("Cloud mobile disconnected successfully")
            except Exception as e:
                logger.error(f"Error disconnecting cloud mobile: {e}")

        if context.local_poller_stop_event and context.local_poller_thread:
            # Stop local device health poller
            logger.info("Stopping device health poller...")
            context.local_poller_stop_event.set()
            context.local_poller_thread.join(timeout=10.0)

            if context.local_poller_thread.is_alive():
                logger.warning("Device health poller thread did not stop gracefully")
            else:
                logger.info("Device health poller stopped successfully")

        logger.info("MCP server shutdown complete")


# Create MCP server with lifespan handler
mcp = FastMCP(
    name="mobile-use-mcp",
    instructions="""
        This server provides analysis tools for connected
        mobile devices (iOS or Android).
        Call get_available_devices() to list them.
    """,
    lifespan=mcp_lifespan,
)

from minitap.mcp.tools import analyze_screen  # noqa: E402, F401
from minitap.mcp.tools import compare_screenshot_with_figma  # noqa: E402, F401
from minitap.mcp.tools import execute_mobile_command  # noqa: E402, F401
from minitap.mcp.tools import save_figma_assets  # noqa: E402, F401


@mcp.resource("data://devices")
def get_available_devices() -> list[DeviceInfo]:
    """Provides a list of connected mobile devices (iOS or Android)."""
    return list_available_devices()


def run_mcp_server(**mcp_run_kwargs):
    """Run the MCP server with proper exception handling.

    This wraps mcp.run() with exception handling for clean shutdown.
    """
    try:
        mcp.run(**mcp_run_kwargs)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        raise
