from copy import deepcopy
import comets as co
from Supplychain.Schema.modifications import changes
from Supplychain.Schema.numeric_attributes import numeric_attributes
from Supplychain.Schema.statistics import statistics, statistic_aliases
from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Wrappers.environment_variables import EnvironmentVariables

"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
Helper functions used in the uncertainty analysis
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""


def apply_uncertainty(value, error, mode):
    return changes[mode](value, error)


def fit_to_attribute(value, attribute_properties):
    if attribute_properties.minimum is not None:
        value = max(attribute_properties.minimum, value)
    if attribute_properties.maximum is not None:
        value = min(value, attribute_properties.maximum)
    if attribute_properties.value_type is int:
        value = round(value)
    return value


def calculate_new_value(value, error, mode, attribute_properties):
    return fit_to_attribute(
        apply_uncertainty(value, error, mode),
        attribute_properties,
    )


def encoder(
    parameters,
    demands,
    uncertainty_specs,
    variable_dse_collection,
):
    """
    Encode the input parameters for the simulator. This is done by transforming the
    sampled values of the uncertainty parameters into real datapaths to be set in the model.

    This transforms a parameterset in "UncertaintySpecs" space to a parameterset in simulator space.
    """

    sorted_parameters = {}
    for spec_id, random_value_list in parameters.items():
        if spec_id == 'AvoidNoSamplingCometsCrash':
            continue
        uncertainty_spec = uncertainty_specs.find_by_id(spec_id)
        variable_dse = variable_dse_collection[
            uncertainty_spec.entity,
            uncertainty_spec.attribute,
        ]
        sorted_parameters.setdefault(
            variable_dse.dataset_element.cosml_datapath,
            (
                uncertainty_spec.entity,
                uncertainty_spec.attribute,
                variable_dse.dataset_element.raw_attribute_value,
                {},
            ),
        )[-1][uncertainty_spec.timestep] = (
            uncertainty_spec.uncertainty_mode,
            random_value_list,
        )

    encoded_parameterset = {}
    for datapath, (entity, attribute, raw_values, random_values) in sorted_parameters.items():
        attribute_properties = numeric_attributes[attribute]
        if attribute_properties.attribute_type == 'fixed':
            mode, random_value = next(v for v in random_values.values())
            encoded_parameterset[datapath] = calculate_new_value(
                raw_values, random_value, mode, attribute_properties
            )
            continue
        if attribute_properties.attribute_type in ('change', 'quantity'):
            T = max(random_values)
            if T < 0:
                T = len(random_values[T][-1])
            else:
                T += 2
            last_value = 0
            for t in range(T):
                timestep = str(t)
                if timestep in raw_values:
                    last_value = raw_values[timestep]
                else:
                    raw_values[timestep] = last_value
        if t := next((t for t in random_values if t < 0), 0):
            mode, random_value_list = random_values[t]
            if attribute_properties.attribute_type == 'quantity':
                encoded_parameterset[datapath] = {
                    timestep: {
                        quantity: calculate_new_value(
                            raw_value, random_value, mode, attribute_properties
                        )
                        for quantity, raw_value
                        in raw_values.get(timestep, {'0': 0.0}).items()
                    }
                    for timestep, random_value
                    in ((str(t), v) for t, v in enumerate(random_value_list))
                }
            else:
                encoded_parameterset[datapath] = {
                    timestep: calculate_new_value(
                        raw_values.get(timestep, 0.0), random_value, mode, attribute_properties
                    )
                    for timestep, random_value
                    in ((str(t), v) for t, v in enumerate(random_value_list))
                }
        else:
            timesteps = sorted(set(raw_values) | set(str(t) for t in random_values if t >= 0))
            encoded_parameterset[datapath] = {}
            for timestep in timesteps:
                value = raw_values.get(timestep, 0.0)
                t = int(timestep)
                if t in random_values:
                    mode, random_value = random_values[t]
                    if attribute_properties.attribute_type == 'quantity':
                        value = {
                            quantity: calculate_new_value(
                                raw_value, random_value, mode, attribute_properties
                            )
                            for quantity, raw_value
                            in value.items()
                        }
                    else:
                        value = calculate_new_value(value, random_value, mode, attribute_properties)
                encoded_parameterset[datapath][timestep] = value
        if attribute == 'Demands':
            encoded_parameterset[datapath] = {
                timestep: new_value
                for timestep, new_value in encoded_parameterset[datapath].items()
                if new_value > 0.0
            }
            for timestep, new_value in encoded_parameterset[datapath].items():
                if demand := demands.get(entity, {}).get(int(timestep)):
                    encoded_parameterset[datapath][timestep] = {
                        k: v
                        for k, v in demand.items()
                    }
                    encoded_parameterset[datapath][timestep]['ExternalDemand'] = new_value
                else:
                    encoded_parameterset[datapath][timestep] = {
                        'ExternalDemand': new_value,
                        'InternalDemand': 0.0,
                        'BacklogWeight': 1.0,
                        'ExternalWeight': 1.0,
                        'InternalWeight': 0.0,
                        'WeightMax': 0.0,
                        'MaxVal': 0.0,
                    }
        if attribute_properties.attribute_type in ('change', 'quantity'):
            last_value = None
            for timestep in sorted(encoded_parameterset[datapath], key=int):
                if encoded_parameterset[datapath][timestep] == last_value:
                    del encoded_parameterset[datapath][timestep]
                else:
                    last_value = encoded_parameterset[datapath][timestep]

    return encoded_parameterset


