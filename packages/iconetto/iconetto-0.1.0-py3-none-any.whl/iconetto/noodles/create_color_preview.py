#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageOps
import io

def create_rounded_color_preview(
    fill = "silver",
    width = 300,
    height = 24,
    outline = "grey",
    outline_width = 2,
    outline_radius = None,
    factor = 3,
):
    """Create and return a background image with rounded corners. Set the outline radius to size/2 to achieve a circular background."""
    if not outline_radius:
        outline_radius = height // 2
    im = Image.new("RGBA", (factor * width, factor * height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, "RGBA")
    draw.rounded_rectangle(
        (0, 0, factor * width, factor * height),
        radius=factor * outline_radius,
        outline=outline,
        fill=fill,
        width=factor * outline_width,
    )
    im = im.resize((width, height), Image.LANCZOS)
    
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr