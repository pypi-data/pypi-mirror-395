from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext
from minitap.mobile_use.sdk import Agent


class LocalDeviceHealthMiddleware(Middleware):
    """Middleware that checks local device health before tool calls.

    Only used in local mode (when CLOUD_MOBILE_NAME is not set).
    For cloud mode, device health is managed by the cloud service.
    """

    def __init__(self, agent: Agent):
        self.agent = agent

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        if not self.agent._initialized:
            raise ToolError(
                "Agent not initialized.\nMake sure a mobile device is connected and try again."
            )
        return await call_next(context)
