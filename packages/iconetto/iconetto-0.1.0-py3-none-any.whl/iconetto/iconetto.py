#!/usr/bin/env python3

##################################################
# Copyright (c) 2024 Björn Seipel, digidigital   #
# This program is released under the MIT license.#
# Details can be found in the LICENSE file or at:#
# https://opensource.org/licenses/MIT            #
##################################################

import os
import json
import random
import tkinter as tk

from .noodles import *
from iconipy import IconFactory
from PIL import Image
from dataclasses import dataclass

try:
    import FreeSimpleGUI as sg
except:
    import PySimpleGUI as sg # Tested with version 4.60    

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    '''iconetto app logic and UI'''
    
    def reset_icons(button_icons):
        for button_key, icons in button_icons.items():
            # Set all icon to the first one 
            window[button_key].update(button_icons[button_key][0]) 
            window[button_key].TooltipObject.leave()

    def color_pick_and_update(key):
        new_color = tk.colorchooser.askcolor(parent=window.TKroot, color=values[key])[1]
        if new_color:
            window[key].update(new_color)
            return new_color
        else: 
            return None    

    def plausibility_check(icon_settings):
        x,y = icon_settings['-ICON_SIZE-']
        smallest_dimension = x if x <= y else y
        max_radius = smallest_dimension // 2 
        
        for key in ('-BACKGROUND_R-', '-OUTLINE_W-'):
            window[key].update(range=(0,max_radius))
            window[key].update(max_radius if icon_settings[key] >= max_radius else icon_settings[key] )
        
        window['-FONT_S-'].update(range=(0,smallest_dimension))
        window['-FONT_S-'].update(smallest_dimension if icon_settings['-FONT_S-'] >= smallest_dimension else icon_settings['-FONT_S-']) 

    def save_icon(icon_name, dest_dir):
        filename = f"{icon_name}_{values['-POSTFIX-']}.{values['-EXPORT_AS-'].lower()}" if values['-POSTFIX-'] else f"{icon_name}.{values['-EXPORT_AS-'].lower()}" 
        iconetto_factory.save(icon_name, os.path.join(dest_dir, filename))
       
    # Class needed to provide coordinates for the TooltipObject later on    
    @dataclass
    class Coordinates:
        x: int = 0
        y: int = 0

    sg.theme('SystemDefault1')

    # Define default attributes that are valid for all icons in one central place
    default_icon_size = (80,26)
    default_font_size = 18
    default_radius = 12

    # Initialize icon factory with desired settings
    # Colors can be names or tuples (R, G, B, Alpha)
    create_icon = IconFactory(icon_set = 'lucide', 
                            icon_size = default_icon_size, 
                            font_size = default_font_size,  
                            font_color = (0, 0, 0, 255), # black solid
                            outline_color = 'dimgrey', 
                            outline_width = 2,
                            background_color = 'silver', 
                            background_radius = default_radius)

    create_mouseover_icon = IconFactory(icon_set = 'lucide', 
                            icon_size = default_icon_size, 
                            font_size = default_font_size,  
                            font_color = (255,255,255,255), # white solid
                            outline_color = 'silver', 
                            outline_width = 2,
                            background_color = 'dimgrey', 
                            background_radius = default_radius)

    app_icon = IconFactory(icon_set = 'lucide', 
                            icon_size = (64,64), 
                            font_size = 48,  
                            font_color = (0, 0, 0, 255), 
                            background_color = (0, 255, 0, 255), 
                            background_radius = 10)

    # Dictionary containing icon names for normal and mouseover state
    # Hint: The icon names for the icon set 'lucide' are listed here -> https://lucide.dev/icons/
    button_cfg ={
        '-LOAD_BUTTON-':('file-input', 'file-up', 'Load settings file'),
        '-SAVE_BUTTON-':('image','save', 'Export current icon and settings'),
        '-SAVEALL_BUTTON-':('images','save-all', 'Export icon set and settings'),
        '-INFO_BUTTON-':('info','book-open-text', 'About iconetto'), 
        '-EXIT_BUTTON-':('door-closed','door-open', 'Exit'),   
        '-COLORPICKER1_BUTTON-':('palette','pipette', 'Choose a color'),
        '-COLORPICKER2_BUTTON-':('palette','pipette', 'Choose a color'),
        '-COLORPICKER3_BUTTON-':('palette','pipette', 'Choose a color'),  
        }

    # Create the icons
    button_icons = {}
    for button_name, icon_names_and_tooltip in button_cfg.items():
        button_icons[button_name] = (create_icon.asBytes(icon_names_and_tooltip[0]), create_mouseover_icon.asBytes(icon_names_and_tooltip[1]), icon_names_and_tooltip[2])

    # Create button_row (will be added to layout in the next step)
    button_row=[]
    for button_name, icons in list(button_icons.items())[:5]:
        # Add one sg.Image for each button, set key to button name and enable events 
        button_row.append(sg.Image(icons[0], key = button_name, enable_events = True, tooltip = icons[2])) 

    # Create color picker buttons
    color_pickers=[]
    for button_name, icons in list(button_icons.items())[5:]:
        # Add one sg.Image for each button, set key to button name and enable events 
        color_pickers.append(sg.Image(icons[0], key = button_name, enable_events = True, tooltip = icons[2])) 

    # Icon settings
    icon_settings = {
        '-CFG_NAME-':get_salad(),
        '-ICON_SET-':'lucide', 
        '-ICON_NAME-':'sticker', 
        '-ICON_SIZE-':(80,34), 
        '-FONT_S-':24,  
        '-FONT_COLOR-':['#000000', 255],
        '-OUTLINE_COLOR-':['#666666', 255],
        '-OUTLINE_W-':3,
        '-BACKGROUND_COLOR-':['#bbbbbb', 255], 
        '-BACKGROUND_R-':17,
        '-POSTFIX-':'regular',
        '-EXPORT_AS-':'PNG'
    }

    available_icon_sets = IconFactory().icon_sets_available

    iconetto_factory = IconFactory(icon_set = icon_settings['-ICON_SET-'], 
                            icon_size = icon_settings['-ICON_SIZE-'] , 
                            font_size = icon_settings['-FONT_S-'] ,  
                            font_color = (*hex_to_rgb(icon_settings['-FONT_COLOR-'][0]),icon_settings['-FONT_COLOR-'][1]), 
                            outline_color = (*hex_to_rgb(icon_settings['-OUTLINE_COLOR-'][0]),icon_settings['-OUTLINE_COLOR-'][1]), 
                            outline_width = icon_settings['-OUTLINE_W-'],
                            background_color = (*hex_to_rgb(icon_settings['-BACKGROUND_COLOR-'][0]),icon_settings['-BACKGROUND_COLOR-'][1]), 
                            background_radius = icon_settings['-BACKGROUND_R-'])

    bg_img = Image.open(os.path.join(_SCRIPT_DIR, 'media', 'bg-image.png'))
    initial_image = overlay_image(bg_img, iconetto_factory.asPil(icon_settings['-ICON_NAME-']))
    max_font_size = icon_settings['-ICON_SIZE-'][0] if icon_settings['-ICON_SIZE-'][0] < icon_settings['-ICON_SIZE-'][1] else icon_settings['-ICON_SIZE-'][1]
    max_radius_and_outline = max_font_size // 2

    # GUI-Layout 
    layout = [
        [sg.Button('dummy', key='-DUMMYBUTTON-', enable_events=True, visible=False)],
        [sg.Frame('Icon', 
            [
                [sg.Text('Icon set:', size=16), sg.Combo(available_icon_sets, default_value='lucide', key='-ICON_SET-', enable_events=True, expand_x=True, readonly=True)],
                [
                sg.Text('Icon name:', size=16), sg.Combo(iconetto_factory.icon_names,default_value=icon_settings['-ICON_NAME-'], key='-ICON_NAME-', enable_events=True, readonly=True,  expand_x=True)],
                [sg.Text('Icon name filter:', size=16), sg.Input(key='-FILTER-', enable_events=True , expand_x=True), 
                
                ], 
                
                [sg.Text('Width:', size=11), sg.Text(icon_settings['-ICON_SIZE-'][0], key='-I_WIDTH-', size=3), sg.Slider(default_value=icon_settings['-ICON_SIZE-'][0], range=(1,512), resolution=1, key='-ICON_W-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
                ],
                [sg.Text('Height:', size=11), sg.Text(icon_settings['-ICON_SIZE-'][1], key='-I_HEIGHT-', size=3), sg.Slider(default_value=icon_settings['-ICON_SIZE-'][1], range=(1,512), resolution=1, key='-ICON_H-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
                ]
            ], expand_x=True, relief='solid', border_width=1,
        )],
        [sg.Frame('Font', 
            [
            [sg.Text('Color:', size=7), sg.InputText(default_text=icon_settings['-FONT_COLOR-'][0], key='-FONT_COLOR-', border_width=0, readonly=True, size=7, enable_events=True),
                sg.Image(data=create_rounded_color_preview(icon_settings['-FONT_COLOR-'][0], height=default_icon_size[1]), key='-FONT_COLOR_PREVIEW-', expand_x=True),
                color_pickers[0]     
            ],
            [ sg.Text('Transparency:', size=11), sg.Text(icon_settings['-FONT_COLOR-'][1], key='-F_ALPHA-', size=3), sg.Slider(default_value=icon_settings['-FONT_COLOR-'][1], range=(0,255), resolution=1, key='-FONT_A-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ],
            [ sg.Text('Size:', size=11), sg.Text(icon_settings['-FONT_S-'], key='-F_SIZE-', size=3), sg.Slider(default_value=icon_settings['-FONT_S-'], range=(0,max_font_size), resolution=1, key='-FONT_S-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ]
            ], expand_x=True, relief='solid', border_width=1,
        )],
        
        [sg.Frame('Background', 
            [
            [sg.Text('Color:', size=7), sg.Input(default_text=icon_settings['-BACKGROUND_COLOR-'][0], key='-BACKGROUND_COLOR-', border_width=0, readonly=True, size=7, enable_events=True),
                sg.Image(data=create_rounded_color_preview(icon_settings['-BACKGROUND_COLOR-'][0], height=default_icon_size[1]),key='-BACKGROUND_COLOR_PREVIEW-', expand_x=True),
                color_pickers[1]
            ],  
            [ sg.Text('Transparency:', size=11), sg.Text(icon_settings['-BACKGROUND_COLOR-'][1], key='-B_ALPHA-', size=3), sg.Slider(default_value=icon_settings['-BACKGROUND_COLOR-'][1], range=(0,255), resolution=1, key='-BACKGROUND_A-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ],
            [ sg.Text('Corner radius:', size=11), sg.Text(icon_settings['-BACKGROUND_R-'], key='-B_RADIUS-', size=3), sg.Slider(default_value=icon_settings['-BACKGROUND_R-'], range=(0,max_radius_and_outline), resolution=1, key='-BACKGROUND_R-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ]              
            ], expand_x=True, relief='solid', border_width=1, 
        )],    

        [sg.Frame('Outline',
            [
                [sg.Text('Color:', size=7), sg.InputText(default_text=icon_settings['-OUTLINE_COLOR-'][0], key='-OUTLINE_COLOR-', border_width=0, readonly=True, size=7, enable_events=True),
                sg.Image(data=create_rounded_color_preview(icon_settings['-OUTLINE_COLOR-'][0], height=default_icon_size[1]), key='-OUTLINE_COLOR_PREVIEW-', expand_x=True),
                color_pickers[2]
                ],
            [ sg.Text('Transparency:', size=11), sg.Text(icon_settings['-OUTLINE_COLOR-'][1], key='-O_ALPHA-', size=3), sg.Slider(default_value=icon_settings['-OUTLINE_COLOR-'][1], range=(0,255), resolution=1, key='-OUTLINE_A-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ],    
            [ sg.Text('Outline width:', size=11), sg.Text(icon_settings['-OUTLINE_W-'], key='-O_WIDTH-', size=3), sg.Slider(default_value=icon_settings['-OUTLINE_W-'], range=(0,max_radius_and_outline), resolution=1, key='-OUTLINE_W-', enable_events=True, orientation='h', disable_number_display=True, expand_x=True),        
            ],          
            ], expand_x=True, relief='solid', border_width=1,   
            
        )], 
        [sg.VPush()],
        [sg.Frame('Export settings', 
            [
                [sg.Text('Name of your design:'), sg.InputText(default_text=icon_settings['-CFG_NAME-'], key='-CFG_NAME-', enable_events=True, expand_x=True) ],
                [sg.Text('Icon filename postfix:'), sg.InputText(default_text=icon_settings['-POSTFIX-'], key='-POSTFIX-', enable_events=True, size=30), sg.Text('Export icons as:'), sg.Combo(['PNG', 'ICO', 'GIF', 'WebP'], default_value='PNG', key='-EXPORT_AS-', enable_events=True, expand_x=True)],
            ], expand_x=True, relief='solid', border_width=1, 
        )],             
    ]

    column_layout = [[sg.Image(data=initial_image, key='-PREVIEW-')]]

    window_layout = [button_row,
                    [sg.HorizontalSeparator()],
                    [sg.Column(layout, element_justification='center'), sg.Column(column_layout, expand_x=True, element_justification='center')]
    ]

    # Create Window
    window = sg.Window('iconetto', window_layout, size=(1200,650), element_justification='center', icon=app_icon.asBytes('sticker', image_format='PNG'), finalize=True)

    # Bind tkinter events to our buttons
    for button_key in button_cfg.keys():
        window[button_key].bind('<Enter>', 'mouse_enter')
        window[button_key].bind('<Leave>', 'mouse_leave')

    # Event loop
    while True:
        event, values = window.read()
        
        if event in (sg.WINDOW_CLOSED, '-EXIT_BUTTON-'):
            break
        
        # mouseover code      
        if '_BUTTON-' in event:
            if 'mouse' in event:
                button_key = event[:-11]    
                if 'mouse_leave' in event: # Set normal icon
                    window[button_key].update(button_icons[button_key][0])
                    window[button_key].TooltipObject.leave()
                elif 'mouse_enter' in event: # Set mouseover icon
                    window[button_key].update(button_icons[button_key][1])
                    window[button_key].TooltipObject.enter(Coordinates()) # Since we "hijacked" the <Enter>-event we need to activate the tooltip 
            else:
                # Tooltips & icons get stuck if file- or folderbrowse ist triggered by ".click()" since we get no <LEAVE>-event
                window[event].update(button_icons[event][0])
                window[event].TooltipObject.leave()
        
        # event matching  
        match event:
            case '-LOAD_BUTTON-':         
                open_file = tk.filedialog.askopenfilename(parent=window.TKroot, filetypes=[("iconetto files", "*.ifg")])
                if open_file:
                    try:
                        with open(open_file, "r") as file:
                            icon_settings=json.load(file)
                            
                            iconetto_factory.changeIconSet(icon_settings['-ICON_SET-'])
                            window['-ICON_NAME-'].update(values=iconetto_factory.icon_names, value=icon_settings['-ICON_NAME-'], size=(None,10))
                            
                            for key in ('-ICON_SET-','-FONT_S-', '-BACKGROUND_R-', '-CFG_NAME-', '-POSTFIX-', '-EXPORT_AS-', '-OUTLINE_W-'):
                                window[key].update(icon_settings[key])

                            for key in ('-FONT_COLOR-', '-OUTLINE_COLOR-', '-BACKGROUND_COLOR-'):
                                window[key].update(icon_settings[key][0])
                        
                            window['-ICON_W-'].update(icon_settings['-ICON_SIZE-'][0])
                            window['-ICON_H-'].update(icon_settings['-ICON_SIZE-'][1])
                            
                            window['-FONT_A-'].update(icon_settings['-FONT_COLOR-'][1])
                            window['-OUTLINE_A-'].update(icon_settings['-OUTLINE_COLOR-'][1])
                            window['-BACKGROUND_A-'].update(icon_settings['-BACKGROUND_COLOR-'][1])                    

                            window['-FONT_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(icon_settings['-FONT_COLOR-'][0], height=default_icon_size[1]))
                            window['-OUTLINE_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(icon_settings['-OUTLINE_COLOR-'][0], height=default_icon_size[1])) 
                            window['-BACKGROUND_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(icon_settings['-BACKGROUND_COLOR-'][0], height=default_icon_size[1]))

                            window['-FILTER-'].update('')     

                            plausibility_check(icon_settings) 
                            
                            window['-DUMMYBUTTON-'].click()
                    except Exception as e:
                        sg.popup_error('An error occured while loading the config file. Please check the file and try again.', keep_on_top=True, title='Load Error')
                continue   
                        
            case '-SAVE_BUTTON-':
                if not icon_settings['-ICON_NAME-']:
                    sg.popup_ok('Before you can save an icon you need to select one...', keep_on_top=True, title='No icon selected')
                    continue
                try:
                    save_dir = tk.filedialog.askdirectory(parent=window.TKroot)
                    if save_dir:
                        with open(os.path.join(save_dir, f"{values['-CFG_NAME-']}.ifg"), "w") as file:
                            json.dump(icon_settings, file, indent=4)
                        
                        save_icon(icon_settings['-ICON_NAME-'], save_dir)            
                except Exception as e:
                    sg.popup_error(f'An error occured while you tried to save an icon. {e}', keep_on_top=True, title='Save Error')
                continue
            
            case '-SAVEALL_BUTTON-':
                try:
                    saveall_dir = tk.filedialog.askdirectory(parent=window.TKroot)
                    if saveall_dir:
                        with open(os.path.join(saveall_dir, f"{values['-CFG_NAME-']}.ifg"), "w") as file:
                            json.dump(icon_settings, file, indent=4) 

                        window.TKroot.config(cursor='watch')
                        count=0
                        for icon_name in iconetto_factory.icon_names:
                            save_icon(icon_name, saveall_dir)    
                            window.refresh()
                            count+=1
                        window.TKroot.config(cursor='')

                        sg.popup_ok(f'{count} icons have been saved to {saveall_dir}.', keep_on_top=True, title='Ready')             
                except Exception as e:
                    sg.popup_error(f'An error occured while you tried to save an icon set. {e}', keep_on_top=True, title='Save Error')
                    window.TKroot.config(cursor='')
                continue
            
            case '-INFO_BUTTON-':
                sg.popup_ok("iconetto is a showcase app for the Python package iconipy and designed to create icons and buttons effortlessly. Developed in 2024 by Björn Seipel and published under the MIT license, iconetto includes a variety of open-source icon fonts that can be used without attribution in users' own applications. The GUI uses the FreeSimpleGUI or PySimpleGUI (4.60) package.\n\niconetto home: https://github.com/digidigital/iconetto\niconipy package @ PyPI: https://pypi.org/project/iconipy/", keep_on_top=True, title='About iconetto')
                continue
            
            case '-COLORPICKER1_BUTTON-':
                new_color=color_pick_and_update('-FONT_COLOR-')
                if new_color: 
                    window['-FONT_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(new_color, height=default_icon_size[1]))
            case '-COLORPICKER2_BUTTON-':
                new_color=color_pick_and_update('-BACKGROUND_COLOR-')
                if new_color:
                    window['-BACKGROUND_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(new_color, height=default_icon_size[1]))
            case '-COLORPICKER3_BUTTON-':
                new_color=color_pick_and_update('-OUTLINE_COLOR-') 
                if new_color:
                    window['-OUTLINE_COLOR_PREVIEW-'].update(data=create_rounded_color_preview(new_color, height=default_icon_size[1]))   
            
            case '-FILTER-':
                new_icon_list = [icon for icon in iconetto_factory.icon_names if values['-FILTER-'].lower().strip() in icon.lower()] 
                new_selection = new_icon_list[0] if len(new_icon_list) else None
                icon_settings['-ICON_NAME-']=new_selection
                window['-ICON_NAME-'].update(values=new_icon_list, value=new_selection, size=(None,10))
                window['-DUMMYBUTTON-'].click()
            
            case '-ICON_SET-':
                icon_settings['-ICON_SET-']=values['-ICON_SET-']
                iconetto_factory.changeIconSet(values['-ICON_SET-'])
                random_icon=random.choice(iconetto_factory.icon_names)
                window['-ICON_NAME-'].update(values=iconetto_factory.icon_names, value=random_icon, size=(None,10))
                icon_settings['-ICON_NAME-']=random_icon
                window['-FILTER-'].update(value='')
                window['-DUMMYBUTTON-'].click()

            case event if event in ('-CFG_NAME-', '-POSTFIX-', '-EXPORT_AS-', '-ICON_NAME-'):
                icon_settings[event]=values[event]
            
            case event if event in ('-FONT_S-', '-BACKGROUND_R-', '-OUTLINE_W-'):
                icon_settings[event]=int(values[event])
                
        # Update ALL sliders    
        window['-F_ALPHA-'].update(int(values['-FONT_A-']))
        window['-B_ALPHA-'].update(int(values['-BACKGROUND_A-']))
        window['-O_ALPHA-'].update(int(values['-OUTLINE_A-']))
        window['-F_SIZE-'].update(int(values['-FONT_S-']))
        window['-B_RADIUS-'].update(int(values['-BACKGROUND_R-']))
        window['-O_WIDTH-'].update(int(values['-OUTLINE_W-']))
        window['-I_WIDTH-'].update(int(values['-ICON_W-']))
        window['-I_HEIGHT-'].update(int(values['-ICON_H-']))    
        
        # Update settings dict of remaining UI elements   
        icon_settings['-ICON_SIZE-'] = (int(values['-ICON_W-']), int(values['-ICON_H-']))
        icon_settings['-FONT_COLOR-'] = (values['-FONT_COLOR-'],int(values['-FONT_A-']))
        icon_settings['-OUTLINE_COLOR-'] = (values['-OUTLINE_COLOR-'],int(values['-OUTLINE_A-']))
        icon_settings['-BACKGROUND_COLOR-'] = (values['-BACKGROUND_COLOR-'],int(values['-BACKGROUND_A-']))

        # Triggers -FONT_S-, -BACKGROUND_R- or -OUTLINE_W- events if necessary by changing the values
        # TODO skip redraw if a value was adjusted - redraw will happen with adjusted values in the next cycle
        plausibility_check(icon_settings)
            
        update_factory(iconetto_factory, icon_settings)

        try:
            redraw_image = overlay_image(bg_img, iconetto_factory.asPil(values['-ICON_NAME-']))
            window['-PREVIEW-'].update(data=redraw_image)
        except ValueError:
            # Icon name not found
            pass
        
    # Close window
    window.close()

if __name__ == "__main__":
    main()