from typing import Union

from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
import pandas as pd
from Supplychain.Generic.timer import Timer
from Supplychain.Wrappers.environment_variables import EnvironmentVariables
from Supplychain.Run.simulation import run_simple_simulation
import comets as co

default_parameters = {
    "simulation_name": "Simulation",
    "simulator_path": "Simulation",
    "saving_results": False,
    "local": False,
    "amqp_consumer_adress": None,
    "adx_writer": None,
    "validation_folder": "Simulation/Output",
    "parameter": "Transportation Lead Time",
    "variation": 0.5,
    "change": "relative",
    "timeinterval": False,
    "initialtimestep": 0,
    "finaltimestep": 0,
    "output_dir": None,
}

# parameter label: (entity_type, attribute_name, default)
sensitive_parameters = {
    "Fixed Production Cost": (
        "Machine",
        "ProductionCostSchedule",
        "ProductionCost",
    ),
    "Production Resource Opening Time": (
        "Machine",
        "OpeningTimeSchedule",
        "OpeningTime",
    ),
    "Operating Performance": (
        "Operation",
        "OperatingPerformanceSchedule",
        "OperatingPerformance",
    ),
    "Cycle Time": (
        "Operation",
        "CycleTimeSchedule",
        "CycleTime",
    ),
    "Variable Production Cost": (
        "Operation",
        "ProductionUnitCostSchedule",
        "ProductionUnitCost",
    ),
    "Production CO2 Unit Emissions": (
        "Operation",
        "CO2UnitEmissionsSchedule",
        "CO2UnitEmissions",
    ),
    "Production Minimum Order Quantity": (
        "Operation",
        "MinimumOrderQuantitySchedule",
        "MinimumOrderQuantity",
    ),
    "Production Multiple Order Quantity": (
        "Operation",
        "MultipleOrderQuantitySchedule",
        "MultipleOrderQuantity",
    ),
    "Production Plan": (
        "Operation",
        "ProductionPlanSchedule",
        "ProductionPlan",
    ),
    "Initial Stock": (
        "Stock",
        "CurrentStock",
        None,
    ),
    "Purchasing Unit Cost": (
        "Stock",
        "PurchasingUnitCostSchedule",
        "PurchasingUnitCost",
    ),
    "Unit Income": (
        "Stock",
        "UnitIncomeSchedule",
        "UnitIncome",
    ),
    "Storage Unit Cost": (
        "Stock",
        "StorageUnitCostSchedule",
        "StorageUnitCost",
    ),
    "Order Point": (
        "Stock",
        "OrderPointSchedule",
        "OrderPoint",
    ),
    "Order Quantities": (
        "Stock",
        "OrderQuantitySchedule",
        "OrderQuantity",
    ),
    "Order Up To Levels": (
        "Stock",
        "OrderQuantitySchedule",
        "OrderQuantity",
    ),
    "Safety Quantities": (
        "Stock",
        "SafetyQuantitySchedule",
        "SafetyQuantity",
    ),
    "Transport Unit Cost": (
        "TransportOperation",
        "TransportUnitCostSchedule",
        "TransportUnitCost",
    ),
    "Duty Unit Cost": (
        "TransportOperation",
        "DutyUnitCostSchedule",
        "DutyUnitCost",
    ),
    "Transportation Lead Time": (
        "TransportOperation",
        "ActualDurationSchedule",
        "Duration",
    ),
    "Transport CO2 Unit Emission": (
        "TransportOperation",
        "CO2UnitEmissionsSchedule",
        "CO2UnitEmissions",
    ),
    "Transport Minimum Order Quantity": (
        "TransportOperation",
        "MinimumOrderQuantitySchedule",
        "MinimumOrderQuantity",
    ),
    "Transport Multiple Order Quantity": (
        "TransportOperation",
        "MultipleOrderQuantitySchedule",
        "MultipleOrderQuantity",
    ),
}

# For each parameter of the sensitivity analysis, to which entities it corresponds to
map_to_entities = {
    label: entity_type
    for label, (entity_type, _, _)
    in sensitive_parameters.items()
}

# For each parameter of the sensitivity analysis, to which attribute of the model it corresponds to
map_to_attribute_name = {
    label: attribute_name
    for label, (_, attribute_name, _)
    in sensitive_parameters.items()
}

