import KratosMultiphysics as Kratos
import KratosMultiphysics as Kratos
from typing import overload

@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fd9470>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b7f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9bcf0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b170>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fd9470>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b7f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9bcf0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b170>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fd9470>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b7f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9bcf0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b170>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fd9470>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b7f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9bcf0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b170>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e414b0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b0ecb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bdf0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bd30>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e414b0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b0ecb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bdf0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bd30>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e414b0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b0ecb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bdf0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bd30>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e414b0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b0ecb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bdf0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6bd30>) -> tuple[float, int]
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6f4f0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6531feeaf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7bef0>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7ba30>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6f4f0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6531feeaf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7bef0>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7ba30>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6f4f0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6531feeaf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7bef0>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7ba30>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e6f4f0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6531feeaf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7bef0>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f7ba30>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea23f0>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b6b0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58ef0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58370>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea23f0>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b6b0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58ef0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58370>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea23f0>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b6b0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58ef0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58370>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea23f0>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f9b6b0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58ef0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e58370>) -> float
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530eea7f0>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e5f0f0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57670>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57830>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530eea7f0>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e5f0f0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57670>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57830>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530eea7f0>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e5f0f0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57670>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57830>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530eea7f0>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e5f0f0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57670>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530f57830>) -> tuple[float, int]
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fa6f70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fb1e70>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2670>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2fb0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fa6f70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fb1e70>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2670>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2fb0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fa6f70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fb1e70>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2670>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2fb0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fa6f70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530fb1e70>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2670>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530ea2fb0>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f653276f0f0>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29b30>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e658f0>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29030>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f653276f0f0>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29b30>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e658f0>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29030>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f653276f0f0>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29b30>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e658f0>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29030>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f653276f0f0>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29b30>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e658f0>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b29030>) -> float
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b13db0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f65327d5370>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41f30>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41770>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b13db0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f65327d5370>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41f30>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41770>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b13db0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f65327d5370>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41f30>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41770>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530b13db0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f65327d5370>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41f30>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f6530e41770>) -> tuple[float, float]
    """
