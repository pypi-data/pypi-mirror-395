class StockConsumer:
    """
    Python Consumer for stocks indicators at each time step.
    """

    def __init__(self):
        self.memory = list()

    def Consume(self, p_data):
        probe_output = self.engine.StocksProbeOutput.Cast(p_data)
        f = probe_output.GetFacts()
        timestep = int(probe_output.GetProbeRunDimension().GetProbeOutputCounter())
        for data in f:
            fact = [
                str(data.GetAttributeAsString("id")),
                timestep,
                float(data.GetAttributeAsDouble("Demand")),
                float(data.GetAttributeAsDouble("RemainingQuantity")),
                float(data.GetAttributeAsDouble("ServedQuantity")),
                float(data.GetAttributeAsDouble("UnservedQuantity")),
                float(data.GetAttributeAsDouble("TotalFillRateServiceLevel")),
                float(data.GetAttributeAsDouble("Value")),
                float(data.GetAttributeAsDouble("OnTimeFillRateServiceLevel")),
            ]
            self.memory.append(fact)


class PerformanceConsumer:
    """
    Python Consumer for performance indicators at the end of the simulation.
    """

    def __init__(self):
        self.memory = list()

    def Consume(self, p_data):
        probe_output = self.engine.PerformanceIndicatorsProbeOutput.Cast(p_data)
        f = probe_output.GetFacts()
        for data in f:
            fact = {
                "OPEX": float(data.GetAttributeAsDouble("OPEX")),
                "Profit": float(data.GetAttributeAsDouble("Profit")),
                "AverageStockValue": float(
                    data.GetAttributeAsDouble("AverageStockValue")
                ),
                "ServiceLevelIndicator": float(
                    data.GetAttributeAsDouble("ServiceLevelIndicator")
                ),
                "CO2Emissions": float(data.GetAttributeAsDouble("CO2Emissions")),
                "TotalDemand": float(data.GetAttributeAsDouble("TotalDemand")),
                "TotalServedQuantity": float(
                    data.GetAttributeAsDouble("TotalServedQuantity")
                ),
                "OnTimeFillRateServiceLevel": data.GetOnTimeFillRateServiceLevel().GetAsFloat(),
                "RemainingQuantityForSelection": data.GetRemainingQuantityForSelection().GetAsFloat(),
                "CoverageRateForSelection": data.GetCoverageRateForSelection().GetAsFloat(),
                "TotalFillRateServiceLevel": (
                    data.GetTotalServedQuantity().GetAsFloat()/ data.GetTotalDemand().GetAsFloat()
                    if data.GetTotalDemand().GetAsFloat() != 0
                    else 0.0
                ),
            }
            self.memory.append(fact)


class StocksAtEndOfSimulationConsumer:
    """
    Python Consumer for stocks global indicators at the end of the simulation.
    """

    def __init__(self):
        self.memory = list()

    def Consume(self, p_data):
        probe_output = self.engine.StocksAtEndOfSimulationProbeOutput.Cast(p_data)
        f = probe_output.GetFacts()
        for data in f:
            fact = {
                "id": str(data.GetAttributeAsString("id")),
                "TotalDemand": float(data.GetAttributeAsDouble("TotalDemand")),
                "TotalServedQuantity": float(data.GetAttributeAsDouble("TotalServedQuantity")),
                "TotalFillRateServiceLevel": 100 * float(data.GetAttributeAsDouble("TotalFillRateServiceLevel")),
                "OnTimeFillRateServiceLevel": 100 * float(data.GetAttributeAsDouble("OnTimeFillRateServiceLevel")),
                "CycleServiceLevel": float(data.GetAttributeAsDouble("CycleServiceLevel")),
            }
            self.memory.append(fact)
