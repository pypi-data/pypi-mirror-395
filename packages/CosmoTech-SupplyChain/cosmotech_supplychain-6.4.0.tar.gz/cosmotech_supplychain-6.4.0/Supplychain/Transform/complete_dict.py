from datetime import date

from Supplychain.Generic.folder_io import FolderWriter, FolderReader
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.adt_column_description import ADTColumnDescription
from Supplychain.Schema.default_values import parameters_default_values, variables_default_values
from Supplychain.Schema.validation_schemas import ValidationSchemas

dataset_description = ADTColumnDescription.format


class DictCompleter(Timer):

    def __init__(self,
                 reader: FolderReader,
                 writer: FolderWriter):
        Timer.__init__(self, prefix="[Complete]")
        self.reader = reader
        self.writer = writer
        self.schema = ValidationSchemas()

    def __initialize_configuration(self):
        self.reader.files.setdefault('Configuration', [])
        if not self.reader.files['Configuration']:
            self.reader.files['Configuration'].append({})

    def __complete_data_generic(self):
        for file_name, values in parameters_default_values.items():
            for datum in self.reader.files.get(file_name, []):
                if datum.get('Label') is None and 'id' in datum:
                    datum['Label'] = datum['id']
                for key, value in values.items():
                    if datum.get(key) is None:
                        datum[key] = value

    def __cast_integers(self):
        for file_name in self.schema.schemas:
            keys = [
                key
                for key, description in self.schema.schemas[file_name]['properties'].items()
                if description.get('type') == 'integer'
            ]
            for datum in self.reader.files.get(file_name, []):
                for key in keys:
                    value = datum.get(key)
                    if value is not None:
                        datum[key] = int(value)

    def __standardize_time_steps(self):
        for file_name, file_description in dataset_description.items():
            time_elements = list(file_description['change'])
            for events in file_description['event'].values():
                time_elements.extend(events)

            for datum in self.reader.files.get(file_name, []):
                for time_element in time_elements:
                    if datum.get(time_element) is not None:
                        datum[time_element] = {
                            str(int(float(time_step))): value
                            for time_step, value in datum[time_element].items()
                        }

    def __complete_sourcing_proportions(self):
        sources_by_stock = {}
        sourcing_proportions = {}

        for output in self.reader.files.get('output', []):
            sources_by_stock.setdefault(output['target'], []).append(output['source'])
        for operation in self.reader.files.get('ProductionOperation', []):
            sourcing_proportions[operation['id']] = operation.get('SourcingProportions')
        for transport in self.reader.files.get('Transport', []):
            sources_by_stock.setdefault(transport['target'], []).append(transport['Label'])
            sourcing_proportions[transport['Label']] = transport.get('SourcingProportions')

        for sources in sources_by_stock.values():
            if all(sourcing_proportions[source] is None for source in sources):
                for source in sources:
                    sourcing_proportions[source] = {'0': 1.0}
            else:
                for source in sources:
                    if sourcing_proportions[source] is None:
                        sourcing_proportions[source] = {}

        for operation in self.reader.files.get('ProductionOperation', []):
            operation['SourcingProportions'] = sourcing_proportions[operation['id']]
        for transport in self.reader.files.get("Transport", []):
            transport['SourcingProportions'] = sourcing_proportions[transport['Label']]

    def __complete_dispatch_proportions(self):
        operations_by_stock = {}
        dispatch_proportions = {}
        retain_proportions = {}

        for i in self.reader.files.get('input', []):
            operations_by_stock.setdefault(i['source'], []).append(i['target'])
            dispatch_proportions[(i['source'], i['target'])] = i.get('DispatchProportions')
        for transport in self.reader.files.get('Transport', []):
            operations_by_stock.setdefault(transport['source'], []).append(transport['Label'])
            dispatch_proportions[(transport['source'], transport['Label'])] = transport.get('DispatchProportions')
        for stock in self.reader.files.get('Stock', []):
            retain_proportions[stock['id']] = stock.get('RetainProportions')

        retainers = set()
        if self.reader.files['Configuration'][0]['IntermediaryStockDispatchPolicy'] == "AllowRetention":
            retainers = set(
                stock['id']
                for stock in self.reader.files.get('Stock', [])
                if any(0 < demand for demand in stock['Demands'].values())
            )

        for stock, operations in operations_by_stock.items():
            if all(dispatch_proportions[(stock, operation)] is None for operation in operations) and retain_proportions[stock] is None:
                if stock in retainers:
                    p = 1 / (len(operations) + 1)
                    retain_proportions[stock] = {'0': p}
                else:
                    p = 1 / len(operations)
                    retain_proportions[stock] = {}
                for operation in operations:
                    dispatch_proportions[(stock, operation)] = {'0': p}
            else:
                for operation in operations:
                    if dispatch_proportions[(stock, operation)] is None:
                        dispatch_proportions[(stock, operation)] = {}
                if retain_proportions[stock] is None:
                    retain_proportions[stock] = {}

        for i in self.reader.files.get('input', []):
            i['DispatchProportions'] = dispatch_proportions[(i['source'], i['target'])]
        for transport in self.reader.files.get("Transport", []):
            transport['DispatchProportions'] = dispatch_proportions[(transport['source'], transport['Label'])]
        for stock in self.reader.files.get("Stock", []):
            stock['RetainProportions'] = retain_proportions[stock['id']]

    def __complete_production_proportions(self):
        operations_by_resource = {}
        production_proportions = {}

        for contains in self.reader.files.get('contains', []):
            operations_by_resource.setdefault(contains['source'], []).append(contains['target'])
        for operation in self.reader.files.get('ProductionOperation', []):
            production_proportions[operation['id']] = operation.get('ProductionProportions')

        for operations in operations_by_resource.values():
            if all(production_proportions[operation] is None for operation in operations):
                p = 1.0 / len(operations)
                for operation in operations:
                    production_proportions[operation] = {'0': p}
            else:
                for operation in operations:
                    if production_proportions[operation] is None:
                        production_proportions[operation] = {}

        for operation in self.reader.files.get('ProductionOperation', []):
            operation['ProductionProportions'] = production_proportions[operation['id']]

    def __complete_data_specific(self):
        for configuration in self.reader.files.get('Configuration', []):
            if configuration.get('StartingDate') is None:
                configuration['StartingDate'] = date.today().isoformat()
            if configuration.get('SelectedTimeStep') is None:
                configuration['SelectedTimeStep'] = configuration['SimulatedCycles'] * configuration['StepsPerCycle'] - 1

        may_be_infinite = (
            set(s['id'] for s in self.reader.files.get('Stock', []))
            - set(o['target'] for o in self.reader.files.get('output', []))
            - set(t['target'] for t in self.reader.files.get('Transport', []))
            - set(t['source'] for t in self.reader.files.get('Transport', []))
        )
        for stock in self.reader.files.get('Stock', []):
            is_infinite = stock.get('IsInfinite')
            initial_stock = stock.get('InitialStock')
            initial_value = stock.get('InitialValue')
            if is_infinite or (is_infinite is None and initial_stock is None and stock['id'] in may_be_infinite):
                stock['IsInfinite'] = True
                stock['InitialStock'] = 0
                stock['InitialValue'] = 0
            else:
                stock['IsInfinite'] = False
                stock['InitialStock'] = initial_stock or 0
                stock['InitialValue'] = initial_value or 0
            demands = stock['Demands']
            demands_weight = stock['DemandWeights']
            for time_step in demands:
                if demands_weight.get(time_step) is None:
                    demands_weight[time_step] = variables_default_values['Stock']['DemandWeights']

        for resource in self.reader.files.get('ProductionResource', []):
            if resource.get('OpeningTimes') is None:
                resource['OpeningTimes'] = {'0': self.reader.files['Configuration'][0]['TimeStepDuration']}

        self.__complete_sourcing_proportions()
        self.__complete_dispatch_proportions()
        self.__complete_production_proportions()

    def __write_updated_files(self):
        for file_name, dict_list in self.reader.files.items():
            self.writer.write_from_list(dict_list, file_name)

    def complete(self):
        self.display_message("Starting completion")
        self.__initialize_configuration()
        self.__complete_data_generic()
        self.__cast_integers()
        self.__standardize_time_steps()
        self.display_message("Generic completion done")
        self.__complete_data_specific()
        self.display_message("Specific completion done")
        self.__write_updated_files()