# For each parameter of the sensitivity analysis, which attribute of the model
# should be used as default value to create a schedule if the provided schedule is empty
map_to_default_attribute_name = {
    label: default
    for label, (_, _, default)
    in sensitive_parameters.items()
}


def local_sensitivity_analysis(
    simulation_name: str = default_parameters["simulation_name"],
    amqp_consumer_adress: Union[str, None] = default_parameters["amqp_consumer_adress"],
    parameter: str = default_parameters["parameter"],  # type of variable on which the analysis is performed
    adx_writer: Union[ADXAndFileWriter, None] = default_parameters["adx_writer"],
    variation: float = default_parameters["variation"],  # variation value
    change: str = default_parameters["change"],  # change mode
    local: bool = default_parameters["local"],  # false to optionally send the results to adx ; true to return the results dataframe (useful for the test)
    simulator_path: str = default_parameters["simulator_path"],
    saving_results: bool = default_parameters["saving_results"],
    validation_folder: str = default_parameters["validation_folder"],  # Folder in which sensitivity analysis results are saved
    timeinterval: bool = default_parameters["timeinterval"],  # Whether the change happens during a specific interval (otherwise it is applied for the complete duration of the simulation)
    initialtimestep: int = default_parameters["initialtimestep"],  # Time step at which the modification starts to take place (included), only if timeinterval is true
    finaltimestep: int = default_parameters["finaltimestep"],  # Time step after which the modification ends (the modification still takes place at this time step), only if timeinterval is true
    output_dir: Union[str, None] = default_parameters["output_dir"],  # directory where to save the probe outputs as CSV if there is no AMQP
):

    with Timer("[Run Sensitivity]") as t:

        if parameter != "All":
            results = run_one_sa(
                simulation_name,
                amqp_consumer_adress,
                parameter,
                adx_writer,
                variation,
                change,
                local,
                simulator_path,
                saving_results,
                validation_folder,
                timeinterval,
                initialtimestep,
                finaltimestep,
            )
        else:
            # Run a sensitivity analysis for each possible parameter and append results to the same table

            result_dataframes = []
            for single_parameter in map_to_entities.keys():
                try:
                    t.display_message(
                        f"Running sensitivity analysis with parameter {single_parameter}"
                    )
                    results = run_one_sa(
                        simulation_name,
                        amqp_consumer_adress,
                        single_parameter,
                        adx_writer,
                        variation,
                        change,
                        local,
                        simulator_path,
                        saving_results,
                        validation_folder,
                        timeinterval,
                        initialtimestep,
                        finaltimestep,
                    )
                    result_dataframes.append(results)
                except Exception as e:
                    t.display_message(
                        f"Error running sensitivity analysis with parameter {single_parameter}, analysis skipped"
                    )
                    print(e)
            results = pd.concat(result_dataframes)

        if saving_results:
            results.to_csv(validation_folder + "/SensitivityAnalysis.csv")

        # useful for tests
        if local:
            return results

        else:
            adx_writer.write_target_file(
                results.to_dict("records"),
                "LocalSensitivityAnalysis",
                EnvironmentVariables.simulation_id,
            )

            t.split("Sent stats to ADX : {time_since_last_split}")
            t.display_message("Running simple simulation to fill ADX")

            run_simple_simulation(
                simulation_name=simulation_name,
                amqp_consumer_adress=amqp_consumer_adress,
                output_dir=output_dir,
            )


