from Supplychain.Generic.folder_io import FolderReader, FolderWriter
from Supplychain.Generic.util import separate_and_interpret_with_display
from Supplychain.Schema.adt_column_description import ADTColumnDescription
from Supplychain.Generic.timer import Timer


def get_primary_key(file_description):
    if 'id' in file_description['fixed']:
        return 'id',
    if 'Label' in file_description['fixed']:
        return 'Label',
    if 'source' in file_description['fixed'] and 'target' in file_description['fixed']:
        return 'source', 'target'
    return ()


def write_transformed_data(reader: FolderReader, writer: FolderWriter):
    with FromTableToDictConverter(reader, writer) as converter:
        return converter.convert_all()


dataset_description = ADTColumnDescription.format


class FromTableToDictConverter(Timer):

    def __init__(self, reader: FolderReader, writer: FolderWriter, descriptor=dataset_description):
        Timer.__init__(self, "[Table -> Dict]")
        self.descriptor = descriptor
        self.reader = reader
        for file_name, interpreted_name in self.check_file_names().items():
            self.reader.files[interpreted_name] = self.reader.files.pop(file_name)
        self.writer = writer

    def check_file_names(self):
        described_files = set(self.descriptor)
        for file_name, file_description in self.descriptor.items():
            if file_description['change']:
                described_files.add(f'{file_name}Schedules')
            for file_type in ('event', 'quantity'):
                described_files |= set(file_description[file_type])
        _, _, interpretation = separate_and_interpret_with_display(self.reader.files, described_files, self.display_message, 'file')
        return interpretation

    def check_column_names(self, file_content, file_name, file_type, subfile_name=None):
        if not file_content:
            return {}
        file_description = self.descriptor[file_name]
        described_columns = set(
            file_description[file_type]
            if file_type in ('fixed', 'change')
            else file_description[file_type][subfile_name]
        )
        if file_type != 'fixed':
            for key in get_primary_key(file_description):
                described_columns.add(key)
            described_columns.add('Timestep')
        if file_type == 'quantity':
            described_columns.add('Quantity')
        _, _, interpretation = separate_and_interpret_with_display(file_content[0], described_columns, self.display_message, f'{subfile_name or file_name} column', '  ')
        return interpretation

    def check_indices(self, name: str, indices: list):
        errors = 0
        unique_indices = set(indices)
        if len(unique_indices) < len(indices):
            duplicates = [
                (index, count)
                for index, count in zip(
                    unique_indices,
                    (indices.count(index) for index in unique_indices),
                )
                if count > 1
            ]
            n = len(duplicates)
            errors += n
            self.display_message(f"ERROR: {name} value{'s' if n > 1 else ''} defined multiple times:")
            for index, count in duplicates:
                self.display_message(f"  {', '.join(str(i) for i in index) if isinstance(index, tuple) else index}: {count}")
        return errors

    def convert_file(self, file_name: str):
        errors = 0

        file_description = self.descriptor[file_name]

        entities = []
        if file_name not in self.reader.files:
            return 0, errors

        fixed_file_to_convert = self.reader.files[file_name]

        primary_key = get_primary_key(file_description)

        interpretation = self.check_column_names(fixed_file_to_convert, file_name, 'fixed')
        main_keys = set(file_description['fixed']) | set(interpretation)
        for element in fixed_file_to_convert:
            entity = {k: v for k, v in element.items() if k in file_description['fixed']}
            entity.update({interpretation[k]: v for k, v in element.items() if k in interpretation})
            if any(entity.get(k) is None for k in primary_key) or not entity:
                continue
            extra = {k: v for k, v in element.items() if k not in main_keys}
            if extra:
                entity['extra'] = extra
            entities.append(entity)

        if primary_key:
            errors += self.check_indices(file_name, [tuple(entity[k] for k in primary_key) for entity in entities])

        if any(file_description[timed] for timed in ('event', 'change', 'quantity')):

            entity_by_id = dict()
            for entity in entities:
                entity_by_id[tuple(entity[k] for k in primary_key)] = entity

            time_files = dict()
            time_files[file_name + "Schedules"] = file_description['change'], 'change'
            for _event_name, _event_descriptor in file_description['event'].items():
                time_files[_event_name] = _event_descriptor, 'event'
            for _quantity_name, _quantity_descriptor in file_description['quantity'].items():
                time_files[_quantity_name] = _quantity_descriptor, 'quantity'
            quantity_files = set(file_description['quantity'].keys())

            for _sheet_name, (_columns, _type) in time_files.items():
                if _sheet_name not in self.reader.files or not _columns:
                    continue
                _sheet_to_convert = self.reader.files[_sheet_name]
                interpretation = self.check_column_names(_sheet_to_convert, file_name, _type, _sheet_name)
                indices = []
                unknown_ids = set()
                invalid_timesteps = set()
                invalid_quantities = set()
                for line in _sheet_to_convert:
                    for key, interpreted_key in interpretation.items():
                        line[interpreted_key] = line.pop(key)
                    _id = tuple(line.get(k) for k in primary_key)
                    if any(v is None for v in _id):
                        continue
                    if _id not in entity_by_id:
                        unknown_ids.add(_id)
                        continue
                    try:
                        timestep = float(line.get('Timestep') or 0)
                    except ValueError:
                        invalid_timesteps.add((_id, line.get('Timestep')))
                        continue
                    if timestep != int(timestep):
                        invalid_timesteps.add((_id, line.get('Timestep')))
                        continue
                    timestep = str(int(timestep))
                    index = (*_id, timestep)
                    if _sheet_name in quantity_files:
                        try:
                            quantity = float(line.get('Quantity') or 0)
                        except ValueError:
                            invalid_quantities.add((_id, line.get('Quantity')))
                            continue
                        if quantity != int(quantity):
                            invalid_quantities.add((_id, line.get('Quantity')))
                            continue
                        quantity = str(int(quantity))
                        index = (*index, quantity)
                    indices.append(index)
                    target_entity = entity_by_id[_id]
                    for column in (c for c in _columns if line.get(c) is not None):
                        if column not in target_entity:
                            target_entity[column] = dict()
                        if column in line:
                            if _sheet_name in quantity_files:
                                target_entity[column].setdefault(timestep, {})[quantity] = line[column]
                            else:
                                target_entity[column][timestep] = line[column]
                if unknown_ids:
                    n = len(unknown_ids)
                    errors += n
                    self.display_message(f"ERROR: {primary_key} value{'s' if n > 1 else ''} from {_sheet_name} not found in {file_name}:")
                    for _id in unknown_ids:
                        self.display_message(f"  {_id}")
                    non_referenced_ids = set(entity_by_id.keys()) - set(index[0] for index in indices)
                    if non_referenced_ids:
                        self.display_message(f"Suggestion: {primary_key} value{'s' if len(non_referenced_ids) > 1 else ''} from {file_name} not found in {_sheet_name}:")
                        for _id in non_referenced_ids:
                            self.display_message(f"  {_id}")
                if invalid_timesteps:
                    n = len(invalid_timesteps)
                    errors += n
                    self.display_message(f"ERROR: invalid Timestep value{'s' if n > 1 else ''} from {_sheet_name}:")
                    for _id, timestep in invalid_timesteps:
                        self.display_message(f"  {primary_key} {_id}: {timestep}")
                if invalid_quantities:
                    n = len(invalid_quantities)
                    errors += n
                    self.display_message(f"ERROR: invalid Quantity value{'s' if n > 1 else ''} from {_sheet_name}:")
                    for _id, quantity in invalid_quantities:
                        self.display_message(f"  {primary_key} {_id}: {quantity}")
                errors += self.check_indices(_sheet_name, indices)

        for entity in entities:
            for change in file_description['change']:
                raw_values = entity.get(change)
                if not raw_values:
                    continue
                timesteps = (t for t in sorted(raw_values.keys(), key=int))
                last_timestep = next(timesteps)
                filtered_values = {last_timestep: raw_values[last_timestep]}
                for timestep in timesteps:
                    if raw_values[timestep] != filtered_values[last_timestep]:
                        filtered_values[timestep] = raw_values[timestep]
                        last_timestep = timestep
                entity[change] = filtered_values

        if entities:
            self.writer.write_from_list(entities, file_name, primary_key[0] if len(primary_key) == 1 else None)
        return len(entities), errors

    def convert_all(self):
        errors = 0
        for _entity_type in self.descriptor.keys():
            self.display_message(f"Converting {_entity_type}")
            entity_count, error_count = self.convert_file(_entity_type)
            errors += error_count
            message = f"  count: {entity_count}"
            if error_count:
                message += f" ({error_count} error{'s' if error_count > 1 else ''})"
            self.display_message(message)
        self.display_message("File is fully converted")
        return errors
