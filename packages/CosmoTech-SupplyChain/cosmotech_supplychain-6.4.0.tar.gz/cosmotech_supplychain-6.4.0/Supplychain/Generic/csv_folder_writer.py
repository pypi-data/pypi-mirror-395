import csv
import os.path
from Supplychain.Generic.folder_io import FolderWriter

from typing import Union

csv.register_dialect('unix_qm', lineterminator='\n')


class CSVWriter(FolderWriter):

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None, fieldnames: Union[list, None] = None, mode: str = "w"):
        filepath = f"{self.output_folder}/{file_name}.csv"
        non_empty_file_exists = os.path.isfile(filepath) and os.path.getsize(filepath)
        with open(filepath, mode, encoding='utf_8') as target_file:
            if dict_list:
                if fieldnames is None:
                    fieldnames = list(dict_list[0].keys())
                    fieldnames.extend(
                        set(fieldname for row in dict_list for fieldname in row)
                        - set(fieldnames)
                    )
                writer = csv.DictWriter(target_file, fieldnames=fieldnames, restval=None, dialect='unix_qm')
                if any(m in mode for m in 'wx') or not non_empty_file_exists:
                    writer.writeheader()
                to_be_writen = dict_list
                if ordering_key is not None and ordering_key in dict_list[0]:
                    to_be_writen = sorted(dict_list, key=lambda e: e[ordering_key])
                for row in to_be_writen:
                    to_be = {k: FolderWriter.json_value(v)
                             for k, v
                             in row.items()}
                    writer.writerow(to_be)

    def __init__(self,
                 output_folder: str = "Output"):
        FolderWriter.__init__(self,
                              output_folder=output_folder)