def run_one_sa(
    simulation_name: str = default_parameters["simulation_name"],
    amqp_consumer_adress: Union[str, None] = default_parameters["amqp_consumer_adress"],
    parameter: str = default_parameters["parameter"],  # type of variable on which the analysis is performed
    adx_writer: Union[ADXAndFileWriter, None] = default_parameters["adx_writer"],
    variation: float = default_parameters["variation"],  # variation value
    change: str = default_parameters["change"],  # change mode
    local: bool = default_parameters["local"],  # false to optionally send the results to adx ; true to return the results dataframe (useful for the test)
    simulator_path: str = default_parameters["simulator_path"],
    saving_results: bool = default_parameters["saving_results"],
    validation_folder: str = default_parameters["validation_folder"],  # Folder in which sensitivity analysis results are saved
    timeinterval: bool = default_parameters["timeinterval"],  # Whether the change happens during a specific interval (otherwise it is applied for the complete duration of the simulation)
    initialtimestep: int = default_parameters["initialtimestep"],  # Time step at which the modification starts to take place (included), only if timeinterval is true
    finaltimestep: int = default_parameters["finaltimestep"],  # Time step after which the modification ends (the modification still takes place at this time step), only if timeinterval is true
):

    with Timer("[Run one sensitivity analysis]") as t:
        attribute = map_to_attribute_name.get(parameter)

        list_of_datapaths, max_time_step, subdataset = get_simulator_data(
            simulator_path, map_to_entities.get(parameter), attribute
        )

        errors = validate_sa_parameters(
            parameter,
            change,
            variation,
            timeinterval,
            initialtimestep,
            finaltimestep,
            max_time_step,
        )
        if errors:
            t.display_message('\n'.join(errors))
            error_message = f"Invalid parameter{'s' if len(errors) > 1 else ''}"
            raise ValueError(error_message)

        list_of_variables = create_variables(
            simulator_path,
            list_of_datapaths,
            change,
            variation,
            timeinterval,
            initialtimestep,
            finaltimestep,
            max_time_step,
            parameter,
            attribute,
        )

        errors = validate_absolute_variations(list_of_variables)
        if errors:
            t.display_message('\n'.join(errors))
            error_message = f"Invalid parameter{'s' if len(errors) > 1 else ''}"
            raise ValueError(error_message)

        t.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Variables creation and validation")

        def encoder(parameters):
            """
            Encoder of the task on which the S.A will be performed. The encoder receives a parameter set where
            the attributes of type 'schedule' are separated (see function create_variables). The aim of this encoder is to
            re concatenate the schedules together. For example, if the encoder receives the following parameter set:
            {"transport_lyon": 2,
                "transport_paris__@__0": 1,
                "transport_paris__@__3": 2,
                "transport_paris__@__5": 4,}

            it will return :
            {'transport_lyon': 2,
                'transport_paris': {'0': 1, '3': 2, '5': 4}}
            Args:
                parameters : Parameter set with the value computed by the S.A algorithm where schedules are separated.
                Note that the keys of the parameter set are either a datatapth or a datapath + '__@__' + time_step.

            Returns:
                parameter_set : Parameter set with the value computed by the S.A algorithm where the schedules are re concatenated.
                Note that the keys of the parameter set are the datapath of the attributes.
            """
            parameter_set = {}
            for key, value in parameters.items():
                if "__@__" in key:  # check if it belongs to a group
                    if key.split("__@__")[0] not in parameter_set.keys():
                        parameter_set[key.split("__@__")[0]] = {
                            key.split("__@__")[-1]: value
                        }
                    else:
                        temp_dic = parameter_set[key.split("__@__")[0]].copy()
                        temp_dic[key.split("__@__")[-1]] = value
                        parameter_set[key.split("__@__")[0]] = temp_dic
                else:
                    parameter_set[key] = value
            return parameter_set

        used_probes = ["PerformanceIndicators"]

        class PerformanceConsumer:
            def __init__(self):
                self.data = {}

            def Consume(self, p_data):
                f = self.engine.PerformanceIndicatorsProbeOutput.Cast(p_data).GetFacts()
                for fact in f:
                    self.data = {
                        "OPEX": fact.GetOPEX().GetAsFloat(),
                        "Profit": fact.GetProfit().GetAsFloat(),
                        "Average stock value": fact.GetAverageStockValue().GetAsFloat(),
                        "CO2 emissions": fact.GetCO2Emissions().GetAsFloat(),
                        "Total served quantity": fact.GetTotalServedQuantity().GetAsFloat(),
                        "Fill rate service level": (
                            fact.GetTotalServedQuantity().GetAsFloat() / fact.GetTotalDemand().GetAsFloat() * 100
                            if fact.GetTotalDemand().GetAsFloat() != 0
                            else 0
                        ),
                    }

        simulator_interface = co.CosmoInterface(
            simulator_path=simulator_path,
            custom_sim_engine=CosmoEngine,
            simulation_name=simulation_name,
            used_consumers=[],
            used_probes=used_probes,
            custom_consumers=[
                (PerformanceConsumer, "PerformanceConsumer", "PerformanceIndicators")
            ],
        )

        def get_outcomes(simulator_interface):
            data = simulator_interface.PerformanceConsumer.data
            return data

        simulationtask = co.ModelTask(
            modelinterface=simulator_interface,
            get_outcomes=get_outcomes,
            encode=encoder,
        )

        experiment = co.LocalSensitivityAnalysis(
            task=simulationtask, variables=list_of_variables, n_jobs=-2
        )

        t.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Experiment initialization")

        experiment.run()

        t.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Simulations")

        results = reformat_results(
            experiment.results,
            change,
            variation,
            parameter,
            timeinterval,
            initialtimestep,
            finaltimestep,
            subdataset,
        )

        t.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Results reformatting")

    return results


