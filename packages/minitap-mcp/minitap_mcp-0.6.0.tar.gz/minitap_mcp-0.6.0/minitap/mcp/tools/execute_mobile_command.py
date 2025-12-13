"""Tool for running manual tasks on a connected mobile device."""

from collections.abc import Mapping
from typing import Any

from fastmcp.exceptions import ToolError
from minitap.mobile_use.sdk.types import ManualTaskConfig
from minitap.mobile_use.sdk.types.task import PlatformTaskRequest
from pydantic import Field

from minitap.mcp.core.cloud_apk import install_apk_on_cloud_mobile, upload_apk_to_cloud_mobile
from minitap.mcp.core.config import settings
from minitap.mcp.core.decorators import handle_tool_errors
from minitap.mcp.core.sdk_agent import get_mobile_use_agent
from minitap.mcp.main import mcp


def _serialize_result(result: Any) -> Any:
    """Convert SDK responses to serializable data for MCP."""
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if hasattr(result, "dict"):
        return result.dict()
    if isinstance(result, Mapping):
        return dict(result)
    return result


@mcp.tool(
    name="execute_mobile_command",
    description="""
    Execute a natural language command on a mobile device using the Minitap SDK.
    This tool allows you to control your Android or iOS device using natural language.
    
    Examples:
    - "Open the settings app and tell me the battery level"
    - "Find the first 3 unread emails in Gmail"
    - "Take a screenshot and save it"
    
    APK Deployment (Cloud Mobile Only):
    When CLOUD_MOBILE_NAME is set, you can deploy and test APKs on cloud mobiles:
    - Set apk_path to the path of your locally built APK
    - The APK will be uploaded to cloud storage and installed on the device
    - Requires MINITAP_API_KEY environment variable
    - Must provide locked_app_package when using apk_path
    
    Example with APK deployment:
    execute_mobile_command(
        apk_path="/path/to/app-debug.apk",
        locked_app_package="com.example.myapp",
        goal="Test the login flow with valid credentials"
    )
    
    Note: If apk path is set and no cloud mobile name -> it will raise a tool error
    """,
)
@handle_tool_errors
async def execute_mobile_command(
    goal: str = Field(description="High-level goal describing the action to perform."),
    output_description: str | None = Field(
        default=None,
        description="Optional description of the expected output format. "
        "For example: 'A JSON array with sender and subject for each email' "
        "or 'The battery percentage as a number'.",
    ),
    locked_app_package: str | None = Field(
        default=None,
        description="Optional package name of the app to lock the device to. "
        "Will launch the app if not already running, and keep it in foreground "
        "until the task is completed. REQUIRED when using apk_path.",
    ),
    apk_path: str | None = Field(
        default=None,
        description="Path to local APK file to deploy to cloud mobile. "
        "Only works when CLOUD_MOBILE_NAME is set. "
        "The APK will be uploaded to cloud storage and installed before task execution. "
        "Requires MINITAP_API_KEY to be configured. ",
    ),
) -> str | dict[str, Any]:
    """Run a manual task on a mobile device via the Minitap platform."""
    try:
        if apk_path:
            if not settings.CLOUD_MOBILE_NAME:
                raise ToolError(
                    "apk_path parameter requires CLOUD_MOBILE_NAME to be set. "
                    "APK deployment is only supported in cloud mobile mode."
                )

            # Step 1: Upload APK via Platform storage API
            filename = await upload_apk_to_cloud_mobile(apk_path=apk_path)

            # Step 2: Install APK on cloud mobile
            await install_apk_on_cloud_mobile(filename=filename)

        request = PlatformTaskRequest(
            task=ManualTaskConfig(
                goal=goal,
                output_description=output_description,
            ),
            execution_origin="mcp",
        )
        agent = get_mobile_use_agent()
        if not agent._initialized:
            await agent.init()
        result = await agent.run_task(
            request=request,
            locked_app_package=locked_app_package,
        )
        return _serialize_result(result)
    except Exception as e:
        raise ToolError(str(e))
