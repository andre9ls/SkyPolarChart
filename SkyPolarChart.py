import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load, wgs84
from datetime import datetime

def plot_sky_map(latitude, longitude, date_time):
    ts = load.timescale()
    eph = load('de421.bsp')
    earth = eph['earth']
    observer = earth + wgs84.latlon(latitude, longitude)
    
    sun = eph['sun']
    moon = eph['moon']
    venus = eph['venus']
    mars = eph['mars']
    jupiter = eph['jupiter barycenter']
    saturn = eph['saturn barycenter']

    time = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)

    # Get current positions
    sun_astrometric = observer.at(time).observe(sun).apparent()
    moon_astrometric = observer.at(time).observe(moon).apparent()
    sun_alt, sun_az, _ = sun_astrometric.altaz()
    moon_alt, moon_az, _ = moon_astrometric.altaz()

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(90, 0)  # Zenith at center, horizon at edge

    ax.set_xticks(np.radians([0, 90, 180, 270]))
    ax.set_xticklabels(['N', 'E', 'S', 'W'])

    # Plot Sun and Moon
    if sun_alt.degrees > 0:
        ax.scatter(np.radians(sun_az.degrees), sun_alt.degrees, color='yellow', s=100, label='Sun')
    if moon_alt.degrees > 0:
        ax.scatter(np.radians(moon_az.degrees), moon_alt.degrees, color='gray', s=80, label='Moon')

    # Plot planets
    planets = [
        (venus, 'Venus', 'magenta'),
        (mars, 'Mars', 'red'),
        (jupiter, 'Jupiter', 'orange'),
        (saturn, 'Saturn', 'gold')
    ]
    for planet_obj, name, color in planets:
        planet_astrometric = observer.at(time).observe(planet_obj).apparent()
        alt, az, _ = planet_astrometric.altaz()
        if alt.degrees > 0:
            ax.scatter(np.radians(az.degrees), alt.degrees, color=color, label=name)

    # Compute sun paths for solstices and equinoxes
    for event_date, color, label in [
        (datetime(date_time.year, 6, 21), 'red', 'Summer Solstice'),
        (datetime(date_time.year, 12, 21), 'blue', 'Winter Solstice'),
        (datetime(date_time.year, 3, 20), 'green', 'Equinox')
    ]:
        event_azimuths = []
        event_altitudes = []
        for minute_offset in range(0, 24 * 60, 10):  # every 10 minutes
            hour = minute_offset // 60
            minute = minute_offset % 60
            event_time = ts.utc(event_date.year, event_date.month, event_date.day, hour, minute)
            event_sun = observer.at(event_time).observe(sun).apparent()
            alt, az, _ = event_sun.altaz()
            if alt.degrees > 0:
                event_azimuths.append(np.radians(az.degrees))
                event_altitudes.append(alt.degrees)
        if event_altitudes:
            ax.plot(event_azimuths, event_altitudes, color=color, label=label)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title(f'Sky Map ({date_time.strftime("%Y-%m-%d %H:%M:%S")})\nLat: {latitude}, Lon: {longitude}')
    plt.show()

# Example Usage
latitude = 45.0703  # Turin
longitude = 7.6869  # Turin
date_time = datetime.now().astimezone()  # Current Italian local time

plot_sky_map(latitude, longitude, date_time)
