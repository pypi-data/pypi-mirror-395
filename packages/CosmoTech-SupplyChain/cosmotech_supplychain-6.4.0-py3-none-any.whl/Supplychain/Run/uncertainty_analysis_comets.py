from typing import Union

import pandas
import comets as co
import numpy as np
import os

from Supplychain.Wrappers.simulator import CosmoEngine, set_log_level
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Run.simulation import run_simple_simulation
from Supplychain.Run.consumers import (
    StockConsumer,
    PerformanceConsumer,
    StocksAtEndOfSimulationConsumer,
)
from Supplychain.Run.uncertainty_analysis_helper_functions import encoder
from Supplychain.Run.uncertainty_specs import (
    UncertaintySpecs,
    VariableDatasetElementCollection,
)
from Supplychain.Run.uncertainty_analysis_helper_functions import (
    get_max_time_step,
    get_attribute,
    get_stocks,
    get_stocks_with_demands,
    get_transports,
    extend_dic,
    add_tag_to_parameterset,
    collect_simulated_stock_final_output,
    collect_simulated_stock_output,
    collect_simulated_transport_output,
    transform_data,
    transform_performances_data,
    # create_demand_generator,
)

from Supplychain.Generic.json_folder_reader import JSONReader
from Supplychain.Wrappers.environment_variables import EnvironmentVariables
from Supplychain.Schema.default_values import parameters_default_values

default_parameters = {
    "simulation_name": "Default Simulation",
    "simulation_path": "Simulation",
    "sample_size": parameters_default_values["Configuration"]["FinalSampleSizeUncertaintyAnalysis"],
    "batch_size": 100,
    "uncertainty_specs": UncertaintySpecs([]),
    "amqp_consumer_adress": None,
    "consumers": parameters_default_values["Configuration"]["UncertaintyAnalysisOutputData"],
    "validation_folder": None,
    "cold_inputs": {},
    "timer": None,
    "n_jobs": parameters_default_values["Configuration"]["MaxNumberOfSimInParallel"],
    "seed": parameters_default_values["Configuration"]["UncertaintyAnalysisSeed"],
    "adx_writer": None,
    "output_dir": None,
}


