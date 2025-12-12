"""
This code has been written by stephane.ploix@grenoble-inp.fr
It is protected under GNU General Public License v3.0

Author: stephane.ploix@grenoble-inp.fr
License: GNU General Public License v3.0"""
from __future__ import annotations
import batem.core.weather
import batem.core.solar
import batem.core.timemg


# site_weather_data_builder = batem.core.weather.SiteWeatherDataBuilder(location='grenoble', latitude_north_deg=45.19154994547585, longitude_east_deg=5.722065312331381)

site_weather_data_builder = batem.core.weather.SWDbuilder(location='sydney', latitude_north_deg=-33.844167622963006, longitude_east_deg=151.03095450863236)

site_weather_data: batem.core.weather.SiteWeatherData = site_weather_data_builder(from_stringdate='01/01/2019', to_stringdate='31/12/2020')
# print(site_weather_data)
# print(site_weather_data.from_stringdate, site_weather_data.to_stringdate)
# print(site_weather_data.from_datetime, site_weather_data.to_datetime)

site_weather_data.plot()
