from Supplychain.Generic.folder_io import FolderReader, FolderWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.simulator_files_description import simulator_format
from Supplychain.Schema.default_values import variables_default_values
from Supplychain.Generic.duration import seconds_to_iso_8061_duration
from datetime import datetime, tzinfo, timedelta
from Supplychain.Wrappers.environment_variables import SECONDS_IN_MINUTE

from collections import defaultdict


class simple_utc(tzinfo):
    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)


def convert_dict(key_type, value_type, dict_item) -> dict:
    if dict_item is None:
        return dict()
    return {
        key_type(k): value_type(v)
        for k, v in sorted(dict_item.items(), key=lambda i: key_type(i[0]))
    }


def convert_nested_dict(key_type, subkey_type, value_type, dict_item) -> dict:
    if dict_item is None:
        return dict()
    return {
        key_type(key): {
            subkey_type(subkey): value_type(value)
            for subkey, value
            in sorted(subdict_item.items(), key=lambda i: subkey_type(i[0]))
        }
        for key, subdict_item
        in sorted(dict_item.items(), key=lambda i: key_type(i[0]))
    }


def find_effective_value_for_time_step(time_step: int, schedule: dict) -> float:
    if time_step in schedule:
        return schedule[time_step]

    effective_time_step = max(int(k) for k in schedule.keys() if int(k) <= time_step)
    return schedule.get(str(effective_time_step), 0.0)


