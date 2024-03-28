import pathlib
import csv


class WeatherCollector:
    def __init__(self, file_path):
        self.file_path = pathlib.Path(file_path)
        self.file_obj = None
        self.fields = []
        self.records_list = []

    @property
    def records_dict(self):
        self.file_obj.seek(0)
        rows = []
        for row in csv.DictReader(self.file_obj):
            rows.append(row)
        return rows

    @property
    def all_rows(self):
        rows = [self.fields]
        rows.extend(self.records_list)
        return rows

    def __enter__(self):
        if self.file_path.exists() and self.file_path.suffix == '.csv':
            self.file_obj = self.file_path.open("r")
            self.fields = self.__extract_fields()
            self.records_list = self.__extract_records()
            return self
        raise FileNotFoundError("File does not exit.")

    def __extract_records(self):
        records = []
        for row in csv.reader(self.file_obj):
            records.append(row)
        return records

    def __extract_fields(self):  # extracting field names through first row
        self.file_obj.seek(0)
        return next(csv.reader(self.file_obj))

    def display_weather_table(self, fields=None):
        if fields is None:
            fields = self.fields
        column_numbers = [self.fields.index(column_name) for column_name in fields]

        for row in self.all_rows:
            for column_number in column_numbers:
                print(f"{row[column_number]:<15}", end='')
            print()

    def max_value(self, field):
        return max([float(row[field]) for row in self.records_dict])

    def min_value(self, field):
        return min([float(row[field]) for row in self.records_dict])

    def average_value(self, field):
        values = [float(row[field]) for row in self.records_dict]  # __shift+del (to delete a line directly)
        return sum(values) / len(values)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()
