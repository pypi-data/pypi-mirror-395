"""Agent to extract Figma asset URLs from design context code using regex."""

import re

from pydantic import BaseModel, Field


class FigmaAsset(BaseModel):
    """Represents a single Figma asset."""

    variable_name: str = Field(description="The variable name from the code (e.g., imgSignal)")
    url: str = Field(description="The full URL to the asset")
    extension: str = Field(description="The file extension (e.g., svg, png, jpg)")


class ExtractedAssets(BaseModel):
    """Container for all extracted Figma assets."""

    assets: list[FigmaAsset] = Field(
        default_factory=list,
        description="List of all extracted assets from the Figma design context",
    )
    code_implementation: str = Field(
        description="The React/TypeScript code with imports instead of const declarations"
    )


def extract_figma_assets(design_context_code: str) -> ExtractedAssets:
    """Extract asset URLs from Figma design context code using regex.

    Args:
        design_context_code: The React/TypeScript code from get_design_context

    Returns:
        ExtractedAssets with list of assets and transformed code
    """
    # Regex captures: (1) variable name, (2) full URL, (4) extension
    # Supports http/https, any domain, query strings, optional semicolon
    pattern = r'const\s+(\w+)\s*=\s*["\']((https?://[^"\']+?)\.(\w+)(?:\?[^"\']*)?)["\'];?'
    matches = re.finditer(pattern, design_context_code)

    assets = []
    asset_lines = []

    for match in matches:
        var_name = match.group(1)
        url = match.group(2)
        extension = match.group(4)

        assets.append(FigmaAsset(variable_name=var_name, url=url, extension=extension))
        asset_lines.append(match.group(0))

    import_statements = []
    for asset in assets:
        import_statements.append(
            f"import {asset.variable_name} from './{asset.variable_name}.{asset.extension}';"
        )

    transformed_code = design_context_code
    for line in asset_lines:
        transformed_code = transformed_code.replace(line, "")

    lines = transformed_code.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)

    final_code = "\n".join(import_statements) + "\n\n" + "\n".join(lines)

    return ExtractedAssets(assets=assets, code_implementation=final_code)
