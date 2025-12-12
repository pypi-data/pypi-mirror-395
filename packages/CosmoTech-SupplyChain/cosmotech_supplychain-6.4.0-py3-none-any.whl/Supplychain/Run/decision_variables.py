from Supplychain.Generic.json_folder_reader import JSONReader
from Supplychain.Transform.helpers import find_element_in_dataset_by_id, find_entities_by_tag, get_sheet_from_dataset
from Supplychain.Run.dataset_helpers import (
    DatasetElement,
    _retrieve_attribute_number_value_or_default,
    mapping_attribute_data_model_to_entity_types,
    mapping_attribute_type_data_model
)
from comets import CosmoInterface
from typing import Union


class DecisionVariable:
    """
    Class describing a decision variable, in the formulation of the CoMETS optimization problem.
    It also contains the information necessary for the transformation from optimization decision variables
    to actual elements that are modified in the optimization. This means that the decision variable itself
    is described by an id, its min, max and initial values, and its type. Information necessary for the
    transformation are the group action and the group members.
    """
    VALID_GROUP_ACTIONS = ["multiply_original_value", "set_new_value"]

    def __init__(
        self, id: str,
        min_value: Union[int, float],
        max_value: Union[int, float],
        init_value: Union[int, float],
        var_type: str,
        action: str,
        group_members: list[DatasetElement],
    ) -> None:
        """
        Constructor of the DecisionVariable class.

        Args:
            id (str): id of the decision variable
            min_value (float or int): minimum value of the decision variable
            max_value (float or int): maximum value of the decision variable
            init_value (float or int): initial value of the decision variable
            var_type (type): type of the decision variable: float or int
            action (str): action of the decision variable on the group of
                dataset elements governed by this decision variable. This
                can be either "multiply_original_value" or "set_new_value"
            group_members (list[DatasetElement]): elements that are part of
                the group
        """

        self.id = id
        self.min = min_value
        self.max = max_value
        self.init_value = init_value
        self.var_type = var_type
        self.action = action
        self.group_members = group_members
        self.inverse = None

        # validate min <= init <= max
        self.validate_values()

        # validate the group action
        self.validate_group_action()

    def validate_values(self) -> None:
        """
        Validate whether min <= init <= max and min<max.
        """

        if self.min >= self.max:
            raise ValueError(
                f"Minimum value of the decision variable {self.id}"
                f" must be smaller than the maximum value.")
        if self.min > self.init_value:
            raise ValueError(
                f"Initial value of the decision variable {self.id}"
                f" is less than the minimum value. This is not allowed.")
        if self.init_value > self.max:
            raise ValueError(
                f"Initial value of the decision variable {self.id}"
                f" is greater than the maximum value. This is not allowed.")

    def validate_group_action(self) -> None:
        """
        Validate whether the group action is valid.
        """

        if self.action not in self.VALID_GROUP_ACTIONS:
            raise ValueError(
                f"Group action {self.action} is not a valid group action. "
                f"Valid group actions are "
                + ", ".join(self.VALID_GROUP_ACTIONS)
            )

    def retrieve_datapaths_from_cosmo_interface(self, cosmo_interface: CosmoInterface) -> None:
        """
        Retrieve the data paths in the CoSML model for all group members. This is done
        by calling the retrieve_datapath_from_cosmo_interface method for all group
        members.
        """

        for group_member in self.group_members:
            group_member.retrieve_datapath_from_cosmo_interface(cosmo_interface)
        if self.inverse is not None:
            self.inverse.retrieve_datapath_from_cosmo_interface(cosmo_interface)

    def __repr__(self) -> str:
        return (
            f"Decision variable(id={self.id}, min={self.min}, max={self.max}, init={self.init_value}, "
            f"type={self.var_type}, group action={self.action}, group members={self.group_members})"
        )

    def __str__(self) -> str:
        group_members_brief = [f"{group_member.entity_id}::{group_member.attribute_name}" for group_member in self.group_members]
        inverse_brief = f"{self.inverse.entity_id}::{self.inverse.attribute_name}" if self.inverse is not None else ""
        n_group_members = len(self.group_members)
        addition = "s" if n_group_members > 1 else ""
        return (
            f"Decision variable {self.id} with min={self.min}, max={self.max}, init={self.init_value}, "
            f"type={self.var_type}, group action={self.action}, and {n_group_members} group member{addition}:\n--"
            + "\n--".join(group_members_brief)
            + f"\ninverse:\n--{inverse_brief}"
        )


