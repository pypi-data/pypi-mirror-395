from Supplychain.Schema.default_values import variables_default_values
from comets import CosmoInterface

from dataclasses import dataclass

# Mapping of attribute names in the data model to attribute names in the CoSML model.
# This is used to determine the data path in the CoSML model for the decision variable
# group members.
mapping_attribute_data_model_to_cosml_model = {
    # Stock:
    # "BacklogWeight": ?? # this is a sub-attribute of "Backlog", not sure how to handle this so leaving out
    "ReviewPeriod": "ReviewPeriod",
    "FirstReview": "NextReview",
    "Advance": "Advance",
    "InitialStock": "CurrentStock",
    # StockSchedules
    "OrderPoints": "OrderPointSchedule",
    "OrderQuantities": "OrderQuantitySchedule",
    "OrderUpToLevels": "OrderQuantitySchedule",
    "SafetyQuantities": "SafetyQuantitySchedule",
    "StorageUnitCosts": "StorageUnitCostSchedule",
    "PurchasingUnitCosts": "PurchasingUnitCostSchedule",
    "VariablePurchasingUnitCosts": "VariablePurchasingUnitCostSchedule",
    "UnitIncomes": "UnitIncomeSchedule",
    "RetainProportions": "RetainProportionSchedule",
    # Demands
    "Demands": "Demand",
    # ProductionResourceSchedules
    "OpeningTimes": "OpeningTimeSchedule",
    "FixedProductionCosts": "ProductionCostSchedule",
    # ProductionOperation:
    "InvestmentCost": "InvestmentCost",
    "Duration": "Duration",
    # Transport
    "TransportationLeadTime": "Duration",
    # ProductionOperation and Transport:
    "Priority": "Priority",
    # ProductionOperationSchedules
    "QuantitiesToProduce": "ProductionPlanSchedule",
    "OperatingPerformances": "OperatingPerformanceSchedule",
    "CycleTimes": "CycleTimeSchedule",
    "RejectRates": "RejectRateSchedule",
    "ProductionUnitCosts": "ProductionUnitCostSchedule",
    "ProductionProportions": "ProductionProportionSchedule",
    # TransportSchedules:
    "ActualTransportationLeadTimes": "ActualDurationSchedule",
    "DutyUnitCosts": "DutyUnitCostSchedule",
    "TransportUnitCosts": "TransportUnitCostSchedule",
    # ProductionOperationSchedules and TransportSchedules
    "MinimumOrderQuantities": "MinimumOrderQuantitySchedule",
    "MultipleOrderQuantities": "MultipleOrderQuantitySchedule",
    "SourcingProportions": "SourcingProportionSchedule",
    "DispatchProportions": "DispatchProportionSchedule",
    # ProductionOperationSchedules, StockSchedules, TransportSchedules
    "CO2UnitEmissions": "CO2UnitEmissionsSchedule",
}

# Mapping to determine what entities have a certain attribute. Used for the
# generation of decision variables based on the Configuration file, where only
# the attribute name is given. This mapping is structured as follows:
# - key: attribute name in the data model
# - value: list of entity types that have this attribute
mapping_attribute_data_model_to_entity_types = {
    "ReviewPeriod": ["Stock"],
    "FirstReview": ["Stock"],
    "Advance": ["Stock"],
    "OrderPoints": ["Stock"],
    "OrderQuantities": ["Stock"],
    "OrderUpToLevels": ["Stock"],
    "SafetyQuantities": ["Stock"],
    "InitialStock": ["Stock"],
    "StorageUnitCosts": ["Stock"],
    "PurchasingUnitCosts": ["Stock"],
    "UnitIncomes": ["Stock"],
    "RetainProportions": ["Stock"],
    "OpeningTimes": ["ProductionResource"],
    "FixedProductionCosts": ["ProductionResource"],
    "ProductionProportions": ["ProductionOperation"],
    "QuantitiesToProduce": ["ProductionOperation"],
    "OperatingPerformances": ["ProductionOperation"],
    "CycleTimes": ["ProductionOperation"],
    "RejectRates": ["ProductionOperation"],
    "ProductionUnitCosts": ["ProductionOperation"],
    "InvestmentCost": ["ProductionOperation"],
    "DutyUnitCosts": ["Transport"],
    "TransportUnitCosts": ["Transport"],
    "MinimumOrderQuantities": ["ProductionOperation", "Transport"],
    "MultipleOrderQuantities": ["ProductionOperation", "Transport"],
    "SourcingProportions": ["ProductionOperation", "Transport"],
    "DispatchProportions": ["StockToOperation"],
    "Priority": ["ProductionOperation", "Transport"],
    "Duration": ["ProductionOperation"],
    "TransportationLeadTime": ["Transport"],
    "ActualTransportationLeadTimes": ["Transport"],
    "CO2UnitEmissions": ["ProductionOperation", "Stock", "Transport"],
}

mapping_entity_type_data_model_to_cosml_model = {
    "ProductionResource": "Machine",
    "ProductionOperation": "Operation",
    "Transport": "TransportOperation",
}

