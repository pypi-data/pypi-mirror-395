from typing import Union
from Supplychain.Wrappers.simulator import CosmoEngine
import comets as co


def run_simple_simulation(simulation_name: str,
                          amqp_consumer_adress: Union[str, None] = None,
                          modifications: Union[dict, None] = None) -> bool:

    if amqp_consumer_adress is None:
        used_consumers = []
    else:
        used_consumers = None

    simulator_interface = co.CosmoInterface(
        simulator_path='Simulation',
        custom_sim_engine=CosmoEngine,
        amqp_consumer_address=amqp_consumer_adress,
        simulation_name=simulation_name,
        used_consumers=used_consumers,
    )

    def get_outcomes(modelinterface):
        return {'IsFinished': modelinterface.sim.IsFinished()}

    simulationtask = co.ModelTask(modelinterface=simulator_interface, get_outcomes=get_outcomes)

    if modifications is None:
        modifications = {}
    outcome = simulationtask.evaluate(modifications)

    return outcome['IsFinished']
