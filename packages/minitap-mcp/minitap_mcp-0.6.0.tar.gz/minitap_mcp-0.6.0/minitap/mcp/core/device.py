"""Device detection and screenshot utilities for Android and iOS devices."""

import base64
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Literal

from adbutils import AdbClient, AdbDevice
from pydantic import BaseModel, ConfigDict


DevicePlatform = Literal["android", "ios"]


class MobileDevice(BaseModel):
    """Represents a mobile device with its platform and connection details."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    device_id: str
    platform: DevicePlatform
    adb_device: AdbDevice | None = None  # Only for Android


class DeviceInfo(BaseModel):
    """Serializable device information."""

    device_id: str
    platform: DevicePlatform
    name: str | None = None
    state: str | None = None


class DeviceNotFoundError(Exception):
    """Raised when no device can be found."""

    pass


def get_adb_client() -> AdbClient:
    """Get an ADB client instance."""
    custom_adb_socket = os.getenv("ADB_SERVER_SOCKET")
    if not custom_adb_socket:
        return AdbClient()
    parts = custom_adb_socket.split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid ADB server socket: {custom_adb_socket}")
    _, host, port = parts
    return AdbClient(host=host, port=int(port))


def list_available_devices() -> list[DeviceInfo]:
    """
    List all available mobile devices (Android and iOS).

    Returns:
        list[DeviceInfo]: A list of device information objects.
    """
    devices: list[DeviceInfo] = []

    # List Android devices
    try:
        adb_client = get_adb_client()
        android_devices = adb_client.device_list()

        for device in android_devices:
            if device.serial:
                devices.append(
                    DeviceInfo(
                        device_id=device.serial,
                        platform="android",
                        name=device.serial,
                        state="connected",
                    )
                )
    except Exception:
        # ADB not available or error listing devices
        pass

    # List iOS devices
    try:
        cmd = ["xcrun", "simctl", "list", "devices", "-j"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        for runtime, ios_devices in data.get("devices", {}).items():
            if "iOS" not in runtime:
                continue

            for device in ios_devices:
                udid = device.get("udid")
                name = device.get("name")
                state = device.get("state")

                if udid:
                    devices.append(
                        DeviceInfo(
                            device_id=udid,
                            platform="ios",
                            name=name,
                            state=state,
                        )
                    )
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        # xcrun not available or error listing devices
        pass

    return devices


def find_mobile_device(device_id: str | None = None) -> MobileDevice:
    """
    Find a mobile device (Android via ADB or iOS via xcrun).

    Args:
        device_id: Optional device ID to target a specific device.
                   If None, returns the first available device.

    Returns:
        MobileDevice: A reference to the device with its platform information.

    Raises:
        DeviceNotFoundError: If no device is found or the specified device_id is not found.
    """
    # Get all available devices
    available_devices = list_available_devices()

    if not available_devices:
        raise DeviceNotFoundError(
            "No mobile device found. "
            "Make sure you have an Android device connected via ADB "
            "or an iOS simulator running."
        )

    # Find the target device
    target_device = None
    if device_id:
        # Look for specific device
        for dev in available_devices:
            if dev.device_id == device_id:
                target_device = dev
                break
        if not target_device:
            raise DeviceNotFoundError(
                f"Device with ID '{device_id}' not found. "
                "Make sure the device is connected and accessible via adb or xcrun."
            )
    else:
        # Prefer connected/booted devices first
        for dev in available_devices:
            if dev.state in ("connected", "Booted"):
                target_device = dev
                break
        # Fall back to any device if no connected/booted device found
        if not target_device:
            target_device = available_devices[0]

    # Create MobileDevice instance with platform-specific details
    if target_device.platform == "android":
        # For Android, get the AdbDevice reference
        try:
            adb_client = get_adb_client()
            adb_device = adb_client.device(serial=target_device.device_id)
            return MobileDevice(
                device_id=target_device.device_id,
                platform="android",
                adb_device=adb_device,
            )
        except Exception as e:
            raise DeviceNotFoundError(f"Failed to connect to Android device: {e}")
    else:
        # For iOS, just return the device info
        return MobileDevice(device_id=target_device.device_id, platform="ios")


def capture_screenshot(device: MobileDevice) -> str:
    """
    Capture a screenshot from the given mobile device.

    Args:
        device: MobileDevice instance returned by find_mobile_device()

    Returns:
        str: Base64-encoded screenshot image (PNG format)

    Raises:
        RuntimeError: If screenshot capture fails
    """
    if device.platform == "android":
        return _capture_android_screenshot(device)
    else:
        return _capture_ios_screenshot(device)


def _capture_android_screenshot(device: MobileDevice) -> str:
    """Capture screenshot from Android device using ADB."""
    if not device.adb_device:
        # Reconnect to device if not available
        adb_client = get_adb_client()
        adb_device = adb_client.device(serial=device.device_id)
        if not adb_device:
            raise RuntimeError(f"Android device {device.device_id} not found")
        device.adb_device = adb_device

    try:
        # Use ADB screencap to get PNG screenshot
        screenshot_bytes = device.adb_device.shell("screencap -p", encoding=None)
        if isinstance(screenshot_bytes, bytes):
            return base64.b64encode(screenshot_bytes).decode("utf-8")
        else:
            raise RuntimeError("Unexpected screenshot data type from ADB")
    except Exception as e:
        raise RuntimeError(f"Failed to capture Android screenshot: {e}")


def _capture_ios_screenshot(device: MobileDevice) -> str:
    """Capture screenshot from iOS simulator using xcrun."""
    try:
        # Create temporary file for screenshot
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Capture screenshot using xcrun simctl
            cmd = ["xcrun", "simctl", "io", device.device_id, "screenshot", str(tmp_path)]
            subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Read and encode the screenshot
            screenshot_bytes = tmp_path.read_bytes()
            return base64.b64encode(screenshot_bytes).decode("utf-8")
        finally:
            # Clean up temporary file
            if tmp_path.exists():
                tmp_path.unlink()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to capture iOS screenshot: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Failed to capture iOS screenshot: {e}")
