import requests
import re
import threading
import time
from functools import lru_cache

_current_search_text = ""
_current_search_lock = threading.Lock()
_last_suggestions = []

def _search_worker(text):
    global _last_suggestions
    time.sleep(0.1)
    if text != _current_search_text:
        return
        # another request finished and superseded this one, which took unusually long
    suggestions = suggest_locations(text)
    with _current_search_lock:
        _last_suggestions = suggestions
        
def trigger_async_search(text):
    global _current_search_text
    with _current_search_lock:
        _current_search_text = text
    threading.Thread(target = _search_worker, args = (text,), daemon = True).start()
    
def get_current_suggestions():
    with _current_search_lock:
        return _last_suggestions[:]

def parse_lat_long(input_str):
    # DECIMAL (regex by AI. I cannot be bothered to learn regex)
    dec_pattern = r'^[-+]?[0-9]*\.?[0-9]+\s*,?\s*[-+]?[0-9]*\.?[0-9]+\s*$'
    decimal_match = re.match(dec_pattern, input_str.replace("°", "").replace("'", "").replace('"', ""))
    if decimal_match:
        parts = re.split(r'[\s,]+', input_str)
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
        except Exception:
            pass
    
    # DEGREES/MINUTES/SECONDS
    dms_pattern = r'''
        (\d{1,3})°\s*          # degrees
        (\d{1,2})[′′′']?\s*    # minutes (allow prime symbols)
        ([\d.]+)[″″""]?\s*     # seconds (allow decimal and double quotes)
        ([NSEW])               # hemisphere
        \s*,?\s*
        (\d{1,3})°\s*
        (\d{1,2})[′′′']?\s*
        ([\d.]+)[″″""]?\s*
        ([NSEW])
    '''
    
    match = re.search(dms_pattern, input_str, re.IGNORECASE | re.VERBOSE)
    if match:
        try:
            lat_deg = float(match.group(1))
            lat_min = float(match.group(2))
            lat_sec = float(match.group(3))
            lat_dir = match.group(4).upper()
            
            lon_deg = float(match.group(5))
            lon_min = float(match.group(6))
            lon_sec = float(match.group(7))
            lon_dir = match.group(8).upper()
            
            lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
            lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)
            
            if lat_dir == "S":
                lat = -lat
            if lon_dir == "W":
                lon = -lon
                
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            
        except Exception:
            pass
    
    # DDM also exists but am too lazy to integrate
    # Consider what3words support?
    return None, None

def geocode_location(location):
    # geocode = find lat/long from location name or address
    lat, lon = parse_lat_long(location)
    if lat and lon:
        return lat, lon # user already entered coords
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json", "limit": "1"}
    headers = {"User-Agent": "mapfisher/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
            
    except Exception: # user very doopid
        pass
    
    return None, None # user doopid

def suggest_locations(text):
    if not text:
        return []
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": text, "format": "json", "limit": "5"}
    headers = {"User-Agent": "mapfisher/1.0"}
    
    try:
        response = requests.get(url, params = params, headers = headers)
        if response.status_code == 200:
            data = response.json()
            return [item["display_name"] for item in data]
        
    except Exception:
        pass
    return []

def location_completer(text, state):
    suggestions = suggest_locations(text)
    if state < len(suggestions):
        return suggestions[state]
    return None