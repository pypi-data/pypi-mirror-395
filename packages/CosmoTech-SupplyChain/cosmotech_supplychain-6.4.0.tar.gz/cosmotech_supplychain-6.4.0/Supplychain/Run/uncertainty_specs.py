from dataclasses import dataclass
import json

from Supplychain.Generic.json_folder_reader import JSONReader
from Supplychain.Transform.helpers import get_sheet_from_dataset, find_element_in_dataset_by_id
from Supplychain.Run.dataset_helpers import DatasetElement
from Supplychain.Schema.modifications import changes
from Supplychain.Schema.numeric_attributes import numeric_attributes

from comets import CosmoInterface


@dataclass
class UncertaintySpecElement:
    """
    A class representing a single line of the Uncertainties table in the dataset.
    """

    id: str
    entity: str
    attribute: str
    timestep: int
    uncertainty_mode: str
    uncertainty_model: str
    parameters: dict[str, str]
    size: int

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """
        Validate the uncertainty_mode.
        """

        # validate the uncertainty mode
        if self.uncertainty_mode not in changes:
            raise ValueError(
                f"Invalid uncertainty mode: {self.uncertainty_mode}. "
                f"Valid modes are: {', '.join(changes)}"
            )

        # validate the type of the parameters
        if not isinstance(self.parameters, dict):
            raise ValueError(f"Spec {self.id}: parameters should be of type dict, not {type(self.parameters)}.")

    def __repr__(self) -> str:
        return (
            f"UncertaintySpecElement (id {self.id}, entity {self.entity}, attribute {self.attribute}, "
            f"timestep {self.timestep}): {self.uncertainty_mode} uncertainties, uncertainty model {self.uncertainty_model}, "
            f"with parameters {self.parameters}, size: {self.size}"
        )


class UncertaintySpecs(list):
    """
    A class representing the Uncertainties table in the dataset.
    """

    def __init__(self, uncertainty_specs: list[UncertaintySpecElement]) -> None:
        super().__init__(uncertainty_specs)

    def find_by_id(self, id: str) -> UncertaintySpecElement:
        """
        Find an UncertaintySpecElement by its id.
        """

        for spec in self:
            if spec.id == id:
                return spec

        # TODO: if not found, should it raise an error or return None?
        raise ValueError(f"Spec with id {id} not found.")

    @classmethod
    def generate_from_dataset(cls, reader: JSONReader, keep_only_activated_specs=False) -> "UncertaintySpecs":
        """
        Generate UncertaintySpecs from the Uncertainties table in the dataset.
        If return_activated_only is True, the UncertaintySpecs will be filtered
        by the uncertainties that are activated as per the configuration.
        """

        configuration = reader.files['Configuration'][0]
        max_time_step = configuration['StepsPerCycle'] * configuration['SimulatedCycles']
        uncertainty_specs = [
            UncertaintySpecElement(
                id=row['id'],
                entity=str(row['Entity']),
                attribute=row['Attribute'],
                timestep=row['TimeStep'],
                uncertainty_mode=row['UncertaintyMode'],
                uncertainty_model=row['UncertaintyModel'],
                parameters=row['Parameters'] if isinstance(row['Parameters'], dict) else json.loads(row['Parameters']),
                size=max_time_step if row['TimeStep'] < 0 and numeric_attributes[row['Attribute']].attribute_type != 'fixed' else None,
            )
            for row in get_sheet_from_dataset('Uncertainties', reader, check=False)
        ]

        if keep_only_activated_specs:
            return cls(uncertainty_specs).filter_on_activated_uncertainties(reader)

        return cls(uncertainty_specs)

    def filter_on_activated_uncertainties(self, reader) -> "UncertaintySpecs":
        """
        Filter specs on activated uncertainties only.
        """

        configuration = get_sheet_from_dataset('Configuration', reader)[0]

        # collect list of activated uncertainties
        activated_attributes = set(configuration['ActivateUncertainties'])

        # filter specs on activated uncertainties
        activated_uncertainty_specs = [
            spec for spec in self if spec.attribute in activated_attributes
        ]

        # return the filtered specs as an UncertaintySpecs object
        return UncertaintySpecs(activated_uncertainty_specs)

    def export_sampling(self):
        """
        Export the uncertainty specs in the 'sampling' format as required by CoMETS.
        """

        return [
            {
                "name": spec.id,
                "sampling": spec.uncertainty_model,
                "parameters": spec.parameters,
                **({} if spec.size is None else {"size": spec.size}),
            }
            for spec in self
        ]

    def export_entity_attributes(self) -> list[tuple[str, str]]:
        """
        Export the entity and attribute names that are modified by the uncertainty specs.
        """

        return [
            (spec.entity, spec.attribute)
            for spec in self
        ]

    def __repr__(self) -> str:

        n_specs = len(self)
        addition = "s" if n_specs > 1 else ""

        return (
            f"UncertaintySpecs with {n_specs} item{addition}.\n- " +
            "\n- ".join([str(spec) for spec in self])
        )

