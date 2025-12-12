import KratosMultiphysics as Kratos
import KratosMultiphysics.Expression
from typing import overload

@overload
def ClusterMasks(list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = ...) -> list[tuple[list[int], Kratos.Expression.NodalExpression]]:
    """ClusterMasks(*args, **kwargs)
    Overloaded function.

    1. ClusterMasks(list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.NodalExpression]]

    2. ClusterMasks(list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ConditionExpression]]

    3. ClusterMasks(list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ElementExpression]]
    """
@overload
def ClusterMasks(list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = ...) -> list[tuple[list[int], Kratos.Expression.ConditionExpression]]:
    """ClusterMasks(*args, **kwargs)
    Overloaded function.

    1. ClusterMasks(list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.NodalExpression]]

    2. ClusterMasks(list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ConditionExpression]]

    3. ClusterMasks(list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ElementExpression]]
    """
@overload
def ClusterMasks(list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = ...) -> list[tuple[list[int], Kratos.Expression.ElementExpression]]:
    """ClusterMasks(*args, **kwargs)
    Overloaded function.

    1. ClusterMasks(list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.NodalExpression]]

    2. ClusterMasks(list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ConditionExpression]]

    3. ClusterMasks(list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[tuple[list[int], Kratos.Expression.ElementExpression]]
    """
@overload
def GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression:
    """GetMask(*args, **kwargs)
    Overloaded function.

    1. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> Kratos.Expression.NodalExpression

    2. GetMask(nodal_scalar_expression: Kratos.Expression.NodalExpression, threshold: float) -> Kratos.Expression.NodalExpression

    3. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> Kratos.Expression.ConditionExpression

    4. GetMask(condition_scalar_expression: Kratos.Expression.ConditionExpression, threshold: float) -> Kratos.Expression.ConditionExpression

    5. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression) -> Kratos.Expression.ElementExpression

    6. GetMask(element_scalar_expression: Kratos.Expression.ElementExpression, threshold: float) -> Kratos.Expression.ElementExpression
    """
@overload
def GetMaskSize(nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = ...) -> int:
    """GetMaskSize(*args, **kwargs)
    Overloaded function.

    1. GetMaskSize(nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> int

    2. GetMaskSize(condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> int

    3. GetMaskSize(element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> int
    """
@overload
def GetMaskSize(condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = ...) -> int:
    """GetMaskSize(*args, **kwargs)
    Overloaded function.

    1. GetMaskSize(nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> int

    2. GetMaskSize(condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> int

    3. GetMaskSize(element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> int
    """
@overload
def GetMaskSize(element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = ...) -> int:
    """GetMaskSize(*args, **kwargs)
    Overloaded function.

    1. GetMaskSize(nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> int

    2. GetMaskSize(condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> int

    3. GetMaskSize(element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> int
    """
