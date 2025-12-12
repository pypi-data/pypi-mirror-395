from typing import Union

from Supplychain.Generic.adx_wrapper import ADXWrapper
from Supplychain.Generic.json_folder_reader import JSONReader
from Supplychain.Generic.json_folder_writer import JSONWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Run.dataset_helpers import mapping_attribute_data_model_to_entity_types
from Supplychain.Wrappers.environment_variables import EnvironmentVariables


def make_adx_wrapper() -> Union[ADXWrapper, None]:
    if all(v is not None for v in EnvironmentVariables.adx_parameters.values()):
        return ADXWrapper(
            database=EnvironmentVariables.adx_parameters['database'],
            cluster_url=EnvironmentVariables.adx_parameters['uri'],
            ingest_url=EnvironmentVariables.adx_parameters['ingest-uri'],
        )
    return None

def find_element_in_dataset_by_id(id: str, reader: JSONReader, sheet_name=None, entities_only=True) -> dict:
    """
    Find the element in the dataset corresponding to a given id. If the flag
    entities_only is set to True, only the true entities (Stocks, Transports,
    ProductionOperations and ProductionResources) are searched. Otherwise, all
    elements are searched.

    NOTE: The ID is assumed to be unique in the entire dataset.
    TODO: is this true? If not, we need to change this function because
    it will only return the first entity with the given ID.

    TODO: is there even an interest to limit the search to entities only? The only
    possible reason would be speed, but maybe it's not worth it. To check with a
    very large instance.

    Args:
        entity_id (str): The ID of the entity to find
        reader (JSONReader): The JSONReader object to get the entities from
        sheet_name (str): The name of the sheet to search in. If None, all sheets
            are searched.
        entities_only: If True, only the true entities are searched. Otherwise,
            all elements are searched.
    """

    if entities_only:
        # TODO: is it a good idea to hardcode this here?
        sheet_names = ['Stock', 'Transport', 'ProductionOperation', 'ProductionResource']
    else:
        sheet_names = reader.files.keys()

    # If a sheet name is provided, only search in that sheet
    if sheet_name is not None:
        sheet_names = [sheet_name]

    # Loop over all entity types in order to find the entity
    for sheet_name in sheet_names:
        entities = get_sheet_from_dataset(sheet_name, reader, False)
        if not entities:
            continue
        # TODO: should get rid of this once Transport is homogenized
        # and also has an id field
        if sheet_name == "Transport":
            id_field_name = "Label"
        else:
            id_field_name = "id"
        # skip sheets without id (e.g. all relationship sheets)
        if id_field_name not in entities[0]:
            continue
        for entity in entities:
            if entity[id_field_name] == id:
                # add entity sheet_name to avoid having to call get_entity_type
                entity['sheet_name'] = sheet_name
                return entity

    # If the entity is not found, raise an error
    raise ValueError(f"Entity with ID {id} not found in {str(sheet_names)}")

def find_entities_by_tag(tag_id: str, reader: JSONReader) -> list:
    """
    Find all entities in the dataset that have a particular tag.

    Args:
        tag_id (str): The ID of the tag to find
        reader (JSONReader): The JSONReader object to get the entities from
    """

    # first look up the tag members in Tags
    taggroups = get_sheet_from_dataset('TagGroups', reader)

    # get the ids of all tag group members
    entity_ids = [taggroup['source'] for taggroup in taggroups if taggroup['target'] == tag_id]

    # get the entities themselves
    entities = []
    for entity_id in entity_ids:
        entities.append(find_element_in_dataset_by_id(entity_id, reader))

    return entities

def get_sheet_from_dataset(sheet_name: str, reader: JSONReader, check: bool=True) -> list:
    """
    Get a particular sheet from the dataset. This corresponds to finding
    all entities of a particular type in the case of entity sheets.
    Raises an error if the entity type is not found. This function
    is essentially a wrapper around the JSONReader object and only exists
    to make the code more readable and ensure an error is raised if the sheet
    is not found.

    Args:
        sheet_name (str): The name of the sheet (the type of entity) to get
        reader (JSONReader): The JSONReader object to read it from.
    Returns:
        list: The contents of the sheet, or an empty list if the sheet is
            not found. This list corresponds to the list of entities of
            the given type in the dataset.
    """
    sheet = reader.files.get(sheet_name, [])
    if check and not sheet:
        raise ValueError(f"Sheet {sheet_name} not found in dataset or has no contents")
    return sheet

