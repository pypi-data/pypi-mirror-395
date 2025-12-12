# flakeframe
A weather app for your CLI, with a fancy map!

## demo
[demo](https://github.com/user-attachments/assets/23d8d9b3-7e41-47e1-84dd-eb197b8218de)

## what is it?
A fast and easy to use CLI weather app with super neat map view!\
Should work on basically everything, as long as you have Python and Internet access.\
(a note: flakeframe was known as Mapfish before submitting!)

## usage and installation
`pip install flakeframe`, or `pipx` if you're on an externally managed system like Arch Linux.

Then just find your desired coordinate pair (degrees or D/M/S), run `flakeframe`, and enter your settings :)

## controls
Use WASD/arrow keys to navigate in the main menu, then +/- to change zoom levels.\
Q to go back to the main menu, R to refresh your weather data.

## features
- Works basically anywhere
- Hourly and daily forecasts
- Color codes
- Map display [anywhere*](https://xkcd.com/3173/) on earth
- No API keys or weird configuration needed.
- Smart aspect ratio detection, unless you use a weird font

## credits
- Map data from ArcGIS world imagery
- Weather data from OpenMeteo
- Uses img2unicode by matrach
- Uses py-staticmaps by flopp
