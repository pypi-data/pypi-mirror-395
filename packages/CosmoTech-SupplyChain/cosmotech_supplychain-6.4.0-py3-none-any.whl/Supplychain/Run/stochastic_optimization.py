import pandas
from typing import Union, List
import comets as co
import numpy as np
import os
import psutil

from Supplychain.Wrappers.simulator import CosmoEngine, set_log_level
from Supplychain.Generic.timer import Timer
from Supplychain.Run.uncertainty_analysis_comets import UncertaintyAnalyzer
from Supplychain.Run.uncertainty_specs import UncertaintySpecs
from Supplychain.Schema.default_values import parameters_default_values
from Supplychain.Schema.statistics import statistic_aliases
from Supplychain.Wrappers.environment_variables import EnvironmentVariables

from Supplychain.Run.decision_variables import (
    DecisionVariableSpace,
    convert_decision_var_parameter_set_to_model_parameter_set,
    transform_decision_var_value_to_group_attribute_values
)


class StochasticOptimizer(Timer):
    """
    Object in charge of performing an optimization on the results of an uncertainty analysis.
    It is possible to run an optimization without uncertainties if the dataset has
    ActivateUncertainties set to false. The main method of the StochasticOptimizer is run,
    which returns the results of the optimization.

    NOTE: Default values are in principle taken from the parameters_default_values dictionary.

    Attributes:
        simulation_name (str): Name of simulation, used by the probes
        KPI (str): Which KPI is objective of the optimization. Choose among Profit, OPEX,
            AverageStockValue, ServiceLevelIndicator, TotalFillRateServiceLevel,
            CO2Emissions, TotalServedQuantity, IndividualTotalFillRateServiceLevel.
        stat (str, optional): Which statistics of the KPI we care about. Choose among mean, std,
            sem, quantile 5%, quantile 10%,	... , quantile 95%.
        optimization_mode (str, optional): Optimization mode, choose among "maximize"/"minimize"
            /"target".
        target_value (float, optional): Target value to reach if optimization_mode is "target".
            Note service levels are expressed between 0 and 100.
        service_level_of_stocks (list, optional): If KPI is
            IndividualTotalFillRateServiceLevel, choose for which stocks we want to
            optimize the service level. Defaults to [], which means all stocks are selected.
        decision_variables (DecisionVariableSpace): Decision variables to optimize. Defaults to
            an empty DecisionVariableSpace, which would result in an invalid optimization.
        constraint_handling (string, optional): If/how constraints are used in the optimization.
            If "None", constraints are not taken into account. Other possible values are methods
            of applying constraints.
        constraints (list, optional): A list of constraints and their values. This list must be
            composed of dictionaries each with the keys 'id', 'ConstrainedKpi', 'Statistic',
            'ConstraintType', 'ConstraintValue', 'PenaltyCoefficient'.
        simulation_path (str): Name of the simulation file.
        amqp_consumer_adress (Union[str, None], optional): Adress of consumer to send probe
            results to.
        sample_size_uncertainty_analysis (int, optional): Number of simulations runs by the
            uncertainty analysis.
        batch_size_uncertainty_analysis (int, optional): Number of simulations runs that are run
            in a same batch by the uncertainty analysis.
        max_iterations_for_optim (int, optional): Max number of runs of the task during the
            optimization.
        max_duration_of_optim (int, optional): Max duration (s) of the optim, the optim runs
            until either this duration, or max_iterations_for_optim is reached.
        optimization_algorithm (str, optional): Name of optimization algorithm.
        pop_batch_size (int, optional): Choose batch size of optimization -- the recommended
            value is highly dependent on the choice of algorithm).
        n_jobs (int, optional): Choose number of cpus used in parallel by the optimization.
            Note that the uncertainty analysis is also parallelized independently.
            Use -1 to use all cpus available.
    """

    def __init__(
        self,
        simulation_name: str,
        KPI: str = parameters_default_values["Configuration"]["Kpi"],
        stat: str = parameters_default_values["Configuration"]["Statistic"],
        optimization_mode: str = parameters_default_values["Configuration"]["OptimizationMode"],
        target_value: float = parameters_default_values["Configuration"]["TargetedValue"],
        service_level_of_stocks: list = [],
        # TODO: deal with default value: if empty, the optimization will not work or produce weird results
        decision_variables: DecisionVariableSpace = DecisionVariableSpace([]),
        constraint_handling: str = parameters_default_values["Configuration"]["ConstraintHandling"],
        constraints: List[Union[dict, None]] = [],
        simulation_path: str = "Simulation",
        amqp_consumer_adress: Union[str, None] = None,
        sample_size_uncertainty_analysis: int = parameters_default_values["Configuration"]["SampleSizeUncertaintyAnalysis"],
        batch_size_uncertainty_analysis: int = 200,
        max_iterations_for_optim: int = parameters_default_values["Configuration"]["MaxIterationsForOptim"],
        max_duration_of_optim: int = parameters_default_values["Configuration"]["OptimizationMaximalDuration"],
        optimization_algorithm: str = parameters_default_values["Configuration"]["OptimizationAlgorithm"],
        pop_batch_size: int = parameters_default_values["Configuration"]["PopulationBatchSize"],
        n_jobs: int = parameters_default_values["Configuration"]["OptimizationParallelization"],
        n_jobs_ua: int = parameters_default_values["Configuration"]["UncertaintyAnalysisParallelization"],
        uncertainty_specs: UncertaintySpecs = UncertaintySpecs([]),
        optim_seed: int = parameters_default_values["Configuration"]["OptimizationSeed"],
        ua_seed: int = parameters_default_values["Configuration"]["UncertaintyAnalysisSeedForOptimization"],
    ) -> None:
        Timer.__init__(self, prefix="[Optimize]")
        self.simulation_name = simulation_name
        self.KPI = KPI
        self.stat = stat
        self.optimization_mode = optimization_mode
        self.target_value = target_value
        self.service_level_of_stocks = service_level_of_stocks
        self.decision_variables = decision_variables
        # Constraints
        self.using_constraints = False if constraint_handling == "None" else True
        if constraint_handling == "automated":
            constraint_handling = "adaptive_barrier"
        self.constraint_handling = constraint_handling if self.using_constraints else "adaptive_barrier"
        self._constraints = constraints if self.using_constraints else []
        # Optimization config
        self.simulation_path = simulation_path
        self.amqp_consumer_adress = amqp_consumer_adress
        self.sample_size_uncertainty_analysis = sample_size_uncertainty_analysis
        self.batch_size_uncertainty_analysis = batch_size_uncertainty_analysis
        self.max_iterations_for_optim = max_iterations_for_optim
        self.max_duration_of_optim = max_duration_of_optim
        self.optimization_algorithm = optimization_algorithm
        self.pop_batch_size = pop_batch_size
        self.n_jobs_optim = n_jobs
        self.n_jobs_ua = n_jobs_ua
        self.uncertainty_specs = uncertainty_specs
        self.ua_seed = ua_seed
        self.optim_seed = optim_seed

    def initialize(self) -> None:
        """
        Initialize the optimization by collecting information from the simulator, creating the optimization space and task.
        """
        # Collect simulator information
        cosmo_interface = co.CosmoInterface(
            self.simulation_path, custom_sim_engine=CosmoEngine
        )
        cosmo_interface.initialize()

        # Retrieve the CoSML datapaths for all decision variable group members
        # This is done here because we have a CosmoInterface open here, and we want to limit
        # the number of times we open a CosmoInterface or call the CoSML API.
        self.decision_variables.retrieve_all_datapaths_from_cosmo_interface(cosmo_interface)

        self.ActivateUncertainties = cosmo_interface.get_outputs(
            ["Model::@ActivateUncertainties"]
        )["Model::@ActivateUncertainties"]

        self.SubDataset = cosmo_interface.get_outputs(
            ["Model::@SubDataset"]
        )["Model::@SubDataset"]

        # Close the simulator interface again to avoid memory leaks
        cosmo_interface.terminate()

        # Create optimization space in the format required by CoMETS, based on the decision variables
        self._create_optimization_space()

        # If uncertainties are not activated in the model, set standard parameters of uncertainty analysis
        if not self.ActivateUncertainties or not self.uncertainty_specs:
            self.sample_size_uncertainty_analysis = 1
            self.batch_size_uncertainty_analysis = 1
            self.stat = "mean"

        # Create constraints in the format required by CoMETS
        self.constraints = []
        if self.using_constraints:
            self.display_message("Adding constraints to the optimization:")
            for raw_constraint in self._constraints:
                constraint = {
                    "name": raw_constraint["id"],
                    "type": raw_constraint["ConstraintType"],
                    "threshold": raw_constraint["ConstraintValue"],
                    "coefficient": raw_constraint["PenaltyCoefficient"]
                }
                self.display_message(
                    f"  {raw_constraint['id']}:"
                    f" {raw_constraint['ConstrainedKpi']}"
                    f" {raw_constraint['Statistic']}"
                    f" {raw_constraint['ConstraintType']}"
                    f" {raw_constraint['ConstraintValue']}"
                    f" (penalty coefficient: {raw_constraint['PenaltyCoefficient']})"
                )
                self.constraints.append(constraint)

        # Create uncertainty analyzer
        consumers = ["Performances"]
        if self.KPI == "IndividualTotalFillRateServiceLevel":
            consumers.append("StocksAtEndOfSimulation")

        self.display_message("Setting up uncertainty analyzer to be used in optimization.")
        self.ua = UncertaintyAnalyzer(
            simulation_name=self.simulation_name,
            simulation_path=self.simulation_path,
            amqp_consumer_adress=None,
            sample_size=self.sample_size_uncertainty_analysis,
            batch_size=self.batch_size_uncertainty_analysis,
            uncertainty_specs=self.uncertainty_specs,
            consumers=consumers,
            cold_inputs={},
            validation_folder=None,
            n_jobs=self.n_jobs_ua,
            seed=self.ua_seed,
        )

        # Initialize uncertainty analysis
        self.ua.create_simulator_interface()
        self.ua.collect_simulation_parameters()
        self.ua.create_encoder()
        self.ua.create_get_outcomes()
        self.ua.create_sampling()

        # Declare task running the uncertainty analysis
        self.display_message("Setting up optimization Task.")

        def task(
            input_parameter_set: dict,
            ua: UncertaintyAnalyzer = self.ua,
            activateuncertainties: bool = self.ActivateUncertainties,
            _compute_objective=_compute_objective,
            KPI: str = self.KPI,
            stat: str = self.stat,
            optimization_mode: str = self.optimization_mode,
            target_value: Union[int, float] = self.target_value,
            service_level_of_stocks: list = self.service_level_of_stocks,
            constraints: list = self._constraints,
            decision_variables: DecisionVariableSpace = self.decision_variables,
        ) -> dict:
            """
            The task to be run by the optimization algorithm. This task runs an uncertainty
            analysis. From the CoMETS point of view, the only input is the input_parameter_set,
            which is a dictionary with the decision variables as keys and their values as values.
            The task then transforms this input_parameter_set into a format that can be used
            by the uncertainty analysis, runs the uncertainty analysis, and computes the
            objective and constrained KPI values.

            NOTE: the task must be a **pure function**, so that it doesn't cause issues
            when running in parallel. This means that all information that is needed inside the
            task must be explicitly passed as an argument to the function, not implicitly from
            e.g. the class instance via a `self.my_attribute`. These arguments are then given
            default values in the function signature, so that from the point of view of the
            CoMETS optimization algorithm, the task is a function that takes only one argument:
            the input_parameter_set.
            """

            if activateuncertainties:
                np.random.seed()
            else:
                np.random.seed(0)

            # Transform the input parameter set (in decision variable space)
            # to a format that can be understood by the Cosmo model
            input_parameters_cosmo_model = convert_decision_var_parameter_set_to_model_parameter_set(
                decision_var_parameter_set=input_parameter_set,
                decision_variable_space=decision_variables,
            )

            ua.create_task(input_parameters_cosmo_model)
            ua.run_experiment()
            ua.reformat_results()

            # Retrieve objective and KPI value
            objective = _compute_objective(
                ua.results,
                KPI=KPI,
                stat=stat,
                optimization_mode=optimization_mode,
                target_value=target_value,
                service_level_of_stocks=service_level_of_stocks,
            )

            # Retrieve values of the constrained KPIs
            constrained_kpi_values = _retrieve_constrained_kpi_values(
                ua.results,
                constraints=constraints,
                service_level_of_stocks=service_level_of_stocks,
            )

            # Combine the objective and constraints output into one dict/parameterset
            task_outputs = {**objective, **constrained_kpi_values}

            return task_outputs

        self.task = task

        self.summarize_optimization()

    def run(self) -> tuple:
        """Run the optimization

        Returns:
            Tuple (kpi_results, optimal_decision_var_attributes, optimal_attribute_values_df, entity_list_info, optimization_history):
                **kpi_results** is a dictionary containing key Objective (the optimal value of the objective
                    function) and value KPI (the optimal value of the KPI, may be different from the objective)
                **optimal_decision_var_attributes** is a dictionary (ParameterSet) with keys that are datapaths
                    of decision variables, and values that are their recommended value by the optimization.
                    It may be used to launch a new uncertainty analysis with the optimal decision variables. The
                    values are in the format that can be directly inserted into the model, i.e. schedulable
                    values are of a dict format.
                **optimal_attribute_values_df** is a pandas dataframe containing the recommended choice
                    of decision variables, with columns Datapath, Value, Attribute, Entity.
                **entity_list_info** is a list of dictionaries with information for updating the decision
                    variables in the data model after optimization.
                **optimization_history** is a pandas dataframe containing the optimization metrics, with columns
                    ObjectiveValue, KPIValue, Iteration, KPI, Stat, optimization_mode, target_value.
        """
        self.initialize()

        if self.optim_seed == -1:
            np.random.seed()
        else:
            np.random.seed(self.optim_seed)

        opt = co.Optimization(
            space=self.space,
            task=self.task,
            objective="Objective",
            maximize=(self.optimization_mode == "maximize"),
            constraint_method=self.constraint_handling,
            constraints=self.constraints,
            algorithm=self.optimization_algorithm,
            batch_size=self.pop_batch_size,
            stop_criteria={
                "max_evaluations": self.max_iterations_for_optim * self.pop_batch_size,
                "max_duration": self.max_duration_of_optim,
            },
            n_jobs=self.n_jobs_optim,
            save_optimization_history=True,
        )

        self.display_message("Running optimization. This may take a while...")
        opt.run()
        self.display_message(f"Optimization finished after {opt.number_of_evaluations} Task evaluations. Retrieving results...")

        # Obtain the KPI results for the optimal variables. This involves running the task
        # one more time.
        kpi_results = self._obtain_kpi_results(opt.results["Optimal variables"])
        optimization_history = self._reformat_optimization_history(
            opt.optimization_history
        )
        # results in decision variable space
        optimal_decision_vars_in_decision_var_space = opt.results["Optimal variables"]
        optimal_decision_var_attributes = convert_decision_var_parameter_set_to_model_parameter_set(
            optimal_decision_vars_in_decision_var_space,
            self.decision_variables,
        )
        # results in attribute space
        optimal_attribute_values_df, entity_list_info = self._transform_optimal_decision_vars_to_attribute_dataframe_and_list_info(
            optimal_decision_vars_in_decision_var_space
        )
        if self.optimization_algorithm == "NGOpt" and self.pop_batch_size == 1:
            del opt.optimizationalgorithm

        # Return log level to Info
        set_log_level(CosmoEngine, os.environ.get('LOG_LEVEL', 'INFO'))

        return (
            kpi_results,
            # TODO: both of these are given in attribute space, should we
            # also return the values in decision variable space?
            optimal_decision_var_attributes,
            optimal_attribute_values_df,
            entity_list_info,
            optimization_history,
        )

    def summarize_optimization(self) -> None:
        """
        Print a summary of the optimization (and UA) settings.
        """

        self.display_message("\nOptimization settings:")
        adding_target = f" to {self.target_value}" if self.optimization_mode == "target" else ""
        d_plural = len(self.decision_variables) != 1
        # count number of modified attributes by the diecision variables
        n_attributes = sum(len(dv.group_members) for dv in self.decision_variables)
        a_plural = n_attributes != 1
        n_constraints = len(self.constraints)
        c_plural = len(self.constraints) != 1
        self.display_message(
            f"- Objective is to {self.optimization_mode} {self.stat} {self.KPI}{adding_target}.\n"
            f"- This is done by varying {len(self.decision_variables)} decision variable{'s' if d_plural else ''}"
            f" that modif{'y' if d_plural else 'ies'} {n_attributes} model attribute{'s' if a_plural else ''} in total.\n"
            f"- The optimization is subject to {n_constraints} constraint{'s' if c_plural else ''}.\n"
            f"- max number of Task evaluations: {self.max_iterations_for_optim * self.pop_batch_size} (timeout: {self.max_duration_of_optim} s)\n"
            f"- optimization algorithm: {self.optimization_algorithm}\n"
            f"- population batch size: {self.pop_batch_size}\n"
            f"- optimization parallelization: {self.n_jobs_optim}\n"
            f"- UA parallelization: {self.n_jobs_ua}\n"
            f"- UA sample size: {self.sample_size_uncertainty_analysis}\n"
        )

    def _create_optimization_space(self) -> None:
        """
        Transform the decision variables into the optimization space in the format
        required by CoMETS. The space is a list of dictionaries, each dictionary
        representing a decision variable. The dictionary must have the following keys:
        - name: the id of the decision variable - must be unique
        - type: the type of the decision variable, currently either "float" or "int"
            but in theory "categorical" is possible in CoMETS.
        - bounds: the bounds of the decision variable (min, max)
        - init: the initial value of the decision variable
        """

        space = []
        for decision_variable in self.decision_variables:
            space.append({
                "name": decision_variable.id,
                "type": decision_variable.var_type,
                "bounds": [decision_variable.min, decision_variable.max],
                "init": decision_variable.init_value,
            })
        self.space = space

    def _transform_optimal_decision_vars_to_attribute_dataframe_and_list_info(self, decision_variable_results: dict) -> tuple[pandas.DataFrame, list]:
        """
        Transform the optimal decision variable results from decision variable space to attribute space
        and generate information about entity types.

        This method:
        1. Maps each decision variable to its corresponding attributes and entities
        2. Calculates optimized values, initial values, and relative variations
        3. Handles special cases like SourcingProportions that need normalization
        4. Creates a dataframe with detailed attribute information
        5. Generates entity type information for downstream processing

        Args:
            decision_variable_results (dict): Dictionary mapping decision variable IDs to their optimal values

        Returns:
            tuple[pandas.DataFrame, list]: A tuple containing:
                - DataFrame with columns for Datapath, OptimizedValue, InitialValue, RelativeVariation,
                  Attribute, Entity, SimulationRun, and SubDataset
                - List of dictionaries with information for updating the decision variables
                  in the data model after optimization
        """

        def calculate_relative_variation(reference, value):
            return (value - reference) / reference if reference else 0.0

        df_contents = []
        # Outer loop: loop over decision variables
        for dv_id, value in decision_variable_results.items():
            # Retrieve the decision variable
            # TODO: this search is not very efficient since decision_variables is a list
            # However, it is only done once each optimization.
            decision_variable = self.decision_variables.find_decision_variable_by_id(dv_id)
            # transform the decision var value to one or multiple attribute values
            attribute_values = transform_decision_var_value_to_group_attribute_values(
                decision_var_value=value,
                decision_variable=decision_variable,
            )
            # transform the initial decision var value to one or multiple initial attribute values
            initial_attribute_values = transform_decision_var_value_to_group_attribute_values(
                decision_var_value=decision_variable.init_value,
                decision_variable=decision_variable,
            )
            # Inner loop: loop over all members of the decision variable group and retrieve
            # all the necessary information for every entity/attribute combination
            # individually. This is because we want to output the attribute values, not the
            # decision variable values.
            for group_member in decision_variable.group_members:
                att_value = attribute_values[group_member.cosml_datapath]
                initial_att_value = initial_attribute_values[group_member.cosml_datapath]
                # Transform time-variable attribute value to value
                att_value = att_value[0] if group_member.attribute_is_time_variable else att_value
                initial_att_value = initial_att_value[0] if group_member.attribute_is_time_variable else initial_att_value
                # Calculate variation percentage
                variation = calculate_relative_variation(initial_att_value, att_value)

                # Append the collected information to the dataframe contents
                df_contents.append(
                    {
                        "Datapath": group_member.cosml_datapath,
                        "OptimizedValue": att_value,
                        "InitialValue": initial_att_value,
                        "RelativeVariation": variation,
                        "Attribute": group_member.attribute_name,
                        "Entity": group_member.entity_id,
                        "SimulationRun": EnvironmentVariables.simulation_id,
                        "SubDataset": self.SubDataset,
                    }
                )
            if decision_variable.inverse is not None:
                # Calculate variation for inverse as well
                initial_inverse_value = 1 - initial_att_value
                inverse_value = 1 - att_value
                inverse_variation = calculate_relative_variation(initial_inverse_value, inverse_value)
                df_contents.append(
                    {
                        "Datapath": decision_variable.inverse.cosml_datapath,
                        "OptimizedValue": inverse_value,
                        "InitialValue": initial_inverse_value,
                        "RelativeVariation": inverse_variation,
                        "Attribute": decision_variable.inverse.attribute_name,
                        "Entity": decision_variable.inverse.entity_id,
                        "SimulationRun": EnvironmentVariables.simulation_id,
                        "SubDataset": self.SubDataset,
                    }
                )
        sourcing_proportion_sums = {}
        rows_to_normalize = []
        for row in df_contents:
            if row['Attribute'] == 'SourcingProportions' and row['Entity'] in self.decision_variables.sources_to_normalize:
                entity = self.decision_variables.stocks_by_source[row['Entity']]
                sourcing_proportion_sums.setdefault(entity, 0)
                sourcing_proportion_sums[entity] += row['OptimizedValue']
                rows_to_normalize.append((row, entity))
        for row, entity in rows_to_normalize:
            row['OptimizedValue'] = row['OptimizedValue'] / sourcing_proportion_sums[entity] if sourcing_proportion_sums[entity] else 1
            # Recalculate variation after normalization
            row['RelativeVariation'] = calculate_relative_variation(row['InitialValue'], row['OptimizedValue'])

        # Create entity list info from the dataframe contents
        entity_list_info = [
            {
                "Attribute": row['Attribute'],
                "OptimizedValue": row['OptimizedValue'],
                "Entity": row['Entity']
            }
            for row in df_contents
        ]

        return pandas.DataFrame(df_contents), entity_list_info

    def _reformat_optimization_history(self, list_of_results: dict[str, list]) -> pandas.DataFrame:
        rows = []
        if self.KPI != "IndividualTotalFillRateServiceLevel":
            for ((iteration, objective), kpivalue) in zip(
                enumerate(list_of_results["mean_objective"]),
                list_of_results["mean_task_outputs"],
            ):
                rows.append(
                    {
                        "ObjectiveValue": objective,
                        "KPIValue": kpivalue["KPI"],
                        "Iteration": iteration,
                        "KPI": self.KPI,
                        "Stat": self.stat,
                        "optimization_mode": self.optimization_mode,
                        "target_value": self.target_value,
                        "SimulationRun": EnvironmentVariables.simulation_id,
                        "SubDataset": self.SubDataset,
                    }
                )
        else:
            for ((iteration, objective), kpivalue) in zip(
                enumerate(list_of_results["mean_objective"]),
                list_of_results["all_task_outputs"],
            ):
                rows.append(
                    {
                        "ObjectiveValue": objective,
                        "KPIValue": np.mean(kpivalue[0]["KPI"]),
                        "Iteration": iteration,
                        "KPI": self.KPI,
                        "Stat": self.stat,
                        "optimization_mode": self.optimization_mode,
                        "target_value": self.target_value,
                        "SimulationRun": EnvironmentVariables.simulation_id,
                        "SubDataset": self.SubDataset,
                    }
                )
        return pandas.DataFrame(rows)

    def _obtain_kpi_results(self, optimal_variables: dict[str, int | float]) -> pandas.DataFrame:
        """
        Run an additional task to obtain the KPI results for the optimal variables.
        """
        results = self.task(optimal_variables)
        index = None
        if all(isinstance(value, float) for value in results.values()):
            index = [0]
        results["SimulationRun"] = EnvironmentVariables.simulation_id
        results["SubDataset"] = self.SubDataset
        return pandas.DataFrame(results, index=index, columns=(
            'Objective',
            'KPI',
            'SimulationRun',
            'SubDataset',
        ))


