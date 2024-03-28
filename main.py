from weather_collector import WeatherCollector


def main():
    with WeatherCollector('weather.csv') as handler:
        handler.display_weather_table(['temperature', 'humidity', 'wind_speed'])


if __name__ == '__main__':
    main()