def validate_sa_parameters(
    sensitive_parameter: str,
    change: str,
    variation: float,
    timeinterval: bool,
    initialtimestep: int,
    finaltimestep: int,
    max_time_step: int,
):
    errors = []

    for label, parameter, parameter_type in [
        ("sensitive parameter", sensitive_parameter, str),
        ("change", change, str),
        ("variation", variation, float),
        ("time interval", timeinterval, bool),
        ("initial time step", initialtimestep, int),
        ("final time step", finaltimestep, int),
    ]:
        if not isinstance(parameter, parameter_type):
            errors.append(
                f"Invalid {label} value: {parameter} is not {parameter_type.__name__}."
            )

    known_parameter = True
    if sensitive_parameter not in sensitive_parameters:
        known_parameter = False
        errors.append(
            f"Unkown sensitive parameter: {sensitive_parameter}. Parameter should be in {sensitive_parameters.keys()}."
        )

    changes = set(("relative", "absolute", "replacement"))
    if change not in changes:
        errors.append(
            f"Unknown change: {change}, it should be in {changes}."
        )
    elif change == "relative" and variation < -1:
        errors.append(
            f"Invalid variation value: {variation}. With relative change, it should be greater than or equal to -1."
        )
    elif change == "replacement" and variation < 0:
        errors.append(
            f"Invalid variation value: {variation}. With replacement change, it should be non negative."
        )

    if timeinterval:
        if known_parameter and map_to_default_attribute_name[sensitive_parameter] is None:
            errors.append(
                f"Unsupported sensitivity analysis: as {sensitive_parameter} cannot be scheduled, time interval should not be activated."
            )
        if (
            initialtimestep > finaltimestep
            or initialtimestep < 0
            or initialtimestep > max_time_step
            or finaltimestep < 0
            or finaltimestep > max_time_step
        ):
            errors.append(
                f"Time steps {initialtimestep} and {finaltimestep} should be integers between 0 and {max_time_step}"
            )

    return errors


def validate_absolute_variations(variables):
    errors = []

    for variable in variables:
        if variable["change"] == "absolute" and variable["variation"] < -variable["reference"]:
            entity_name = variable["name"].split('::{Entity}')[-1].split('::@')[0]
            time_step_message = ""
            if "__@__" in variable["name"]:
                time_step = variable["name"].split("__@__")[-1]
                time_step_message = f" at time step {time_step}"
            errors.append(
                f"Invalid variation value: {variable['variation']}."
                f" With absolute change, it should be greater than or equal to {-variable['reference']}"
                f" for entity {entity_name}{time_step_message}."
            )

    return errors


def get_simulator_data(simulator_path, entity_type, attribute):
    """
    Function to automatically retrieve the list of datapath on which the S.A will be performed, based on the entity type
    specified by the user.

    Args:
        simulator_path : path to the simulator
        entity_type : type of the entities on which the S.A will be performed
    Returns:
        (list, integer, string): list of datapaths on which the S.A will be used, number of time steps of the simulation and subdataset name
    """
    sim2 = co.CosmoInterface(simulator_path, custom_sim_engine=CosmoEngine)
    sim2.initialize()

    list_of_datapaths = (
        get_list_of_datapaths(sim2, entity_type, attribute)
        if entity_type and attribute
        else None
    )

    max_time_step = get_max_time_step(sim2)

    subdataset = sim2.get_outputs(["Model::@SubDataset"])["Model::@SubDataset"]

    sim2.terminate()

    return list_of_datapaths, max_time_step, subdataset