class DecisionVariableSpace:
    """
    Class describing the space of decision variables. The space is a list of DecisionVariables
    and has methods to generate a space of decision variables from other input.
    """

    def __init__(self, decision_variables: list[DecisionVariable]) -> None:
        self._decision_variables = decision_variables
        self.stocks_by_source = {}
        self.sources_to_normalize = []

    def add_decision_variable(self, decision_variable: DecisionVariable) -> None:
        """
        Manually add a decision variable to the space.
        """

        # do some basic checks
        if not isinstance(decision_variable, DecisionVariable):
            raise ValueError("Only objects of type DecisionVariable can be added to the DecisionVariableSpace.")
        if decision_variable.id in [decvar.id for decvar in self._decision_variables]:
            raise ValueError(f"Decision variable with id {decision_variable.id} is already present in the DecisionVariableSpace.")
        # add decision variable
        self._decision_variables.append(decision_variable)

    def find_decision_variable_by_id(self, id: str) -> DecisionVariable:
        """
        Find a decision variable by its id.

        NOTE: this is not implemented very efficiently (loop over all decision variables),
        but that's probably ok since we don't expect the decision variables to be enormous.
        """

        # TODO: this is not very efficient, perhaps DecisionVariableSpace should be a dict.
        for decvar in self._decision_variables:
            if decvar.id == id:
                return decvar

    def retrieve_all_datapaths_from_cosmo_interface(self, cosmo_interface: CosmoInterface) -> None:
        """
        Retrieve the data paths in the CoSML model for all group members of all decision variables.
        This is done by calling the retrieve_datapaths_from_cosmo_interface method for all
        decision variables.
        """

        for decvar in self._decision_variables:
            decvar.retrieve_datapaths_from_cosmo_interface(cosmo_interface)

    def check_normalization_sets(self, reader: JSONReader):
        """
        Check if the decision variables can be grouped in sets where their
        attribute values can be normalized. This should be the case for
        proportions if the related proportions are all in the decision
        variables. The sum of the attribute values for such a set should be one.
        If such a set contains only one attribute value, then the decision
        variable can be removed as the normalized attribute value will always be
        one.
        If such a set contains exactly two attributes values, with two decision
        variables, both setting a new value between zero and one, then the
        decision variables can be reduced to only one by calculating the other
        attribute value as the inverse of the first one (v, 1 - v).
        """
        stocks_by_source = {}
        sources_by_stock = {}
        for output in reader.files.get('output', []):
            stocks_by_source[output['source']] = output['target']
            sources_by_stock.setdefault(output['target'], []).append(output['source'])
        for transport in reader.files.get('Transport', []):
            stocks_by_source[transport['Label']] = transport['target']
            sources_by_stock.setdefault(transport['target'], []).append(transport['Label'])
        sources_by_stock = {
            stock: set(sources_by_stock[stock])
            for stock in list(sources_by_stock)
            if len(sources_by_stock[stock]) >= 2
        }
        self.stocks_by_source = stocks_by_source

        sourcing_sets = {}
        for dv in self._decision_variables:
            dv.group_members = [
                de
                for de in dv.group_members
                if (
                    de.attribute_name != 'SourcingProportions'
                    or stocks_by_source[de.entity_id] in sources_by_stock
                )
            ]
            for i, de in enumerate(dv.group_members):
                if de.attribute_name == 'SourcingProportions':
                    sourcing_sets.setdefault(stocks_by_source[de.entity_id], set()).add(de.entity_id)
        source_pairs_by_stock = {
            stock: sources
            for stock, sources in sourcing_sets.items()
            if sources == sources_by_stock[stock] and len(sources) == 2
        }
        source_pairs_dv_by_stock = {}
        for i, dv in enumerate(self._decision_variables):
            if dv.min == 0 and dv.max == 1 and dv.action == 'set_new_value' and len(dv.group_members) == 1:
                de = dv.group_members[0]
                if de.attribute_name == 'SourcingProportions' and stocks_by_source[de.entity_id] in source_pairs_by_stock:
                    source_pairs_dv_by_stock.setdefault(stocks_by_source[de.entity_id], []).append(i)
        for pair in source_pairs_dv_by_stock.values():
            if len(pair) == 2:
                i, j = pair
                self._decision_variables[i].inverse = self._decision_variables[j].group_members[0]
                self._decision_variables[j].group_members = []
        self._decision_variables = [
            dv
            for dv in self._decision_variables
            if dv.group_members
        ]
        self.sources_to_normalize = set(
            source
            for stock, sources in sourcing_sets.items()
            if sources == sources_by_stock[stock]
            for source in sources
        )

    @classmethod
    def generate_from_configuration(cls, reader: JSONReader) -> "DecisionVariableSpace":
        """
        Generate a list of decision variables from the parameters in Configuration. In this case,
        all entities of a given entity type are considered, with the same attribute, min and
        max values. Initial values are taken from the actual entities themselves.

        Decision variable ids are coded as "c_{counter}", where counter is an integer that is
        incremented for every decision variable. This corresponds to a counter of all the entities
        that are considered.
        """

        # read in decision variable parameters from Configuration
        (
            entity_types,
            attribute_name,
            decision_variable_min,
            decision_variable_max,
        ) = _get_configuration_decision_var_info_from_dataset(reader)

        # initialize empty decision variable list and counter
        decision_variables = []
        counter = 0

        for entity_type in entity_types:
            # obtain the entities and their initial values based on the entity_type and attribute_name
            entities = get_sheet_from_dataset(entity_type, reader, False)
            for entity in entities:
                # hack to make sure sheet_name is available for the DatasetElement
                entity['sheet_name'] = entity_type
                # create a decision variable id based on the counter value -- this ensures the id is unique
                decision_var_id = f"c_{counter}"
                # obtain the entity id
                try:
                    entity_id = entity['id']
                except KeyError:
                    # This is for Transport, which does not have an id field but uses the Label instead.
                    # TODO: really that should be fixed in the data model.
                    entity_id = entity["Label"]
                # create the dataset element
                dataset_element = DatasetElement(entity_id, attribute_name)
                dataset_element.retrieve_attribute_properties_from_entity(entity)
                # transform the raw attribute to a value that can be used as the initial value
                decision_var_init_value = _transform_raw_attribute_value_to_initial_value(
                    raw_attribute=dataset_element.raw_attribute_value,
                    entity_type=entity_type,
                    attribute_name=attribute_name,
                    min_value=decision_variable_min,
                    max_value=decision_variable_max,
                )
                # determine the attribute type. This is taken from the mapping, or set to float if not found
                # TODO: must be improved because it's a hack.
                decision_var_type = mapping_attribute_type_data_model.get(attribute_name, "float")
                # create the decision variable
                decision_var = DecisionVariable(
                    id=decision_var_id,
                    min_value=decision_variable_min,
                    max_value=decision_variable_max,
                    init_value=decision_var_init_value,
                    var_type=decision_var_type,
                    action="set_new_value",
                    group_members=[dataset_element],
                )
                # add the decision variable to the list
                decision_variables.append(decision_var)
                # increment the counter
                counter += 1

        return cls(decision_variables)

    @classmethod
    def generate_from_selection(cls, reader: JSONReader) -> "DecisionVariableSpace":
        """
        Generate a DecisionVariableSpace based on the entity/attribute combinations that are
        selected by the user in the sheet OptimizationDecisionVariables. The initial values
        are taken from the actual entities themselves.

        Entities can either be selected directly, or by selecting a group of entities based
        on the tag by which the group is identified.

        Decision variable ids are coded as "{selection_id}_{counter}", where selection_id
        is the id of the selection in the OptimizationDecisionVariables sheet, and counter
        is an integer that is incremented for every decision variable. This corresponds to
        a counter of all the entities that are considered. If a selection is based on a tag,
        the counter is incremented for every entity that is part of the tag because every
        entity is considered a separate decision variable.
        """

        # read in the OptimizationDecisionVariables sheet
        selections = get_sheet_from_dataset("OptimizationDecisionVariables", reader)

        # initialize empty decision variable list
        decision_variables = []

        # loop over all lines in the selection sheet
        for selection in selections:
            # get the selection id
            selection_id = selection["id"]
            # get the entities corresponding to "SelectedEntity" or "SelectedTag"
            if selection["SelectedEntity"]:
                entities = [find_element_in_dataset_by_id(selection["SelectedEntity"], reader)]
            elif selection["SelectedTag"]:
                entities = find_entities_by_tag(selection["SelectedTag"], reader)
            else:
                # TODO: should this error be raised here?
                raise ValueError("No entity or tag selected.")

            # obtain the attribute name, min and max
            attribute_name = selection["Attribute"]
            decision_var_min_value = selection["AttributeMinimumValue"]
            decision_var_max_value = selection["AttributeMaximumValue"]

            # for every entity, create a decision variable
            counter = 0
            for entity in entities:
                # decision variable id is based on the counter value -- this ensures the id is unique
                decision_var_id = f"{selection_id}_{counter}"
                # obtain the entity id
                try:
                    entity_id = entity['id']
                except KeyError:
                    # This is for Transport, which does not have an id field but uses the Label instead.
                    # TODO: really that should be fixed in the dataset.
                    entity_id = entity["Label"]

                if attribute_name == 'DispatchProportions':
                    entity_id = f"{entity['source']}_to_{entity_id}"

                dataset_element = DatasetElement(entity_id, attribute_name)
                dataset_element.retrieve_attribute_properties_from_entity(entity)

                # determine the decision variable initial value, based on the raw attribute value
                # as recorded in the dataset element.
                decision_var_init_value = _transform_raw_attribute_value_to_initial_value(
                    raw_attribute=dataset_element.raw_attribute_value,
                    entity_type=entity['sheet_name'],
                    attribute_name=attribute_name,
                    min_value=decision_var_min_value,
                    max_value=decision_var_max_value,
                )
                # determine the decision var type. This is taken from the mapping, or set to float if not found
                # TODO: must be improved. Ugly hack!
                decision_var_type = mapping_attribute_type_data_model.get(attribute_name, "float")
                # create the decision variable
                decision_var = DecisionVariable(
                    id=decision_var_id,
                    min_value=decision_var_min_value,
                    max_value=decision_var_max_value,
                    init_value=decision_var_init_value,
                    var_type=decision_var_type,
                    action="set_new_value",
                    group_members=[dataset_element],
                )

                # add the decision variable to the list
                decision_variables.append(decision_var)

                # increment the counter
                counter += 1

        return cls(decision_variables)

    @classmethod
    def generate_from_groups(cls, reader: JSONReader) -> "DecisionVariableSpace":
        """
        Generate a DecisionVariableSpace based on the entity groups that are
        selected by the user in the sheet OptDecisionVariableGroups and the
        attribute that is indicated. Every group of entity/attribute combinations
        is controlled by a single decision variable, and all group members will move
        according to the defined group behavior. Implemented group behaviors are:
        - "MultiplyOriginalValue": multiply the original attribute value by the
          decision variable value. This means that for instance all group members
          will increase by the same factor (e.g. if the decision variable is 1.1,
          the given attribute value for all group members will increase by 10%).
        - "SetNewValue": set the attribute value to the decision variable value.
          This means that all group members will have the same attribute value.

        The decision variable initial value is specified, the attribute initial
        value is taken from the actual entities themselves.
        """

        group_action_mapping = {
            "MultiplyOriginalValue": "multiply_original_value",
            "SetNewValue": "set_new_value",
        }

        # Read in the Groups sheet
        decision_vars = get_sheet_from_dataset("OptDecisionVariableGroups", reader)

        # Initialize empty decision variable list
        decision_variables = []

        # Loop over all lines in the group sheet
        for dataset_dv in decision_vars:
            attribute_name = dataset_dv["Attribute"]
            action = group_action_mapping[dataset_dv["GroupBehaviorMode"]]
            # determine the decision var type.
            if action == "multiply_original_value":
                decision_var_type = "float"
            else:
                # This is taken from the mapping, or set to float if not found
                # TODO: must be improved. Ugly hack!
                decision_var_type = mapping_attribute_type_data_model.get(attribute_name, "float")

            # get the entities corresponding to "GroupTag"
            entities = find_entities_by_tag(dataset_dv["GroupTag"], reader)
            # create the decision variable group members from the collected entities
            group_members = []
            for entity in entities:
                # obtain the entity id
                try:
                    entity_id = entity['id']
                except KeyError:
                    # This is for Transport, which does not have an id field but uses the Label instead.
                    # TODO: really that should be fixed in the dataset.
                    entity_id = entity["Label"]

                # Prepare the decision variable group member
                dataset_element = DatasetElement(entity_id, attribute_name)
                dataset_element.retrieve_attribute_properties_from_entity(entity)
                group_members.append(dataset_element)

            # create the decision variable using the collected group members
            decision_var = DecisionVariable(
                id=dataset_dv["id"],
                min_value=dataset_dv["DecisionVariableMinimum"],
                max_value=dataset_dv["DecisionVariableMaximum"],
                init_value=dataset_dv["DecisionVariableStartingPoint"],
                var_type=decision_var_type,
                action=action,
                group_members=group_members,
            )
            # add the decision variable to the list
            decision_variables.append(decision_var)

        return cls(decision_variables)

    def __iter__(self) -> iter:
        return iter(self._decision_variables)

    def __getitem__(self, index) -> DecisionVariable:
        return self._decision_variables[index]

    def __len__(self) -> int:
        return len(self._decision_variables)

    def __add__(self, other: "DecisionVariableSpace") -> "DecisionVariableSpace":
        return DecisionVariableSpace(self._decision_variables + other._decision_variables)

    def __repr__(self) -> str:
        n_dec_vars = len(self._decision_variables)
        addition = "s" if n_dec_vars > 1 else ""
        return (
            f"DecisionVariableSpace with {len(self._decision_variables)} decision variable{addition}:\n- "
            + "\n- ".join([str(decvar) for decvar in self._decision_variables])
        )

    def __str__(self) -> str:
        return self.__repr__()


