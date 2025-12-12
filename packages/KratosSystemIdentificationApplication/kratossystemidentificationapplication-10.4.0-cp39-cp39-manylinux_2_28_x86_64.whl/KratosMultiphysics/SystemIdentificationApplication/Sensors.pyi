import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import KratosMultiphysics.Expression
from typing import ClassVar

class ConditionSensorView:
    def __init__(self, sensor: Sensor, expression_name: str) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView, sensor: KratosSystemIdentificationApplication.Sensors.Sensor, expression_name: str) -> None"""
    def AddAuxiliaryExpression(self, suffix: str, condition_expression: Kratos.Expression.ConditionExpression) -> None:
        """AddAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView, suffix: str, condition_expression: Kratos.Expression.ConditionExpression) -> None"""
    def GetAuxiliaryExpression(self, suffix: str) -> Kratos.Expression.ConditionExpression:
        """GetAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView, suffix: str) -> Kratos.Expression.ConditionExpression"""
    def GetAuxiliarySuffixes(self) -> list[str]:
        """GetAuxiliarySuffixes(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView) -> list[str]"""
    def GetContainerExpression(self) -> Kratos.Expression.ConditionExpression:
        """GetContainerExpression(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView) -> Kratos.Expression.ConditionExpression"""
    def GetExpressionName(self) -> str:
        """GetExpressionName(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView) -> str"""
    def GetSensor(self) -> Sensor:
        """GetSensor(self: KratosSystemIdentificationApplication.Sensors.ConditionSensorView) -> KratosSystemIdentificationApplication.Sensors.Sensor"""

class DisplacementSensor(Sensor):
    def __init__(self, name: str, node: Kratos.Node, direction: Kratos.Array3, element: Kratos.Element, weight: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Sensors.DisplacementSensor, name: str, node: Kratos.Node, direction: Kratos.Array3, element: Kratos.Element, weight: float) -> None"""
    @staticmethod
    def Create(domain_model_part: Kratos.ModelPart, sensor_model_part: Kratos.ModelPart, sensor_id: int, sensor_parameters: Kratos.Parameters) -> Sensor:
        """Create(domain_model_part: Kratos.ModelPart, sensor_model_part: Kratos.ModelPart, sensor_id: int, sensor_parameters: Kratos.Parameters) -> KratosSystemIdentificationApplication.Sensors.Sensor"""
    @staticmethod
    def GetDefaultParameters() -> Kratos.Parameters:
        """GetDefaultParameters() -> Kratos.Parameters"""

class ElementSensorView:
    def __init__(self, sensor: Sensor, expression_name: str) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView, sensor: KratosSystemIdentificationApplication.Sensors.Sensor, expression_name: str) -> None"""
    def AddAuxiliaryExpression(self, suffix: str, element_expression: Kratos.Expression.ElementExpression) -> None:
        """AddAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView, suffix: str, element_expression: Kratos.Expression.ElementExpression) -> None"""
    def GetAuxiliaryExpression(self, suffix: str) -> Kratos.Expression.ElementExpression:
        """GetAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView, suffix: str) -> Kratos.Expression.ElementExpression"""
    def GetAuxiliarySuffixes(self) -> list[str]:
        """GetAuxiliarySuffixes(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView) -> list[str]"""
    def GetContainerExpression(self) -> Kratos.Expression.ElementExpression:
        """GetContainerExpression(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView) -> Kratos.Expression.ElementExpression"""
    def GetExpressionName(self) -> str:
        """GetExpressionName(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView) -> str"""
    def GetSensor(self) -> Sensor:
        """GetSensor(self: KratosSystemIdentificationApplication.Sensors.ElementSensorView) -> KratosSystemIdentificationApplication.Sensors.Sensor"""

class NodalSensorView:
    def __init__(self, sensor: Sensor, expression_name: str) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView, sensor: KratosSystemIdentificationApplication.Sensors.Sensor, expression_name: str) -> None"""
    def AddAuxiliaryExpression(self, suffix: str, nodal_expression: Kratos.Expression.NodalExpression) -> None:
        """AddAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView, suffix: str, nodal_expression: Kratos.Expression.NodalExpression) -> None"""
    def GetAuxiliaryExpression(self, suffix: str) -> Kratos.Expression.NodalExpression:
        """GetAuxiliaryExpression(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView, suffix: str) -> Kratos.Expression.NodalExpression"""
    def GetAuxiliarySuffixes(self) -> list[str]:
        """GetAuxiliarySuffixes(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView) -> list[str]"""
    def GetContainerExpression(self) -> Kratos.Expression.NodalExpression:
        """GetContainerExpression(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView) -> Kratos.Expression.NodalExpression"""
    def GetExpressionName(self) -> str:
        """GetExpressionName(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView) -> str"""
    def GetSensor(self) -> Sensor:
        """GetSensor(self: KratosSystemIdentificationApplication.Sensors.NodalSensorView) -> KratosSystemIdentificationApplication.Sensors.Sensor"""

