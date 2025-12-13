"""Tool for fetching and saving Figma assets locally."""

import shutil
from pathlib import Path

import mcp as mcp_ref
import requests
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from fastmcp.exceptions import ToolError
from fastmcp.tools.tool import ToolResult
from pydantic import Field

from minitap.mcp.core.config import settings
from minitap.mcp.core.decorators import handle_tool_errors
from minitap.mcp.core.logging_config import get_logger
from minitap.mcp.core.models import (
    AssetDownloadResult,
    AssetDownloadSummary,
    DownloadStatus,
    FigmaDesignContextOutput,
)
from minitap.mcp.core.utils.figma import ExtractedAssets, FigmaAsset, extract_figma_assets
from minitap.mcp.main import mcp
from minitap.mcp.tools.compare_screenshot_with_figma import (
    compress_image_base64,
    get_figma_screenshot,
)

logger = get_logger(__name__)


@mcp.tool(
    name="save_figma_assets",
    description="""
    Fetch Figma design assets/react implementation code and save them locally in the workspace.
    
    This tool:
    1. Calls get_design_context from Figma MCP to get the React/TypeScript code
    2. Extracts asset URLs and transforms const declarations to import statements
    3. Downloads each asset to .mobile-use/figma_assets/<node-id>/ folder
    4. Saves the transformed code to .mobile-use/figma_assets/<node-id>/code_implementation.ts
    5. Returns a list of downloaded files
    """,
)
@handle_tool_errors
async def save_figma_assets(
    node_id: str = Field(
        description=(
            "The node ID of the Figma design. Expected format is ':' separated.\n"
            "Example: If given the URL https://figma.com/design/:fileKey/:fileName?node-id=1-2,\n"
            "the extracted nodeId would be 1:2. Strictly respect this format."
        )
    ),
    file_key: str = Field(
        description=(
            "The file key of the Figma file.\n"
            "Example: If given the URL https://figma.com/design/abc123/MyFile?node-id=1-2,\n"
            "the extracted fileKey would be 'abc123'."
        )
    ),
    workspace_path: str = Field(
        default=".",
        description=(
            "The workspace path where assets should be saved. Defaults to current directory."
        ),
    ),
) -> ToolResult:
    """Fetch and save Figma assets locally."""

    # Step 1: Get design context from Figma MCP
    design_context = await get_design_context(node_id, file_key)

    # Step 2: Extract asset URLs and transform code
    extracted_context: ExtractedAssets = extract_figma_assets(design_context.code_implementation)
    if not extracted_context.assets:
        raise ToolError("No assets found in the Figma design context.")

    # Step 3: Create directory structure
    # Convert node_id format (1:2) to folder name (1-2)
    folder_name = node_id.replace(":", "-")
    assets_dir = Path(workspace_path) / ".mobile-use" / "figma_assets" / folder_name

    # Delete existing directory to remove stale assets
    if assets_dir.exists():
        shutil.rmtree(assets_dir)

    # Create fresh directory
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Step 4: Download assets with resilient error handling
    download_summary = AssetDownloadSummary()

    for idx, asset in enumerate(extracted_context.assets, 1):
        logger.debug(
            "Downloading asset",
            idx=idx,
            total_count=len(extracted_context.assets),
            variable_name=asset.variable_name,
            extension=asset.extension,
        )
        result = download_asset(asset, assets_dir)
        if result.status == DownloadStatus.SUCCESS:
            logger.debug(
                "Asset downloaded successfully",
                idx=idx,
                variable_name=asset.variable_name,
                extension=asset.extension,
            )
            download_summary.successful.append(result)
        else:
            logger.debug(
                "Asset download failed",
                idx=idx,
                variable_name=asset.variable_name,
                extension=asset.extension,
                error=result.error,
            )
            download_summary.failed.append(result)

    # Step 4.5: Save code implementation
    code_implementation_file = assets_dir / "code_implementation.ts"

    commented_code_implementation_guidelines = ""
    if design_context.code_implementation_guidelines:
        commented_code_implementation_guidelines = "\n".join(
            ["// " + line for line in design_context.code_implementation_guidelines.split("\n")]
        )

    commented_nodes_guidelines = ""
    if design_context.nodes_guidelines:
        commented_nodes_guidelines = "\n".join(
            ["// " + line for line in design_context.nodes_guidelines.split("\n")]
        )

    code_implementation_file.write_text(
        extracted_context.code_implementation
        + "\n\n"
        + commented_code_implementation_guidelines
        + "\n\n"
        + commented_nodes_guidelines,
        encoding="utf-8",
    )

    # Step 5: Generate friendly output message
    result_parts = []

    if download_summary.successful:
        result_parts.append(
            f"✅ Successfully downloaded {download_summary.success_count()} asset(s) "
            f"to .mobile-use/figma_assets/{folder_name}/:\n"
        )
        for asset_result in download_summary.successful:
            result_parts.append(f"  • {asset_result.filename}")

    if download_summary.failed:
        result_parts.append(
            f"\n\n⚠️ Failed to download {download_summary.failure_count()} asset(s):"
        )
        for asset_result in download_summary.failed:
            error_msg = f": {asset_result.error}" if asset_result.error else ""
            result_parts.append(f"  • {asset_result.filename}{error_msg}")

    if code_implementation_file.exists():
        result_parts.append(
            f"\n\n✅ Successfully saved code implementation to {code_implementation_file.name}"
        )

    expected_screenshot = await get_figma_screenshot(node_id)
    compressed_expected = compress_image_base64(expected_screenshot)

    return ToolResult(
        content=[
            mcp_ref.types.TextContent(
                type="text",
                text="\n".join(result_parts),
            ),
            mcp_ref.types.TextContent(
                type="text",
                text="**Expected (Figma design)**",
            ),
            mcp_ref.types.ImageContent(
                type="image",
                data=compressed_expected,
                mimeType="image/jpeg",
            ),
        ]
    )


