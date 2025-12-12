import numpy
import random
import multiprocessing
import os
from typing import Union
from Supplychain.Wrappers.simulator import CosmoEngine, set_log_level
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
import pandas as pd
from Supplychain.Generic.timer import Timer
from math import sqrt
from Supplychain.Wrappers.environment_variables import EnvironmentVariables
from Supplychain.Run.helpers import select_csv_or_amqp_consumers
from Supplychain.Run.simulation import run_simple_simulation


def run_simulation_with_seed(simulation_name: str,
                             seed: int,
                             amqp_consumer_adress: Union[str, None] = None,
                             output_list=None,
                             output_dir: Union[str, None] = None) -> bool:
    # Reduce log level to Error during optimization
    set_log_level(CosmoEngine, 'ERROR')
    simulator = CosmoEngine.LoadSimulator('Simulation')

    simulator.FindAttribute("{Model}Model::{Attribute}Seed").SetAsString(
        str(seed)
    )

    select_csv_or_amqp_consumers(
        simulation_name=simulation_name,
        simulator=simulator,
        output_dir=output_dir,
        amqp_consumer_adress=amqp_consumer_adress,
        used_probes=['PerformanceIndicators', 'Stocks'],
    )

    # Replace Stocks consumer

    for consumer in simulator.GetConsumers():
        if consumer.GetName() in ["CSVStocksConsumer", "StocksAMQP"]:
            simulator.DestroyConsumer(consumer)

    class StockConsumer(CosmoEngine.Consumer):
        memory = list()

        def Consume(self, p_data):
            probe_output = CosmoEngine.StocksProbeOutput.Cast(p_data)
            f = probe_output.GetFacts()
            timestep = int(probe_output.GetProbeRunDimension().GetProbeOutputCounter())
            for data in f:
                fact = [str(data.GetAttributeAsString('id')),
                        timestep,
                        float(data.GetAttributeAsDouble('Demand')),
                        float(data.GetAttributeAsDouble('RemainingQuantity')),
                        float(data.GetAttributeAsDouble('ServedQuantity')),
                        float(data.GetAttributeAsDouble('UnservedQuantity'))]
                self.memory.append(fact)

    consumer = StockConsumer("LocalConsumer")
    consumer.Connect(simulator.GetProbe("Stocks"))

    # Run simulation
    simulator.Run()

    if output_list is not None:
        output_list.extend(StockConsumer.memory)

    # Remove all the consumers in case that amqp consumers are still connected to ADX
    for consumer in simulator.GetConsumers():
        simulator.DestroyConsumer(consumer)

    return simulator.IsFinished()


def uncertainty_analysis(simulation_name: str,
                         amqp_consumer_adress: Union[str, None] = None,
                         sample_size: int = 1000,
                         batch_size: int = 100,
                         adx_writer: Union[ADXAndFileWriter, None] = None,
                         output_dir: Union[str, None] = None):
    with Timer('[Run Uncertainty]') as t:
        if batch_size > sample_size:
            batch_size = sample_size

        maxint = numpy.iinfo(numpy.int32).max
        seedlist = random.sample(range(maxint), sample_size)
        processes_size = min(multiprocessing.cpu_count(), batch_size)
        manager = multiprocessing.Manager()
        probe_data = manager.list()
        t.display_message("Starting simulations")
        with multiprocessing.Pool(processes_size) as p:
            for i in range(0, len(seedlist), batch_size):
                subseedlist = seedlist[i:i + batch_size]
                params = list(map(lambda seed: (simulation_name, seed, amqp_consumer_adress, probe_data, output_dir), subseedlist))
                p.starmap(run_simulation_with_seed, params)
        t.split("Ended simulations : {time_since_start}")

        df = pd.DataFrame((record for record in probe_data))
        df.columns = ['id', 'TimeStep', 'Demand', 'RemainingQuantity', 'ServedQuantity', 'UnservedQuantity']
        t.split("Create dataframes for stats computation: {time_since_last_split}")

        quantiles = (
            (0.05, 'FirstVigintile'),
            (0.25, 'FirstQuartile'),
            (0.50, 'Median'),
            (0.75, 'LastQuartile'),
            (0.95, 'LastVigintile'),
        )
        quantile_list, quantile_name_list = [list(t) for t in zip(*quantiles)]
        groups = df.groupby(['id', 'TimeStep'])
        df_quantiles = groups.quantile(quantile_list)
        df_average = groups.mean()
        df_error = groups.agg(lambda x: x.std() / sqrt(x.count()))
        t.split("Compute stats : {time_since_last_split}")

        # since use of pivot to have 1 column per tuple (quantile, valuetype)
        # then use of stack to have 1 line per (stock, timestep, valuetype)
        df3 = df_quantiles.reset_index().pivot(index=['id',
                                                      'TimeStep'],
                                               columns='level_2',
                                               values=['Demand',
                                                       'RemainingQuantity',
                                                       'ServedQuantity',
                                                       'UnservedQuantity']).stack(level=0)
        df3.reset_index(inplace=True)
        df3.columns = ['id',
                       'TimeStep',
                       'Category'] + quantile_name_list

        # use of stack to have 1 line per (stock, timestep, valuetype)
        df4 = df_average.stack(level=0)
        df4 = df4.reset_index()
        df4.columns = ['id',
                       'TimeStep',
                       'Category',
                       'Mean']

        # use of stack to have 1 line per (stock, timestep, valuetype)
        df5 = df_error.stack(level=0)
        df5 = df5.reset_index()
        df5.columns = ['id',
                       'TimeStep',
                       'Category',
                       'SE']

        # Merge of dfs to final df
        final_df = pd.merge(df3, df4, on=['id',
                                          'TimeStep',
                                          'Category'])
        final_df = pd.merge(final_df, df5, on=['id',
                                               'TimeStep',
                                               'Category'])

        final_df['SimulationRun'] = EnvironmentVariables.simulation_id
        final_df = final_df[
            [
                'TimeStep',
                'SimulationRun',
                'id',
            ]
            + quantile_name_list
            + [
                'Mean',
                'SE',
                'Category',
            ]
        ]
        adx_writer.write_target_file(final_df.to_dict('records'), 'StockUncertaintyStatistics', EnvironmentVariables.simulation_id)

        t.split("Sent stats to ADX : {time_since_last_split}")
        t.display_message("Running simple simulation to fill ADX")
        # Put back log level to Info for final simulation
        set_log_level(CosmoEngine, os.environ.get('LOG_LEVEL', 'INFO'))

        stop_uncertainty = {
            "Model::@ActivateUncertainties": "false"
        }

        run_simple_simulation(simulation_name=simulation_name,
                              amqp_consumer_adress=amqp_consumer_adress,
                              modifications=stop_uncertainty,
                              output_dir=output_dir)