class Sensor(Kratos.AdjointResponseFunction):
    def __init__(self, *args, **kwargs) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
    def AddContainerExpression(self, expression_name: str, expression: Kratos.Expression.NodalExpression | Kratos.Expression.ConditionExpression | Kratos.Expression.ElementExpression) -> None:
        """AddContainerExpression(self: KratosSystemIdentificationApplication.Sensors.Sensor, expression_name: str, expression: Union[Kratos.Expression.NodalExpression, Kratos.Expression.ConditionExpression, Kratos.Expression.ElementExpression]) -> None"""
    def ClearContainerExpressions(self) -> None:
        """ClearContainerExpressions(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> None"""
    def GetContainerExpression(self, expression_name: str) -> Kratos.Expression.NodalExpression | Kratos.Expression.ConditionExpression | Kratos.Expression.ElementExpression:
        """GetContainerExpression(self: KratosSystemIdentificationApplication.Sensors.Sensor, expression_name: str) -> Union[Kratos.Expression.NodalExpression, Kratos.Expression.ConditionExpression, Kratos.Expression.ElementExpression]"""
    def GetContainerExpressionsMap(self) -> dict[str, Kratos.Expression.NodalExpression | Kratos.Expression.ConditionExpression | Kratos.Expression.ElementExpression]:
        """GetContainerExpressionsMap(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> dict[str, Union[Kratos.Expression.NodalExpression, Kratos.Expression.ConditionExpression, Kratos.Expression.ElementExpression]]"""
    def GetName(self) -> str:
        """GetName(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> str"""
    def GetNode(self) -> Kratos.Node:
        """GetNode(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> Kratos.Node"""
    def GetSensorParameters(self) -> Kratos.Parameters:
        """GetSensorParameters(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> Kratos.Parameters"""
    def GetSensorValue(self) -> float:
        """GetSensorValue(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> float"""
    def GetWeight(self) -> float:
        """GetWeight(self: KratosSystemIdentificationApplication.Sensors.Sensor) -> float"""
    def SetSensorValue(self, arg0: float) -> None:
        """SetSensorValue(self: KratosSystemIdentificationApplication.Sensors.Sensor, arg0: float) -> None"""

class StrainSensor(Sensor):
    class StrainType:
        """Members:

          STRAIN_XX

          STRAIN_YY

          STRAIN_ZZ

          STRAIN_XY

          STRAIN_XZ

          STRAIN_YZ"""
        __members__: ClassVar[dict] = ...  # read-only
        STRAIN_XX: ClassVar[StrainSensor.StrainType] = ...
        STRAIN_XY: ClassVar[StrainSensor.StrainType] = ...
        STRAIN_XZ: ClassVar[StrainSensor.StrainType] = ...
        STRAIN_YY: ClassVar[StrainSensor.StrainType] = ...
        STRAIN_YZ: ClassVar[StrainSensor.StrainType] = ...
        STRAIN_ZZ: ClassVar[StrainSensor.StrainType] = ...
        __entries: ClassVar[dict] = ...
        def __init__(self, value: int) -> None:
            """__init__(self: KratosSystemIdentificationApplication.Sensors.StrainSensor.StrainType, value: int) -> None"""
        def __eq__(self, other: object) -> bool:
            """__eq__(self: object, other: object) -> bool"""
        def __hash__(self) -> int:
            """__hash__(self: object) -> int"""
        def __index__(self) -> int:
            """__index__(self: KratosSystemIdentificationApplication.Sensors.StrainSensor.StrainType) -> int"""
        def __int__(self) -> int:
            """__int__(self: KratosSystemIdentificationApplication.Sensors.StrainSensor.StrainType) -> int"""
        def __ne__(self, other: object) -> bool:
            """__ne__(self: object, other: object) -> bool"""
        @property
        def name(self) -> str:
            """name(self: object) -> str

            name(self: object) -> str
            """
        @property
        def value(self) -> int:
            """(arg0: KratosSystemIdentificationApplication.Sensors.StrainSensor.StrainType) -> int"""
    STRAIN_XX: ClassVar[StrainSensor.StrainType] = ...
    STRAIN_XY: ClassVar[StrainSensor.StrainType] = ...
    STRAIN_XZ: ClassVar[StrainSensor.StrainType] = ...
    STRAIN_YY: ClassVar[StrainSensor.StrainType] = ...
    STRAIN_YZ: ClassVar[StrainSensor.StrainType] = ...
    STRAIN_ZZ: ClassVar[StrainSensor.StrainType] = ...
    def __init__(self, name: str, node: Kratos.Node, strain_variable: Kratos.MatrixVariable, strain_type: StrainSensor.StrainType, element: Kratos.Element, weight: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.Sensors.StrainSensor, name: str, node: Kratos.Node, strain_variable: Kratos.MatrixVariable, strain_type: KratosSystemIdentificationApplication.Sensors.StrainSensor.StrainType, element: Kratos.Element, weight: float) -> None"""
    @staticmethod
    def Create(domain_model_part: Kratos.ModelPart, sensor_model_part: Kratos.ModelPart, sensor_id: int, sensor_parameters: Kratos.Parameters) -> Sensor:
        """Create(domain_model_part: Kratos.ModelPart, sensor_model_part: Kratos.ModelPart, sensor_id: int, sensor_parameters: Kratos.Parameters) -> KratosSystemIdentificationApplication.Sensors.Sensor"""
    @staticmethod
    def GetDefaultParameters() -> Kratos.Parameters:
        """GetDefaultParameters() -> Kratos.Parameters"""
