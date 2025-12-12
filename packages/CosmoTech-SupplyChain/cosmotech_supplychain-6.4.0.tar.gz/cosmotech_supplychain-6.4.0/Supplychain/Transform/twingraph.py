from Supplychain.Generic.folder_io import FolderReader


def rename_to_twingraph(reader: FolderReader):
    for file_name, records in reader.files.items():
        if 'source' in records[0]:
            for record in records:
                record['src'] = record.pop('source')
                record['dest'] = record.pop('target')
                if 'id' not in record:
                    record['id'] = (
                        record.pop('Label')
                        if 'Label' in record
                        else f"{record['src']}_to_{record['dest']}"
                    )
        if 'id' not in records[0]:
            for i, record in enumerate(records):
                record['id'] = f'{file_name}{i}'


def rename_from_twingraph(reader: FolderReader):
    for file_name, records in reader.files.items():
        if 'src' in records[0]:
            for record in records:
                record['source'] = record.pop('src')
                record['target'] = record.pop('dest')
                if 'Label' not in record and 'id' in record:
                    record['Label'] = record.pop('id')
