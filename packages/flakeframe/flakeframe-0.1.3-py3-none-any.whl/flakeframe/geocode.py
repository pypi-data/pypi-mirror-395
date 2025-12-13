import re
import requests

def parse_coordinates(input_str: str, final: bool) -> (float, float):
    
    # DECIMAL (regex by AI. I cannot be bothered to learn regex)
    dec_pattern = r'^[-+]?[0-9]*\.?[0-9]+\s*,?\s*[-+]?[0-9]*\.?[0-9]+\s*$'
    decimal_match = re.match(dec_pattern, input_str.strip().replace("°", "").replace("'", "").replace('"', ""))
    if decimal_match:
        parts = re.split(r'[\s,]+', input_str.strip())
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon, False
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
    match = re.search(dms_pattern, input_str.strip(), re.IGNORECASE | re.VERBOSE)
    if match:
        try:
            lat = float(match.group(1)) + float(match.group(2)) / 60 + float(match.group(3)) / 3600
            lon = float(match.group(5)) + float(match.group(6)) / 60 + float(match.group(7)) / 3600
            if match.group(4).upper() == "S":
                lat = -lat
            if match.group(8).upper() == "w":
                lon = -lon
            return lat, lon, False
            
        except Exception: # user doopid
            pass
    
    if final:
        url = "https://nominatim.openstreetmap.org/search"
        headers = { "User-Agent": "flakeframe/1.0" }
        params = {
            "q": input_str,
            "limit": 1,
            "format": "json"
        }
        resp = requests.get(url = url, params = params, headers = headers) # don't get banned from nominatim (again)
        response = resp.json()
        # TODO: global rate limit
        
        try:
            lat = float(response[0]["lat"])
            lon = float(response[0]["lon"])
            return lat, lon, False
        except Exception: # response failed for whatever reason
            return None, None, True
    
    return None, None, False # no coord

def validate_input_live(text):
    lat, lon, _ = parse_coordinates(text, final = False)
    if lat is not None and lon is not None:
        return True, lat, lon, f"{lat:.6f}, {lon:.6f}\x1b[0m"
    return False, None, None, "Invalid Coordinates\x1b[0m"