class UncertaintyAnalyzer:
    """
    Object in charge of performing the different steps of the uncertainty analysis.
    Its main method is "execute".

    Args:
        simulation_name (str): Name of simulation, used by the probes
        simulation_path (str): Name of the simulation file (typically Simulation)
        sample_size (int): Number of simulations runs by the uncertainty analysis
        batch_size (int): Number of simulations runs that are run in a same batch by the uncertainty analysis
        amqp_consumer_adress (Union[str, None], optional): Adress of consumer to send probe results to.
        consumers (list, optional): Which consumers are activated.
        validation_folder (str, optional): Local folder to which results are written to, used by the tests.
        cold_inputs (dict, optional): Parameters that are passed to the simulator at each simulation and don't change during the analysis.
        timer (Timer object, optional): Timer object that can be used for logs and counting time.
    """

    def __init__(
        self,
        simulation_name=default_parameters["simulation_name"],
        simulation_path=default_parameters["simulation_path"],
        sample_size=default_parameters["sample_size"],
        batch_size=default_parameters["batch_size"],
        uncertainty_specs=default_parameters["uncertainty_specs"],
        amqp_consumer_adress=default_parameters["amqp_consumer_adress"],
        consumers=default_parameters["consumers"],
        validation_folder=default_parameters["validation_folder"],
        cold_inputs=default_parameters["cold_inputs"],
        timer=default_parameters["timer"],
        n_jobs=default_parameters["n_jobs"],
        seed=default_parameters["seed"],
    ):
        if timer is None:
            self.t = Timer("[Run Uncertainty]")
        else:
            self.t = timer
        self.simulation_name = simulation_name
        self.simulation_path = simulation_path
        self.amqp_consumer_adress = amqp_consumer_adress
        self.sample_size = sample_size
        self.batch_size = batch_size
        self.uncertainty_specs = uncertainty_specs
        self.validation_folder = validation_folder
        if amqp_consumer_adress is None and "PerformanceAMQP" in consumers:
            consumers.remove("PerformanceAMQP")
        self.consumers = consumers
        self.cold_inputs = cold_inputs
        self.seed = seed
        if self.batch_size > self.sample_size:
            self.batch_size = self.sample_size

        self.n_jobs = n_jobs

        # Initialize the variable dataset element collection
        self.initialize_variable_dse_collection()

    def initialize_variable_dse_collection(self):
        """
        Initialize the variable dataset element collection. This collection contains
        all the dataset elements that are varied during the uncertainty analysis, plus
        their datapaths as well as information on which uncertainty variables affect them.

        Building the VariableDatasetElementCollection requires:
        - the uncertainty specs (via self)
        - access to the dataset via a reader (read using the EnvironmentVariables)
        - a CosmoInterface object (via self)
        """

        # create and initialize the CosmoInterface
        self.create_simulator_interface()
        self.simulator_interface.initialize()
        # initialize reader
        reader = JSONReader(EnvironmentVariables.from_adt_folder)
        # generate a VariableDatasetElementCollection from the uncertainty specs
        varied_entity_attributes = self.uncertainty_specs.export_entity_attributes()
        self.variable_dse_collection = VariableDatasetElementCollection(
            entity_attributes=varied_entity_attributes,
            reader=reader,
            uncertainty_specs=self.uncertainty_specs,
            cosmo_interface=self.simulator_interface,
        )
        # terminate the CosmoInterface (to prevent memory leaks)
        self.simulator_interface.terminate(remove_sim_clone=True)

    def execute(self):
        """Setup and run the uncertainty analysis

        Returns:
            dict: dictionary with keys among the non AMQP consumers
                containing the output tables. Which table is available depends on the specified
                consumers of the UncertaintyAnalyzer.
        """
        self.t.split("Initialize uncertainty analysis")
        self.create_simulator_interface()
        self.collect_simulation_parameters()
        self.create_encoder()
        self.create_get_outcomes()
        self.create_sampling()
        self.create_task(self.cold_inputs)
        self.t.split(
            "Ended uncertainty analysis initialization : {time_since_last_split}"
        )

        self.t.display_message("Run uncertainty analysis")
        self.run_experiment()
        self.t.split("Ended uncertainty analysis run : {time_since_last_split}")

        self.t.display_message("Reformat uncertainty analysis results")
        self.reformat_results()
        if self.validation_folder:
            self.write_results_locally()
        self.t.split(
            "Ended uncertainty analysis reformatting : {time_since_last_split}"
        )

        return self.results

    def create_simulator_interface(self):
        used_probes = []
        used_consumers = []
        custom_consumers = []

        if "Stocks" in self.consumers:
            used_probes.append("Stocks")
            custom_consumers.append((StockConsumer, "LocalConsumer", "Stocks"))
        if "StocksAtEndOfSimulation" in self.consumers:
            used_probes.append("StocksAtEndOfSimulation")
            custom_consumers.append(
                (StocksAtEndOfSimulationConsumer, "StocksAtEndOfSimulationConsumer", "StocksAtEndOfSimulation")
            )
        if "Performances" in self.consumers:
            used_probes.append("PerformanceIndicators")
            custom_consumers.append(
                (
                    PerformanceConsumer,
                    "LocalPerformanceConsumer",
                    "PerformanceIndicators",
                )
            )
        if "PerformanceAMQP" in self.consumers:
            used_consumers.append("PerformanceIndicatorsAMQP")

        self.simulator_interface = co.CosmoInterface(
            simulator_path=self.simulation_path,
            custom_sim_engine=CosmoEngine,
            simulation_name=self.simulation_name,
            amqp_consumer_address=self.amqp_consumer_adress,
            used_consumers=used_consumers,
            used_probes=used_probes,
            custom_consumers=custom_consumers,
            use_clone=(self.n_jobs == 1),
            controlPlaneTopic=("PerformanceAMQP" in self.consumers)  # Prevent the SDK from sending any data to ADX when not required
        )

    def collect_simulation_parameters(self):
        """
        Collect values of attributes of the model
        """
        # Load simulator to be able to access attributes of the model
        self.simulator_interface.initialize()

        # Retrieving model information
        self.max_time_step = get_max_time_step(self.simulator_interface)
        self.ActivateCorrelatedDemandUncertainties = False
        # self.ActivateCorrelatedDemandUncertainties = get_attribute(
        #     self.simulator_interface, "Model::@ActivateCorrelatedDemandUncertainties"
        # )
        # self.DemandCorrelations = get_attribute(
        #     self.simulator_interface, "Model::@DemandCorrelations"
        # )
        self.ActivateUncertainties = get_attribute(
            self.simulator_interface,
            "Model::@ActivateUncertainties",
        )
        self.SubDataset = get_attribute(
            self.simulator_interface,
            "Model::@SubDataset",
        )

        # Getting the name of all the stocks with uncertain demand
        if self.ActivateCorrelatedDemandUncertainties:
            self.uncertain_stocks = get_stocks(self.simulator_interface)
        else:
            self.uncertain_stocks = []

        # Getting the name of all the transport operations
        self.all_transports = get_transports(self.simulator_interface)

        # Collect model information about demands of each stock
        self.demands = {}
        demands = {}
        stocks = get_stocks_with_demands(self.simulator_interface)
        for stock in stocks:
            self.demands[stock] = get_attribute(
                self.simulator_interface,
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{stock}::@Demand",
            )
            if stock in self.uncertain_stocks:
                demands[stock] = self.demands[stock]

        self.simulator_interface.terminate(remove_sim_clone=True)

        # Extending the dictionaries above for scheduled attributes so that all time steps are present
        self.extended_demands = extend_dic(demands, self.max_time_step)

        if not self.ActivateUncertainties:
            # Remove uncertain stocks if ActivateUncertainties is false
            self.uncertain_stocks = []

    def create_encoder(self):
        """Create encoder of the task"""

        self.encoder = lambda input_parameter_set: encoder(
            input_parameter_set,
            demands=self.demands,
            uncertainty_specs=self.uncertainty_specs,
            variable_dse_collection=self.variable_dse_collection,
        )

    def create_get_outcomes(self):
        """Create the get_outcomes function of the task"""

        def get_outcomes(
            modelinterface,
            consumers=self.consumers,
            all_transports=self.all_transports,
            max_time_step=self.max_time_step,
        ):
            """
            Returns a parameter set with all the model's output. More precisely, the parameter set is the
            the result of the concatenation of up to four parameter sets, depending on the consumers that have been chosen.
            In front of the name of each parameter, we add a '1_', '2_', '3_' or '4_' to identify the 4 original parametersets.
            The first one looks like this:
            {'1_U__&@&__0': 5, '1_U__&@&__1': 5, [...], '1_U__&@&__10': 6}.
            The keys correspond to transport_name + __&@&__ + time_step,
            and the value to the duration of the transport at this time step.
            The second parameter set looks like this:
            {'2_A__&@&__ServedQuantity__&@&__0': 0.0, '2_A__&@&__UnservedQuantity__&@&__0': 0.0}.
            The keys correspond to stock + __&@&__ + category (Demand, ServedQuantity,...)  + __&@&__ +  time_step
            The third parameter set contains the performance indicators {'3_OPEX': 0.0, '3_Profit': 1.0, ...}.
            The fourth parameter set looks like:
            {'4_A__&@&__TotalDemand': 1.0}.
            The keys correspond to stock name + __&@&__ + category (TotalDemand, TotalServedQuantity, TotalFillRateServiceLevel, CycleServiceLevel)
            """

            output_parameterset = {}
            if "Transports" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "1_",
                        collect_simulated_transport_output(
                            all_transports, modelinterface, max_time_step
                        ),
                    )
                )
            if "Stocks" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "2_",
                        collect_simulated_stock_output(
                            modelinterface.LocalConsumer.memory
                        ),
                    )
                )
            if "Performances" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "3_", modelinterface.LocalPerformanceConsumer.memory[0]
                    )
                )
            if "StocksAtEndOfSimulation" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "4_",
                        collect_simulated_stock_final_output(
                            modelinterface.StocksAtEndOfSimulationConsumer.memory
                        ),
                    )
                )
            return output_parameterset

        self.get_outcomes = get_outcomes

    def create_sampling(self):
        """Create the sampling of the uncertainty analysis"""

        self.sampling = self.uncertainty_specs.export_sampling()
        if not self.sampling:
            self.sampling.append(
                {
                    'name': 'AvoidNoSamplingCometsCrash',
                    'sampling': 'seed_generator',
                }
            )


    def create_task(self, cold_inputs={}):
        """Create the task on which the uncertainty analysis will be performed

        Args:
            cold_inputs (dict): ParameterSet containing parameters of the simulator
                that will be applied to each evaluation of the task.
                Allows to modify other attributes than those modified by the uncertainty analysis.
        """
        if (
            self.ActivateCorrelatedDemandUncertainties
        ):  # Correlated demands are not compatible with demands drawn inside the model
            cold_input_parameter_set = {
                "{Model}Model::{Attribute}ActivateUncertainties": 0
            }
        else:
            cold_input_parameter_set = {}

        cold_input_parameter_set.update(cold_inputs)

        self.simulationtask = co.ModelTask(
            modelinterface=self.simulator_interface,
            encode=self.encoder,
            get_outcomes=self.get_outcomes,
            cold_input_parameter_set=cold_input_parameter_set,
        )

    def run_experiment(self):
        """Create and run the uncertainty analysis experiment"""
        if self.validation_folder is not None:
            save_task_history = True
        else:
            save_task_history = False

        if self.seed == -1:
            np.random.seed()
        else:
            np.random.seed(self.seed)

        self.experiment = co.UncertaintyAnalysis(
            task=self.simulationtask,
            sampling=self.sampling,
            stop_criteria={"max_evaluations": self.sample_size},
            analyzer=["standard", "quantiles"],
            n_jobs=self.n_jobs,
            save_task_history=save_task_history,
        )

        self.experiment.run()

    def reformat_results(self):
        """Reformat results of the experiment so that they are compatible with the output tables"""
        self.results = {}
        # Separating the results data on the different types of outputs (stock, transport, performances, stocksatendofsimulation)
        self.experiment.results["statistics"].reset_index(inplace=True)
        self.experiment.results["statistics"]["OutputType"] = (
            self.experiment.results["statistics"]["index"]
            .str.split(pat="_", expand=False, n=1)
            .str[0]
        )
        self.experiment.results["statistics"]["index"] = (
            self.experiment.results["statistics"]["index"]
            .str.split(pat="_", expand=False, n=1)
            .str[1]
        )
        if "Transports" in self.consumers:
            df_transportation_lead_time = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "1"
            ]
            df_transportation_lead_time = df_transportation_lead_time.drop("OutputType", axis=1)
            df_transport_final = transform_data(df_transportation_lead_time)
            self.results["Transports"] = df_transport_final
        if "Stocks" in self.consumers:
            df_probe_data = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "2"
            ]
            df_probe_data = df_probe_data.drop("OutputType", axis=1)
            df_stock_final = transform_data(df_probe_data)
            self.results["Stocks"] = df_stock_final
        if "Performances" in self.consumers:
            performances = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "3"
            ]
            performances = performances.drop("OutputType", axis=1)
            performances = transform_performances_data(performances)
            performances["SubDataset"] = self.SubDataset
            self.results["Performances"] = performances
        if "StocksAtEndOfSimulation" in self.consumers:
            df_stocksatendofsimulationconsumer = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "4"
            ]
            df_stocksatendofsimulationconsumer = df_stocksatendofsimulationconsumer.drop("OutputType", axis=1)
            df_stocksatendofsimulationconsumer = transform_data(df_stocksatendofsimulationconsumer, timestep=False)
            self.results["StocksAtEndOfSimulation"] = df_stocksatendofsimulationconsumer

    def write_results_locally(self):
        """Write the results tables locally to csv files"""

        # Get all demands directly from the experiment, before aggregation of statistics
        demands = []
        j = 0
        for i in self.experiment.task_history["outputs"]:

            for (k, v) in i.items():
                if "__&@&__Demand__&@&__" in k:
                    demand_result_dict = {}
                    demand_result_dict["Simulation"] = j
                    demand_result_dict["Entity"] = k.split("__&@&__Demand__&@&__")[
                        0
                    ].split("_", 1)[1]
                    demand_result_dict["TimeStep"] = k.split("__&@&__Demand__&@&__")[1]
                    demand_result_dict["Demand"] = v

                    demands.append(demand_result_dict)
            j += 1
        demand_df = pandas.DataFrame(demands)
        demand_df.to_csv(
            str(self.validation_folder) + "/df_all_demands.csv", index=False
        )
        self.results["Stocks"].to_csv(
            str(self.validation_folder) + "/final_df_comets.csv", index=False
        )
        self.results["StocksAtEndOfSimulation"].to_csv(
            str(self.validation_folder) + "/df_stocksatendofsimulation.csv", index=False
        )
        self.results["Transports"].to_csv(
            str(self.validation_folder) + "/df_transport.csv", index=False
        )
        self.results["Performances"].to_csv(
            str(self.validation_folder) + "/df_performances.csv", index=False
        )


