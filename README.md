# ts-weather

## Description

This is the micro service that retrieves weather data from the dark sky API for specific geo-coordinates.

## setting up API KEYS
Due to security, you will need to create a new file: `app/config/tskeys.py`

add the following to the new file:

```
from config.tsconfig import APP_ENV

### API KEYS ###

if APP_ENV == "DEV":
    DARK_SKIES_API_KEY = '<Dark Skies API Key>'
```

## Running in docker

**You will need docker installed on your computer to run the code**

you are going to need to `cd` in to the directory you have pulled the code to. Once you are there, go ahead and run the following commands based on your needs.

`make build`
This will build the docker container where you will run the code.

`make run`
This will run the container and allow you to interact with the API.

`make inspect`
**container must be running** This will allow you to open a shell in the container for viewing log files and debugging configurations.

`make stop`
This will stop the running container.

`make clean`
This will purge the docker registry of this container.

## API
For app name and version, query *http://127.0.0.1:4082/*

The api will be located at *http://127.0.0.1:4082/ts-weather*

### `/routeForcast/{lat}/{lon}/{trans_id} [GET]`

This is used to pull Dark Sky weather data for a specific geo-location.

##### Request

Var Name | Var Type | Description
-------- | -------- | -----------
lat | float | location latitude.
lon | float | location longitude.
trans_id | String | used for tracking and debugging requests accross micro services.

##### Response (json)

Var Name | Var Type | Description
-------- | -------- | -----------
alerts | Object Array | These are weather alerts for the area where weather data is pulled from. if there are no alerts, the value will be set to "EMPTY".
alerts -> [] -> description | String | This will give a full description for the alert.
alerts -> [] -> expires | int | This is when the alert is set to expire measured in a unix timestamp.
alerts -> [] -> regions | String Array | These are the regions affected by the alert.
alerts -> [] -> severity | String | This is the level of severity the alert has been given.
alerts -> [] -> time | int | This is when the alert was put in to effect measured in a unix timestamp.
alerts -> [] -> title | String | This is a short, formal description of the alert.
alerts -> [] -> uri | String | This is the reference of where the alert data was retrieved from.
latitude | float | This is the latitude where the weather data was pulled from.
longitude | float | This is the longitude where the weather data was pulled from.
status | String | "OK" means the application was able to complete the request with no issues. any other response means an error occured, and the integrity of any data may be compromised.
timezone | String | This is the timezone of the geo-coordinates (**important:** time variables in this object are set to this timezone).
weather_data | Object Array | This is where detailed weather data is stored.
weather_data -> [] -> apparentTemperature | float | This is the temperature it feels like, measured in Fahrenheit.
weather_data -> [] -> cloudCover | float | No Description.
weather_data -> [] -> dewPoint | float | No Description.
weather_data -> [] -> humidity | float | No Description.
weather_data -> [] -> icon | String | This is issued to display a corresponding image icon.
weather_data -> [] -> ozone | float | No Description.
weather_data -> [] -> precipIntensity | float | No Description.
weather_data -> [] -> precipProbability | float | No Description.
weather_data -> [] -> pressure | float | No Description.
weather_data -> [] -> summary | String | summarizes the forecast.
weather_data -> [] -> temperature | float | This is the actual temperature measured in Fahrenheit.
weather_data -> [] -> time | int | the time for the forecast measured in a unix timestamp. it is important to link this time with the timezone provided, or time may not display accurately.
weather_data -> [] -> uvIndex | float | No Description.
weather_data -> [] -> visibility | float | No Description.
weather_data -> [] -> windBearing | float | No Description.
weather_data -> [] -> windGust | float | No Description.
weather_data -> [] -> windSpeed | float | No Description.


