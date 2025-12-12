import os
import shutil

from Supplychain.Generic.folder_io import FolderReader, FolderWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.adt_column_description import ADTColumnDescription


class DatasetSplitter(Timer):

    def __init__(self, reader: FolderReader, writer: FolderWriter, filter_name='subdataset'):
        Timer.__init__(self, '[Split]')
        self.reader = reader
        self.writer = writer
        self.filter_name = filter_name
        self.file_names = sorted(ADTColumnDescription.format.keys())
        self.graph_file_names = set(
            file_name
            for file_name, file_descriptor in ADTColumnDescription.format.items()
            if any(k in file_descriptor['fixed'] for k in ('id', 'source')) and file_name != 'OptimizationConstraints'
        )
        self.output_directory = os.path.join(writer.output_folder, 'subdatasets')
        if os.path.lexists(self.output_directory):
            if os.path.isdir(self.output_directory):
                shutil.rmtree(self.output_directory)
            else:
                os.remove(self.output_directory)
        self.subdataset_names = []
        self.subdataset_record_count = {}
        self.errors = False

    def get_subdataset_names(self):
        subdataset_names = set()
        files_without_filter = []

        for file_name, records in self.reader.files.items():
            if file_name in self.graph_file_names:
                for record in records:
                    if self.filter_name in record:
                        subdataset_names.add(record[self.filter_name])
                    else:
                        files_without_filter.append(file_name)
                        break

        if files_without_filter and len(files_without_filter) != len(self.graph_file_names):
            self.errors = True
            self.display_message(
                f"The following file{'s' if len(files_without_filter) > 1 else ''}"
                f" lack subdaset data: {', '.join(sorted(files_without_filter))}."
            )

        if len(subdataset_names) > 1:
            self.subdataset_names = sorted(subdataset_names)
        else:
            self.display_message('No subdataset')

    def write_subdataset(self, subdataset_name):
        self.writer.__init__(os.path.join(self.output_directory, subdataset_name))
        for file_name in self.file_names:
            records = self.reader.files.get(file_name, [])
            if not records:
                continue
            if file_name in self.graph_file_names:
                filtered_records = [record for record in records if record[self.filter_name] == subdataset_name]
                if filtered_records:
                    self.subdataset_record_count.setdefault(subdataset_name, {})[file_name] = len(filtered_records)
                    self.writer.write_from_list(
                        filtered_records,
                        file_name,
                    )
            else:
                self.writer.write_from_list(records, file_name)

    def split(self):
        self.get_subdataset_names()
        if not self.errors:
            for subdataset_name in self.subdataset_names:
                self.write_subdataset(subdataset_name)