def uncertainty_analysis(
    simulation_name: str = default_parameters["simulation_name"],
    simulation_path: str = default_parameters["simulation_path"],
    amqp_consumer_adress: Union[str, None] = default_parameters["amqp_consumer_adress"],
    sample_size: int = default_parameters["sample_size"],
    batch_size: int = default_parameters["batch_size"],
    n_jobs: int = default_parameters["n_jobs"],
    uncertainty_specs = default_parameters["uncertainty_specs"],
    adx_writer: Union[ADXAndFileWriter, None] = default_parameters["adx_writer"],
    validation_folder: Union[str, None] = default_parameters["validation_folder"],
    cold_inputs: dict = default_parameters["cold_inputs"],  # Additional parameters that might be passed to the simulator at each task evaluation
    output_dir: Union[str, None] = default_parameters["output_dir"],
    seed: int = default_parameters["seed"],
    consumers: list = default_parameters["consumers"],
):

    with Timer("[Run Uncertainty Analysis]") as t:

        if not uncertainty_specs:
            t.display_message('No uncertainties, skipping analysis', 'WARNING')
        else:
            ua = UncertaintyAnalyzer(
                simulation_name=simulation_name,
                simulation_path=simulation_path,
                amqp_consumer_adress=amqp_consumer_adress,
                sample_size=sample_size,
                batch_size=batch_size,
                uncertainty_specs=uncertainty_specs,
                n_jobs=n_jobs,
                validation_folder=validation_folder,
                consumers=consumers,
                cold_inputs=cold_inputs,
                timer=t,
                seed=seed,
            )

            results = ua.execute()

            if adx_writer is not None:
                t.split("Sending stats to ADX")
                if "Performances" in consumers:
                    performances_df = results["Performances"]
                    renaming = {
                        "KPI": "Category",
                        "mean": "Mean",
                        "sem": "SE",
                        "std": "STD",
                        "confidence interval of the mean at 95%": "CI95",
                    }
                    for i in range(5, 100, 5):
                        renaming[f"quantile {i}%"] = "Percentile{i}"
                    performances_df = performances_df.rename(columns=renaming)
                result_names = [
                    ("Stocks", "StockUncertaintyStatistics"),
                    ("StocksAtEndOfSimulation", "StocksAtEndOfSimulationUncertaintyStatistics"),
                    ("Transports", "TransportUncertaintyStatistics"),
                    ("Performances", "PerformanceIndicatorUncertaintyStatistics"),
                ]
                for consumer, table in result_names:
                    if consumer in consumers:
                        adx_writer.write_target_file(results[consumer].to_dict("records"), table)

                t.split("Sent stats to ADX : {time_since_last_split}")

            t.display_message("Running simple simulation to fill ADX")
            # Put back log level to Info for final simulation
            set_log_level(CosmoEngine, os.environ.get('LOG_LEVEL', 'INFO'))

        stop_uncertainty = {"Model::@ActivateUncertainties": "false"}

        run_simple_simulation(
            simulation_name=simulation_name,
            simulation_path=simulation_path,
            amqp_consumer_adress=amqp_consumer_adress,
            modifications=stop_uncertainty,
            output_dir=output_dir,
        )
        t.split("Final simulation succeeded : {time_since_last_split}")