def get_list_of_datapaths(cosmo_interface, entity_type, attribute):
    entities = cosmo_interface.sim.GetModel().FindEntitiesByType(entity_type)
    if entity_type == "Stock" and attribute != "PurchasingUnitCostSchedule":
        entities = [
            stock
            for stock in entities
            if not stock.GetAttribute("IsInfinite").Get()
        ]
    suffixes = sorted(
        f"{{Entity}}{entity.GetName()}::@{attribute}"
        for entity in entities
    )

    if not suffixes:
        raise ValueError(
            f"No entity of type {entity_type} is present in the instance, the sensitivity analysis on {attribute} is not supported."
        )

    datapaths = cosmo_interface.get_datapaths()

    return [
        next(filter(
            lambda datapath: datapath.endswith(suffix),
            datapaths,
        ))
        for suffix in suffixes
    ]


def get_max_time_step(cosmo_interface):
    p = "Model::@TimeStepPerCycle"
    time_step_per_cycle = cosmo_interface.get_outputs([p])[p]
    p = "Model::@NumberOfCycle"
    number_of_cycle = cosmo_interface.get_outputs([p])[p]
    return time_step_per_cycle * number_of_cycle


def create_variables(
    simulator_path,
    datapaths,
    change,
    variation,
    timeinterval,
    initialtimestep,
    finaltimestep,
    max_time_step,
    parameter,
    attribute,
):
    """
    Function to create the list of variables to perform the S.A based on a list of datapaths.
    Each datapath corresponds to an attribute in the model. If the attribute is of type "schedule":
    i.e {'time_step_0': value on time step 0, [...], 'time_step_k': value on time step k}
    the function will create more than one variable per datapath. More precisely n variables all belonging to
    the same group will be created, where n corresponds to the number of items in the dic. For example,
    the following attribute : {'0': 3, '2': 4, '7':2} will lead to the creation of the following variables:
    {"name": datapath__@__0,
     "type": int),
     "reference": 3,
     "variation": variation,
     "change": change,
     "group": datapath,
                }
    {"name": datapath__@__2,
     "type": int),
     "reference": 4,
     "variation": variation,
     "change": change,
     "group": datapath,
                }
    {"name": datapath__@__7,
     "type": int),
     "reference": 2,
     "variation": variation,
     "change": change,
     "group": datapath,
                }
    In the case of timeinterval==true, a variable will also be created for time steps initialtimestep and finaltimestep+1,
    even if they were not already present in the schedule, in order to start the change of value, and to remove it.

    Args:
        simulator_path : path to the simulator
        datapaths : list containing the datapaths that need to be mapped to a variable
        change : change mode of the S.A
        variation : variation of the variable for the S.A

    Returns
        list_of_variables : list of dic where each dic is a variable according to the
        definition of a variable in CoMETs' sensitivity analysis

    """
    sim = CosmoEngine.LoadSimulator(simulator_path)
    list_of_variables = []
    for elements in datapaths:
        reference = sim.FindAttribute(elements).Get()

        if not timeinterval:
            if isinstance(reference, dict):

                if reference == {}:
                    if map_to_default_attribute_name[parameter] is not None:
                        newelement = elements.replace(
                            map_to_attribute_name[parameter],
                            map_to_default_attribute_name[parameter],
                        )
                        new_reference = sim.FindAttribute(newelement).Get()
                        reference = {0: new_reference}
                    else:
                        raise ValueError(
                            f"Schedule for attribute {elements} is empty and no default value is available, sensitivity analysis requires a reference value to be provided."
                        )

                for key in reference:
                    variable = {
                        "name": str(elements + "__@__" + str(key)),
                        "type": get_type(reference[key]),
                        "reference": reference[key],
                        "variation": variation,
                        "change": change,
                        "group": elements,
                    }
                    list_of_variables.append(variable)

            else:
                variable = {
                    "name": elements,
                    "type": get_type(reference),
                    "reference": reference,
                    "variation": variation,
                    "change": change,
                }
                list_of_variables.append(variable)
        else:

            if not isinstance(reference, dict):
                raise ValueError(
                    f"No schedule is provided for attribute {elements}, sensitivity analysis with timeinterval is not supported."
                )

            if reference == {}:
                if map_to_default_attribute_name[parameter] is not None:
                    newelement = elements.replace(
                        map_to_attribute_name[parameter],
                        map_to_default_attribute_name[parameter],
                    )
                    new_reference = sim.FindAttribute(newelement).Get()
                    reference = {0: new_reference}
                else:
                    raise ValueError(
                        f"Schedule for attribute {elements} is empty and no default value is available, sensitivity analysis requires a reference value to be provided."
                    )

            previousvalue = 0  # keep track of last defined value in the schedule
            for timestep in range(max_time_step):
                if timestep < initialtimestep or (timestep > finaltimestep + 1):
                    # outside the interval, no variation should be applied
                    if timestep in reference.keys():
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(reference[timestep]),
                            "reference": reference[timestep],
                            "variation": 0,
                            "change": "absolute",
                            "group": elements,
                        }
                        list_of_variables.append(variable)
                        previousvalue = reference[timestep]
                elif timestep == initialtimestep:
                    # start the change of value at initialtimestep,
                    # if initialtimestep is not in the schedule, use the last defined value previousvalue as reference
                    if timestep in reference.keys():
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(reference[timestep]),
                            "reference": reference[timestep],
                            "variation": variation,
                            "change": change,
                            "group": elements,
                        }
                        list_of_variables.append(variable)
                        previousvalue = reference[timestep]
                    else:
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(previousvalue),
                            "reference": previousvalue,
                            "variation": variation,
                            "change": change,
                            "group": elements,
                        }
                        list_of_variables.append(variable)
                elif timestep > initialtimestep and timestep <= finaltimestep:
                    # inside the interval, the variation should be applied
                    if timestep in reference.keys():
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(reference[timestep]),
                            "reference": reference[timestep],
                            "variation": variation,
                            "change": change,
                            "group": elements,
                        }
                        list_of_variables.append(variable)
                        previousvalue = reference[timestep]
                elif timestep == finaltimestep + 1:
                    # end the change of value at finaltimestep+1,
                    # if finaltimestep is not in the schedule, use the last defined value previousvalue as reference
                    if timestep in reference.keys():
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(reference[timestep]),
                            "reference": reference[timestep],
                            "variation": 0,
                            "change": "absolute",
                            "group": elements,
                        }
                        list_of_variables.append(variable)
                        previousvalue = reference[timestep]
                    else:
                        variable = {
                            "name": str(elements + "__@__" + str(timestep)),
                            "type": get_type(previousvalue),
                            "reference": previousvalue,
                            "variation": 0,
                            "change": "absolute",
                            "group": elements,
                        }
                        list_of_variables.append(variable)
    return list_of_variables


