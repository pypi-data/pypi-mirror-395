"""Core models for the MCP server."""

from enum import Enum

from pydantic import BaseModel, Field


class FigmaAsset(BaseModel):
    """Represents a single Figma asset."""

    variable_name: str = Field(description="The variable name from the code (e.g., imgSignal)")
    url: str = Field(description="The full URL to the asset")
    extension: str = Field(description="The file extension (e.g., svg, png, jpg)")


class FigmaDesignContextOutput(BaseModel):
    """Output from Figma design context containing code and guidelines."""

    code_implementation: str = Field(description="The React/TypeScript code implementation")
    code_implementation_guidelines: str | None = Field(
        default=None, description="Guidelines for implementing the code"
    )
    nodes_guidelines: str | None = Field(
        default=None, description="Guidelines specific to the nodes"
    )


class DownloadStatus(str, Enum):
    """Status of asset download operation."""

    SUCCESS = "success"
    FAILED = "failed"


class AssetDownloadResult(BaseModel):
    """Result of downloading a single asset."""

    filename: str = Field(description="The filename of the asset")
    status: DownloadStatus = Field(description="The download status")
    error: str | None = Field(default=None, description="Error message if download failed")


class AssetDownloadSummary(BaseModel):
    """Summary of all asset download operations."""

    successful: list[AssetDownloadResult] = Field(
        default_factory=list, description="List of successfully downloaded assets"
    )
    failed: list[AssetDownloadResult] = Field(
        default_factory=list, description="List of failed asset downloads"
    )

    def success_count(self) -> int:
        """Return the number of successful downloads."""
        return len(self.successful)

    def failure_count(self) -> int:
        """Return the number of failed downloads."""
        return len(self.failed)
