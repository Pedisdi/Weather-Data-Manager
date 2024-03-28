import pprint

import requests

import json
import tabulate


response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m')
# print(response.text)
# pprint.pprint(data_dict)
# data_dict = response.json()
# print(data_dict['hourly'].keys())

before = {
    "temp": [1, 231, 2],
    "humidity": [1, 91, 32]
}
after = [
    {"temp": 1, "humidity": 1},
    {"temp": 231, "humidity":91},
    {"temp": 2, "humidity": 32}
]
o = []

data_dict = response.json()
print(data_dict['hourly'].keys())
before = (data_dict['hourly'])
# print(before)
lst = []
iter_times = len(list(before.values())[0])
for i in range(iter_times):
    row = {}
    for key in before:
        row[key] = before[key][i]
    lst.append(row)
print(lst)

# for i in range(len(after)):
for key in after[0].keys():
    print(key, end="\t")
print()

for row in after:
    for value in row.values():
        print(value, end='\t')
    print()
print(tabulate.tabulate(after, headers="keys", tablefmt="grid"))