```
/routeForcast/39.6728/-106.79992/abc123

(response has been omitted due to it's size)

{
  "alerts": [
    {
      "description": "...RED FLAG WARNING NOW IN EFFECT FROM FRIDAY AFTERNOON THROUGH FRIDAY EVENING FOR GUSTY WINDS, LOW RELATIVE HUMIDITY AND DRY FUELS FOR COLORADO FIRE WEATHER ZONES 200, 202, 203, 290, 292 AND ZONES 205, AND 207 BELOW 8000 FEET AND ZONE 294 BELOW 9500 FEET AND UTAH FIRE WEATHER ZONE 490... ...RED FLAG WARNING IN EFFECT FROM NOON TO 9 PM MDT FRIDAY FOR GUSTY WINDS, LOW RELATIVE HUMIDITY AND DRY FUELS FOR FIRE WEATHER ZONES 203, 205, AND 207 BELOW 8000 FEET... The National Weather Service in Grand Junction has issued a Red Flag Warning below 8000 feet for gusty winds, low relative humidity and dry fuels, which is in effect from noon to 9 PM MDT Friday. The Fire Weather Watch is no longer in effect. * AFFECTED AREA...In Colorado, Fire Weather Zone 203 Lower Colorado River, Fire Weather Zone 205 Colorado River Headwaters and Fire Weather Zone 207 Southwest Colorado Lower Forecast Area below 8000 feet. * WINDS...Southwest 15 to 25 mph with gusts up to 35 mph. * RELATIVE HUMIDITY...7 to 12 percent. * IMPACTS...Conditions may become favorable for the rapid ignition, growth and spread of fires.\n",
      "expires": 1590202800,
      "regions": [
        "Colorado River Headwaters",
        "Lower Colorado River",
        "Southwest Colorado Lower Forecast Area"
      ],
      "severity": "warning",
      "time": 1590170400,
      "title": "Red Flag Warning",
      "uri": "https://alerts.weather.gov/cap/wwacapget.php?x=CO125F4CE3F2AC.RedFlagWarning.125F4CFFDDF0CO.GJTRFWGJT.c318e98697b01bcd09b03222ee690636"
    },
    {
      "description": "...Rivers and Streams Will Continue to Run High this Week into the Weekend due to Snowmelt... Flows in area rivers, streams, and creeks will continue to run at elevated levels as the recent snowmelt works downstream. Significant flooding is NOT forecast at this time as many waterways peak over the next week. Many smaller streams and creeks will run at bankfull conditions through the end of the week causing localized lowland flooding. Anyone planning to recreate on area waterways should maintain awareness and use an abundance of caution in or near the water. Areas that will need to be watched closely include: The Yampa River, Elk River, upper Slater Fork, and other small streams in the upper Yampa, White, and Eagle Basins.\n",
      "expires": 1590451200,
      "regions": [
        "Eagle",
        "Garfield",
        "Moffat",
        "Rio Blanco",
        "Routt"
      ],
      "severity": "advisory",
      "time": 1589913240,
      "title": "Hydrologic Outlook",
      "uri": "https://alerts.weather.gov/cap/wwacapget.php?x=CO125F4CC52C28.HydrologicOutlook.125F4D2D2F80CO.GJTESFGJT.cf955ef1e2c1028fe1acbe4ea736bb0b"
    }
  ],
  "latitude": 39.6728,
  "longitude": -106.79992,
  "status": "OK",
  "timezone": "America/Denver",
  "weather_data": [
    {
      "apparentTemperature": 66.32,
      "cloudCover": 0.02,
      "dewPoint": 20.64,
      "humidity": 0.17,
      "icon": "clear-day",
      "ozone": 341.6,
      "precipIntensity": 0,
      "precipProbability": 0,
      "pressure": 1009,
      "summary": "Clear",
      "temperature": 66.32,
      "time": 1590094800,
      "uvIndex": 8,
      "visibility": 10,
      "windBearing": 256,
      "windGust": 17.77,
      "windSpeed": 11.23
    },
    ...
    {
      "apparentTemperature": 69.06,
      "cloudCover": 0.37,
      "dewPoint": 24.69,
      "humidity": 0.19,
      "icon": "partly-cloudy-day",
      "ozone": 344.4,
      "precipIntensity": 0.0003,
      "precipProbability": 0.01,
      "precipType": "rain",
      "pressure": 1003.9,
      "summary": "Partly Cloudy",
      "temperature": 69.06,
      "time": 1590267600,
      "uvIndex": 6,
      "visibility": 10,
      "windBearing": 234,
      "windGust": 27.99,
      "windSpeed": 15.45
    }
  ]
}
```
## Tasks
- [x] configure app to run on gunicorn
- [ ] optimize gunicorn settings for prod
- [ ] fix logging since gunicorn doesn't use logging class
- [ ] set up SSL
- [ ] set up mutual authentication
- [ ] create config file to store API keys
- [ ] create config files for webapp settings (request timeout, port, etc...)
