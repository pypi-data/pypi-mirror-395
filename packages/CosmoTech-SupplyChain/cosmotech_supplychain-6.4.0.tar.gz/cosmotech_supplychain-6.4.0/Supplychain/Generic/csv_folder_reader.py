import csv
import glob
import io
import json
import os
import sys

from collections import defaultdict

from Supplychain.Generic.folder_io import FolderReader


class CSVReader(FolderReader):
    extension = ".csv"

    def refresh(self):
        filenames = glob.glob(os.path.join(self.input_folder, "*" + self.extension))
        self.files = defaultdict(list)
        csv.field_size_limit(sys.maxsize)

        for filename in filenames:
            with open(filename, "r") as f:
                # Read every file in the input folder
                current_filename = os.path.basename(filename)[:-len(self.extension)]
                too_many = set()
                too_few = set()
                reader = csv.DictReader(f)
                try:
                    for row in reader:
                        new_row = dict()
                        for key, value in row.items():
                            if key is None:
                                too_many.add(str(reader.line_num))
                                continue
                            if value is None:
                                too_few.add(str(reader.line_num))
                                continue
                            if key in self.id_keys:
                                new_row[key] = None if value is None else str(value)
                                continue
                            try:
                                # Try to convert any json row to dict object
                                converted_value = json.load(io.StringIO(value))
                            except json.decoder.JSONDecodeError:
                                converted_value = value
                            if converted_value == '':
                                converted_value = None
                            if isinstance(converted_value, str) and converted_value.lower() in ["false", "true"]:
                                converted_value = converted_value.lower() == "true"
                            if converted_value is not None or self.keep_nones:
                                new_row[key] = converted_value
                        self.files[current_filename].append(new_row)
                except csv.Error as e:
                    self.errors[current_filename] = f"Error while reading {filename}, at line {reader.line_num}: {e}"
                    continue
                if too_many or too_few:
                    error = f"Error while reading {filename}.\nHeader fields: {', '.join(reader.fieldnames)}."
                    if too_many:
                        lines = (str(line) for line in sorted(too_many))
                        error += f"\nMore fields than header in line{'s' if len(too_many) > 1 else ''} {', '.join(lines)}."
                    if too_few:
                        lines = (str(line) for line in sorted(too_few))
                        error += f"\nLess fields than header in line{'s' if len(too_few) > 1 else ''} {', '.join(lines)}."
                    self.errors[current_filename] = error

        if self.errors and self.raise_errors:
            message = "\n".join(self.errors.values())
            raise Exception(message)

    def __init__(self,
                 input_folder: str = "Input",
                 keep_nones: bool = True,
                 raise_errors: bool = True):

        FolderReader.__init__(self,
                              input_folder=input_folder,
                              keep_nones=keep_nones)
        self.raise_errors = raise_errors
        self.errors = {}

        self.refresh()
