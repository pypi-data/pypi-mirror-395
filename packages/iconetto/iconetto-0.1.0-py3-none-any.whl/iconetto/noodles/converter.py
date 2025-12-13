#!/usr/bin/env python3

def hex_to_rgb(hex_color: str) -> tuple:
    '''Coverts a hex color string (#RRGGBB) to RGB tuple (R, G, B)'''
    if not isinstance(hex_color, str) or not hex_color.startswith('#') or len(hex_color) != 7:
        raise ValueError("Input must be a hex color string in the format '#RRGGBB'")
    
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError("Input must be a valid hex color string")
    
    
def rgb_to_hex(rgb: tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])    