import os
import uuid

if 'CSM_SIMULATION_ID' not in os.environ:
    os.environ['CSM_SIMULATION_ID'] = str(uuid.uuid1())

SECONDS_IN_MINUTE = 60


def get_alternative_environ_var(*args):
    if not args:
        return None
    for key in args[:-1]:
        if key in os.environ:
            return os.environ[key]
    return args[-1]


class EnvironmentVariables:
    from_adt_folder = get_alternative_environ_var(
        'SUPPLY_DRIVER_FROM_ADT_FOLDER',
        'CSM_DATASET_ABSOLUTE_PATH',
        '/mnt/scenariorun-data/',
    )
    parameters_folder = get_alternative_environ_var(
        'SUPPLY_DRIVER_PARAMETER_FOLDER',
        'CSM_PARAMETERS_ABSOLUTE_PATH',
        '/mnt/scenariorun-parameters/',
    )
    temp_folder = get_alternative_environ_var(
        'SUPPLY_DRIVER_TEMP_FOLDER',
        'CSM_TEMP_ABSOLUTE_PATH',
        '/tmp/supply_tmp/',
    )
    simulation_import_folder = get_alternative_environ_var(
        'SUPPLY_DRIVER_SIMU_IMPORT_FOLDER',
        os.path.join(from_adt_folder, 'Import'),
    )
    simulation_id = get_alternative_environ_var(
        'CSM_SIMULATION_ID',
        str(uuid.uuid1()),
    )
    simulation_name = get_alternative_environ_var(
        'CSM_SIMULATION_VAR',
        'Simulation',
    )
    amqp_consumer = get_alternative_environ_var(
        'CSM_PROBES_MEASURES_TOPIC',
        None,
    )
    adx_parameters = {
        'uri': get_alternative_environ_var(
            'AZURE_DATA_EXPLORER_RESOURCE_URI',
            None,
        ),
        'ingest-uri': get_alternative_environ_var(
            'AZURE_DATA_EXPLORER_RESOURCE_INGEST_URI',
            None,
        ),
        'database': get_alternative_environ_var(
            'AZURE_DATA_EXPLORER_DATABASE_NAME',
            None,
        ),
    }