# Implementing a function instead of a method to be able to use it in the multiprocessing module
def _compute_objective(
    results: dict,
    KPI: str,
    stat: str,
    optimization_mode: str,
    target_value: float,
    service_level_of_stocks: list
) -> dict:
    """
    Function to compute the objective of the optimization. Depending on the optimization
    mode, the objective is either the KPI value itself, the distance to a target value,
    or the sum of the KPI values. The function also handles the case where the KPI is
    IndividualTotalFillRateServiceLevel, in which case the objective is the
    distance to the target value for the worst performing stock in case of target mode,
    or the sum of the service levels otherwise.

    NOTE: this is implemented as a pure function in order to be able to use it in the
    multiprocessing module.

    Args:
        results (dict): the results of the uncertainty analysis
        KPI (str): the name of the KPI to optimize
        stat (str): the statistic on the KPI to use
        optimization_mode (str): the mode of optimization, either "maximize", "minimize"
            or "target"
        target_value (float): the target value to reach (only used in target mode)
        service_level_of_stocks (list): the stocks for which to optimize the service
            level (only used in case of IndividualTotalFillRateServiceLevel)

    Returns:
        objective (dict): a dictionary containing the objective value and the KPI value(s).
    """

    if KPI != "IndividualTotalFillRateServiceLevel":
        results["Performances"] = results["Performances"].set_index("KPI")
        kpi = results["Performances"].loc[KPI, stat]
        if optimization_mode == "target":
            objective = {"Objective": (kpi - target_value) ** 2, "KPI": kpi}
        else:
            objective = {"Objective": kpi, "KPI": kpi}
    else:
        df_service = results["StocksAtEndOfSimulation"][
            results["StocksAtEndOfSimulation"]["Category"] == "TotalFillRateServiceLevel"
        ]
        if service_level_of_stocks != []:
            df_service = df_service[df_service["id"].isin(service_level_of_stocks)]
        else:
            df_demand = results["StocksAtEndOfSimulation"][
                results["StocksAtEndOfSimulation"]["Category"] == "TotalDemand"
            ]
            stocks_with_demand = set(df_demand[df_demand["Mean"] > 0]["id"])
            if stocks_with_demand:
                df_service = df_service[df_service["id"].isin(stocks_with_demand)]
        vector_of_service_levels = df_service[statistic_aliases[stat]].to_numpy()
        if optimization_mode == "target":
            distance_to_target = (vector_of_service_levels - target_value) ** 2
            objective = {
                "Objective": np.max(distance_to_target),  # np.sum(distance_to_target)
                "KPI": list(vector_of_service_levels),
            }
        else:
            objective = {
                "Objective": np.sum(vector_of_service_levels),
                "KPI": list(vector_of_service_levels),
            }
    return objective


