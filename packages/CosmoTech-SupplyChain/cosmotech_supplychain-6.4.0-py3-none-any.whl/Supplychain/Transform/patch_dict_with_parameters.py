import io
import json
import math
from collections import defaultdict
from dateutil import parser

from Supplychain.Generic.cosmo_api_parameters import CosmoAPIParameters
from Supplychain.Generic.csv_folder_reader import CSVReader
from Supplychain.Generic.excel_folder_reader import ExcelReader
from Supplychain.Generic.folder_io import FolderWriter, FolderReader
from Supplychain.Generic.memory_folder_io import MemoryFolderIO
from Supplychain.Generic.timer import Timer
from Supplychain.Generic.util import str_to_bool
from Supplychain.Schema.default_values import parameters_default_values
from Supplychain.Transform.from_table_to_dict import write_transformed_data
from Supplychain.Wrappers.environment_variables import SECONDS_IN_MINUTE

GRANULARITIES = {
    "minute": 1,
    "hour": 60,
    "day": 60 * 24,
    "week": 60 * 24 * 7,
    "month": 60 * 24 * 30,
    "quarter": 60 * 24 * 90,
    "year": 60 * 24 * 365,
}


def enforce_type(value, type_function):
    if type_function is not str and isinstance(value, str):
        if type_function is bool:
            value = str_to_bool(value)
        if type_function in (list, dict):
            try:
                value = json.load(io.StringIO(value))
            except (json.decoder.JSONDecodeError, TypeError):
                pass
    if not isinstance(value, type_function):
        value = type_function(value)
    return value


def get_value(row, entity_type, attribute):
    value = row.get(attribute)
    if value is None or value == "":
        value = parameters_default_values[entity_type][attribute]
    return value


