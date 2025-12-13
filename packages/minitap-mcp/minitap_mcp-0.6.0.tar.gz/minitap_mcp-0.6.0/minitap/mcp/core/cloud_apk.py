"""Cloud APK deployment utilities for uploading and installing APKs on cloud mobiles."""

import uuid
from pathlib import Path

import httpx

from minitap.mcp.core.config import settings


async def upload_apk_to_cloud_mobile(apk_path: str) -> str:
    """
    Upload an APK file via Platform storage API to user storage bucket.

    Args:
        apk_path: Path to the APK file

    Returns:
        Filename to use with install-apk endpoint

    Raises:
        FileNotFoundError: If APK file doesn't exist
        httpx.HTTPError: If upload fails
        ValueError: If MINITAP_API_KEY or MINITAP_API_BASE_URL is not configured
    """
    if not settings.MINITAP_API_KEY:
        raise ValueError("MINITAP_API_KEY is not configured")
    if not settings.MINITAP_API_BASE_URL:
        raise ValueError("MINITAP_API_BASE_URL is not configured")

    apk_file = Path(apk_path)
    if not apk_file.exists():
        raise FileNotFoundError(f"APK file not found: {apk_path}")

    filename = f"app_{uuid.uuid4().hex[:6]}.apk"
    api_key = settings.MINITAP_API_KEY.get_secret_value()
    api_base_url = settings.MINITAP_API_BASE_URL.rstrip("/")

    async with httpx.AsyncClient(timeout=300.0) as client:
        # Step 1: Get signed upload URL from storage API
        response = await client.get(
            f"{api_base_url}/storage/signed-upload",
            headers={"Authorization": f"Bearer {api_key}"},
            params={"filenames": filename},
        )
        response.raise_for_status()
        upload_data = response.json()

        # Extract the signed URL for our file
        signed_urls = upload_data.get("signed_urls", {})
        if filename not in signed_urls:
            raise ValueError(f"No signed URL returned for {filename}")

        signed_url = signed_urls[filename]

        # Step 2: Upload APK to signed URL
        with open(apk_file, "rb") as f:
            upload_response = await client.put(
                signed_url,
                content=f.read(),
                headers={"Content-Type": "application/vnd.android.package-archive"},
            )
            upload_response.raise_for_status()

        # Step 3: Return filename for install-apk call
        return filename


async def install_apk_on_cloud_mobile(filename: str) -> None:
    """
    Install an APK on a cloud mobile device via mobile-manager API.

    Args:
        filename: Filename returned from upload_apk_to_cloud_mobile

    Raises:
        httpx.HTTPError: If installation fails
        ValueError: If required config settings are not configured
    """
    if not settings.MINITAP_API_KEY:
        raise ValueError("MINITAP_API_KEY is not configured")
    if not settings.MINITAP_DAAS_API:
        raise ValueError("MINITAP_DAAS_API is not configured")
    if not settings.CLOUD_MOBILE_NAME:
        raise ValueError("CLOUD_MOBILE_NAME is not configured")

    api_key = settings.MINITAP_API_KEY.get_secret_value()
    base_url = settings.MINITAP_DAAS_API
    cloud_mobile_name = settings.CLOUD_MOBILE_NAME

    async with httpx.AsyncClient(timeout=120.0) as client:
        cloud_mobile_response = await client.get(
            f"{base_url}/virtual-mobiles/{cloud_mobile_name}",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        cloud_mobile_response.raise_for_status()
        response_data = cloud_mobile_response.json()
        cloud_mobile_uuid = response_data.get("id")
        if not cloud_mobile_uuid:
            raise ValueError(f"Cloud mobile '{cloud_mobile_name}' response missing 'id' field")
        response = await client.post(
            f"{base_url}/virtual-mobiles/{cloud_mobile_uuid}/install-apk",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"filename": filename},
        )
        response.raise_for_status()
