import pathlib
import csv
import requests
import tabulate


class WeatherCollector:
    def __init__(self, file_path="", url=""):
        self.url = url
        self.file_path = file_path
        self.file_obj_live = None
        self.file_obj_historical = None
        self.fields = []  # ["filed1", "field2", ...]
        self.records_list = []  # [{"field1": "value1", "field2": "value2"}, ...]
        self.last_record = None

    def __enter__(self):
        self.load_last_record()
        self.fields, self.records_list = self.__extract_fields_and_records()
        return self

    def __extract_fields_and_records(self):  # extracting field names through first row
        fields = []
        records = []
        if self.file_path:
            path = pathlib.Path(self.file_path)
            if path.exists() and path.suffix == '.csv':
                self.file_obj_live = path.open("r")
                fields = next(csv.reader(self.file_obj_live))
                self.file_obj_live.seek(0)
                for record in csv.DictReader(self.file_obj_live):
                    records.append(record)
            else:
                raise FileNotFoundError("File does not exit.")
        elif self.url:
            response = requests.get(self.url)
            weather_data_dict = response.json()['hourly']
            fields = list(weather_data_dict.keys())
            records = []
            for values in zip(*weather_data_dict.values()):
                records.append({field: value for field, value in zip(fields, values)})
            with open('weather.csv', 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writerows(records)
        return fields, records

    def load_last_record(self):
        with open('weather.csv', 'r') as csv_file:
            for record in csv.DictReader(csv_file):
                self.last_record = record

    def compare_live_history(self):
        last_record_online = self.records_list[-2]
        print(f"online:{last_record_online}")
        # time,temperature_2m,relative_humidity_2m,wind_speed_10m
        temperature = float(self.last_record['temperature_2m']) < float(last_record_online['temperature_2m'])
        print(f"temperature: offline{'<' if temperature else '>'}online")

    def display_weather_table(self):
        print(tabulate.tabulate(self.records_list, headers="keys", tablefmt="rounded_grid"))

    def max_value(self, field):
        return max([float(row[field]) for row in self.records_list])

    def min_value(self, field):
        return min([float(row[field]) for row in self.records_list])

    def average_value(self, field):
        values = [float(row[field]) for row in self.records_list]  # __shift+del (to delete a line directly)
        return sum(values) / len(values)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj_live:
            self.file_obj_live.close()
