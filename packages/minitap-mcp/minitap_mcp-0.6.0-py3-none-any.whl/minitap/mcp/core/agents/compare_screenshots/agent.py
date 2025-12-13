import asyncio
import base64
from pathlib import Path
from uuid import uuid4

from jinja2 import Template
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel

from minitap.mcp.core.device import capture_screenshot, find_mobile_device
from minitap.mcp.core.llm import get_minitap_llm
from minitap.mcp.core.utils.images import get_screenshot_message_for_llm
from minitap.mcp.server.cloud_mobile import get_cloud_mobile_id, get_cloud_screenshot


class CompareScreenshotsOutput(BaseModel):
    comparison_text: str
    expected_screenshot_base64: str
    current_screenshot_base64: str


async def compare_screenshots(
    expected_screenshot_base64: str,
) -> CompareScreenshotsOutput:
    """
    Compare screenshots and return the comparison text along with both screenshots.

    Supports both local devices (Android/iOS) and cloud devices.

    Returns:
        CompareScreenshotsOutput
    """
    system_message = Template(
        Path(__file__).parent.joinpath("prompt.md").read_text(encoding="utf-8")
    ).render()

    cloud_mobile_id = get_cloud_mobile_id()

    if cloud_mobile_id:
        screenshot_bytes = await get_cloud_screenshot(cloud_mobile_id)
        current_screenshot = base64.b64encode(screenshot_bytes).decode("utf-8")
    else:
        device = find_mobile_device()
        current_screenshot = capture_screenshot(device)

    messages: list[BaseMessage] = [
        SystemMessage(content=system_message),
        HumanMessage(content="Here is the Figma screenshot (what needs to be matched):"),
        get_screenshot_message_for_llm(expected_screenshot_base64),
        HumanMessage(content="Here is the screenshot of the mobile device:"),
        get_screenshot_message_for_llm(current_screenshot),
    ]

    llm = get_minitap_llm(
        trace_id=str(uuid4()),
        remote_tracing=True,
        model="google/gemini-2.5-pro",
        temperature=1,
    )
    response = await llm.ainvoke(messages)
    return CompareScreenshotsOutput(
        comparison_text=str(response.content),
        expected_screenshot_base64=expected_screenshot_base64,
        current_screenshot_base64=current_screenshot,
    )


async def main():
    expected_screenshot_base64 = "Base64 encoded screenshot to compare with."
    result = await compare_screenshots(expected_screenshot_base64)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