def get_entity_type(entity_id: str, reader: JSONReader) -> str:
    """
    Get the type of an entity given its ID. This is done by searching for
    the entity in all sheets of the dataset and returning the name of the
    sheet where it was found.

    NOTE: this function is not very efficient because of the search.

    Args:
        entity_id (str): The ID of the entity to get the type of.
        reader (JSONReader): The JSONReader object to get the entities from.
    Returns:
        str: The type of the entity.
    """

    sheet_names = reader.files.keys()
    for sheet_name in sheet_names:
        # TODO: should get rid of this once Transport is homogenized
        # and also has an id field
        if sheet_name == "Transport":
            id_field_name = "Label"
        else:
            id_field_name = "id"
        entities = get_sheet_from_dataset(sheet_name, reader)
        for entity in entities:
            if id_field_name not in entity:
                continue
            if entity[id_field_name] == entity_id:
                return sheet_name
    raise ValueError(f"Entity with ID {entity_id} not found in dataset")


def match_entity_to_dataset_row(entity_name, entity_type, dataset_row):
    if entity_type == 'StockToOperation':
        return entity_name == f"{dataset_row.get('source')}_to_{dataset_row.get('target')}"
    if entity_type == 'Transport':
        return entity_name == dataset_row.get('Label')
    return entity_name == dataset_row.get('id')


def update_entity_attribute(entity_info: dict, reader: JSONReader):
    entity_name = entity_info["Entity"]
    attribute = entity_info["Attribute"]
    for entity_type in mapping_attribute_data_model_to_entity_types.get(attribute, []):
        for entity in reader.files.get(entity_type, []):
            if match_entity_to_dataset_row(entity_name, entity_type, entity):
                if isinstance(entity[attribute], dict):
                    entity[attribute]["0"] = entity_info["OptimizedValue"]
                else:
                    entity[attribute] = entity_info["OptimizedValue"]
                return entity_type


def update_entity_attributes_with_optimized_values(entity_list_info: list, reader: JSONReader, writer: JSONWriter):
    """
    Update entities with optimized attribute values.

    Processes a list of entity information dictionaries and updates
    corresponding entities with optimized attribute values. It finds the
    appropriate entity based on entity type and name, then updates the specified
    attribute with the optimized value.

    Args:
        entity_list_info (list): List of dictionaries containing entity information with the following keys:
            - Attribute (str): Name of the attribute to update
            - OptimizedValue (any): New value to set for the attribute
            - Entity (str): Name of the entity to update
        reader (JSONReader): JSONReader object to access the entity data
        writer (JSONWriter): JSONWriter object to write updated entity data

    Returns:
        None

    Updating Logic:
        1. For each entity_info, extracts Entity, Attribute, and OptimizedValue
        2. Loads the corresponding entities using the reader
        3. Searches for entities which matches the Entity name
        4. When a match is found, updates the attribute, handling both dictionary and simple values
        5. If any entity is modified, writes the updated data using the writer

    Note:
        - Handles attributes that are either dictionaries (updates the "0" key) or simple values
        - Skips processing if entity_list_info is empty
    """
    with Timer("[Run/Engine/Update Entities]") as t:
        t.display_message(f"{len(entity_list_info)} attribute{'s' if len(entity_list_info) > 1 else ''} to update.")

        modification_counter = {}
        for entity_info in entity_list_info:
            entity_type = update_entity_attribute(entity_info, reader)
            if entity_type is not None:
                modification_counter.setdefault(entity_type, 0)
                modification_counter[entity_type] += 1

        for entity_type, n in modification_counter.items():
            writer.write_from_list(dict_list=reader.files[entity_type], file_name=entity_type)
            t.display_message(f"{n} attribute{'s' if n > 1 else ''} updated in {entity_type}.")