"""
-------------------------------------------------
Simple helper functions
-------------------------------------------------
"""


def extend_simple_dic(my_dic, number_of_iterations):
    """Function to extend dictionaries of schedulable attributes.

    Args:
        my_dic (dict): dictionary of scheduled values such as {0: 3, 6: 4, 7: 3, 8: 2, 9: 8, 10: 40}
        number_of_iterations (int): total number of time steps of the schedule

    Returns:
        dict: extended dictionary for all time steps {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 4, 7: 3, 8: 2, 9: 8, 10: 40}
    """
    if my_dic != {}:  # checking that the dic isn't empty
        extended_dic = {
            0: my_dic[0]
        }  # We assume that the uncertainty starts at the first time step
        for i in range(1, number_of_iterations):
            if i in my_dic:
                extended_dic[i] = deepcopy(my_dic[i])
            else:
                extended_dic[i] = deepcopy(extended_dic[i - 1])
    else:
        extended_dic = {}
    return extended_dic


def extend_dic(my_dic, number_of_iterations):
    """Function to extend dictionaries of schedulable attributes.

    Args:
        my_dic (dict): dictionary of dictionary of scheduled values
        number_of_iterations (int): total number of time steps of the schedule

    Returns:
        dict: dictionary containing extended dictionary for all time steps
    """
    extended_dic = {}
    for entity in my_dic.keys():
        extended_dic[entity] = extend_simple_dic(my_dic[entity], number_of_iterations)
    return extended_dic


def add_tag(tag, name):
    return tag + name


def add_tag_to_parameterset(tag, parameterset):
    """Add string tag in front of the keys of a parameterset"""
    return {add_tag(tag, key): value for key, value in parameterset.items()}


"""
-------------------------------------------------
Functions that collect simulator attributes before the analysis
-------------------------------------------------
"""


def get_transports(cosmo_interface):
    """Function to get the list of all the transports in the simulation"""
    transports_list = []
    transports = cosmo_interface.sim.get_entities_names_by_type(
        entity_type="TransportOperation"
    )
    for keys in transports:
        transports_list.append(keys)
    return transports_list


def get_stocks(cosmo_interface):
    """Function to get the list of all the stocks that have uncertain demand"""
    uncertain_stocks = []
    for stock in cosmo_interface.sim.get_entities_by_type("Stock"):
        demands = CosmoEngine.DataTypeMapInterface.Cast(stock.GetAttribute("Demand"))
        stock_name = stock.GetName()
        for time_step in demands.GetKeys():
            demand = demands.GetAt(time_step)
            if demand.GetAttribute("DemandRelativeUncertainty").Get() > 0:
                uncertain_stocks.append(stock_name)
                break
    return uncertain_stocks


def get_stocks_with_demands(cosmo_interface):
    """Function to get the list of all the stocks that have demand"""
    stocks = []
    for stock in cosmo_interface.sim.get_entities_by_type("Stock"):
        demands = CosmoEngine.DataTypeMapInterface.Cast(stock.GetAttribute("Demand")).Get()
        if any(demand["ExternalDemand"] > 0 for demand in demands.values()):
            stocks.append(stock.GetName())
    return stocks


def get_attribute(cosmo_interface, attribute):
    """Get value of attribute in the model"""
    return cosmo_interface.get_outputs([attribute])[attribute]


def get_max_time_step(cosmo_interface):
    time_step_per_cycle = get_attribute(cosmo_interface, "Model::@TimeStepPerCycle")
    number_of_cycle = get_attribute(cosmo_interface, "Model::@NumberOfCycle")
    max_time_step = time_step_per_cycle * number_of_cycle
    return max_time_step


"""
-------------------------------------------------
Functions that collect simulator outputs
-------------------------------------------------
"""


