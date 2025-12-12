import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
import KratosMultiphysics.Expression
from typing import overload

@overload
def AssignEquivalentProperties(source_conditions: Kratos.ConditionsArray, destination_conditions: Kratos.ConditionsArray) -> None:
    """AssignEquivalentProperties(*args, **kwargs)
    Overloaded function.

    1. AssignEquivalentProperties(source_conditions: Kratos.ConditionsArray, destination_conditions: Kratos.ConditionsArray) -> None

    2. AssignEquivalentProperties(source_elements: Kratos.ElementsArray, destination_elements: Kratos.ElementsArray) -> None
    """
@overload
def AssignEquivalentProperties(source_elements: Kratos.ElementsArray, destination_elements: Kratos.ElementsArray) -> None:
    """AssignEquivalentProperties(*args, **kwargs)
    Overloaded function.

    1. AssignEquivalentProperties(source_conditions: Kratos.ConditionsArray, destination_conditions: Kratos.ConditionsArray) -> None

    2. AssignEquivalentProperties(source_elements: Kratos.ElementsArray, destination_elements: Kratos.ElementsArray) -> None
    """
@overload
def ClipContainerExpression(nodal_expression: Kratos.Expression.NodalExpression, min: float, max: float) -> None:
    """ClipContainerExpression(*args, **kwargs)
    Overloaded function.

    1. ClipContainerExpression(nodal_expression: Kratos.Expression.NodalExpression, min: float, max: float) -> None

    2. ClipContainerExpression(condition_expression: Kratos.Expression.ConditionExpression, min: float, max: float) -> None

    3. ClipContainerExpression(element_expression: Kratos.Expression.ElementExpression, min: float, max: float) -> None
    """
@overload
def ClipContainerExpression(condition_expression: Kratos.Expression.ConditionExpression, min: float, max: float) -> None:
    """ClipContainerExpression(*args, **kwargs)
    Overloaded function.

    1. ClipContainerExpression(nodal_expression: Kratos.Expression.NodalExpression, min: float, max: float) -> None

    2. ClipContainerExpression(condition_expression: Kratos.Expression.ConditionExpression, min: float, max: float) -> None

    3. ClipContainerExpression(element_expression: Kratos.Expression.ElementExpression, min: float, max: float) -> None
    """
@overload
def ClipContainerExpression(element_expression: Kratos.Expression.ElementExpression, min: float, max: float) -> None:
    """ClipContainerExpression(*args, **kwargs)
    Overloaded function.

    1. ClipContainerExpression(nodal_expression: Kratos.Expression.NodalExpression, min: float, max: float) -> None

    2. ClipContainerExpression(condition_expression: Kratos.Expression.ConditionExpression, min: float, max: float) -> None

    3. ClipContainerExpression(element_expression: Kratos.Expression.ElementExpression, min: float, max: float) -> None
    """
