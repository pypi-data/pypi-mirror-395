from Supplychain.Generic.folder_io import FolderReader
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.validation_schemas import ValidationSchemas
from Supplychain.Schema.default_values import parameters_default_values
from Supplychain.Schema.numeric_attributes import numeric_attributes
from Supplychain.Schema.statistics import statistics, statistic_aliases

from collections import Counter
from typing import Union

import itertools
import jsonschema
from comets import DistributionRegistry


class DictValidator(Timer):

    def __init__(self,
                 reader: FolderReader,
                 run_type: Union[str, None] = None):
        Timer.__init__(self, prefix="[Validation]")

        self.reader = reader

        self.schema = ValidationSchemas()

        self.run_type = "Simulation" if run_type is None else run_type

        self.errors = []

        self.lookup_memory = dict()

        self.all_ids = {}

    def __get_configuration_parameter(self, parameter_name: str):
        parameter = None
        if self.reader.files.get('Configuration'):
            parameter = self.reader.files['Configuration'][0].get(parameter_name)
        if parameter is None:
            parameter = parameters_default_values['Configuration'].get(parameter_name)
        return parameter

    def validate(self) -> bool:
        checks = [self.validate_files(), self.validate_graph(), self.specific_validations()]
        if all(checks):
            self.display_message("Dataset is valid")
            return True
        else:
            self.display_message("Dataset is invalid")
            return False

    def validate_graph(self) -> bool:
        self.errors = []
        self.display_message("Validate graph")
        for file_to_validate in sorted(self.schema.graph.keys()):
            self.__validate_graph(file_to_validate)
        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
            return False
        self.__validate_acyclicity()
        if self.errors:
            self.display_message("1 error found in the files")
            self.display_message(self.errors[0])
            return False
        self.display_message("Graph is valid")
        return True

    def validate_files(self) -> bool:
        self.errors = []
        self.display_message("Validate file content")
        for file_to_validate in sorted(self.schema.schemas.keys()):
            self.__validate_file(file_to_validate)

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                message = err.message.replace("{", "{{").replace("}", "}}")
                path = '/'.join(str(loc) for loc in err.path)
                self.display_message(f" - {filename}: {item_id}: {path}: {message}")
        else:
            self.display_message("Individual files are valid")
            return True
        return False

    def __validate_file(self, file_name: str):
        if file_name not in self.reader.files:
            return
        for item in self.reader.files[file_name]:
            validator = jsonschema.Draft7Validator(schema=self.schema.schemas[file_name])
            errors = validator.iter_errors(item)
            item_id = 0
            if "id" in item:
                item_id = item["id"]
            elif "Label" in item:  # TODO specific for relationship here transport (only Transport relationship is validated) to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                item_id = item["Label"]
            elif 'source' in item or 'target' in item:
                item_id = item.get('source', "") + " -> " + item.get('target', "")
            for error in errors:
                self.errors.append((file_name, item_id, error))
        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_graph(self, file_name: str):
        config = self.schema.graph[file_name]
        source_file, source_id = config['links']['source']
        target_file, target_id = config['links']['target']

        source_entities = set(entity[source_id] for entity in self.reader.files.get(source_file, []))
        target_entities = set(entity[target_id] for entity in self.reader.files.get(target_file, []))

        arcs = [
            (arc[config['source']], arc[config['target']])
            for arc in self.reader.files.get(file_name, [])
        ]
        sources, targets = zip(*arcs) if arcs else ((), ())
        source_vertices = set(sources)
        target_vertices = set(targets)

        # Check relation existences
        for check, entities, vertices, entity_file in [
            (config['all_source_present'], source_entities, source_vertices, source_file),
            (config['all_target_present'], target_entities, target_vertices, target_file),
        ]:
            if check:
                if entities and not vertices:
                    self.errors.append((entity_file, 'all', f"have no relations in {file_name} which is empty"))
                else:
                    for entity in entities - vertices:
                        self.errors.append((entity_file, entity, f"has no relations in {file_name}"))

        # Check entity existences
        for entities, vertices, entity_file in [
            (source_entities, source_vertices, source_file),
            (target_entities, target_vertices, target_file),
        ]:
            if vertices and not entities:
                self.errors.append((file_name, 'all', f"do not exist in {entity_file} which is empty"))
            else:
                for vertex in vertices - entities:
                    self.errors.append((file_name, vertex, f"does not exist in {entity_file}"))

        # Check cardinalities
        indegree, outdegree = config['cardinalities'].split(':')
        for vertices, occurrences, cardinality, entity_file in [
            (source_vertices, sources, outdegree, source_file),
            (target_vertices, targets, indegree, target_file),
        ]:
            if cardinality == "1":
                for vertex in vertices:
                    if occurrences.count(vertex) > 1:
                        self.errors.append((entity_file, vertex, f"has more than one relation in {file_name}"))

        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_acyclicity(self):
        arcs_by_file_name = {
            file_name: [
                (i[config['source']], i[config['target']])
                for i in self.reader.files.get(file_name, [])
            ]
            for file_name, config in self.schema.graph.items()
        }
        arcs = [
            arc
            for arcs_of_file in arcs_by_file_name.values()
            for arc in arcs_of_file
        ]
        if arcs:
            vertices = set(itertools.chain(*arcs))
            targets_by_source = {
                vertex: set()
                for vertex in vertices
            }
            for source, target in arcs:
                targets_by_source[source].add(target)
            visited = set()
            loop = []

            def visit(vertex):
                if vertex in visited:
                    return False
                if vertex in loop:
                    loop.append(vertex)
                    return True
                vertices.discard(vertex)
                loop.append(vertex)
                for next_vertex in targets_by_source[vertex]:
                    if visit(next_vertex):
                        return True
                visited.add(loop.pop())

            while vertices:
                if visit(vertices.pop()):
                    break
            if loop:
                loop = loop[loop.index(loop[-1]):]
                vertex_types = []
                file_names = []
                for arc in zip(loop[:-1], loop[1:]):
                    for file_name, arcs_of_file in arcs_by_file_name.items():
                        if arc in arcs_of_file:
                            break
                    vertex_types.append(self.schema.graph[file_name]['links']['source'][0])
                    file_names.append(file_name)
                spacing = max(
                    max(map(len, vertex_types)),
                    max(map(len, file_names)) - 2,
                )
                vertex_types.append(vertex_types[0])
                sep = '\n\t'
                relations = [sep] + [
                    f'{file_name:>{spacing + 2}} ↓{sep}'
                    for file_name in file_names
                ]
                loop_links = [
                    f"{relation}[{vertex_type:^{spacing}}] {vertex}"
                    for relation, vertex_type, vertex in zip(relations, vertex_types, loop)
                ]
                self.errors.append(f"The graph contains at least one loop:{sep.join(loop_links)} (same as first)")

    def specific_validations(self) -> bool:
        # If specific validations are required add them here
        self.errors = []
        self.display_message("Specific validations")

        self.__transports_specific_checks()
        self.split("\ttransports_specific_checks: {time_since_last_split:6.4f}s")
        ids = [
            ('Transport', 'Label'),
            ('ProductionOperation', 'id'),
            ('ProductionResource', 'id'),
            ('Stock', 'id'),
            ('OptimizationConstraints', 'id'),
            ('OptimizationDecisionVariables', 'id'),
            ('OptDecisionVariableGroups', 'id'),
            ('Tags', 'id'),
            ('Uncertainties', 'id'),
        ]
        for filename, id_column in ids:
            self.__unique_id_validation(filename, id_column)
        self.__global_unique_id_validation()
        self.split("\tunique_id_validation: {time_since_last_split:6.4f}s")

        if self.run_type == "MILPOptimization":
            self.__part_retention_validation()
            self.split("\tpart_retention_validation: {time_since_last_split:6.4f}s")

        if self.run_type in ("CustomOptimization", "StochasticOptimization"):
            self.__decision_variable_validation()
            self.split("\tdecision_variable_validation: {time_since_last_split:6.4f}s")
            self.__kpi_statistic_validation()
            self.split("\tkpi_statistic_validation: {time_since_last_split:6.4f}s")

        if self.run_type not in ("CustomOptimization", "MILPOptimization"):
            self.__uncertainties_validation()
            self.split("\tuncertainties_validation: {time_since_last_split:6.4f}s")

        self.__infinite_stocks_checks()
        self.split("\tinfinite_stocks_checks: {time_since_last_split:6.4f}s")

        self.__obsolescence_check()
        self.split("\tobsolescence_check: {time_since_last_split:6.4f}s")

        self.__sourcing_proportions_check()
        self.split("\tsourcing_proportions_check: {time_since_last_split:6.4f}s")

        self.__dispatch_proportions_check()
        self.split("\tdispatch_proportions_check: {time_since_last_split:6.4f}s")

        self.__production_proportions_check()
        self.split("\tproduction_proportions_check: {time_since_last_split:6.4f}s")

        self.__mandatory_attributes_check()
        self.split("\tmandatory_attributes_check: {time_since_last_split:6.4f}s")

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
        else:
            self.display_message("Specific checks are valid")
            return True
        return False

    def __part_retention_validation(self):
        stocks = self.reader.files.get('Stock', [])
        transports = self.reader.files.get('Transport', [])
        outputs = self.reader.files.get('input', [])
        isdp = self.__get_configuration_parameter('IntermediaryStockDispatchPolicy')
        if isdp == 'DispatchAll':
            non_final_stocks = set()
            for t in transports:
                non_final_stocks.add(t['source'])
            for o in outputs:
                non_final_stocks.add(o['source'])
            for stock in stocks:
                if stock['id'] not in non_final_stocks:
                    continue
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                if any(stock_demands.values()):
                    self.errors.append(("Stock",
                                        stock['id'],
                                        "has demands and is not a final stock,"
                                        " set IntermediaryStockDispatchPolicy to AllowRetention"))

    def __decision_variable_validation(self):
        decision_variable = self.__get_configuration_parameter('DecisionVariable')
        if decision_variable == 'FromDataset' and not any(self.reader.files.get(file_name) for file_name in ('OptimizationDecisionVariables', 'OptDecisionVariableGroups')):
            self.errors.append((
                'Configuration',
                'DecisionVariable',
                'No decision variable defined.'
            ))
        minimum = self.__get_configuration_parameter('DecisionVariableMin')
        maximum = self.__get_configuration_parameter('DecisionVariableMax')
        if minimum >= maximum:
            self.errors.append((
                'Configuration',
                'DecisionVariableMin/DecisionVariableMax',
                f'The decision variable minimum ({minimum}) should be strictly less than the decision variable maximum ({maximum}).'
            ))

    def __kpi_statistic_validation(self):
        statistics, statistic_aliases
        unavailable_statistics = set(statistics) - set(statistic_aliases)
        kpi = self.__get_configuration_parameter('Kpi')
        if kpi == 'IndividualTotalFillRateServiceLevel':
            statistic = self.__get_configuration_parameter('Statistic')
            if statistic in unavailable_statistics:
                self.errors.append((
                    'Configuration',
                    'Statistic',
                    f"{statistic}: The statistics {', '.join(unavailable_statistics)} are unavailable for the {kpi} KPI.",
                ))
        for constraint in self.reader.files.get('OptimizationConstraints', []):
            kpi = constraint.get('ConstrainedKpi')
            if kpi == 'IndividualTotalFillRateServiceLevel':
                statistic = constraint.get('Statistic')
                if statistic in unavailable_statistics:
                    self.errors.append((
                        'OptimizationConstraints',
                        'Statistic',
                        f"{statistic}: The statistics {', '.join(unavailable_statistics)} are unavailable for the {kpi} KPI.",
                    ))

    def __uncertainties_validation(self):
        uncertainties = self.reader.files.get('Uncertainties', [])
        undefined_entities = {}
        no_time_step_uncertainties = {}
        all_time_steps_uncertainties = {}
        one_time_step_uncertainties = {}
        for uncertainty in uncertainties:
            id_ = uncertainty['id']
            entity = str(uncertainty.get('Entity'))
            attribute = uncertainty.get('Attribute')
            t = uncertainty.get('TimeStep')
            if entity:
                file_names = set(self.all_ids.get(entity, []))
                if not file_names:
                    undefined_entities.setdefault(entity, []).append(id_)
                if attribute in numeric_attributes:
                    properties = numeric_attributes[attribute]
                    entity_types = set(properties.entity_types)
                    if file_names and not file_names & entity_types:
                        self.errors.append((
                            'Uncertainties',
                            id_,
                            f"The entity {entity} ({', '.join(file_names)}) has no attribute {attribute} ({', '.join(entity_types)}).",
                        ))
                    if properties.attribute_type == 'fixed':
                        if t and t > 0:
                            self.errors.append((
                                'Uncertainties',
                                id_,
                                f"The attribute {attribute} value does not depend on the time step but it was set to {t}.",
                            ))
                        no_time_step_uncertainties.setdefault((entity, attribute), []).append(id_)
                    else:
                        if t is None or t < 0:
                            all_time_steps_uncertainties.setdefault((entity, attribute), []).append(id_)
                        else:
                            one_time_step_uncertainties.setdefault((entity, attribute, t), []).append(id_)
            uncertainty_model = uncertainty.get('UncertaintyModel')
            parameters = uncertainty.get('Parameters', {})
            if uncertainty_model in DistributionRegistry and isinstance(parameters, dict):
                actual_parameter_names = set(parameters)
                distribution = DistributionRegistry[uncertainty_model]
                param_info = {
                    info.name: (info.integrality, info.domain)
                    for info in distribution._param_info()
                }
                expected_parameter_names = set(param_info)
                unexpected_parameter_names = actual_parameter_names - expected_parameter_names
                missing_parameter_names = expected_parameter_names - actual_parameter_names
                for names, label in ((unexpected_parameter_names, 'unexpected'), (missing_parameter_names, 'missing')):
                    if names:
                        plural = len(names) > 1
                        self.errors.append((
                            'Uncertainties',
                            id_,
                            f"The parameter{'s' if plural else ''} {', '.join(names)} {'are' if plural else 'is'} {label} for the {uncertainty_model} uncertainty model.",
                        ))
                parameter_names = actual_parameter_names & expected_parameter_names
                individually_valid_parameter_names = set()
                errors = []
                for name in parameter_names:
                    value = parameters[name]
                    if not isinstance(value, (int, float)):
                        errors.append((name, value, 'not a number'))
                        continue
                    integrality, (minimum, maximum) = param_info[name]
                    if integrality and value != round(value):
                        errors.append((name, value, 'not an integer'))
                        continue
                    if not minimum <= value <= maximum:
                        errors.append((name, value, f'out of domain [{minimum}, {maximum}]'))
                        continue
                    individually_valid_parameter_names.add(name)
                for name, value, message in errors:
                    self.errors.append((
                        'Uncertainties',
                        id_,
                        f"The parameter {name} value {value!r} is {message}.",
                    ))
                shape_parameter_names = set(info.name for info in distribution._shape_info())
                if individually_valid_parameter_names >= shape_parameter_names:
                    shape_parameters = {
                        name: value
                        for name, value in parameters.items()
                        if name in shape_parameter_names
                    }
                    if not distribution._argcheck(**shape_parameters):
                        shape_parameters_str = ', '.join(f'{name} {value}' for name, value in shape_parameters.items())
                        self.errors.append((
                            'Uncertainties',
                            id_,
                            f"This combination of shape parameter values is not allowed for the {uncertainty_model} uncertainty model: {shape_parameters_str}.",
                        ))
        for entity, ids in undefined_entities.items():
            self.errors.append((
                'Uncertainties',
                ', '.join(ids),
                f"The name {entity} does not refer to any defined entity.",
            ))
        for (entity, attribute), ids in no_time_step_uncertainties.items():
            if len(ids) > 1:
                self.errors.append((
                    'Uncertainties',
                    ', '.join(ids),
                    f"Multiple uncertainties defined on entity {entity}, attribute {attribute}.",
                ))
        for (entity, attribute), ids in all_time_steps_uncertainties.items():
            if len(ids) > 1:
                self.errors.append((
                    'Uncertainties',
                    ', '.join(ids),
                    f"Multiple uncertainties defined on entity {entity}, attribute {attribute} for all timesteps.",
                ))
            time_steps = [
                (other_ids, t)
                for (e, a, t), other_ids
                in one_time_step_uncertainties.items()
                if e == entity and a == attribute
            ]
            if time_steps:
                self.errors.append((
                    'Uncertainties',
                    ', '.join(itertools.chain(ids, *[other_ids for other_ids, _ in time_steps])),
                    f"Uncertainties defined on entity {entity}, attribute {attribute} for both all timesteps and timestep{'s' if len(time_steps) > 1 else ''} {', '.join(str(t) for _, t in time_steps)}.",
                ))
        for (entity, attribute, t), ids in one_time_step_uncertainties.items():
            if len(ids) > 1:
                self.errors.append((
                    'Uncertainties',
                    ', '.join(ids),
                    f"Multiple uncertainties defined on entity {entity}, attribute {attribute} at timestep {t}.",
                ))

    def __unique_id_validation(self, filename: str, id_column: str):
        if filename not in self.reader.files:
            return
        _file = self.reader.files[filename]

        _ids = Counter(item[id_column] for item in _file)

        for _id, count in _ids.items():
            self.all_ids.setdefault(_id, []).append(filename)
            if count > 1:
                self.errors.append((filename,
                                    _id,
                                    f"{id_column} is not unique, found {count} times"))

    def __global_unique_id_validation(self):
        for _id, file_names in self.all_ids.items():
            if len(file_names) > 1:
                self.errors.append(('/'.join(file_names),
                                    _id,
                                    "identifier is not globally unique"))

    def __transports_specific_checks(self):
        transports = self.reader.files.get('Transport', [])
        for transport in transports:
            initial_transported_quantities = transport.get('InitialTransportedQuantities', {})
            initial_transported_values = transport.get('InitialTransportedValues', {})
            key_errors = [
                k
                for k in initial_transported_values
                if k not in initial_transported_quantities
            ]
            for k in key_errors:
                self.errors.append(("Transports",
                                    transport.get('Label'),
                                    f"InitialTransportedValues: key {k} has no quantities associated"))

    def __infinite_stocks_checks(self):
        transports = self.reader.files.get('Transport', [])
        stocks = self.reader.files.get('Stock', [])

        infinite_stocks = [stock for stock in stocks if stock.get('IsInfinite')]
        if not infinite_stocks:
            return

        infinite_stocks_ids = set(stock['id'] for stock in infinite_stocks)

        def check_attribute(stock, attribute, strict=True, timed=False):
            value = stock.get(attribute)
            attribute_errors = []
            if value is not None:
                if timed:
                    for t, v in value.items():
                        if (v > 0 if strict else v >= 0):
                            attribute_errors.append(f"Timestep {t}: {v}")
                else:
                    if (value > 0 if strict else value >= 0):
                        attribute_errors.append(value)
            for error in attribute_errors:
                self.errors.append((
                    "Stock",
                    stock['id'],
                    f"Is infinite and has {'strictly positive ' if strict else ''}{attribute}: {error}"
                ))

        for stock in infinite_stocks:
            check_attribute(stock, 'InitialStock')
            check_attribute(stock, 'InitialValue')
            check_attribute(stock, 'MinimalStock', False)
            check_attribute(stock, 'MaximalStock', False)
            check_attribute(stock, 'MaximizationWeight')
            check_attribute(stock, 'StorageUnitCosts', timed=True)
            check_attribute(stock, 'Demands', timed=True)

        transports_from_infinite_stocks = [transport
                                           for transport in transports
                                           if transport['source'] in infinite_stocks_ids]
        for transport in transports_from_infinite_stocks:
            self.errors.append(("Stock",
                                transport.get('source'),
                                f"Is infinite and has outgoing transport: {transport.get('Label')}"))

    def __obsolescence_check(self):
        empty_obsolete_stocks = self.__get_configuration_parameter('EmptyObsoleteStocks')
        if empty_obsolete_stocks:
            stocks = self.reader.files.get('Stock', [])
            for stock in stocks:
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                has_demands = any(stock_demands.values())
                stock_policy = stock.get('StockPolicy')
                if stock_policy is None:
                    stock_policy = parameters_default_values['Stock']['StockPolicy']
                has_stock_policy = stock_policy != 'None'
                if has_demands and has_stock_policy:
                    self.errors.append(('Configuration',
                                        'EmptyObsoleteStocks',
                                        'The stock obsolescence option is not compatible with stock policies.'))
                    break

    def __sourcing_proportions_check(self):
        sources_by_stock = {}
        sourcing_proportions = {}

        for output in self.reader.files.get('output', []):
            sources_by_stock.setdefault(output['target'], []).append(output['source'])
        for operation in self.reader.files.get('ProductionOperation', []):
            sourcing_proportions[operation['id']] = operation.get('SourcingProportions')
        for transport in self.reader.files.get('Transport', []):
            sources_by_stock.setdefault(transport['target'], []).append(transport['Label'])
            sourcing_proportions[transport['Label']] = transport.get('SourcingProportions')

        e = 1e-2
        for stock, sources in sources_by_stock.items():
            considered_sources = {source for source in sources if sourcing_proportions.get(source) is not None}
            if considered_sources:
                time_steps = sorted(set(
                    t
                    for source in considered_sources
                    for t in sourcing_proportions[source]
                ), key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for source in considered_sources:
                        if time_step in sourcing_proportions[source]:
                            proportions[source] = sourcing_proportions[source][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('ProductionOperationSchedules/TransportSchedules',
                                        'SourcingProportions',
                                        f"The sum of the {stock} sources proportions ({', '.join(sources)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def __dispatch_proportions_check(self):
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

        e = 1e-2
        for stock, operations in operations_by_stock.items():
            considered_operations = {operation for operation in operations if dispatch_proportions[(stock, operation)] is not None}
            retain = retain_proportions.get(stock) is not None
            if considered_operations or retain:
                time_steps = set(
                    t
                    for operation in considered_operations
                    for t in dispatch_proportions[(stock, operation)]
                )
                if retain:
                    time_steps |= set(t for t in retain_proportions[stock])
                time_steps = sorted(time_steps, key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for operation in considered_operations:
                        if time_step in dispatch_proportions[(stock, operation)]:
                            proportions[operation] = dispatch_proportions[(stock, operation)][time_step]
                    if retain and time_step in retain_proportions[stock]:
                        proportions[stock] = retain_proportions[stock][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('inputSchedules',
                                        'DispatchProportions',
                                        f"The sum of the {stock} dispatch proportions to ({', '.join(operations)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def __production_proportions_check(self):
        operations_by_resource = {}
        production_proportions = {}

        for contains in self.reader.files.get('contains', []):
            operations_by_resource.setdefault(contains['source'], []).append(contains['target'])
        for operation in self.reader.files.get('ProductionOperation', []):
            production_proportions[operation['id']] = operation.get('ProductionProportions')

        e = 1e-2
        for resource, operations in operations_by_resource.items():
            considered_operations = {operation for operation in operations if production_proportions.get(operation) is not None}
            if considered_operations:
                time_steps = sorted(set(
                    t
                    for operation in considered_operations
                    for t in production_proportions[operation]
                ), key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for operation in considered_operations:
                        if time_step in production_proportions[operation]:
                            proportions[operation] = production_proportions[operation][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('ProductionOperationSchedules',
                                        'ProductionProportions',
                                        f"The sum of the {resource} operations proportions ({', '.join(operations)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def find_relations_by_id(self, relation_name: str, looked_id: str, relation_column: str):
        if (relation_name, looked_id, relation_column) not in self.lookup_memory:
            self.lookup_memory[(relation_name, looked_id, relation_column)] = [
                row
                for row in self.reader.files.get(relation_name, [])
                if row.get(relation_column) == looked_id
            ]
        return self.lookup_memory[(relation_name, looked_id, relation_column)]

    parent_operations_mem = dict()

    def __find_parent_operations(self, stock_id: str):
        if stock_id in self.parent_operations_mem:
            return self.parent_operations_mem[stock_id]

        _ret = []
        self.parent_operations_mem[stock_id] = _ret
        # transports won't increment the current level
        for _transport in self.find_relations_by_id('Transport', stock_id, 'target'):
            for operation in self.__find_parent_operations(_transport.get('source')):
                _ret.append(operation)

        for _output in self.find_relations_by_id('output', stock_id, 'target'):
            _operation_id = _output.get('source')
            _ret.append(_operation_id)
        return _ret

    def __mandatory_attributes_check(self):
        if not self.reader.files.get('Stock', []):
            self.errors.append(('Stock',
                                'Presence',
                                'There is no stock.'))
        else:
            demand = any(
                len(stock_demands.values())
                for stock in self.reader.files.get('Stock', [])
                for stock_demands in (stock.get('Demands'),)
                if stock_demands
            )
            if not demand:
                self.errors.append(('Stock',
                                    'Demands',
                                    'There is no demand.'))
        # for future warnings:
        """
        for resource in self.reader.files['ProductionResource']:
            if 'OpeningTimes' not in resource:
                self.display_message(f"Production resource {resource['id']} has no opening time.")
        for operation in self.reader.files['ProductionOperation']:
            if 'CycleTimes' not in operation:
                self.display_message(f"Production operation {operation['id']} has no opening time.")
        for transport in self.reader.files['Transport']:
            if 'TransportationLeadTime' not in transport:
                self.display_message(f"Transport {transport['Label']} has no transportation lead time.")
        """
