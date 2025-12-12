from collections import namedtuple
from itertools import chain

from Supplychain.Schema.adt_column_description import ADTColumnDescription
from Supplychain.Schema.validation_schemas import ValidationSchemas

entity_types = [
    'Stock',
    'ProductionResource',
    'ProductionOperation',
    'Transport',
]

numeric_types = {
    'integer': int,
    'number': float,
}

NumericAttribute = namedtuple('NumericAttribute', [
    'entity_types',
    'attribute_type',
    'value_type',
    'minimum',
    'maximum',
])


def __get_properties(file_name, attribute, attribute_type):
    schemas = ValidationSchemas.schemas[file_name]['properties']
    if attribute not in schemas:
        return
    properties = schemas[attribute]
    depth = None
    match attribute_type:
        case 'fixed':
            depth = 0
        case 'change' | 'event':
            depth = 1
        case 'quantity':
            depth = 2
    for _ in range(depth):
        properties = properties['patternProperties']['^[0-9]+$']
    value_type = properties['type']
    if value_type not in numeric_types:
        return
    value_type = numeric_types[value_type]
    minimum = properties.get('minimum')
    maximum = properties.get('maximum')
    return file_name, attribute_type, value_type, minimum, maximum

excluded_numeric_attributes = set((
    'Latitude',
    'Longitude',
))

numeric_attributes = {}
for file_name, file_descriptor in ADTColumnDescription.format.items():
    if file_name not in entity_types:
        continue
    for attribute_type, attributes in file_descriptor.items():
        if isinstance(attributes, dict):
            attributes = list(chain(*attributes.values()))
        for attribute in attributes:
            if attribute in excluded_numeric_attributes:
                continue
            properties = __get_properties(file_name, attribute, attribute_type)
            if properties is not None:
                numeric_attributes.setdefault(attribute, []).append(properties)
for attribute_name, attribute_occurrences in numeric_attributes.items():
    (
        entity_types,
        attribute_types,
        value_types,
        minima,
        maxima
    ) = zip(*attribute_occurrences)
    numeric_attributes[attribute_name] = NumericAttribute(
        entity_types,
        attribute_types[0],
        value_types[0],
        minima[0],
        maxima[0],
    )
