import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import KratosMultiphysics.ystemIdentificationApplication.Sensors

class MeasurementResidualResponseFunction(Kratos.AdjointResponseFunction):
    def __init__(self, p_coefficient: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Responses.MeasurementResidualResponseFunction, p_coefficient: float) -> None"""
    def AddSensor(self, sensor: KratosSystemIdentificationApplication.Sensors.Sensor) -> None:
        """AddSensor(self: KratosSystemIdentificationApplication.Responses.MeasurementResidualResponseFunction, sensor: KratosSystemIdentificationApplication.Sensors.Sensor) -> None"""
    def Clear(self) -> None:
        """Clear(self: KratosSystemIdentificationApplication.Responses.MeasurementResidualResponseFunction) -> None"""
    def GetSensorsList(self) -> list[KratosSystemIdentificationApplication.Sensors.Sensor]:
        """GetSensorsList(self: KratosSystemIdentificationApplication.Responses.MeasurementResidualResponseFunction) -> list[KratosSystemIdentificationApplication.Sensors.Sensor]"""
