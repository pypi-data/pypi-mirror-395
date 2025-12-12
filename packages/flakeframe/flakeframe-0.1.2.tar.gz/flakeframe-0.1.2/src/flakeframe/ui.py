import sys
import shutil
import json
from flakeframe.input import read_key
from flakeframe.geocode import validate_input_live, parse_coordinates

CONFIG_FILE = "flakeframe.json"

BOX_WIDTH = 64
BOX_HEIGHT = 12

COLOR_RESET = ""
COLOR_HIGHLIGHT = "----> "
COLOR_SELECTED = "> "
COLOR_PROMPT = ""


def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

def get_terminal_size():
    return shutil.get_terminal_size((80, 24))

class SettingsUI:
    def __init__(self, config):
        self.options = [
            {"name": "units_precip", "label": "Distance Units"   , "states": ["mm", "inch"], "value": config["DEFAULT"]["units_precip"]},
            {"name": "units_temp"  , "label": "Temperature Units", "states": ["°C", "°F"  ], "value": config["DEFAULT"]["units_temp"]},
            {"name": "search", "label": "Search Locations" , "states": None          , "value": None},
            {"name": "quit"  , "label": "Quit"             , "states": None          , "value": None},
        ]
        self.current_option = 0
        self.search_mode = False
        self.search_input = ""
        self.suggestions = []
        self.selected_sugg = 0
        self.config = config
    
    def draw_ui(self):
        clear()
        lines = [
            "flakeframe | setup",
            ""
        ]
        
        for i, opt in enumerate(self.options[:]):
            highlight = COLOR_HIGHLIGHT if i == self.current_option and not self.search_mode else ""
            if opt["states"]:
                state_idx = opt["states"].index(opt["value"])
                states_str = " | ".join(
                    COLOR_SELECTED + s + COLOR_RESET if j == state_idx else s
                    for j, s in enumerate(opt["states"])
                )
                lines.append(f"{highlight}  {opt["label"]}: {states_str}{COLOR_RESET}")
            else:
                lines.append(f"{highlight}  {opt["label"]}{COLOR_RESET}")
        
        draw_box(lines)
        
        if self.search_mode:
            term_w, term_h = get_terminal_size()
            box_x = (term_w - BOX_WIDTH) // 2
            box_y = (term_h - BOX_HEIGHT) // 2
            
            prompt_y = box_y + 7
            status_y = prompt_y + 2
            
            prompt = f"{COLOR_PROMPT}Coordinates or location >... {self.search_input}{COLOR_RESET}"
            sys.stdout.write(f"\x1b[{prompt_y};{box_x + 3}H{prompt.ljust(BOX_WIDTH - 6)}")
            
            is_valid, lat, lon, status = validate_input_live(self.search_input)
            color = "\x1b[32m" if is_valid else "\x1b[31m"
            sys.stdout.write(f"\x1b[{status_y};{box_x + 3}H{color}{status}{COLOR_RESET}")
                
            cursor_x = box_x + 3 + len("Coordinates or location >... ") + len(self.search_input)
            sys.stdout.write(f"\x1b[{prompt_y};{cursor_x}H")
            sys.stdout.flush()
                
    def run(self):
        self.draw_ui()
        
        while True:
            key = read_key()
            
            if not self.search_mode:
                # nav mode
                if key in ("w", "up"):
                    self.current_option = max(0, self.current_option - 1)
                elif key in ("s", "down"):
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)
                elif key in ("a", "left"):
                    self.toggle_state(-1)
                elif key in ("d", "right"):
                    self.toggle_state(1)
                elif key == "enter":
                    if self.options[self.current_option]["name"] == "search":
                        self.search_mode = True
                    elif self.options[self.current_option]["name"] == "quit":
                        return "quit"
                
            else:
                # search mode
                if key == "esc":
                    self.search_mode  = False
                    self.search_input = ""
                elif key == "backspace":
                    self.search_input = self.search_input[:-1]
                elif len(key) == 1 and key.isprintable():
                    self.search_input += key
                elif key == "enter":
                    lat, lon = parse_coordinates(self.search_input, final = True)
                    if lat and lon:
                        self.search_mode = False
                        self.search_input = ""
                        return (lat, lon)
                    
            self.draw_ui()
    
    def toggle_state(self, direction):
        opt = self.options[self.current_option]
        if opt["states"]:
            idx = opt["states"].index(opt["value"])
            new_idx = (idx + direction) % len(opt["states"])
            opt["value"] = opt["states"][new_idx]
            self.config["DEFAULT"][opt["name"]] = opt["value"]
            save_config(self.config) # noqa - from MAIN.PY
        
def draw_box(lines):
    clear()
    term_width, term_height = get_terminal_size()
    start_x = (term_width - BOX_WIDTH) // 2
    start_y = (term_height - BOX_HEIGHT) // 2
    
    sys.stdout.write(f"\x1b[{start_y};{start_x}H")
    sys.stdout.write("╭" + "─" * (BOX_WIDTH - 2) + "╮\n")
    
    content_height = BOX_HEIGHT - 2
    for i in range(content_height):
        y = start_y + 1 + i
        if i < len(lines):
            padded = lines[i].center(BOX_WIDTH - 2)
            sys.stdout.write(f"\x1b[{y};{start_x}H│{padded}│")
        else:
            sys.stdout.write(f"\x1b[{y};{start_x}H│{" " * (BOX_WIDTH - 2)}│")
            
    bottom_y = start_y + BOX_HEIGHT - 1
    sys.stdout.write(f"\x1b[{bottom_y};{start_x}H╰" + "─" * (BOX_WIDTH - 2) + "╯")
    sys.stdout.flush()
    
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        config.write(f)