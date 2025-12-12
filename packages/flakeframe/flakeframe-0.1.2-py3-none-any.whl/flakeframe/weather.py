import requests
from datetime import datetime, date
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CurrentWeather:
    time:               datetime
    temperature:        float
    condition:          str
    wind_speed_kmh:     float
    wind_direction_deg: int
    wind_direction_str: str
    precipitation_mm:   float
    
@dataclass
class HourlyForecast:
    time:             datetime
    temperature:      float
    condition:        str
    precipitation_mm: float
    
@dataclass
class DailyForecast:
    date:                 date
    temp_min:             float
    temp_max:             float
    condition:            str
    precipitation_sum_mm: float

@dataclass
class WeatherData:
    latitude:     float
    longitude:    float
    current:      CurrentWeather
    hourly:       List[HourlyForecast] # count: 5
    daily:        List[DailyForecast]  # count: 5
    units_temp:   str
    units_precip: str
    

WEATHER_CODES = {
    0 : "\x1b[38;2;255;220;100mSunny\x1b[0m",
    1 : "\x1b[38;2;255;230;120mMainly Sunny\x1b[0m",
    2 : "\x1b[38;2;220;220;220mPartly Cloudy\x1b[0m",
    3 : "\x1b[38;2;180;180;180mCloudy\x1b[0m",
    45: "\x1b[38;2;200;200;210mFoggy\x1b[0m",
    48: "\x1b[38;2;190;210;220mRime Fog\x1b[0m",
    51: "\x1b[38;2;100;180;255mLight Drizzle\x1b[0m",
    53: "\x1b[38;2;80;160;255mDrizzle\x1b[0m",
    55: "\x1b[38;2;60;140;255mHeavy Drizzle\x1b[0m",
    56: "\x1b[38;2;130;190;255mFreezing Drizzle\x1b[0m",
    57: "\x1b[38;2;110;170;255mFreezing Drizzle\x1b[0m",
    61: "\x1b[38;2;100;180;255mLight Rain\x1b[0m",
    63: "\x1b[38;2;80;160;255mRain\x1b[0m",
    65: "\x1b[38;2;60;140;255mHeavy Rain\x1b[0m",
    66: "\x1b[38;2;130;190;255mFreezing Rain\x1b[0m",
    67: "\x1b[38;2;110;170;255mFreezing Rain\x1b[0m",
    71: "\x1b[38;2;200;230;255mLight Snow\x1b[0m",
    73: "\x1b[38;2;180;220;255mSnow\x1b[0m",
    75: "\x1b[38;2;160;210;255mHeavy Snow\x1b[0m",
    77: "\x1b[38;2;190;220;250mSnow Grains\x1b[0m",
    80: "\x1b[38;2;100;190;255mLight Showers\x1b[0m",
    81: "\x1b[38;2;80;170;255mShowers\x1b[0m",
    82: "\x1b[38;2;60;150;255mHeavy Showers\x1b[0m",
    85: "\x1b[38;2;180;220;255mSnow Showers\x1b[0m",
    86: "\x1b[38;2;160;210;255mSnow Showers\x1b[0m",
    95: "\x1b[38;2;255;200;100mThunderstorm\x1b[0m",
    96: "\x1b[38;2;255;180;80mThunder + Hail\x1b[0m",
    99: "\x1b[38;2;255;160;60mThunder + Hail\x1b[0m",
}

#               N    NE    E    SE    S   SW    W    NW
WIND_ARROWS = ['⬆', '⬈', '➡', '⬊', '⬇', '⬋', '⬅', '⬉']

def wind_arrow(deg):
    idx = int((deg + 22.5) % 360 / 45)
    return WIND_ARROWS[idx]

def condition(code):
    return WEATHER_CODES.get(code, f"No name for code {code}")

def parse_weather(data, config) -> Optional[WeatherData]:
    try:
        current = data["current"]
        hourly  = data["hourly"]
        daily   = data["daily"]

        curr_time = datetime.fromisoformat(current["time"].replace("Z", "+00:00"))
        current_weather = CurrentWeather(
            time               = curr_time,
            temperature        = current["temperature_2m"],
            condition          = condition(current["weather_code"]),
            wind_speed_kmh     = current["wind_speed_10m"],
            wind_direction_deg = current["wind_direction_10m"],
            wind_direction_str = wind_arrow(current["wind_direction_10m"]),
            precipitation_mm   = current["precipitation"]
        )
        
        hourly_list = []
        for i in range(len(hourly["time"])):
            h_time = datetime.fromisoformat(hourly["time"][i].replace("Z", "+00:00"))
            hourly_list.append(HourlyForecast(
                time =             h_time,
                temperature =      hourly["temperature_2m"][i],
                condition =        condition(hourly["weather_code"][i]),
                precipitation_mm = hourly["precipitation"][i]
            ))
            
        daily_list = []
        for i in range(len(daily["time"])):
            d_date = date.fromisoformat(daily["time"][i])
            daily_list.append(DailyForecast(
                date =                 d_date,
                temp_min =             daily["temperature_2m_min"][i],
                temp_max =             daily["temperature_2m_max"][i],
                condition =            condition(daily["weather_code"][i]),
                precipitation_sum_mm = daily["precipitation_sum"][i]
            ))
        
        return WeatherData(
            latitude =     round(data.get("latitude", 0), 2),
            longitude =    round(data.get("longitude", 0), 2),
            current =      current_weather,
            hourly =       hourly_list,
            daily =        daily_list,
            units_temp =   config["DEFAULT"]["units_temp"],
            units_precip = config["DEFAULT"]["units_precip"]
        )
    
    except (KeyError, IndexError, ValueError) as e:
        print(f"WARNING: Failed to parse weather data: {e}")
        return None
        

def fetch_weather(lat, lon, config):
    temp_unit   = "celsius" if config["DEFAULT"]["units_temp"]   == "°C" else "fahrenheit"
    precip_unit = "mm"      if config["DEFAULT"]["units_precip"] == "mm" else "inch"
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,wind_speed_10m,wind_direction_10m,weather_code",
        "hourly": "temperature_2m,precipitation,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "temperature_unit": temp_unit,
        "precipitation_unit": precip_unit,
        "timezone": "auto",
    }
    response = requests.get(url, params = params)
    
    if response.status_code == 200:
        return parse_weather(response.json(), config)
    return None