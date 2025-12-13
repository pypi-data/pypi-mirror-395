"""Device health monitoring poller for the MCP server."""

import asyncio
import logging
import threading

from minitap.mobile_use.sdk import Agent

from minitap.mcp.core.device import list_available_devices

logger = logging.getLogger(__name__)


async def _async_device_health_poller(stop_event: threading.Event, agent: Agent) -> None:
    """
    Async implementation of device health poller.

    Args:
        stop_event: Threading event to signal when to stop polling.
        agent: The Agent instance to monitor and reinitialize if needed.
    """
    while not stop_event.is_set():
        try:
            # Sleep in smaller chunks to be more responsive to stop signal
            for _ in range(50):  # 50 * 0.1 = 5 seconds total
                if stop_event.is_set():
                    break
                await asyncio.sleep(0.1)

            if stop_event.is_set():
                break

            devices = list_available_devices()

            if len(devices) > 0:
                if not agent._initialized:
                    logger.warning("Agent is not initialized. Initializing...")
                    await agent.init()
                    logger.info("Agent initialized successfully")
            else:
                logger.info("No mobile device found, retrying in 5 seconds...")

        except Exception as e:
            logger.error(f"Error in device health poller: {e}")

    try:
        if agent._initialized:
            await agent.clean(force=True)
            logger.info("Agent cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up agent: {e}")


def device_health_poller(stop_event: threading.Event, agent: Agent) -> None:
    """
    Background poller that monitors device availability and agent health.
    Runs every 5 seconds to ensure a device is connected and the agent is healthy.

    This is a sync wrapper that runs the async poller in a new event loop.

    Args:
        stop_event: Threading event to signal when to stop polling.
        agent: The Agent instance to monitor and reinitialize if needed.
    """
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(_async_device_health_poller(stop_event, agent))
    except Exception as e:
        logger.error(f"Error in device health poller thread: {e}")
    finally:
        if loop is not None:
            try:
                loop.close()
            except Exception:
                pass