def collect_simulated_transport_output(transports_names, modelinterface, max_time_step):
    """
    Function that returns a parameterset with the transport duration for each transport at the end of the simulation
    The transport duration is separated for each time step. The output parameterset (for a simulation
    with 1 TransportOperation: U) will have the following format:
    {Model[...]U::@ActualDurationSchedule__&@&__0': 10,
           [...],
      Model[...]U::@ActualDurationSchedule__&@&__10': 7}
    """
    transportation_lead_time = {}
    transportation_lead_time_transformed = {}
    for transport in transports_names:
        if (
            modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]
            == {}
        ):
            duration = modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"
                ]
            )[f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"]
            # Use a dict format so that the function "extend_dict" can be applied
            actual_duration_schedule = {0: duration}
        else:
            actual_duration_schedule = modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]
        transportation_lead_time[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
        ] = extend_simple_dic(
            actual_duration_schedule,
            max_time_step,
        )
        time_step = 0
        for value in transportation_lead_time[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
        ].values():
            transportation_lead_time_transformed[f"{transport}__&@&__ActualDuration__&@&__{time_step}"] = value
            time_step += 1
    return transportation_lead_time_transformed


def collect_simulated_stock_output(consumer_memory):
    """
    This function transforms the consumer memory from a list of list to a dict of
    ParameterSet. Note that each sublist in the initial format is transformed into
    len(sublist) - 2 ParameterSets.
    """
    measures = (
      "Demand",
      "RemainingQuantity",
      "ServedQuantity",
      "UnservedQuantity",
      "TotalFillRateServiceLevel",
      "Value",
      "OnTimeFillRateServiceLevel",
    )
    parametersets = {}
    for fact in consumer_memory:
        stock = fact[0]
        time_step = fact[1]
        for i, measure in enumerate(measures, 2):
            parametersets[f"{stock}__&@&__{measure}__&@&__{time_step}"] = fact[i]
    return parametersets


def collect_simulated_stock_final_output(consumer_memory):
    """
    This function transforms the consumer memory from a list of dict to a dict of
    ParameterSet, where one ParameterSet is used for each stock-measure.
    """
    return {
        f"{fact['id']}__&@&__{measure}": fact[measure]
        for fact in consumer_memory
        for measure in fact
        if measure != 'id'
    }


"""
-------------------------------------------------
Functions that create the uncertainty analysis "sampling"
-------------------------------------------------
"""


def create_demand_generator(extended_demands, number_of_time_steps, DemandCorrelations):
    """Function to create the uncertainty analysis sampling for the demands according to CoMETS format.
    Defines a generator of uncertain time series for each stock.

    Args:
        extended_demands (dict): Demand attributes obtained from the simulator
        number_of_time_steps (int): _description_
        DemandCorrelations (float): amount of correlation between consecutive time steps

    Returns:
        list: list of sampling variables according to CoMETS format
    """
    sampling = []
    for stock, demand_attribute in extended_demands.items():
        mean_demand = []
        uncertainties = []
        for t in range(number_of_time_steps):

            demand = demand_attribute[t]["ExternalDemand"]
            mean_demand.append(demand)
            uncertainties.append(
                demand * demand_attribute[t]["DemandRelativeUncertainty"]
            )  # Uncertainty proportional to demand, DemandRelativeUncertainty*Demand is the standard deviation
        sampling.append(
            {
                "name": f"{stock}",
                "sampling": co.TimeSeriesSampler(
                    correlation=DemandCorrelations,
                    dimension=number_of_time_steps,
                    forecast=mean_demand,
                    uncertainties=uncertainties,
                    minimum=0,
                ),
            }
        )
    return sampling


"""
-------------------------------------------------
Functions that reformat the outputs of the uncertainty analysis
-------------------------------------------------
"""


def transform_data(data, timestep=True):
    """
    Transform output data so that it matches the ADX table format
    """
    df = data.copy()
    index_cols = [
        "id",
        "Category",
        "TimeStep"
    ]
    if not timestep:
        index_cols.remove("TimeStep")
    if not df.empty:
        df.loc[:, "SimulationRun"] = EnvironmentVariables.simulation_id
        df[index_cols] = df["index"].str.split(pat="__&@&__", expand=True)
    else:
        index_cols.insert(0, "SimulationRun")
        df[index_cols] = None
    cols = [
        "SimulationRun",
        "TimeStep",
        "id",
        "Category",
    ]
    cols.extend(statistic_aliases)
    if not timestep:
        cols.remove("TimeStep")
    df = df[cols]
    df.rename(columns=statistic_aliases, inplace=True)
    return df


def transform_performances_data(data):
    """
    Transform output data so that it matches the ADX table format
    """
    df = data.copy()
    df.loc[:, "SimulationRun"] = EnvironmentVariables.simulation_id
    cols = [
        "SimulationRun",
        "index",
    ]
    cols.extend(statistics)
    df = df[cols]
    df = df.rename(columns={"index": "KPI"})
    return df
