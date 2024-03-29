from weather_collector import WeatherCollector

import argparse


def url():
    with WeatherCollector(url='https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&'
                              'current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_'
                              'humidity_2m,wind_speed_10m') as handler:
        handler.display_weather_table()
        print(handler.records_list)
        print(handler.fields)
        print(handler.max_value(field=handler.fields[1]))
        print(handler.last_record)
        print(handler.compare_live_history())


def file():
    with WeatherCollector(file_path='weather.csv') as handler:
        handler.display_weather_table()
        print(handler.records_list)
        print(handler.fields)
        print(handler.max_value(field=handler.fields[1]))


if __name__ == '__main__':
    url()
    # file()