# some loose helper functions
def _transform_raw_attribute_value_to_initial_value(
    raw_attribute: Union[dict, float, int],
    entity_type: str,
    attribute_name: str,
    min_value: Union[int, float],
    max_value: Union[int, float],
) -> Union[float, int]:
    """
    Transform the attribute value to the initial value of the decision variable,
    taking into account the "validity rules" for the initial value:
    1. if the value is in the data file, use that value. Otherwise, use
       the default value.
    3. if the resulting value is not within the min and max values, set it to
       the average of min and max.

    The first rule is applied using the function
    `_retrieve_attribute_number_value_or_default()`.
    """

    # retrieve the attribute value
    init_value = _retrieve_attribute_number_value_or_default(raw_attribute, entity_type, attribute_name)

    # then make sure init_value is within min and max
    if init_value < min_value or init_value > max_value:
        init_value = (min_value + max_value) / 2

    return init_value


def _get_configuration_decision_var_info_from_dataset(
    reader: JSONReader
) -> tuple[list[str], str, float | int, float | int]:
    """
    Retrieve information about decision variables from the Configuration file as
    stored in the dataset (JSON format).

    Returns:
        tuple: tuple containing: the entity types (list), attribute name (str),
            the decision variable minimum value (float or int), and the decision variable maximum
            value (float or int).
    """
    # retrieve the Configuration file
    configuration = get_sheet_from_dataset("Configuration", reader)[0]

    # read in decision variable parameters from Configuration
    attribute_name = configuration["DecisionVariable"]
    try:
        entity_types = mapping_attribute_data_model_to_entity_types[attribute_name]
    except KeyError as e:
        raise KeyError(
            "When reading decision variables from the Configuration sheet, the decision variable "
            f"{attribute_name} is not defined. Defined attributes are "
            f"{list(mapping_attribute_data_model_to_entity_types.keys())}."
        ) from e
    decision_variable_min = configuration["DecisionVariableMin"]
    decision_variable_max = configuration["DecisionVariableMax"]

    return (entity_types, attribute_name, decision_variable_min, decision_variable_max)