class FromDictToSimulatorConverter(Timer):
    def __init__(self, reader: FolderReader, writer: FolderWriter):
        Timer.__init__(self, prefix="[Convert]")

        self.reader = reader
        self.writer = writer

        self.configuration = self.reader.files.get("Configuration", [])[0]

        self.total_time_steps = (
            self.configuration["StepsPerCycle"] * self.configuration["SimulatedCycles"]
        )

        self.tags = {}
        for link in self.reader.files.get("TagGroups", []):
            self.tags.setdefault(link["source"], []).append(link["target"])

        self.files_content = dict()

        self.current_group = 0

        for key in simulator_format.keys():
            self.files_content[key] = list()

        self.entity_order = dict()

        self.lead_times = {}
        self.min_lead_times = {}

    def __scheduler(self):
        inputs = self.reader.files.get("input", [])
        outputs = self.reader.files.get("output", [])
        contains = self.reader.files.get("contains", [])
        transports = self.reader.files.get("Transport", [])

        operations_names = set(i["target"] for i in inputs)
        transports_names = set(
            t["Label"] for t in transports
        )  # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector

        _input_stocks = set(i["source"] for i in inputs) | set(
            t["source"] for t in transports
        )
        _output_stocks = set(o["target"] for o in outputs) | set(
            t["target"] for t in transports
        )

        start_stocks = _input_stocks - _output_stocks
        final_stocks = _output_stocks - _input_stocks

        self.writer.write_from_list(
            [
                {"Type": "Rule", "Name": stock, "TaskName": "Dispatch"}
                for stock in sorted(start_stocks)
            ],
            "IndustrialNetworkScheduler",
        )

        for st in final_stocks:
            self.entity_order[st] = 0

        parents = defaultdict(set)

        # While we have stocks to treat we continue
        for links in [inputs, outputs]:
            for link in links:
                parents[link["source"]].add(link["target"])
        for tr in transports:
            parents[tr["source"]].add(tr["Label"])
            parents[tr["Label"]].add(tr["target"])

        max_depth = 0

        def get_entity_order(_entity):
            if _entity not in self.entity_order:
                self.entity_order[_entity] = 1 + max(
                    map(get_entity_order, parents[_entity])
                )
            return self.entity_order[_entity]

        for entity in parents.keys():
            o = get_entity_order(entity)
            max_depth = max(max_depth, o)

        operation_order = [[] for _ in range(max_depth)]
        for k, v in self.entity_order.items():
            if k in transports_names or k in operations_names:
                operation_order[v].append(k)

        operation_order.reverse()
        operation_order = [set(i) for i in operation_order if len(i) > 0]

        output_stocks = {
            o["source"]: o["target"]
            for o in outputs
        } | {
            t["Label"]: t["target"]
            for t in transports
        }

        containing_machines = {
            c["target"]: c["source"]
            for c in contains
        }

        input_stocks = defaultdict(list)
        for i in inputs:
            input_stocks[i["target"]].append(i["source"])

        scheduled_machines = set()

        for all_operations in operation_order:
            # For each rank of operation, every operation can be done in parallel, so order is not important

            # To schedule we need some entities and information about them:

            operations = all_operations & operations_names
            # Production operations entities considered at this rank.

            machines = {containing_machines[operation] for operation in operations}
            machines -= scheduled_machines
            # Machine entities containing the non transport Operation entities
            # considered at this rank.

            operation_ee = {
                f"{stock}_to_{operation}"
                for operation in operations
                for stock in input_stocks[operation]
            }
            # StockToOperation edge entities for the non transport Operation
            # entities considered at this rank.

            transport_ops = all_operations - operations
            # Operation entities considered at this rank which are transports.

            end_stocks = {output_stocks[operation] for operation in all_operations}
            # Stock entities outputed by the Operation entities considered at
            # this rank.

            # Names must be sorted to stabilize the output schedule.
            operations = sorted(operations)
            machines = sorted(machines)
            operation_ee = sorted(operation_ee)
            transport_ops = sorted(transport_ops)
            end_stocks = sorted(end_stocks)

            # Now we can create our scheduled Processes / Rules
            scheduled_elements = []

            # As soon as a ComputeStockToTransfer process is scheduled for a
            # particular stock, all ComputeStockToTransfer processes for the
            # said stock should be scheduled at the same time. Moreover, they
            # should be scheduled only once.
            for mac in machines:
                scheduled_element = dict(Type="Rule", Name=mac, TaskName="SelectStock")
                scheduled_elements.append(scheduled_element)
                scheduled_machines.add(mac)

            for operation in operations:
                scheduled_element = dict(
                    Type="Rule", Name=operation, TaskName="Process"
                )
                scheduled_elements.append(scheduled_element)

            for EE in operation_ee:
                scheduled_element = dict(
                    Type="Process", Name=EE, TaskName="SendBackStockIfNecessary"
                )
                scheduled_elements.append(scheduled_element)

            for transport in transport_ops:
                scheduled_element = dict(
                    Type="Rule", Name=transport, TaskName="SelectStock"
                )
                scheduled_elements.append(scheduled_element)

            for transport in transport_ops:
                scheduled_element = dict(
                    Type="Rule", Name=transport, TaskName="Process"
                )
                scheduled_elements.append(scheduled_element)

            for stock in end_stocks:
                scheduled_element = dict(
                    Type="Rule", Name=stock, TaskName="ReceiveStock"
                )
                scheduled_elements.append(scheduled_element)

            for stock in end_stocks:
                scheduled_element = dict(Type="Rule", Name=stock, TaskName="Dispatch")
                scheduled_elements.append(scheduled_element)

            self.writer.write_from_list(
                scheduled_elements,
                "IndustrialNetworkScheduler",
                mode="a",
            )
        self.writer.write_from_list(
            [{"Type": "Process", "Name": "IndustrialNetwork", "TaskName": "MesoResolveDemands"}],
            "IndustrialNetworkScheduler",
            mode="a",
        )
        self.writer.write_from_list(
            [
                {"Type": "Rule", "Name": stock, "TaskName": "CheckLevelAndOrderIfNecessary"}
                for stock in sorted(sorted(_output_stocks), key=lambda e: self.entity_order[e])
            ],
            "IndustrialNetworkScheduler",
            mode="a",
        )

    def __lead_times(self):
        inputs = self.reader.files.get("input", [])
        operations = self.reader.files.get("ProductionOperation", [])
        outputs = self.reader.files.get("output", [])
        stocks = self.reader.files.get("Stock", [])
        transports = self.reader.files.get("Transport", [])

        stock_names = set(stock["id"] for stock in stocks)

        non_input_stock_names = (
            stock_names
            - set(i["source"] for i in inputs)
            - set(transport["source"] for transport in transports)
        )
        non_output_stock_names = (
            stock_names
            - set(output["target"] for output in outputs)
            - set(transport["target"] for transport in transports)
        )

        parents = defaultdict(set)
        for links in [inputs, outputs]:
            for link in links:
                parents[link["target"]].add(link["source"])
        for transport in transports:
            parents[transport["Label"]].add(transport["source"])
            parents[transport["target"]].add(transport["Label"])

        durations = (
            {stock["id"]: 0 for stock in stocks}
            | {operation["id"]: operation["Duration"] for operation in operations}
            | {transport["Label"]: transport["TransportationLeadTime"] for transport in transports}
        )

        for stock_name in non_output_stock_names:
            self.lead_times[stock_name] = 0
            self.min_lead_times[stock_name] = 0

        def get_lead_time(entity):
            if entity not in self.lead_times:
                self.lead_times[entity] = (
                    max(get_lead_time(parent) for parent in parents[entity])
                    + durations[entity]
                )
            return self.lead_times[entity]

        def get_min_lead_time(entity):
            if entity not in self.min_lead_times:
                self.min_lead_times[entity] = (
                    (min if entity in stock_names else max)(
                        get_min_lead_time(parent) for parent in parents[entity]
                    )
                    + durations[entity]
                )
            return self.min_lead_times[entity]

        for stock_name in non_input_stock_names:
            get_lead_time(stock_name)
            get_min_lead_time(stock_name)

    def __operation(self):

        operations_csv = self.reader.files.get("ProductionOperation", [])
        contains_csv = self.reader.files.get("contains", [])
        outputs = self.reader.files.get("output", [])
        stock_csv = self.reader.files.get("Stock", [])

        for operation in operations_csv:
            parent_resource = next(
                c["source"] for c in contains_csv if c["target"] == operation["id"]
            )
            output_stock = next(
                link["target"] for link in outputs if link["source"] == operation["id"]
            )
            follows_stock_policy = next(
                stock["StockPolicy"] != "None"
                for stock in stock_csv
                if stock["id"] == output_stock
            )
            operation_item = {
                "Name": operation["id"],
                "ParentName": parent_resource,
                "OperatingPerformanceSchedule": convert_dict(
                    int, float, operation["OperatingPerformances"]
                ),
                "CycleTimeSchedule": convert_dict(int, float, operation["CycleTimes"]),
                "RejectRateSchedule": convert_dict(
                    int, float, operation["RejectRates"]
                ),
                "ProductionUnitCostSchedule": convert_dict(
                    int, float, operation["ProductionUnitCosts"]
                ),
                "CO2UnitEmissionsSchedule": convert_dict(
                    int, float, operation["CO2UnitEmissions"]
                ),
                "ProductionPlanSchedule": convert_dict(
                    int, float, operation["QuantitiesToProduce"]
                ),
                "MinimumOrderQuantitySchedule": convert_dict(
                    int, float, operation["MinimumOrderQuantities"]
                ),
                "MultipleOrderQuantitySchedule": convert_dict(
                    int, float, operation["MultipleOrderQuantities"]
                ),
                "SourcingProportionSchedule": convert_dict(
                    int, float, operation["SourcingProportions"]
                ),
                "ProductionProportionSchedule": convert_dict(
                    int, float, operation["ProductionProportions"]
                ),
                "InvestmentCost": operation["InvestmentCost"],
                "IsContractor": operation["IsContractor"],
                "Priority": operation["Priority"],
                "SchedulingStep": self.entity_order.get(operation["id"], -1),
                "FollowsStockPolicy": follows_stock_policy,
                "Duration": operation["Duration"],
                "LeadTime": self.lead_times[operation["id"]],
                "MinimalLeadTime": self.min_lead_times[operation["id"]],
            }
            self.files_content["BE_Operation"].append(operation_item)
        self.writer.write_from_list(
            self.files_content["BE_Operation"], "BE_Operation", ordering_key="Name"
        )

    def __model_parameters(self):

        production_plan_is_available = all(
            bool(po["QuantitiesToProduce"])
            for po in self.reader.files.get("ProductionOperation", [])
        )

        subdatasets = set()
        for file_name in (
            "contains",
            "input",
            "output",
            "ProductionOperation",
            "ProductionResource",
            "Stock",
            "Transport",
        ):
            subdatasets |= set(
                record["subdataset"]
                for record in self.reader.files.get(file_name, [])
            )

        model_parameters = {
            "TimeStepDuration": seconds_to_iso_8061_duration(
                self.configuration["TimeStepDuration"] * SECONDS_IN_MINUTE
            ),
            "TimeStepPerCycle": self.configuration["StepsPerCycle"],
            "NumberOfCycle": self.configuration["SimulatedCycles"],
            "StartingDate": datetime.fromisoformat(self.configuration["StartingDate"])
            .replace(tzinfo=simple_utc())
            .isoformat(),
            "ManageBacklogQuantities": self.configuration["ManageBacklogQuantities"],
            "OptimizationObjective": self.configuration["OptimizationObjective"],
            "ActivateUncertainties": any(self.configuration["ActivateUncertainties"]),
            "EmptyObsoleteStocks": self.configuration["EmptyObsoleteStocks"],
            "ActivateVariableMachineOpeningRate": self.configuration[
                "ActivateVariableMachineOpeningRate"
            ],
            "ImmobilizedCashRelativeCost": self.configuration["InventoryCapitalCost"],
            "CarbonTax": self.configuration["CarbonTax"],
            "BatchSize": self.configuration["BatchSize"],
            "ExtraProductionPlanIsAvailable": production_plan_is_available,
            "EnforceProductionPlan": self.configuration["EnforceProductionPlan"],
            "FiniteProductionCapacity": self.configuration["FiniteProductionCapacity"],
            "AllowPartRetention": self.configuration["IntermediaryStockDispatchPolicy"]
            == "AllowRetention",
            "ActualizeShipments": self.configuration["ActualizeShipments"],
            "ServeDemandBeforeBacklog": self.configuration["ServeDemandBeforeBacklog"],
            "SelectedTimeStep": self.configuration["SelectedTimeStep"],
            "InventoryQuantityForCostComputation": self.configuration["InventoryQuantityForCostComputation"],
            "SubDataset": subdatasets.pop() if len(subdatasets) == 1 else "",
            "UseDemandsAsSalesForecasts": self.configuration["UseDemandsAsSalesForecasts"],
        }

        self.files_content["ModelParameters"].append(model_parameters)
        self.writer.write_from_list(
            self.files_content["ModelParameters"], "ModelParameters", ordering_key=None
        )

    def __stock(self):
        stock_csv = self.reader.files.get("Stock", [])
        for stock in stock_csv:
            maximal_stock = stock["MaximalStock"]
            stock_item = {
                "Name": stock["id"],
                "CurrentStock": stock["InitialStock"],
                "MinimalStock": stock["MinimalStock"],
                "MaximalStock": maximal_stock if maximal_stock is not None else -1,
                "Value": stock["InitialValue"],
                "PurchasingUnitCostSchedule": convert_dict(
                    int, float, stock["PurchasingUnitCosts"]
                ),
                "VariablePurchasingUnitCostSchedule": convert_nested_dict(
                    int, int, float, stock["VariablePurchasingUnitCosts"]
                ),
                "CO2UnitEmissionsSchedule": convert_dict(
                    int, float, stock["CO2UnitEmissions"]
                ),
                "UnitIncomeSchedule": convert_dict(int, float, stock["UnitIncomes"]),
                "Demand": dict(),
                "StorageUnitCostSchedule": convert_dict(
                    int, float, stock["StorageUnitCosts"]
                ),
                "IsInfinite": stock["IsInfinite"],
                "StockPolicy": stock["StockPolicy"],
                "SourcingPolicy": stock["SourcingPolicy"],
                "DispatchPolicy": stock["DispatchPolicy"],
                "ReviewPeriod": stock["ReviewPeriod"],
                "FirstReview": stock["FirstReview"],
                "Advance": stock["Advance"],
                "LeadTime": self.lead_times[stock["id"]],
                "SalesForecasts": convert_dict(int, float, stock["SalesForecasts"]),
                "OrderPointSchedule": convert_dict(int, float, stock["OrderPoints"]),
                "OrderQuantitySchedule": dict(),
                "SafetyQuantitySchedule": convert_dict(
                    int, float, stock["SafetyQuantities"]
                ),
                "CoverageHorizon": stock["CoverageHorizon"],
                "CoverageOffset": stock["CoverageOffset"],
                "CoverageRate": stock["CoverageRate"],
                "SchedulingStep": self.entity_order.get(stock["id"], -1),
                "IgnoreDownstreamRequiredQuantities": stock["IgnoreDownstreamRequiredQuantities"],
                "SourcingLimit": stock["SourcingLimit"],
                "Selected": self.configuration["SelectedTag"] in self.tags.get(stock["id"], []),
                "Backlogs": [],
                "OrderForEndOfTimeStep": stock["OrderForEndOfTimeStep"],
                "RetainProportionSchedule": convert_dict(int, float, stock["RetainProportions"]),
            }

            if stock_item["StockPolicy"] == "OrderPointFixedQuantity":
                stock_item["OrderQuantitySchedule"] = convert_dict(
                    int, float, stock["OrderQuantities"]
                )
            elif stock_item["StockPolicy"] == "OrderPointVariableQuantity":
                stock_item["OrderQuantitySchedule"] = convert_dict(
                    int, float, stock["OrderUpToLevels"]
                )

            backlog_weight = stock["BacklogWeight"]
            if stock["InitialBacklog"]:
                stock_item["Backlogs"].append({
                    "MissingProduction": stock["InitialBacklog"],
                    "OriginalDemand": stock["InitialBacklog"],
                    "Weight": stock["BacklogWeight"],
                })

            if stock["Demands"]:
                demands = convert_dict(int, float, stock["Demands"])
                demands_weight = convert_dict(int, float, stock["DemandWeights"])

                last_weight = 0

                for time_step in range(self.total_time_steps + 1):
                    if time_step in demands_weight:
                        last_weight = demands_weight[time_step]
                    if time_step in demands and demands[time_step]:
                        current_demand = dict(
                            ExternalDemand=demands[time_step],
                            InternalDemand=0.0,
                            BacklogWeight=backlog_weight,
                            ExternalWeight=last_weight,
                            InternalWeight=0.0,
                            WeightMax=0.0,
                            MaxVal=0.0,
                        )
                        stock_item["Demand"][time_step] = current_demand

            maximization_weight = stock["MaximizationWeight"]
            if maximization_weight:
                total_max_production = 0
                for time_step in range(self.total_time_steps):
                    total_max_production += self.compute_theoretical_maximum_production(
                        stock["id"], time_step
                    )
                if self.total_time_steps - 1 not in stock_item["Demand"]:
                    current_demand = dict(
                        ExternalDemand=0.0,
                        InternalDemand=0.0,
                        BacklogWeight=backlog_weight,
                        ExternalWeight=0.0,
                        InternalWeight=0.0,
                        WeightMax=0.0,
                        MaxVal=0.0,
                    )
                    stock_item["Demand"][self.total_time_steps - 1] = current_demand
                stock_item["Demand"][self.total_time_steps - 1][
                    "WeightMax"
                ] = maximization_weight
                stock_item["Demand"][self.total_time_steps - 1][
                    "MaxVal"
                ] = total_max_production

            self.files_content["BE_Stock"].append(stock_item)
        self.writer.write_from_list(
            self.files_content["BE_Stock"], "BE_Stock", ordering_key="Name"
        )

    def compute_theoretical_maximum_production(
        self, stock_id: str, time_step: int
    ) -> float:
        stock = next(
            s for s in self.reader.files.get("Stock", []) if s["id"] == stock_id
        )
        theoretical_maximum = stock["InitialStock"] if time_step == 0 else 0.0
        transports = [
            transport
            for transport in self.reader.files.get("Transport", [])
            if transport["target"] == stock_id
        ]
        for transport in transports:
            origin = transport["source"]
            duration = transport["TransportationLeadTime"]
            theoretical_maximum += transport["InitialTransportedQuantities"].get(
                str(time_step), 0.0
            )
            if time_step >= duration:
                theoretical_maximum += self.compute_theoretical_maximum_production(
                    origin, time_step - duration
                )
        operation_names = set(
            output["source"]
            for output in self.reader.files.get("output", [])
            if output["target"] == stock_id
        )
        operations = [
            operation
            for operation in self.reader.files.get("ProductionOperation", [])
            if operation["id"] in operation_names
        ]
        for operation in operations:
            if operation["IsContractor"]:
                theoretical_maximum += find_effective_value_for_time_step(
                    time_step, operation["QuantitiesToProduce"]
                )
            else:
                pr_name = next(
                    contains["source"]
                    for contains in self.reader.files.get("contains", [])
                    if contains["target"] == operation["id"]
                )
                pr_data = next(
                    pr
                    for pr in self.reader.files.get("ProductionResource", [])
                    if pr["id"] == pr_name
                )
                max_opening_time = find_effective_value_for_time_step(
                    time_step, pr_data["OpeningTimes"]
                )
                ct = (
                    find_effective_value_for_time_step(
                        time_step, operation["CycleTimes"]
                    )
                    if operation["CycleTimes"]
                    else variables_default_values["ProductionOperation"]["CycleTimes"]
                )
                rr = (
                    find_effective_value_for_time_step(
                        time_step, operation["RejectRates"]
                    )
                    if operation["RejectRates"]
                    else variables_default_values["ProductionOperation"]["RejectRates"]
                )
                op = (
                    find_effective_value_for_time_step(
                        time_step, operation["OperatingPerformances"]
                    )
                    if operation["OperatingPerformances"]
                    else variables_default_values["ProductionOperation"][
                        "OperatingPerformances"
                    ]
                )
                theoretical_maximum += (max_opening_time / ct) * op * (1.0 - rr)
        return theoretical_maximum

    def __machine(self):
        pr_csv = self.reader.files.get("ProductionResource", [])
        contains_csv = self.reader.files.get("contains", [])
        output_csv = self.reader.files.get("output", [])
        stock_csv = self.reader.files.get("Stock", [])

        for pr in pr_csv:
            target_operations = [
                c["target"] for c in contains_csv if c["source"] == pr["id"]
            ]
            operations_count = len(target_operations)

            group = {}
            if operations_count > 1:
                group = {
                    self.current_group: {
                        "StartCycle": 0,
                        "EndCycle": self.configuration["SimulatedCycles"] - 1,
                    }
                }
                self.current_group += 1

            output_stocks = [
                o["target"] for o in output_csv if o["source"] in target_operations
            ]

            future_range = 1 + max(
                self.lead_times[stock["id"]] + stock["Advance"]
                for stock in stock_csv
                if stock["id"] in output_stocks
            )

            pr_item = {
                "Name": pr["id"],
                "Groups": group,
                "OpeningRateSchedule": convert_dict(int, float, pr["OpeningRates"]),
                "OpeningTimeSchedule": convert_dict(int, float, pr["OpeningTimes"]),
                "ProductionCostSchedule": convert_dict(
                    int, float, pr["FixedProductionCosts"]
                ),
                "ProductionPolicy": pr["ProductionPolicy"],
                "FutureRange": future_range,
            }
            self.files_content["CE_Machine"].append(pr_item)
        self.writer.write_from_list(
            self.files_content["CE_Machine"], "CE_Machine", ordering_key="Name"
        )

    def __op_to_stock(self):
        output_csv = self.reader.files.get("output", [])
        for o in output_csv:
            op_to_stock_item = {"StockName": o["target"], "OperationName": o["source"]}
            self.files_content["Arcs_OperationToStock"].append(op_to_stock_item)
        output_csv = self.reader.files.get("Transport", [])
        for o in output_csv:
            op_to_stock_item = {"StockName": o["target"], "OperationName": o["Label"]}
            self.files_content["Arcs_OperationToStock"].append(op_to_stock_item)
        self.writer.write_from_list(
            self.files_content["Arcs_OperationToStock"],
            "Arcs_OperationToStock",
            ordering_key="StockName",
        )

    def __transport(self):
        transport_csv = self.reader.files.get("Transport", [])
        stock_csv = self.reader.files.get("Stock", [])

        follows_stock_policy = {
            stock["id"]: stock["StockPolicy"] != "None"
            for stock in stock_csv
        }

        for transport in transport_csv:
            transport_item = {
                "Name": transport["Label"],
                # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                "Duration": transport["TransportationLeadTime"],
                "Shipments": {},
                "TransportUnitCostSchedule": convert_dict(
                    int, float, transport["TransportUnitCosts"]
                ),
                "DutyUnitCostSchedule": convert_dict(
                    int, float, transport["DutyUnitCosts"]
                ),
                "CO2UnitEmissionsSchedule": convert_dict(
                    int, float, transport["CO2UnitEmissions"]
                ),
                "ActualDurationSchedule": convert_dict(
                    int, int, transport["ActualTransportationLeadTimes"]
                ),
                "MinimumOrderQuantitySchedule": convert_dict(
                    int, float, transport["MinimumOrderQuantities"]
                ),
                "MultipleOrderQuantitySchedule": convert_dict(
                    int, float, transport["MultipleOrderQuantities"]
                ),
                "SourcingProportionSchedule": convert_dict(
                    int, float, transport["SourcingProportions"]
                ),
                "Priority": transport["Priority"],
                "SchedulingStep": self.entity_order.get(transport["Label"], -1),
                "FollowsStockPolicy": follows_stock_policy[transport["target"]],
                "LeadTime": self.lead_times[transport["Label"]],
                "MinimalLeadTime": self.min_lead_times[transport["Label"]],
            }
            initial_quantities = convert_dict(
                int, float, transport["InitialTransportedQuantities"]
            )
            initial_values = convert_dict(
                int, float, transport["InitialTransportedValues"]
            )
            co2_unit_emissions = transport_item["CO2UnitEmissionsSchedule"].get(
                0, variables_default_values["Transport"]["CO2UnitEmissions"]
            )
            default_value = variables_default_values["Transport"][
                "InitialTransportedValues"
            ]
            time_steps = reversed(
                [
                    (-i, t)
                    for i, t in enumerate(
                        sorted(
                            (t for t, q in initial_quantities.items() if 0.0 < q),
                            reverse=True,
                        ),
                        1,
                    )
                ]
            )
            for departure, arrival in time_steps:
                quantity = initial_quantities[arrival]
                transport_item["Shipments"][departure] = {
                    "Arrival": arrival,
                    "ActualArrival": arrival,
                    "Quantity": quantity,
                    "Value": initial_values.get(arrival, default_value),
                    "CO2Emissions": quantity * co2_unit_emissions,
                }
            self.files_content["BE_TransportOperation"].append(transport_item)

        self.writer.write_from_list(
            self.files_content["BE_TransportOperation"],
            "BE_TransportOperation",
            ordering_key="Name",
        )

    def __stock_to_operation(self):
        input_csv = self.reader.files.get("input", [])
        transport_csv = self.reader.files.get("Transport", [])
        stock_csv = self.reader.files.get("Stock", [])

        number_of_edges_by_stock = defaultdict(int)

        for i in input_csv:
            number_of_edges_by_stock[i["source"]] += 1

        for t in transport_csv:
            number_of_edges_by_stock[t["source"]] += 1

        groups = dict()

        stock_has_demand = {
            s["id"]: bool(s["Demands"])  # DS
            for s in stock_csv
        }

        for stock in sorted(number_of_edges_by_stock.keys()):
            groups[stock] = {}
            if number_of_edges_by_stock[stock] > 1 or stock_has_demand[stock]:
                groups[stock] = {
                    self.current_group: {
                        "StartCycle": 0,
                        "EndCycle": self.configuration["SimulatedCycles"] - 1,
                    }
                }
                self.current_group += 1

        for i in input_csv:
            sto_item = {
                "Name": i["source"] + "_to_" + i["target"],
                "OperationName": i["target"],
                "StockName": i["source"],
                "DispatchProportionSchedule": convert_dict(int, float, i["DispatchProportions"]),
                "Groups": groups[i["source"]],
                "Cardinality": i["InputQuantity"],
            }
            self.files_content["EE_StockToOperation"].append(sto_item)

        for i in transport_csv:
            sto_item = {
                "Name": i["source"] + "_to_" + i["Label"],
                "OperationName": i["Label"],
                # TODO to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                "StockName": i["source"],
                "DispatchProportionSchedule": convert_dict(int, float, i["DispatchProportions"]),
                "Groups": groups[i["source"]],
                "Cardinality": 1,
            }
            self.files_content["EE_StockToOperation"].append(sto_item)

        self.writer.write_from_list(
            self.files_content["EE_StockToOperation"],
            "EE_StockToOperation",
            ordering_key="Name",
        )

    def transform(self):
        self.__scheduler()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - IndustrialNetworkScheduler"
        )
        self.__lead_times()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Lead times"
        )
        self.__stock()
        self.split("{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_Stock")
        self.__operation()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_Operation"
        )
        self.__transport()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - BE_TransportOperation"
        )
        self.__machine()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - CE_Machine"
        )
        self.__op_to_stock()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - Arcs_OperationToStock"
        )
        self.__stock_to_operation()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - EE_StockToOperation"
        )
        self.__model_parameters()
        self.split(
            "{time_since_last_split:6.4f} ({time_since_start:6.4f}) - ModelParameters"
        )