def _retrieve_constrained_kpi_values(ua_results: dict, constraints: list, service_level_of_stocks: list) -> dict:
    """
    Retrieve the values of the constrained KPIs from the uncertainty analysis results.
    Note that these values are not the constraining values (i.e. not the limits), but
    the real resulting values of the KPIs that at the end of the optimisaion. These
    values may or may not satisfy the constraints.

    Args:
        ua_results (dict): the results of the uncertainty analysis
        constraints (list): the list of constraints and their values
        service_level_of_stocks (list): the stocks for which to optimize the service
            level (only used in case of IndividualTotalFillRateServiceLevel)

    Returns:
        constrained_kpi_values (dict): a dictionary containing the values of the
            constrained KPIs, with the keys being the ids of the constraints.
    """

    df_perf = None
    if "Performances" in ua_results:
        df_perf = ua_results["Performances"]
        if df_perf.index.name is None:
            df_perf = df_perf.set_index('KPI')
    df_stocks = None
    if "StocksAtEndOfSimulation" in ua_results:
        df_stocks = ua_results["StocksAtEndOfSimulation"]
        if not service_level_of_stocks:
            df_demand = df_stocks[df_stocks["Category"] == "TotalDemand"]
            service_level_of_stocks = set(df_demand[df_demand["Mean"] > 0]["id"])
        if service_level_of_stocks:
            df_stocks = df_stocks[df_stocks["id"].isin(service_level_of_stocks)]

    constrained_kpi_values = {}

    for constraint in constraints:
        id = constraint["id"]
        kpi = constraint['ConstrainedKpi']
        stat = constraint['Statistic']
        constrained_kpi_value = None
        if kpi == "IndividualTotalFillRateServiceLevel":
            df_service = df_stocks[df_stocks["Category"] == "TotalFillRateServiceLevel"].set_index('id')
            vector_of_service_levels = df_service[statistic_aliases[stat]].to_numpy()
            match constraint["ConstraintType"]:
                case "greater_than":
                    constrained_kpi_value = vector_of_service_levels.min()
                case "less_than":
                    constrained_kpi_value = vector_of_service_levels.max()
                case "equal_to":
                    target_value = constraint['ConstraintValue']
                    distance_to_target = abs(vector_of_service_levels - target_value)
                    constrained_kpi_value = vector_of_service_levels[distance_to_target.argmax()]
        else:
            constrained_kpi_value = df_perf.loc[kpi, stat]
        constrained_kpi_values[id] = constrained_kpi_value

    return constrained_kpi_values


def check_children(timer: Timer) -> list:
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    if children:
        timer.display_message(
            f"Child processes are still running. "
            "\nWhen running locally on your own machine, this may cause undesirable memory leaks. "
            "\nTo kill these processes using a terminal, run:\n"
            f"$ for pid in {' '.join(str(child.pid) for child in children)}; do kill -9 $pid; done"
        )
    return children