# Transformation functions for decision variables, used in StochasticOptimizer
def convert_decision_var_parameter_set_to_model_parameter_set(
    decision_var_parameter_set: dict,
    decision_variable_space: DecisionVariableSpace,
) -> dict:
    """
    Transform a decision variable parameter set to a parameter set in attribute space.
    In the former, the keys are the ids of the decision variables, while the values are
    the decision variable values at this particular point in the optimization.
    In the latter, the keys are the datapaths of the attributes to be modified in the
    CoSML model, and the values are the actual attribute values. Because there can be
    multiple attributes associated to a single decision variable, the model parameter
    set can be larger than the decision variable parameter set.
    """

    model_parameter_set = {}

    for decision_variable_id, dv_value in decision_var_parameter_set.items():
        # retrieve the corresponding decision variable
        decision_variable = decision_variable_space.find_decision_variable_by_id(decision_variable_id)
        attribute_values = transform_decision_var_value_to_group_attribute_values(
            decision_var_value=dv_value, decision_variable=decision_variable
        )
        model_parameter_set.update(attribute_values)

    return model_parameter_set


def transform_decision_var_value_to_group_attribute_values(
    decision_var_value: float,
    decision_variable: DecisionVariable,
) -> dict:
    """
    Transform a single decision variable value to a set of attribute values
    corresponding to the group members of the decision variable.
    """

    # loop over decision variable group members and transform each group member
    attribute_values = {}
    for group_member in decision_variable.group_members:
        # obtain attribute value for this group member
        attribute_value = apply_decision_var_action_to_single_attribute_value(
            decision_var_action=decision_variable.action,
            decision_var_value=decision_var_value,
            attribute_orig_value=group_member.attribute_number_value,
        )
        # transform time-variable attribute values to a dict format
        if group_member.attribute_is_time_variable:
            attribute_value = {0: attribute_value}
        # add the attribute value to the attribute values dictionary, with as key the datapath
        attribute_key = group_member.cosml_datapath
        attribute_values[attribute_key] = attribute_value
    if decision_variable.inverse is not None:
        attribute_values[decision_variable.inverse.cosml_datapath] = {t: 1 - v for t, v in attribute_value.items()}

    return attribute_values


def apply_decision_var_action_to_single_attribute_value(
    decision_var_action: str,
    decision_var_value: float,
    attribute_orig_value: float | int,
) -> float:
    """
    Apply the decision variable action to a single attribute value,
    based on the decision variable value. The action can be either
    "multiply_original_value" or "set_new_value".
    """
    if decision_var_action == "multiply_original_value":
        model_value = attribute_orig_value * decision_var_value
    elif decision_var_action == "set_new_value":
        model_value = decision_var_value
    else:
        raise ValueError(
            f"Action {decision_var_action} is not recognized. Must "
            "be 'multiply_original_value' or 'set_new_value'."
        )
    return model_value
