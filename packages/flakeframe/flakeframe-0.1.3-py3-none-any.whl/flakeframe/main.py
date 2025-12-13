# Main entry point
import json
import os
import sys
from configparser import ConfigParser
from flakeframe.ui import SettingsUI
from flakeframe.mapview import MapViewUI
from flakeframe.theme import ThemeHandler, Theme, Asset, ThemeUI

CONFIG_FILE = "flakeframe.json" # TODO: check if distributors break this
THEME_FILE = "flakeframe.themes"

def load_config(config):
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    else:
        config["DEFAULT"]["units_precip"] = "mm"
        config["DEFAULT"]["units_temp"] = "°C"
        config["DEFAULT"]["show_map"] = "Yes"

def save_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
        
def entry():
    config = ConfigParser()
    load_config(config)
    themes = ThemeHandler()
    themes.load_themefile(THEME_FILE)
    
    while True:
        ui = SettingsUI(config)
        result = ui.run()
        
        if result == "quit":
            break
        elif result == "themes":
            themeui = ThemeUI(themes)
            res = themeui.run_menu()
            if res == "quit":
                continue
            elif res is None:
                pass
            else:
                print("this shouldn't happen")
                input()
            
        elif result and isinstance(result, tuple):
            lat, lon = result
            save_config(config)
            mapview = MapViewUI(lat, lon, config)
            mapview.run()

if __name__ == "__main__":
    try:
        entry()
    except KeyboardInterrupt:
        sys.exit(0)