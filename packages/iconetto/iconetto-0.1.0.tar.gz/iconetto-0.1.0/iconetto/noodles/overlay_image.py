#!/usr/bin/env python3
from PIL import Image
from io import BytesIO

def overlay_image(bg_img, overlay_img):
    # Background image dimensions   
    bg_width, bg_height = bg_img.size

    # Overlay image_dimensions
    overlay_width, overlay_height = overlay_img.size

    # Center the overlay image
    x_offset = (bg_width - overlay_width) // 2
    y_offset = (bg_height - overlay_height) // 2

    # Create the new image
    new_img = Image.new("RGBA", (bg_width, bg_height))
    new_img.paste(bg_img, (0, 0))
    new_img.paste(overlay_img, (x_offset, y_offset), overlay_img)

    # Return the new image as bytes
    with BytesIO() as output:
        new_img.save(output, 'PNG')
        return output.getvalue()
    return new_img