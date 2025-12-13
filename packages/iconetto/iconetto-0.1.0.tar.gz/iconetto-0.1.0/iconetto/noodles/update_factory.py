#!/usr/bin/env python3
from . import hex_to_rgb

def update_factory(factory, icon_settings):
    new_cfg ={
        'icon_size':icon_settings['-ICON_SIZE-'], 
        'font_size':icon_settings['-FONT_S-'],  
        'font_color':(*hex_to_rgb(icon_settings['-FONT_COLOR-'][0]),icon_settings['-FONT_COLOR-'][1]),
        'outline_color':(*hex_to_rgb(icon_settings['-OUTLINE_COLOR-'][0]),icon_settings['-OUTLINE_COLOR-'][1]),
        'outline_width':icon_settings['-OUTLINE_W-'],
        'background_color':(*hex_to_rgb(icon_settings['-BACKGROUND_COLOR-'][0]),icon_settings['-BACKGROUND_COLOR-'][1]), 
        'background_radius':icon_settings['-BACKGROUND_R-']
    }     
    factory.updateCfg(**new_cfg)