@overload
def GetMaskThreshold(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> float:
    """GetMaskThreshold(*args, **kwargs)
    Overloaded function.

    1. GetMaskThreshold(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> float

    2. GetMaskThreshold(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> float

    3. GetMaskThreshold(element_scalar_expression: Kratos.Expression.ElementExpression) -> float
    """
@overload
def GetMaskThreshold(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> float:
    """GetMaskThreshold(*args, **kwargs)
    Overloaded function.

    1. GetMaskThreshold(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> float

    2. GetMaskThreshold(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> float

    3. GetMaskThreshold(element_scalar_expression: Kratos.Expression.ElementExpression) -> float
    """
@overload
def GetMaskThreshold(element_scalar_expression: Kratos.Expression.ElementExpression) -> float:
    """GetMaskThreshold(*args, **kwargs)
    Overloaded function.

    1. GetMaskThreshold(nodal_scalar_expression: Kratos.Expression.NodalExpression) -> float

    2. GetMaskThreshold(condition_scalar_expression: Kratos.Expression.ConditionExpression) -> float

    3. GetMaskThreshold(element_scalar_expression: Kratos.Expression.ElementExpression) -> float
    """
@overload
def GetMasksDividingReferenceMask(reference_nodal_mask_expression: Kratos.Expression.NodalExpression, list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = ...) -> list[int]:
    """GetMasksDividingReferenceMask(*args, **kwargs)
    Overloaded function.

    1. GetMasksDividingReferenceMask(reference_nodal_mask_expression: Kratos.Expression.NodalExpression, list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[int]

    2. GetMasksDividingReferenceMask(reference_condition_mask_expression: Kratos.Expression.ConditionExpression, list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[int]

    3. GetMasksDividingReferenceMask(reference_element_mask_expression: Kratos.Expression.ElementExpression, list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[int]
    """
@overload
def GetMasksDividingReferenceMask(reference_condition_mask_expression: Kratos.Expression.ConditionExpression, list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = ...) -> list[int]:
    """GetMasksDividingReferenceMask(*args, **kwargs)
    Overloaded function.

    1. GetMasksDividingReferenceMask(reference_nodal_mask_expression: Kratos.Expression.NodalExpression, list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[int]

    2. GetMasksDividingReferenceMask(reference_condition_mask_expression: Kratos.Expression.ConditionExpression, list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[int]

    3. GetMasksDividingReferenceMask(reference_element_mask_expression: Kratos.Expression.ElementExpression, list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[int]
    """
@overload
def GetMasksDividingReferenceMask(reference_element_mask_expression: Kratos.Expression.ElementExpression, list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = ...) -> list[int]:
    """GetMasksDividingReferenceMask(*args, **kwargs)
    Overloaded function.

    1. GetMasksDividingReferenceMask(reference_nodal_mask_expression: Kratos.Expression.NodalExpression, list_of_nodal_mask_expressions: list[Kratos.Expression.NodalExpression], required_minimum_redundancy: int = 1) -> list[int]

    2. GetMasksDividingReferenceMask(reference_condition_mask_expression: Kratos.Expression.ConditionExpression, list_of_condition_mask_expressions: list[Kratos.Expression.ConditionExpression], required_minimum_redundancy: int = 1) -> list[int]

    3. GetMasksDividingReferenceMask(reference_element_mask_expression: Kratos.Expression.ElementExpression, list_of_element_mask_expressions: list[Kratos.Expression.ElementExpression], required_minimum_redundancy: int = 1) -> list[int]
    """
@overload
def Intersect(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.NodalExpression:
    """Intersect(*args, **kwargs)
    Overloaded function.

    1. Intersect(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Intersect(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Intersect(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Intersect(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ConditionExpression:
    """Intersect(*args, **kwargs)
    Overloaded function.

    1. Intersect(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Intersect(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Intersect(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Intersect(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ElementExpression:
    """Intersect(*args, **kwargs)
    Overloaded function.

    1. Intersect(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Intersect(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Intersect(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Scale(nodal_scalar_expression: Kratos.Expression.NodalExpression, nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.NodalExpression:
    """Scale(*args, **kwargs)
    Overloaded function.

    1. Scale(nodal_scalar_expression: Kratos.Expression.NodalExpression, nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Scale(condition_scalar_expression: Kratos.Expression.ConditionExpression, condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Scale(element_scalar_expression: Kratos.Expression.ElementExpression, element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Scale(condition_scalar_expression: Kratos.Expression.ConditionExpression, condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ConditionExpression:
    """Scale(*args, **kwargs)
    Overloaded function.

    1. Scale(nodal_scalar_expression: Kratos.Expression.NodalExpression, nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Scale(condition_scalar_expression: Kratos.Expression.ConditionExpression, condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Scale(element_scalar_expression: Kratos.Expression.ElementExpression, element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Scale(element_scalar_expression: Kratos.Expression.ElementExpression, element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ElementExpression:
    """Scale(*args, **kwargs)
    Overloaded function.

    1. Scale(nodal_scalar_expression: Kratos.Expression.NodalExpression, nodal_mask_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Scale(condition_scalar_expression: Kratos.Expression.ConditionExpression, condition_mask_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Scale(element_scalar_expression: Kratos.Expression.ElementExpression, element_mask_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Subtract(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.NodalExpression:
    """Subtract(*args, **kwargs)
    Overloaded function.

    1. Subtract(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Subtract(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Subtract(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Subtract(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ConditionExpression:
    """Subtract(*args, **kwargs)
    Overloaded function.

    1. Subtract(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Subtract(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Subtract(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Subtract(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ElementExpression:
    """Subtract(*args, **kwargs)
    Overloaded function.

    1. Subtract(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Subtract(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Subtract(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Union(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.NodalExpression:
    """Union(*args, **kwargs)
    Overloaded function.

    1. Union(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Union(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Union(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Union(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ConditionExpression:
    """Union(*args, **kwargs)
    Overloaded function.

    1. Union(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Union(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Union(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
@overload
def Union(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = ...) -> Kratos.Expression.ElementExpression:
    """Union(*args, **kwargs)
    Overloaded function.

    1. Union(nodal_mask_1_expression: Kratos.Expression.NodalExpression, nodal_mask_2_expression: Kratos.Expression.NodalExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.NodalExpression

    2. Union(condition_mask_1_expression: Kratos.Expression.ConditionExpression, condition_mask_2_expression: Kratos.Expression.ConditionExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ConditionExpression

    3. Union(element_mask_1_expression: Kratos.Expression.ElementExpression, element_mask_2_expression: Kratos.Expression.ElementExpression, required_minimum_redundancy: int = 1) -> Kratos.Expression.ElementExpression
    """
