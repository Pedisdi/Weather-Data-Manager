import pathlib
import csv
import requests
import tabulate


class WeatherCollector:
    def __init__(self, file_path="", url=""):
        self.url = url
        self.file_path = file_path
        self.file_obj = None
        self.fields = []  # ["filed1", "field2", ...]
        self.records_list = []  # [{"field1": "value1", "field2": "value2"}, ...]

    def __enter__(self):
        self.fields, self.records_list = self.__extract_fields_and_records()
        return self

    def __extract_fields_and_records(self):  # extracting field names through first row
        fields = []
        records = []
        if self.file_path:
            path = pathlib.Path(self.file_path)
            if path.exists() and path.suffix == '.csv':
                self.file_obj = path.open("r")
                fields = next(csv.reader(self.file_obj))
                self.file_obj.seek(0)
                for record in csv.DictReader(self.file_obj):
                    records.append(record)
            else:
                raise FileNotFoundError("File does not exit.")
        elif self.url:
            response = requests.get(self.url)
            weather_data_dict = response.json()['hourly']
            fields = list(weather_data_dict.keys())
            iter_times = len(list(weather_data_dict.values())[0])
            for i in range(iter_times):
                record = {}
                for field in fields:
                    record[field] = weather_data_dict[field][i]
                records.append(record)
        return fields, records

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
        if self.file_obj:
            self.file_obj.close()
