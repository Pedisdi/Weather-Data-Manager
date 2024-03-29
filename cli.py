import argparse
from weather_collector import WeatherCollector

parser = argparse.ArgumentParser(prog="WeatherDataManager")
parser.add_argument('--file', required=True)
parser.add_argument('-d', '--datatype', nargs=1, choices=['temperature', 'humidity', 'wind_speed'])
parser.add_argument('-o', '--operation', nargs=1, choices=['max', 'min', 'average'])

args = parser.parse_args()
print(args)
with WeatherCollector(args.file) as handler:
    if args.operation[0] == 'max':
        print(handler.max_value(args.datatype[0]))
    elif args.operation[0] == 'min':
        print(handler.min_value(args.datatype[0]))
    elif args.operation[0] == 'average':
        print(handler.average_value(args.datatype[0]))



