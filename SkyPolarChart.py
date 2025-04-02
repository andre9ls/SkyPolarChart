import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load, wgs84
from datetime import datetime, timezone, timedelta

def plot_sky_map(latitude, longitude, date_time):
    ts = load.timescale()
    eph = load('de421.bsp')
    earth = eph['earth']
    observer = earth + wgs84.latlon(latitude, longitude)
    
    sun, moon = eph['sun'], eph['moon']
    time = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)
    
    sun_astrometric = observer.at(time).observe(sun).apparent()
    moon_astrometric = observer.at(time).observe(moon).apparent()
    
    sun_alt, sun_az, _ = sun_astrometric.altaz()
    moon_alt, moon_az, _ = moon_astrometric.altaz()
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    ax.set_rlim(90, 0)  # Zenith at center, horizon at edge
    ax.set_yticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_yticklabels(['horizon', '15', '30', '45', '60', '75','zenith'])
    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    ax.scatter(np.radians(sun_az.degrees), 90 - sun_alt.degrees, color='yellow', s=100, label='Sun')
    ax.scatter(np.radians(moon_az.degrees), 90 - moon_alt.degrees, color='gray', s=80, label='Moon')
    
    # Compute solstice and equinox sun paths
    for event_date, color, label in [(datetime(date_time.year, 6, 21), 'red', 'Summer Solstice'),
                                      (datetime(date_time.year, 12, 21), 'blue', 'Winter Solstice'),
                                      (datetime(date_time.year, 3, 20), 'green', 'Spring Equinox'),
                                      (datetime(date_time.year, 9, 22), 'orange', 'Autumn Equinox')]:
        event_altitudes = []
        event_azimuths = []
        for hour in range(0, 24):
            event_time = ts.utc(event_date.year, event_date.month, event_date.day, hour)
            event_sun = observer.at(event_time).observe(sun).apparent()
            alt, az, _ = event_sun.altaz()
            event_altitudes.append(90 - alt.degrees)
            event_azimuths.append(np.radians(az.degrees))
        ax.plot(event_azimuths, event_altitudes, color=color, linestyle='dashed', label=label)
    
    ax.legend()
    plt.title(f'Sky Map ({date_time})\nLat: {latitude}, Lon: {longitude}')
    plt.show()

# Example Usage
latitude = 45.0  # Turin latitude
longitude = 7.0  # Turin longitude
date_time = datetime.now().astimezone()  # Current Italian date and time

plot_sky_map(latitude, longitude, date_time)
