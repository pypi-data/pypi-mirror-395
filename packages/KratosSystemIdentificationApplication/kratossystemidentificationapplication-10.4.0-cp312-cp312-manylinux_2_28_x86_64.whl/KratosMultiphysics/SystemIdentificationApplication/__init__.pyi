import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import KratosMultiphysics.Expression
from . import ControlUtils as ControlUtils, MaskUtils as MaskUtils, Responses as Responses, SensorUtils as SensorUtils, Sensors as Sensors

class ConditionSmoothClamper:
    def __init__(self, min: float, max: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.ConditionSmoothClamper, min: float, max: float) -> None"""
    def CalculateForwardProjectionGradient(self, x_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression:
        """CalculateForwardProjectionGradient(self: KratosSystemIdentificationApplication.ConditionSmoothClamper, x_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression"""
    def ProjectBackward(self, y_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression:
        """ProjectBackward(self: KratosSystemIdentificationApplication.ConditionSmoothClamper, y_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression"""
    def ProjectForward(self, x_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression:
        """ProjectForward(self: KratosSystemIdentificationApplication.ConditionSmoothClamper, x_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression"""

class DistanceMatrix:
    def __init__(self) -> None:
        """__init__(self: KratosSystemIdentificationApplication.DistanceMatrix) -> None"""
    def GetDistance(self, index_i: int, index_j: int) -> float:
        """GetDistance(self: KratosSystemIdentificationApplication.DistanceMatrix, index_i: int, index_j: int) -> float"""
    def GetEntriesSize(self) -> int:
        """GetEntriesSize(self: KratosSystemIdentificationApplication.DistanceMatrix) -> int"""
    def GetNumberOfItems(self) -> int:
        """GetNumberOfItems(self: KratosSystemIdentificationApplication.DistanceMatrix) -> int"""
    def Update(self, values_container_expression: Kratos.Expression.NodalExpression | Kratos.Expression.ConditionExpression | Kratos.Expression.ElementExpression) -> None:
        """Update(self: KratosSystemIdentificationApplication.DistanceMatrix, values_container_expression: Union[Kratos.Expression.NodalExpression, Kratos.Expression.ConditionExpression, Kratos.Expression.ElementExpression]) -> None"""

class ElementSmoothClamper:
    def __init__(self, min: float, max: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.ElementSmoothClamper, min: float, max: float) -> None"""
    def CalculateForwardProjectionGradient(self, x_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression:
        """CalculateForwardProjectionGradient(self: KratosSystemIdentificationApplication.ElementSmoothClamper, x_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression"""
    def ProjectBackward(self, y_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression:
        """ProjectBackward(self: KratosSystemIdentificationApplication.ElementSmoothClamper, y_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression"""
    def ProjectForward(self, x_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression:
        """ProjectForward(self: KratosSystemIdentificationApplication.ElementSmoothClamper, x_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression"""

class KratosSystemIdentificationApplication(Kratos.KratosApplication):
    def __init__(self) -> None:
        """__init__(self: KratosSystemIdentificationApplication.KratosSystemIdentificationApplication) -> None"""

class NodeSmoothClamper:
    def __init__(self, min: float, max: float) -> None:
        """__init__(self: KratosSystemIdentificationApplication.NodeSmoothClamper, min: float, max: float) -> None"""
    def CalculateForwardProjectionGradient(self, x_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression:
        """CalculateForwardProjectionGradient(self: KratosSystemIdentificationApplication.NodeSmoothClamper, x_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression"""
    def ProjectBackward(self, y_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression:
        """ProjectBackward(self: KratosSystemIdentificationApplication.NodeSmoothClamper, y_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression"""
    def ProjectForward(self, x_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression:
        """ProjectForward(self: KratosSystemIdentificationApplication.NodeSmoothClamper, x_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression"""
