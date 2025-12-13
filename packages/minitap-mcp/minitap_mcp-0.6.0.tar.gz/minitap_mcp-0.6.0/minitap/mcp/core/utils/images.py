import base64
from PIL import Image
from io import BytesIO

from langchain_core.messages import HumanMessage


def compress_base64_jpeg(base64_str: str, quality: int = 50) -> str:
    """
    Compress a base64-encoded image to JPEG format.

    Args:
        base64_str: Base64-encoded image string
        quality: JPEG quality (0-100, default 50)

    Returns:
        Base64-encoded JPEG image
    """
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]

    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))

    # Convert RGBA/LA/PA to RGB (JPEG doesn't support transparency)
    if image.mode in ("RGBA", "LA", "PA"):
        # Create a white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        # Paste the image on the background using alpha channel as mask
        if image.mode == "RGBA":
            background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
        else:
            background.paste(image, mask=image.split()[1])  # Use alpha for LA
        image = background
    elif image.mode != "RGB":
        # Convert any other mode to RGB
        image = image.convert("RGB")

    compressed_io = BytesIO()
    image.save(compressed_io, format="JPEG", quality=quality, optimize=True)

    compressed_base64 = base64.b64encode(compressed_io.getvalue()).decode("utf-8")
    return compressed_base64


def get_screenshot_message_for_llm(screenshot_base64: str):
    prefix = "" if screenshot_base64.startswith("data:image") else "data:image/jpeg;base64,"
    return HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": f"{prefix}{screenshot_base64}"},
            }
        ]
    )
