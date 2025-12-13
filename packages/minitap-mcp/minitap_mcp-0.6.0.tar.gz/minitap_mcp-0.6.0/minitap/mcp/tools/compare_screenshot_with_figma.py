"""Tool for navigating to a screen and comparing it with Figma design."""

import base64
from io import BytesIO

import mcp as mcp_ref
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from fastmcp.exceptions import ToolError
from fastmcp.tools.tool import ToolResult
from PIL import Image
from pydantic import Field

from minitap.mcp.core.agents.compare_screenshots.agent import compare_screenshots
from minitap.mcp.core.config import settings
from minitap.mcp.core.decorators import handle_tool_errors
from minitap.mcp.main import mcp


@mcp.tool(
    name="compare_screenshot_with_figma",
    description="""
    Compare a screenshot of the current state with a Figma design.
    
    This tool:
    1. Captures a screenshot of the current state (supports both local and cloud devices)
    2. Compares the live device screenshot with the Figma design
    3. Returns a detailed comparison report with both screenshots for visual context
    """,
)
@handle_tool_errors
async def compare_screenshot_with_figma(
    node_id: str = Field(
        description=(
            "The node ID of the Figma design. Expected format is ':' separated.\n"
            "Example: If given the URL https://figma.com/design/:fileKey/:fileName?node-id=1-2,\n"
            "the extracted nodeId would be 1:2. Strictly respect this format."
        )
    ),
) -> ToolResult:
    expected_screenshot_base64 = await get_figma_screenshot(node_id)

    result = await compare_screenshots(
        expected_screenshot_base64=expected_screenshot_base64,
    )

    compressed_expected = compress_image_base64(result.expected_screenshot_base64)
    compressed_current = compress_image_base64(result.current_screenshot_base64)

    return ToolResult(
        content=[
            mcp_ref.types.TextContent(
                type="text",
                text="## Comparison Analysis\n\n" + str(result.comparison_text),
            ),
            mcp_ref.types.ImageContent(
                type="image",
                data=compressed_expected,
                mimeType="image/jpeg",
            ),
            mcp_ref.types.TextContent(
                type="text",
                text="**Expected (Figma design)** ↑\n\n**Actual (Current device)** ↓",
            ),
            mcp_ref.types.ImageContent(
                type="image",
                data=compressed_current,
                mimeType="image/jpeg",
            ),
        ]
    )


def compress_image_base64(base64_str: str, max_width: int = 800, quality: int = 75) -> str:
    """Compress and resize a base64-encoded image to reduce size.

    Args:
        base64_str: Base64-encoded image string
        max_width: Maximum width for the resized image
        quality: JPEG quality (1-95, lower = smaller file)

    Returns:
        Compressed base64-encoded image string
    """
    try:
        img_data = base64.b64decode(base64_str)
        img = Image.open(BytesIO(img_data))

        if img.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if "A" in img.mode:
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        compressed_data = buffer.getvalue()

        return base64.b64encode(compressed_data).decode("utf-8")
    except Exception:
        return base64_str


async def get_figma_screenshot(node_id: str) -> str:
    try:
        async with Client(settings.FIGMA_MCP_SERVER_URL) as client:
            result: CallToolResult = await client.call_tool(
                "get_screenshot",
                {
                    "nodeId": node_id,
                    "clientLanguages": "javascript",
                    "clientFrameworks": "react",
                },
            )
            if len(result.content) == 0 or not isinstance(
                result.content[0], mcp_ref.types.ImageContent
            ):
                raise ToolError("Failed to fetch screenshot from Figma")
        return result.content[0].data
    except Exception as e:
        raise ToolError(f"Failed to fetch screenshot from Figma: {str(e)}")
