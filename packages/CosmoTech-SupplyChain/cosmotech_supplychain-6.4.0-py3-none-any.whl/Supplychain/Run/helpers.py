import os
from typing import Union

import csm.engine as CosmoEngine


def select_csv_or_amqp_consumers(
    simulation_name: str,
    simulator: CosmoEngine,
    output_dir: Union[str, None] = None,
    amqp_consumer_adress: Union[str, None] = None,
    used_probes: Union[list, None] = None,
) -> None:
    if used_probes is not None:
        # Delete unused probes and connected consumers
        for probe in simulator.GetProbes():
            if probe.GetType() not in used_probes:
                simulator.DestroyProbe(probe)
        for consumer in simulator.GetConsumers():
            if consumer.GetProbes()[0] not in used_probes:
                simulator.DestroyConsumer(consumer)

    if amqp_consumer_adress is not None and "CSM_CONTROL_PLANE_TOPIC" in os.environ:
        # Remove local CSV consumers
        if output_dir is None:
            for consumer in simulator.GetConsumers():
                simulator.DestroyConsumer(consumer)
        # Instantiate AMQP consumers to send data to the cloud service
        simulator.InstantiateAMQPConsumers(simulation_name, amqp_consumer_adress)
    if output_dir is not None:
        # Set the destination of local CSV consumers
        for consumer in simulator.GetConsumers():
            consumer.SetProperty("OutputDirectory", output_dir)