class DictPatcher(Timer):
    def __write_updated_files(self):
        to_use_reader = self.memory

        # ADT column names to be replaced for post ADT simulation
        name_replacements = {"$sourceId": "source", "$targetId": "target", "$id": "id"}

        for file_name, file_content in to_use_reader.files.items():
            self.writer.write_from_list(
                dict_list=[
                    {
                        name_replacements.get(item_k, item_k): item_v
                        for item_k, item_v in item.items()
                    }
                    for item in file_content
                ],
                file_name=file_name,
            )

    def __init__(
        self, reader: FolderReader, writer: FolderWriter, parameters: CosmoAPIParameters
    ):
        Timer.__init__(self, "[ParameterHandler]")
        self.parameters = parameters
        self.writer = writer
        self.reader = reader

        self.memory = MemoryFolderIO()
        for file_name, file_content in self.reader.files.items():
            self.memory.write_from_list(dict_list=file_content, file_name=file_name)
        if "Configuration" not in self.memory.files:
            self.memory.files["Configuration"] = [
                dict(),
            ]

    def handle_mass_action_lever(self):
        try:
            lever_folder = self.parameters.get_dataset_path("mass_lever_excel_file")
        except ValueError:
            self.display_message("No mass action lever found - skipping", "DEBUG")
            return False, 0
        lever_reader = ExcelReader(lever_folder, keep_nones=False)
        self.memory.reset()

        reading_errors = write_transformed_data(reader=lever_reader, writer=self.memory)
        if reading_errors:
            return True, reading_errors
        if not self.memory.files.setdefault("Configuration", []):
            self.memory.files["Configuration"].append({})

        self.__write_updated_files()
        return True, 0

    def handle_simple_simulation(self):
        configuration = self.memory.files["Configuration"][0]

        time_parameters = ("start_date", "end_date", "simulation_granularity")
        parameter_values = {}
        for parameter_name in time_parameters:
            try:
                parameter_values[parameter_name] = self.parameters.get_named_parameter(parameter_name).value
            except ValueError:
                self.display_message(f"{parameter_name} is not defined - skipping", "DEBUG")
                continue

        start_date = None
        if "start_date" in parameter_values:
            start_date = parser.isoparse(parameter_values["start_date"])
            configuration["StartingDate"] = start_date.isoformat()
            self.display_message(f"Starting Date: {configuration['StartingDate']}")
        elif "StartingDate" in configuration:
            start_date = parser.isoparse(configuration["StartingDate"])
            self.display_message(f"Starting Date: {configuration['StartingDate']}")

        end_date = None
        if "end_date" in parameter_values:
            end_date = parser.isoparse(parameter_values["end_date"])

        simulation_granularity = configuration.get("TimeStepDuration", parameters_default_values["Configuration"]["TimeStepDuration"])
        if "simulation_granularity" in parameter_values:
            simulation_granularity = GRANULARITIES[parameter_values["simulation_granularity"]]
        configuration["TimeStepDuration"] = simulation_granularity
        self.display_message(f"TimeStep Duration: {simulation_granularity} minutes")

        steps_per_cycle = configuration.get("StepsPerCycle", parameters_default_values["Configuration"]["StepsPerCycle"])
        configuration["StepsPerCycle"] = steps_per_cycle
        self.display_message(f"Steps per Cycle: {steps_per_cycle}")

        cycles = configuration.get("SimulatedCycles", parameters_default_values["Configuration"]["SimulatedCycles"])
        if start_date is not None and end_date is not None:
            duration = (end_date - start_date).total_seconds() // SECONDS_IN_MINUTE
            cycles = int(math.ceil(duration / simulation_granularity / steps_per_cycle))
        configuration["SimulatedCycles"] = cycles
        self.display_message(f"Simulated Cycles: {cycles}")

        self.__write_updated_files()

    def handle_optimization_parameter(self):
        parameters = (('optimization_objective', 'OptimizationObjective', 'Optimization Objective', str),)
        errors = 0
        for name, config_name, display_name, type_f in parameters:
            errors += self.__handle_configuration_parameter(name, config_name, display_name, type_f)
        self.__write_updated_files()
        return errors

    def handle_flow_management_policies(self):
        parameters = (
            ("stock_policy", "Stock", "StockPolicy"),
            ("sourcing_policy", "Stock", "SourcingPolicy"),
            ("stock_dispatch_policy", "Stock", "DispatchPolicy"),
            ("production_policy", "ProductionResource", "ProductionPolicy"),
        )
        for parameter_name, entity_type, entity_parameter_name in parameters:
            try:
                parameter_value = self.parameters.get_named_parameter(
                    parameter_name
                ).value
            except ValueError:
                self.display_message(f"{parameter_name} is not defined - skipping", "DEBUG")
                continue
            if parameter_value == "FromDataset":
                continue
            if entity_type not in self.memory.files:
                continue
            entities = self.memory.files[entity_type]
            for entity in entities:
                entity[entity_parameter_name] = parameter_value
            entities_count = len(entities)
            self.display_message(
                f"Set {entity_parameter_name} to {parameter_value} for all {entity_type} "
                f'({entities_count} entit{"ies" if entities_count > 1 else "y"})'
            )
        self.__write_updated_files()

    def handle_safety_quantity_variation(self):
        self.__handle_safety_stock_tab()
        parameter_name = "safety_quantity_variation"
        try:
            variation = self.parameters.get_named_parameter(parameter_name).value
        except ValueError:
            self.display_message(f"{parameter_name} is not defined - skipping", "DEBUG")
            return
        variation = enforce_type(variation, float)
        self.display_message(f"Safety quantity variation: {variation}")
        key = "SafetyQuantities"
        for stock in self.memory.files["Stock"]:
            if stock.get(key):
                stock[key] = {
                    t: safety_quantity * (1 + variation)
                    for t, safety_quantity
                    in stock[key].items()
                }
        self.__write_updated_files()

    def handle_model_behavior(self):
        parameters = (
            (
                "manage_backlog_quantities",
                "ManageBacklogQuantities",
                "Manage Backlog Quantities",
                bool,
            ),
            (
                "empty_obsolete_stocks",
                "EmptyObsoleteStocks",
                "Empty Obsolete Stocks",
                bool,
            ),
            ("batch_size", "BatchSize", "Batch Size", int),
            (
                "inventory_capital_cost",
                "InventoryCapitalCost",
                "Inventory Capital Cost",
                float,
            ),
            ("carbon_tax", "CarbonTax", "Carbon Tax", float),
            (
                "intermediary_stock_dispatch_policy",
                "IntermediaryStockDispatchPolicy",
                "Intermediary Stock Dispatch Policy",
                str,
            ),
            (
                "actualize_shipments",
                "ActualizeShipments",
                "Actualize Shipments",
                bool,
            ),
            (
                "finite_production_capacity",
                "FiniteProductionCapacity",
                "Finite Production Capacity",
                bool,
            ),
            (
                "use_demands_as_sales_forecasts",
                "UseDemandsAsSalesForecasts",
                "Use Demands As Sales Forecasts",
                bool,
            ),
        )
        errors = 0
        for name, config_name, display_name, type_f in parameters:
            errors += self.__handle_configuration_parameter(
                name, config_name, display_name, type_f
            )
        self.__write_updated_files()
        return errors

    def handle_uncertainties_settings(self):
        parameters = (
            (
                "activate_uncertainties",
                "ActivateUncertainties",
                "Activate uncertainties",
                list,
            ),
            (
                "sample_size_uncertainty_analysis",
                "FinalSampleSizeUncertaintyAnalysis",
                "Final Sample Size Uncertainty Analysis",
                int,
            ),
            (
                "max_number_of_sim_in_parallel",
                "MaxNumberOfSimInParallel",
                "Max Number Of Sim In Parallel",
                int,
            ),
            (
                "uncertainty_analysis_output_data",
                "UncertaintyAnalysisOutputData",
                "Uncertainty analysis output data",
                list,
            ),
        )
        errors = 0
        for name, config_name, display_name, type_f in parameters:
            errors += self.__handle_configuration_parameter(
                name, config_name, display_name, type_f
            )
        self.__write_updated_files()
        return errors

    def __handle_configuration_parameter(
        self,
        parameter_name: str,
        configuration_parameter_name: str,
        display_name: str,
        type_function,
    ) -> bool:
        configuration = self.memory.files["Configuration"][0]
        try:
            parameter_value = self.parameters.get_named_parameter(parameter_name).value
        except ValueError:
            self.display_message(f"{parameter_name} is not defined - skipping", "DEBUG")
            return 0
        try:
            parameter_value = enforce_type(parameter_value, type_function)
        except ValueError:
            self.display_message(f"{parameter_name}: {parameter_value!r} could not be converted to {type_function.__name__}", "ERROR")
            return 1
        self.display_message(f"{display_name}: {parameter_value}")
        configuration[configuration_parameter_name] = parameter_value
        return 0

    def __handle_safety_stock_tab(self):
        try:
            safety_stock_folder = self.parameters.get_dataset_path("safety_stocks_tab")
        except ValueError:
            self.display_message("No safety stock found - skipping", "DEBUG")
            return
        reader = CSVReader(safety_stock_folder)
        stock_changes = dict()
        for k, safety_stock in reader.files.items():
            for _safety_stock in safety_stock:
                stock_id = _safety_stock.get("StockName")
                timestep = '0'
                stock_changes.setdefault(stock_id, dict())
                stock_changes[stock_id][timestep] = _safety_stock.get("SafetyStockLevels")

        for e in self.memory.files.get("Stock", []):
            change = stock_changes.get(e["Label"])
            if change:
                e["SafetyQuantities"] = change
        self.__write_updated_files()

    def handle_stochastic_optimization_parameters(self):
        parameters = (
            (
                "KPI",
                "Kpi",
                "KPI",
                str,
            ),
            (
                "optimization_mode",
                "OptimizationMode",
                "Optimization Mode",
                str,
            ),
            (
                "statistic",
                "Statistic",
                "Statistic",
                str,
            ),
            (
                "targeted_value",
                "TargetedValue",
                "Targeted Value",
                float,
            ),
            (
                "decision_variable",
                "DecisionVariable",
                "Decision Variable",
                str,
            ),
            (
                "decision_variable_min",
                "DecisionVariableMin",
                "DecisionVariable Min",
                float,
            ),
            (
                "decision_variable_max",
                "DecisionVariableMax",
                "DecisionVariable Max",
                float,
            ),
            (
                "optimization_maximal_duration",
                "OptimizationMaximalDuration",
                "Optimization Maximal Duration",
                float,
            ),
            (
                "optimization_algorithm",
                "OptimizationAlgorithm",
                "Optimization Algorithm",
                str,
            ),
            (
                "population_batch_size",
                "PopulationBatchSize",
                "Population Batch Size",
                int,
            ),
            (
                "activate_uncertainties",
                "ActivateUncertainties",
                "Activate uncertainties",
                list,
            ),
            (
                "sample_size_uncertainty_analysis_optim",
                "SampleSizeUncertaintyAnalysis",
                "Sample Size Uncertainty Analysis",
                int,
            ),
            (
                "final_sample_size_uncertainty_analysis",
                "FinalSampleSizeUncertaintyAnalysis",
                "Final Sample Size Uncertainty Analysis",
                int,
            ),
            (
                "max_iterations_for_optim",
                "MaxIterationsForOptim",
                "Max Iterations For Optim",
                int,
            ),
            (
                "automatic_parallelization_config",
                "AutomaticParallelizationConfig",
                "Automatic Parallelization Config",
                bool,
            ),
            (
                "max_number_of_sim_in_parallel",
                "MaxNumberOfSimInParallel",
                "Max Number Of Sim In Parallel",
                int,
            ),
        )

        errors = 0
        for name, config_name, display_name, type_f in parameters:
            errors += self.__handle_configuration_parameter(
                name, config_name, display_name, type_f
            )

        self.__write_updated_files()
        return errors

    def handle_opening_times_update(self):
        try:
            opening_times_folder = self.parameters.get_dataset_path("opening_times")
        except ValueError:
            self.display_message("No opening times found - skipping", "DEBUG")
            return
        reader = CSVReader(opening_times_folder)
        opening_times_by_production_resource = {
            row.get("id"): row.get("OpeningTimes")
            for file_content in reader.files.values()
            for row in file_content
        }

        for r in self.memory.files.get("ProductionResource", []):
            if (opening_times := opening_times_by_production_resource.get(r.get("id"))) is not None:
                r["OpeningTimes"] = opening_times
        self.__write_updated_files()

    def handle_demands(self):
        try:
            demands_path = self.parameters.get_dataset_path("demands")
        except ValueError:
            self.display_message("No demands found - skipping", "DEBUG")
            return 0
        reader = CSVReader(demands_path)
        counter = defaultdict(int)
        demands_by_stock = {}
        for file_content in reader.files.values():
            for row in file_content:
                stock = row.get("id")
                if stock is not None and stock != "":
                    demands_by_stock[stock] = get_value(row, "Stock", "Demands")
                    counter[stock] += 1

        errors = 0
        for stock, n in counter.items():
            if 1 < n:
                self.display_message(f"{n} demand definitions for {stock}", "ERROR")
                errors += 1

        updated = 0
        for s in self.memory.files.get("Stock", []):
            stock = s.get("id")
            if stock in demands_by_stock:
                s["Demands"] = demands_by_stock.pop(stock)
                updated += 1
        self.__write_updated_files()
        self.display_message(f"Demands updated on {updated} stock{'s' if 1 < updated else ''}.")

        if demands_by_stock:
            self.display_message(f"Stock{'s' if 1 < len(demands_by_stock) else ''} from demands not found in dataset: {', '.join(demands_by_stock)}.", "WARNING")

        return errors