# Mapping of attribute names in the data model to attribute types in the model.
# This is used to determine the type of the decision variable (float or int).
mapping_attribute_type_data_model = {
    "ReviewPeriod": "int",
    "FirstReview": "int",
    "Advance": "int",
    "OpeningTimes": "float",
    "OrderPoints": "float",
    "OrderQuantities": "float",
    "OrderUpToLevels": "float",
    "SafetyQuantities": "float",
    "InitialStock": "float",
    "StorageUnitCosts": "float",
    "PurchasingUnitCosts": "float",
    "UnitIncomes": "float",
    "RetainProportions": "float",
    "FixedProductionCosts": "float",
    "ProductionProportions": "float",
    "QuantitiesToProduce": "float",
    "OperatingPerformances": "float",
    "CycleTimes": "float",
    "RejectRates": "float",
    "ProductionUnitCosts": "float",
    "InvestmentCost": "float",
    "DutyUnitCosts": "float",
    "TransportUnitCosts": "float",
    "MinimumOrderQuantities": "float",
    "MultipleOrderQuantities": "float",
    "SourcingProportions": "float",
    "DispatchProportions": "float",
    "Priority": "int",
    "Duration": "int",
    "TransportationLeadTime": "int",
    "ActualTransportationLeadTimes": "int",
    "CO2UnitEmissions": "float",
}


@dataclass
class DatasetElement:
    """
    Class describing an element of the dataset that can be modified in an
    experiment. In first instance, this will be an attribute of a particular
    entity, but this can be extended to other (non-entity) elements as well.

    The class contains the following attributes:
    - entity_id: id of the entity
    - attribute_name: name of the attribute
    - raw_attribute_value: raw attribute value from the dataset. This may
        be a dict if the attribute is time-variable.
    - attribute_number_value: value of the attribute as given in the dataset.
        This is always a number, even if the attribute is time-variable. If
        the attribute is time-variable, this is the value for key "0". If there
        is no key "0", the default value is used.
    - attribute_is_time_variable: boolean indicating whether the attribute is
        variable in time. This is determined by the type of the
        raw_attribute_value.
    """

    entity_id: str
    attribute_name: str
    # below attributes are not settable at initialization but taken from the dataset
    raw_attribute_value: float|int|dict[str,float|int]|None = None
    attribute_number_value: float|int|None = None
    attribute_is_time_variable: bool|None = None
    # below attributes are not settable at initialization but taken from the CoSML model
    # Requires an initialized CosmoInterface.
    cosml_datapath: str|None = None

    def retrieve_attribute_properties_from_entity(self, entity: dict) -> None:
        """
        Retrieve information about the attribute from the entity itself:
        - the raw attribute value (numeric or dict)
        - the attribute number value (numeric only, derived from the
          raw attribute value)
        - whether the attribute is time-variable
        """

        # retrieve the raw attribute value from the entity
        try:
            raw_attribute_value = entity[self.attribute_name]
        except KeyError:
            raise KeyError(
                f"Attribute '{self.attribute_name}' not found in entity {self.entity_id}."
            )

        attribute_number_value = _retrieve_attribute_number_value_or_default(
            raw_attribute=raw_attribute_value,
            entity_type=entity['sheet_name'],
            attribute_name=self.attribute_name
        )

        # set the values in the object
        self.raw_attribute_value = raw_attribute_value
        self.attribute_number_value = attribute_number_value
        self.attribute_is_time_variable = isinstance(raw_attribute_value, dict)

    def retrieve_datapath_from_cosmo_interface(self, cosmo_interface: CosmoInterface) -> None:
        """
        Retrieve the data path in the CoSML model for the group member. This is done
        by obtaining the entity abridged data path, and transforming this manually to the
        full attribute data path.

        Args:
            cosmo_interface (CosmoInterface): CoMETS interface to the CoSML model
        """

        # transform the attribute to the cosml format. This is necessary in particular
        # for the "Schedules". If the attribute is not found in the mapping, the attribute
        # name inside the cosml model is assumed to be the same as in the data model.
        attribute_cosml = mapping_attribute_data_model_to_cosml_model.get(self.attribute_name, self.attribute_name)

        if cosmo_interface is None:
            self.cosml_datapath = f'Model::{{Entity}}IndustrialNetwork::{{Entity}}{self.entity_id}::@{attribute_cosml}'
            return

        # build the entity datapath from its abridged UntypedDataPath
        # Not sure this is fail proof, but it's done like this in CoMETS so I guess it works. Famous last words.
        datapath = str(cosmo_interface.sim.GetModel().GetEntityByName(self.entity_id).BuildUntypedDataPath(True))
        datapath = datapath.replace("::", "::{Entity}")
        datapath += f"::@{attribute_cosml}"

        # store the data path in the object
        self.cosml_datapath = datapath

def _retrieve_attribute_number_value_or_default(
    raw_attribute: dict|float|int,
    entity_type: str,
    attribute_name: str
) -> float|int:
    """
    Transform the raw attribute value (may be a dict) to a single value (float
    or int). If the raw attribute is time variable, the first timestep value
    (key "0") is used and if this key is not present, the default value is
    retrieved.

    NOTE: If the raw attribute is a dict, only the value for key "0" is
    considered. If this key is not present, the default value is used.
    """

    # first obtain the value directly from the data file
    if isinstance(raw_attribute, dict):
        # for time-variable items, the raw_attribute is a dictionary
        value = raw_attribute.get("0", variables_default_values[entity_type][attribute_name])
    else:
        # for constant (non time-variable) items, the raw_attribute is always present
        value = raw_attribute

    return value
