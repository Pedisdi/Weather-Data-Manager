from weather_collector import WeatherCollector

import argparse

def main():
    with WeatherCollector('weather.csv') as handler:
        handler.display_weather_table(['temperature', 'humidity', 'wind_speed'])
        print(handler.average_value('temperature'))


if __name__ == '__main__':
    main()
