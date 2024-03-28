import pathlib
import csv


class WeatherCollector:
    def __init__(self, file_path):
        self.file_path = pathlib.Path(file_path)
        self.file_obj = None
        self.fields = []
        self.records = []

    @property
    def all_rows(self):
        rows = [self.fields]
        rows.extend(self.records)
        return rows

    def __enter__(self):
        if self.file_path.exists():
            self.file_obj = self.file_path.open("r")
            self.fields = self.__extract_fields()
            self.records = self.__extract_records()
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()