class VariableDatasetElement:
    """
    Class to represent a DatasetElement object that is varied in an
    uncertainty analysis. It consists of the following:
    - a dataset element (fully initialized with information from the reader and cosmointerface)
    - a list of UncertaintySpec spec_ids that modify this element
    """

    def __init__(
        self,
        entity_id: str,
        attribute_name: str,
        uncertainty_specs: UncertaintySpecs,
        reader: JSONReader,
        cosmo_interface: CosmoInterface
    ) -> None:
        """
        Initialize a full VariableDatasetElement object.
        Requires:
        - UncertaintySpecs object
        - JSONReader object pointing to the dataset
        - an initialized CosmoInterface object
        """
        self.entity_id = entity_id
        self.attribute_name = attribute_name

        # retrieve related uncertainty spec ids from the UncertaintySpecs object
        self.related_uncertainty_spec_ids = self._load_related_spec_ids_from_uncertainty_specs(uncertainty_specs)

        # create an empty dataset element
        self.dataset_element = DatasetElement(entity_id, attribute_name)

        # retrieve dataset element properties from the reader and initialized cosmointerface
        self._load_dataset_element_properties_from_reader(reader)
        self._load_dataset_element_properties_from_cosmointerface(cosmo_interface)

    def _load_related_spec_ids_from_uncertainty_specs(self, uncertainty_specs: UncertaintySpecs):
        """
        Retrieve the uncertainty spec ids that are related to this variable dataset element.
        """

        return [
            spec.id for spec in uncertainty_specs
            if spec.entity == self.entity_id and spec.attribute == self.attribute_name
        ]

    def _load_dataset_element_properties_from_reader(self, reader: JSONReader):
        """
        Load the dataset element properties from the reader.
        """

        # retrieve the entity from the reader
        entity = find_element_in_dataset_by_id(self.entity_id, reader)
        # attach reader-derived information to the dataset element
        self.dataset_element.retrieve_attribute_properties_from_entity(entity)

    def _load_dataset_element_properties_from_cosmointerface(self, cosmo_interface: CosmoInterface):
        """
        Load the dataset element properties from the cosmo interface.
        Requires the CosmoInterface to be initialized.
        """
        self.dataset_element.retrieve_datapath_from_cosmo_interface(cosmo_interface)

    def __repr__(self) -> str:
        return (
            f"VariableDatasetElement (entity {self.entity_id}, attribute {self.attribute_name}):\n" +
            f"- DatasetElement: {self.dataset_element}\n" +
            f"- Related uncertainty spec ids: {self.related_uncertainty_spec_ids}\n"
        )

class VariableDatasetElementCollection(dict):
    """
    A collection of VariableDatasetElement objects.
    """

    def __init__(
        self,
        entity_attributes: list[tuple[str,str]],
        uncertainty_specs: UncertaintySpecs,
        reader: JSONReader,
        cosmo_interface=CosmoInterface
    ) -> None:

        variable_dataset_elements = {}
        for entity_id, attribute_name in entity_attributes:
            variable_dataset_elements[(entity_id, attribute_name)] = VariableDatasetElement(entity_id, attribute_name, uncertainty_specs, reader, cosmo_interface)
        super().__init__(variable_dataset_elements)

    def retrieve_all_datapaths_from_cosmo_interface(self, initialized_cosmo_interface: CosmoInterface) -> None:
        """
        Retrieve all datapaths for the variable dataset elements. This is done
        by calling the retrieve_datapath_from_cosmo_interface method for each
        DatasetElement.

        Requires the CosmoInterface to be initialized.
        """

        for vde in self.values():
            vde.dataset_element.retrieve_datapath_from_cosmo_interface(initialized_cosmo_interface)