async def get_design_context(node_id: str, file_key: str) -> FigmaDesignContextOutput:
    """Fetch design context from Figma MCP server.

    Args:
        node_id: The Figma node ID in format "1:2"
        file_key: The Figma file key

    Returns:
        The React/TypeScript code as a string

    Raises:
        ToolError: If fetching fails
    """
    try:
        async with Client(settings.FIGMA_MCP_SERVER_URL) as client:
            result: CallToolResult = await client.call_tool(
                "get_design_context",
                {
                    "nodeId": node_id,
                    "fileKey": file_key,
                    "clientLanguages": "typescript",
                    "clientFrameworks": "react",
                },
            )

            code_implementation = ""
            code_implementation_guidelines = None
            nodes_guidelines = None

            if len(result.content) > 0 and isinstance(result.content[0], mcp_ref.types.TextContent):
                code_implementation = result.content[0].text
            else:
                raise ToolError("Failed to fetch design context from Figma")

            if len(result.content) > 1:
                if isinstance(result.content[1], mcp_ref.types.TextContent):
                    code_implementation_guidelines = result.content[1].text
            if len(result.content) > 2 and isinstance(result.content[2], mcp_ref.types.TextContent):
                nodes_guidelines = result.content[2].text

            return FigmaDesignContextOutput(
                code_implementation=code_implementation,
                code_implementation_guidelines=code_implementation_guidelines,
                nodes_guidelines=nodes_guidelines,
            )
    except Exception as e:
        raise ToolError(
            f"Failed to fetch design context from Figma: {str(e)}.\n"
            "Ensure the Figma MCP server is running through the official Figma desktop app."
        )


def download_asset(asset: FigmaAsset, assets_dir: Path) -> AssetDownloadResult:
    """Download a single asset with error handling.

    Args:
        asset: FigmaAsset model with variable_name, url, and extension
        assets_dir: Directory to save the asset

    Returns:
        AssetDownloadResult with status and optional error message
    """
    variable_name = asset.variable_name
    url = asset.url
    extension = asset.extension

    # Convert camelCase variable name to filename
    # e.g., imgSignal -> imgSignal.svg
    filename = f"{variable_name}.{extension}"
    filepath = assets_dir / filename

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filepath.write_bytes(response.content)
            return AssetDownloadResult(filename=filename, status=DownloadStatus.SUCCESS)
        else:
            return AssetDownloadResult(
                filename=filename,
                status=DownloadStatus.FAILED,
                error=f"HTTP {response.status_code}",
            )
    except requests.exceptions.Timeout:
        return AssetDownloadResult(filename=filename, status=DownloadStatus.FAILED, error="Timeout")
    except Exception as e:
        return AssetDownloadResult(filename=filename, status=DownloadStatus.FAILED, error=str(e))
