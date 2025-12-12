# Main entry point
import json
import os
from configparser import ConfigParser
from flakeframe.ui import SettingsUI
from flakeframe.mapview import MapViewUI

CONFIG_FILE = "flakeframe.json" # TODO: check if distributors break this

def load_config(config):
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    else:
        config["DEFAULT"]["units_precip"] = "mm"
        config["DEFAULT"]["units_temp"] = "°C"
        # config["DEFAULT"]["last_location"] = None

def save_config(config):
    # if os.path.exists(os.getcwd() / CONFIG_FILE):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
        
def entry():
    config = ConfigParser()
    load_config(config)
    
    # fallback
    # readline.set_completer(location_completer)
    # readline.parse_and_bind("tab: complete")
    
    while True:
        ui = SettingsUI(config)
        result = ui.run()
        
        if result == "quit":
            break
        elif result and isinstance(result, tuple):
            lat, lon = result
            #config["DEFAULT"]["last_location"] = { "lat": lat, "lon": lon }
            save_config(config)
            mapview = MapViewUI(lat, lon, config)
            mapview.run()

if __name__ == "__main__":
    entry()