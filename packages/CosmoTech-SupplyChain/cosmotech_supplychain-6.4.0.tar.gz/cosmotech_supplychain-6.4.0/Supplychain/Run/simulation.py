from typing import Union
import json

import numpy

from comets import CompositeSampling
from comets.utilities import to_list

from Supplychain.Generic.json_folder_reader import JSONReader
from Supplychain.Run.helpers import select_csv_or_amqp_consumers
from Supplychain.Run.uncertainty_analysis_helper_functions import encoder
from Supplychain.Run.uncertainty_specs import UncertaintySpecs, VariableDatasetElementCollection
from Supplychain.Schema.default_values import parameters_default_values
from Supplychain.Wrappers.environment_variables import EnvironmentVariables
from Supplychain.Wrappers.simulator import CosmoEngine, set_log_level


def run_simple_simulation(simulation_name: str,
                          uncertainty_specs: UncertaintySpecs = UncertaintySpecs([]),
                          simulation_path: str = 'Simulation',
                          amqp_consumer_adress: Union[str, None] = None,
                          modifications: Union[dict, None] = None,
                          output_dir: Union[str, None] = None,
                          seed: int = parameters_default_values["Configuration"]["UncertaintyAnalysisSeed"],
                          log_level: Union[str, None] = None) -> bool:
    if uncertainty_specs:
        reader = JSONReader(EnvironmentVariables.from_adt_folder)
        variable_dse_collection = VariableDatasetElementCollection(
            entity_attributes=uncertainty_specs.export_entity_attributes(),
            reader=reader,
            uncertainty_specs=uncertainty_specs,
            cosmo_interface=None,
        )
        sampling = uncertainty_specs.export_sampling()
        demands = {
            s['id']: s['Demands']
            for s in reader.files['Stock']
            if s['Demands']
        }

        numpy.random.seed(seed if seed >= 0 else None)
        input_sampling = to_list(sampling)
        sampler = CompositeSampling(input_sampling)
        list_of_samples = sampler.get_samples(1)
        input_parameter_set = list_of_samples[0]

        encoded_parameterset = encoder(
            input_parameter_set,
            demands,
            uncertainty_specs,
            variable_dse_collection,
        )
        if modifications is None:
            modifications = encoded_parameterset
        else:
            modifications.update(encoded_parameterset)

    simulator = CosmoEngine.LoadSimulator(simulation_path)

    set_log_level(CosmoEngine, log_level)

    if modifications:
        for datapath, stringvalue in modifications.items():
            valuetoset = stringvalue if isinstance(stringvalue, str) else json.dumps(stringvalue)
            simulator.FindAttribute(datapath).SetAsString(valuetoset)

    select_csv_or_amqp_consumers(
        simulation_name=simulation_name,
        simulator=simulator,
        output_dir=output_dir,
        amqp_consumer_adress=amqp_consumer_adress,
    )

    # Run simulation
    simulator.Run()
    return simulator.IsFinished()
