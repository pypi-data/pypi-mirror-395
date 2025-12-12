from comets import DistributionRegistry

from Supplychain.Schema.modifications import changes, variables


class ValidationSchemas:
    schemas = {
        "Configuration": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "StartingDate": {"type": "string", "format": "date"},
                "SimulatedCycles": {"type": "integer", "minimum": 1},
                "StepsPerCycle": {"type": "integer", "minimum": 1},
                "TimeStepDuration": {"type": "integer", "minimum": 1},
                "ManageBacklogQuantities": {"type": "boolean"},
                "OptimizationObjective": {
                    "type": "string",
                    "enum": ["ServiceLevelMaximization", "ProfitMaximization"],
                },
                "ActivateUncertainties": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": variables,
                    },
                    "uniqueItems": True,
                },
                "InventoryCapitalCost": {"type": "number", "minimum": 0, "maximum": 1},
                "CarbonTax": {"type": "number", "minimum": 0},
                "BatchSize": {"type": "integer", "minimum": 0},
                "EmptyObsoleteStocks": {"type": "boolean"},
                "ActivateVariableMachineOpeningRate": {"type": "boolean"},
                "EnforceProductionPlan": {"type": "boolean"},
                "FiniteProductionCapacity": {"type": "boolean"},
                "IntermediaryStockDispatchPolicy": {
                    "type": "string",
                    "enum": ["DispatchAll", "AllowRetention"],
                },
                "ActualizeShipments": {"type": "boolean"},
                "ServeDemandBeforeBacklog": {"type": "boolean"},
                "SelectedTimeStep": {"type": "integer", "minimum": 0},
                "SelectedTag": {"type": "string"},
                "InventoryQuantityForCostComputation": {
                    "type": "string",
                    "enum": ["Lowest", "Average", "Highest"],
                },
                "DemandCorrelations": {"type": "number", "minimum": 0, "maximum": 1},
                "Kpi": {
                    "type": "string",
                    "enum": [
                        "Profit",
                        "OPEX",
                        "AverageStockValue",
                        "ServiceLevelIndicator",
                        "TotalFillRateServiceLevel",
                        "CO2Emissions",
                        "TotalServedQuantity",
                        "IndividualTotalFillRateServiceLevel",
                    ],
                },
                "OptimizationMode": {
                    "type": "string",
                    "enum": [
                        "maximize",
                        "minimize",
                        "target",
                    ],
                },
                "Statistic": {
                    "type": "string",
                    "enum": [
                        "mean",
                        "std",
                        "sem",
                        "quantile 5%",
                        "quantile 10%",
                        "quantile 15%",
                        "quantile 20%",
                        "quantile 25%",
                        "quantile 30%",
                        "quantile 35%",
                        "quantile 40%",
                        "quantile 45%",
                        "quantile 50%",
                        "quantile 55%",
                        "quantile 60%",
                        "quantile 65%",
                        "quantile 70%",
                        "quantile 75%",
                        "quantile 80%",
                        "quantile 85%",
                        "quantile 90%",
                        "quantile 95%",
                    ],
                },
                "TargetedValue": {"type": "number"},
                "DecisionVariable": {
                    "type": "string",
                    "enum": [
                        "FromDataset",
                        "ReviewPeriod",
                        "FirstReview",
                        "Advance",
                        "OrderPoints",
                        "OrderQuantities",
                        "OrderUpToLevels",
                        "SafetyQuantities",
                        "InitialStock",
                        "StorageUnitCosts",
                        "PurchasingUnitCosts",
                        "UnitIncomes",
                        "OpeningTimes",
                        "FixedProductionCosts",
                        "ProductionProportions",
                        "QuantitiesToProduce",
                        "OperatingPerformances",
                        "CycleTimes",
                        "RejectRates",
                        "ProductionUnitCosts",
                        "InvestmentCost",
                        "DutyUnitCosts",
                        "TransportUnitCosts",
                        "MinimumOrderQuantities",
                        "MultipleOrderQuantities",
                        "SourcingProportions",
                        "Priority",
                        "Duration",
                        "CO2UnitEmissions",
                    ],
                },
                "DecisionVariableMin": {"type": "number", "minimum": 0},
                "DecisionVariableMax": {"type": "number", "minimum": 0},
                "OptimizationMaximalDuration": {"type": "number"},
                "OptimizationAlgorithm": {"type": "string"},
                "PopulationBatchSize": {"type": "integer", "minimum": 1},
                "SampleSizeUncertaintyAnalysis": {"type": "integer"},
                "FinalSampleSizeUncertaintyAnalysis": {"type": "integer"},
                "MaxIterationsForOptim": {"type": "integer"},
                "AutomaticParallelizationConfig": {"type": "boolean"},
                "MaxNumberOfSimInParallel": {"type": "integer", "not": {"type": "integer", "minimum": 0, "maximum": 0}},
                "ConstraintHandling": {
                    "type": "string",
                    "enum": [
                        "None",
                        "simple_penalization",
                        "relative_penalization",
                        "automated",
                    ],
                },
                "OptimizationParallelization": {"type": "integer", "not": {"type": "integer", "minimum": 0, "maximum": 0}},
                "UncertaintyAnalysisParallelization": {"type": "integer", "not": {"type": "integer", "minimum": 0, "maximum": 0}},
                "UncertaintyAnalysisSeedForOptimization": {"type": "integer", "minimum": -1},
                "UncertaintyAnalysisSeed": {"type": "integer", "minimum": -1},
                "OptimizationSeed": {"type": "integer", "minimum": -1},
                "UncertaintyAnalysisOutputData": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Transports",
                            "Stocks",
                            "StocksAtEndOfSimulation",
                            "Performances",
                            "PerformanceAMQP",
                        ],
                    },
                    "uniqueItems": True,
                },
                "UseDemandsAsSalesForecasts": {"type": "boolean"},
            },
        },
        "contains": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "subdataset": {"type": "string"},
            },
        },
        "input": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "InputQuantity": {"type": "number", "exclusiveMinimum": 0},
                "subdataset": {"type": "string"},
                "DispatchProportions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
            },
        },
        "output": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "subdataset": {"type": "string"},
            },
        },
        "OptimizationConstraints": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "ConstrainedKpi": {
                    "type": "string",
                    "enum": [
                        "Profit",
                        "OPEX",
                        "AverageStockValue",
                        "ServiceLevelIndicator",
                        "TotalFillRateServiceLevel",
                        "CO2Emissions",
                        "TotalServedQuantity",
                        "IndividualTotalFillRateServiceLevel",
                        "OnTimeFillRateServiceLevel",
                        "CoverageRateForSelection",
                    ],
                },
                "Statistic": {
                    "type": "string",
                    "enum": [
                        "mean",
                        "std",
                        "sem",
                        "quantile 5%",
                        "quantile 10%",
                        "quantile 15%",
                        "quantile 20%",
                        "quantile 25%",
                        "quantile 30%",
                        "quantile 35%",
                        "quantile 40%",
                        "quantile 45%",
                        "quantile 50%",
                        "quantile 55%",
                        "quantile 60%",
                        "quantile 65%",
                        "quantile 70%",
                        "quantile 75%",
                        "quantile 80%",
                        "quantile 85%",
                        "quantile 90%",
                        "quantile 95%",
                    ],
                },
                "ConstraintType": {
                    "type": "string",
                    "enum": [
                        "greater_than",
                        "less_than",
                        "equal_to",
                    ],
                },
                "ConstraintValue": {"type": "number"},
                "PenaltyCoefficient": {"type": "number"},
            },
        },
        "OptimizationDecisionVariables": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "SelectedEntity": {"type": "string"},
                "SelectedTag": {"type": "string"},
                "Attribute": {"type": "string"},
                "AttributeMinimumValue": {"type": "number"},
                "AttributeMaximumValue": {"type": "number"},
            },
        },
        "OptDecisionVariableGroups": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "GroupTag": {"type": "string"},
                "Attribute": {"type": "string"},
                "GroupBehaviorMode": {
                    "type": "string",
                    "enum": [
                        "MultiplyOriginalValue",
                        "SetNewValue",
                    ],
                },
                "DecisionVariableMinimum": {"type": "number"},
                "DecisionVariableMaximum": {"type": "number"},
                "DecisionVariableStartingPoint": {"type": "number"},
            },
        },
        "ProductionOperation": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "QuantitiesToProduce": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "OperatingPerformances": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "CycleTimes": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "exclusiveMinimum": 0}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "RejectRates": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "ProductionUnitCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "CO2UnitEmissions": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "MinimumOrderQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "MultipleOrderQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "SourcingProportions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "ProductionProportions": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "IsContractor": {"type": "boolean"},
                "InvestmentCost": {
                    "type": "number",
                    "minimum": 0,
                },
                "Priority": {"type": "integer", "minimum": 0},
                "Duration": {"type": "integer", "minimum": 0},
                "subdataset": {"type": "string"},
            },
            "required": ["CycleTimes"],
        },
        "ProductionResource": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "ProductionPolicy": {
                    "type": "string",
                    "enum": [
                        "Equidistribution",
                        "GreatestWorkload",
                        "SmallestWorkload",
                        "HighestPriority",
                        "ProductionProportions",
                    ],
                },
                "OpeningTimes": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "OpeningRates": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "FixedProductionCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "Latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "Longitude": {"type": "number", "minimum": -180, "maximum": 180},
                "subdataset": {"type": "string"},
            },
            "required": ["OpeningTimes"],
        },
        "Stock": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "StorageCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "IsInfinite": {"type": "boolean"},
                "MinimalStock": {
                    "type": "number",
                    "if": {"maximum": -1},
                    "then": {"minimum": -1},
                    "else": {"minimum": 0},
                },
                "MaximalStock": {
                    "type": "number",
                    "if": {"maximum": -1},
                    "then": {"minimum": -1},
                    "else": {"minimum": 0},
                },
                "InitialStock": {"type": "number", "minimum": 0},
                "InitialValue": {"type": "number", "minimum": 0},
                "PurchasingUnitCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "VariablePurchasingUnitCosts": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "object", "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}}}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "CO2UnitEmissions": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "UnitIncomes": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "Demands": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                },
                "DemandWeights": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                },
                "BacklogWeight": {"type": "number", "minimum": 0},
                "InitialBacklog": {"type": "number", "minimum": 0},
                "MaximizationWeight": {"type": "number", "minimum": 0},
                "StockPolicy": {
                    "type": "string",
                    "enum": [
                        "None",
                        "OrderPointFixedQuantity",
                        "OrderPointVariableQuantity",
                        "MakeToForecast",
                        "MakeToOrder",
                    ],
                },
                "SourcingPolicy": {
                    "type": "string",
                    "enum": [
                        "Equidistribution",
                        "HighestStock",
                        "HighestPriority",
                        "SourcingProportions",
                    ],
                },
                "DispatchPolicy": {
                    "type": "string",
                    "enum": [
                        "Equidistribution",
                        "GreatestQuantity",
                        "SmallestQuantity",
                        "HighestPriority",
                        "DispatchProportions",
                    ],
                },
                "ReviewPeriod": {"type": "integer", "minimum": 1},
                "FirstReview": {"type": "integer", "minimum": 0},
                "OrderPoints": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "OrderQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "OrderUpToLevels": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "Advance": {"type": "integer", "minimum": 0},
                "SafetyQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "CoverageHorizon": {"type": "integer", "minimum": 0},
                "CoverageOffset": {"type": "integer"},
                "CoverageRate": {"type": "number", "minimum": 0},
                "SalesForecasts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                },
                "Latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "Longitude": {"type": "number", "minimum": -180, "maximum": 180},
                "IgnoreDownstreamRequiredQuantities": {"type": "boolean"},
                "SourcingLimit": {
                    "type": "string",
                    "enum": [
                        "None",
                        "Capacity",
                        "CapacityQuantity",
                    ],
                },
                "OrderForEndOfTimeStep": {"type": "boolean"},
                "subdataset": {"type": "string"},
                "RetainProportions": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
            },
            "dependencies": {"InitialValue": ["InitialStock"]},
        },
        "Transport": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "TransportationLeadTime": {"type": "integer", "minimum": 0},
                "Priority": {"type": "integer", "minimum": 0},
                "Mode": {"type": "string"},
                "subdataset": {"type": "string"},
                "InitialTransportedQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                },
                "InitialTransportedValues": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                },
                "DutyUnitCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "TransportUnitCosts": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "CO2UnitEmissions": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "ActualTransportationLeadTimes": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "integer", "minimum": 0}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "MinimumOrderQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "MultipleOrderQuantities": {
                    "type": "object",
                    "patternProperties": {"^[0-9]+$": {"type": "number", "minimum": 0}},
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "SourcingProportions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
                "DispatchProportions": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]+$": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "if": {"minProperties": 1},
                    "then": {"required": ["0"]},
                },
            },
            "required": ["TransportationLeadTime"],
            "dependencies": {
                "InitialTransportedValues": ["InitialTransportedQuantities"]
            },
        },
        "Tags": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "TagType": {"type": "string"},
                "subdataset": {"type": "string"},
            },
        },
        "TagGroups": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "subdataset": {"type": "string"},
            },
        },
        "Uncertainties": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "Entity": {},
                "Attribute": {
                    "type": "string",
                    "enum": variables,
                },
                "TimeStep": {"type": "integer"},
                "UncertaintyMode": {
                    "type": "string",
                    "enum": sorted(changes),
                },
                "UncertaintyModel": {
                    "type": "string",
                    "enum": sorted(DistributionRegistry),
                },
                "Parameters": {"type": "object"},
            },
            "required": ["Entity", "Attribute", "UncertaintyMode", "UncertaintyModel", "Parameters"],
        },
    }
    graph = {
        "contains": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["ProductionResource", "id"],
                "target": ["ProductionOperation", "id"],
            },
            "cardinalities": "1:N",
            "all_target_present": True,
            "all_source_present": True,
        },
        "input": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["Stock", "id"],
                "target": ["ProductionOperation", "id"],
            },
            "cardinalities": "N:N",
            "all_target_present": True,
            "all_source_present": False,
        },
        "output": {
            "source": "source",
            "target": "target",
            "links": {
                "source": ["ProductionOperation", "id"],
                "target": ["Stock", "id"],
            },
            "cardinalities": "N:1",
            "all_target_present": False,
            "all_source_present": True,
        },
        "Transport": {
            "source": "source",
            "target": "target",
            "links": {"source": ["Stock", "id"], "target": ["Stock", "id"]},
            "cardinalities": "N:N",
            "all_target_present": False,
            "all_source_present": False,
        },
    }