def get_type(value):
    """
    Function to return the value's type. Instead of returning "<class 'int'>" the function returns 'int'.
    Similarly, for float, instead of <class 'float'>" the function returns 'float'
    """
    return type(value).__name__


def reformat_results(
    row_results,
    change,
    variation,
    parameter,
    timeinterval,
    initialtimestep,
    finaltimestep,
    subdataset,
):
    """
    Function to reformat the S.A results to be compatible with the adx table.

    """
    df = row_results.reset_index()

    if (
        "Group" not in df.columns
    ):  # if there is no 'Group' column, creates one where the name of the groups correspond to the ID.
        df.insert(1, "Group", df["Name"])

    df["Name"] = df["Name"].apply(
        lambda name: (
            name.split("{Entity}")[-1].split("::@", 1)[0]
            + (f"__@__{name.rsplit('__@__', 1)[1]}" if "__@__" in name else "__@__0")
        )
    )
    df[["Name", "TimeStep"]] = df["Name"].str.split("__@__", n=1, expand=True)
    df["TimeStep"] = df["TimeStep"].astype(int)

    # Filter lines for time steps where no modification has been done
    if timeinterval:
        df = df[(df["TimeStep"] >= initialtimestep) & (df["TimeStep"] <= finaltimestep)]

    df["SimulationRun"] = EnvironmentVariables.simulation_id
    df["Variable"] = str(parameter)
    df["Variation"] = float(variation)
    df["Change"] = str(change)
    df["TimeInterval"] = bool(timeinterval)
    df["InitialTimeStep"] = int(initialtimestep)
    df["FinalTimeStep"] = int(finaltimestep)
    df["SubDataset"] = subdataset

    df = df.rename(
        columns={
            "Output": "KPI",
            "Name": "id",
            "ReferenceOutputValue": "ReferenceKPI",
            "NewOutputValue": "NewKPI",
            "Difference": "Gap",
        }
    )
    # if type(df["ReferenceInputValue"][0]) == dict:
    #     for i in range(len(df.index)):
    #         df["ReferenceInputValue"][i] = df["ReferenceInputValue"][i][0]
    #         df["NewInputValue"][i] = df["NewInputValue"][i][0]

    return df
