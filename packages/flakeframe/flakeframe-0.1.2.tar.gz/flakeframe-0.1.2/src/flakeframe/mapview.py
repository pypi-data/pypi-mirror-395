import sys
import shutil
import re
from datetime import date, datetime, time
from flakeframe.input import read_key
from flakeframe.map import render_map
from flakeframe.ui import clear, get_terminal_size
from flakeframe.weather import fetch_weather, WEATHER_CODES

def display_width(s):
    # regex by ai
    s = re.sub(r'\x1b\[[0-9;]*m', '', s)
    return len(s)

class MapViewUI:
    def __init__(self, lat, lon, config):
        self.lat = lat
        self.lon = lon
        self.config = config
        self.zoom = 14
        self.map_data = None
        self.weather_data = fetch_weather(self.lat, self.lon, self.config)
        
    def show_loading(self):
        clear()
        term_w, term_h = get_terminal_size()
        msg = "Loading... ☺"
        x = (term_w - len(msg)) // 2
        y = term_h // 2
        sys.stdout.write(f"\x1b[{y};{x}H{msg}")
        sys.stdout.flush()
        
    def draw_ui(self):
        clear()
        sys.stdout.write(self.map_data + "\n")
        term_w, term_h = get_terminal_size()
        rsc = "\x1b[0m"
        
        # weather box
        box_x = (term_w - 38) // 2
        box_y = 2
        c_time = self.weather_data.current.time.strftime("%I:%M %p")
        c_tempcol = "\x1b[0;38;2;255;100;0m" if self.weather_data.current.temperature > 0 else "\x1b[0;38;2;0;128;255m"
        
        sys.stdout.write(f"\x1b[{box_y    };{box_x}H ╭──────────────────────────────────────╮ ")
        sys.stdout.write(f"\x1b[{box_y + 1};{box_x}H │      {self.lat:+.2f}, {self.lon:+.2f} @ {c_time}       │ ")
        sys.stdout.write(f"\x1b[{box_y + 2};{box_x}H ╞══════╤═══════════════════════════════╡ ")
        
        condlen = display_width(self.weather_data.current.condition)
        cond = self.weather_data.current.condition + (" " * (29 - condlen))
        
        sys.stdout.write(f"\x1b[{box_y + 3};{box_x}H │ {c_tempcol}{int(self.weather_data.current.temperature):3}°{rsc} │ {cond} │ ")
        sys.stdout.write(f"\x1b[{box_y + 4};{box_x}H ├──────┴────────────┬──────────────────┤ ")
        sys.stdout.write(f"\x1b[{box_y + 5};{box_x}H │ {self.weather_data.current.wind_direction_deg:>3}° ({self.weather_data.current.wind_direction_str}) {self.weather_data.current.wind_speed_kmh:>4.0f}km/h │ {f"{self.weather_data.current.precipitation_mm:<.0f}mm precip":16} │ ")
        sys.stdout.write(f"\x1b[{box_y + 6};{box_x}H ╞══════╤════════════╧══════════════════╡ ")
        
        for i in range(5):
            current_time = datetime.now().hour
            
            h = self.weather_data.hourly[current_time + i + 1]
            h_time = h.time.strftime("%I%p").lower()
            h_tempcol = "\x1b[0;38;2;255;100;0m" if h.temperature > 0 else "\x1b[0;38;2;0;128;255m"
            h_temp = f"{h_tempcol}{int(h.temperature):3}°{rsc}"
            h_precip = f"{h.precipitation_mm:.0f}mm"
            h_line = f" {h_time} ┆ {h_temp} {h.condition}, {h_precip} "
            linelen = display_width(h_line)
            h_line = h_line + (" " * (38 - linelen))
            sys.stdout.write(f"\x1b[{box_y + 7 + i};{box_x}H │{h_line:<38}│ ")
            
        sys.stdout.write(f"\x1b[{box_y + 12};{box_x}H ╞══════╪═══════════════════════════════╡ ")
        
        for i in range(5):
            d = self.weather_data.daily[i+1]
            d_day = d.date.strftime("%a")
            d_lowcol = "\x1b[0;38;2;255;100;0m" if d.temp_min > 0 else "\x1b[0;38;2;0;128;255m"
            d_highcol = "\x1b[0;38;2;255;100;0m" if d.temp_max > 0 else "\x1b[0;38;2;0;128;255m"
            d_low = f"{d_lowcol}{int(d.temp_min)}{rsc}"
            d_high = f"{d_highcol}{int(d.temp_max)}{rsc}"
            d_precip = f"{d.precipitation_sum_mm:.0f}mm"
            d_line = f" {d_day}  ┆ {d_low} to {d_high}°, {d.condition}, {d_precip} "
            linelen = display_width(d_line)
            d_line = d_line + (" " * (38 - linelen))
            sys.stdout.write(f"\x1b[{box_y + 13 + i};{box_x}H │{d_line:<38}│ ")
        
        sys.stdout.write(f"\x1b[{box_y + 18};{box_x}H ╰──────┴───────────────────────────────╯ ")
        
        # controls
        controls = "\x1b[38;5;86m< \x1b[32m[+/-]\x1b[38;5;86m zoom | \x1b[32m[r]\x1b[38;5;86meload | \x1b[32m[esc/q]\x1b[38;5;86m back >"
        controls_visw = display_width(controls)
        controls_x = term_w - controls_visw - 4
        controls_y = term_h - 1
        sys.stdout.write(f"\x1b[{controls_y};{controls_x}H{controls}")
        sys.stdout.flush()
        
    def run(self):
        self.refresh_map()
        while True:
            key = read_key()
            if key in ("+", "="):
                self.zoom = min(18, self.zoom + 1)
                self.refresh_map()
            elif key == "-":
                self.zoom = max(1, self.zoom - 1)
                self.refresh_map()
            elif key == "r":
                self.weather_data = fetch_weather(self.lat, self.lon, self.config)
                self.draw_ui()
            elif key in ("esc", "q"):
                return
            
    def refresh_map(self):
        self.show_loading()
        self.map_data = render_map(self.lat, self.lon, self.zoom)
        self.draw_ui()