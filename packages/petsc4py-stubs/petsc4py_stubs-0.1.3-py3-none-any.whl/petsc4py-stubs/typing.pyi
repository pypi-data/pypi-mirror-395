"""Type stubs for petsc4py.typing module.

This module provides typing support for PETSc objects.
Based on official documentation from:
https://petsc.org/release/petsc4py/reference/petsc4py.typing.html
"""

from typing import (
    Any,
    Callable,
    Literal,
    Sequence,
)
from numpy import ndarray, dtype, bool_, intp, floating, complexfloating

# Forward declarations for callback types
from .PETSc.Const import InsertMode, ScatterMode, NormType
from .PETSc.Object import Object
from .PETSc.Vec import Vec
from .PETSc.Mat import Mat, NullSpace
from .PETSc.DM import DM
from .PETSc.KSP import KSP
from .PETSc.SNES import SNES
from .PETSc.TS import TS
from .PETSc.TAO import TAO, TAOLineSearch

# =============================================================================
# Scalar Type
# =============================================================================

Scalar = float | complex
"""Scalar type.

Scalars can be either `float` or `complex` (but not both) depending on how
PETSc was configured (``./configure --with-scalar-type=real|complex``).

"""

# =============================================================================
# Array Types (using numpy ndarray with dtype)
# =============================================================================

ArrayBool = ndarray[Any, dtype[bool_]]
"""Array of `bool`."""

ArrayInt = ndarray[Any, dtype[intp]]
"""Array of `int`."""

ArrayReal = ndarray[Any, dtype[floating[Any]]]
"""Array of `float`."""

ArrayComplex = ndarray[Any, dtype[complexfloating[Any, Any]]]
"""Array of `complex`."""

ArrayScalar = ndarray[Any, dtype[floating[Any] | complexfloating[Any, Any]]]
"""Array of `Scalar` numbers."""

# =============================================================================
# Specification Types
# =============================================================================

DimsSpec = int | tuple[int, ...] | Sequence[int]
"""Dimensions specification.

A single int, tuple or Sequence of int indicates grid sizes.
"""

AccessModeSpec = Literal["rw", "r", "w"] | None
"""Access mode specification.

Possible values are:
     - ``'rw'`` Read-Write mode.
     - ``'r'`` Read-only mode.
     - ``'w'`` Write-only mode.
     - `None` as ``'rw'``.

"""

InsertModeSpec = InsertMode | bool | None
"""Insertion mode specification.

Possible values are:
     - `InsertMode.ADD_VALUES` Add new value to existing one.
     - `InsertMode.INSERT_VALUES` Replace existing entry with new value.
     - `None` as `InsertMode.INSERT_VALUES`.
     - `False` as `InsertMode.INSERT_VALUES`.
     - `True` as `InsertMode.ADD_VALUES`.

   See Also
   --------
   InsertMode

"""

ScatterModeSpec = ScatterMode | bool | str | None
"""Scatter mode specification.

Possible values are:
     - `ScatterMode.FORWARD` Forward mode.
     - `ScatterMode.REVERSE` Reverse mode.
     - `None` as `ScatterMode.FORWARD`.
     - `False` as `ScatterMode.FORWARD`.
     - `True` as `ScatterMode.REVERSE`.
     - ``'forward'`` as `ScatterMode.FORWARD`.
     - ``'reverse'`` as `ScatterMode.REVERSE`.

   See Also
   --------
   ScatterMode

"""

LayoutSizeSpec = int | tuple[int, int]
"""`int` or 2-`tuple` of `int` describing the layout sizes.

   A single `int` indicates global size.
   A `tuple` of `int` indicates ``(local_size, global_size)``.

   See Also
   --------
   Sys.splitOwnership

"""

NormTypeSpec = NormType | None
"""Norm type specification.

    Possible values include:

    - `NormType.NORM_1` The 1-norm: Σₙ abs(xₙ) for vectors, maxₙ (Σᵢ abs(xₙᵢ)) for matrices.
    - `NormType.NORM_2` The 2-norm: √(Σₙ xₙ²) for vectors, largest singular values for matrices.
    - `NormType.NORM_INFINITY` The ∞-norm: maxₙ abs(xₙ) for vectors, maxᵢ (Σₙ abs(xₙᵢ)) for matrices.
    - `NormType.NORM_FROBENIUS` The Frobenius norm: same as 2-norm for vectors, √(Σₙᵢ xₙᵢ²) for matrices.
    - `NormType.NORM_1_AND_2` Compute both `NormType.NORM_1` and `NormType.NORM_2`.
    - `None` as `NormType.NORM_2` for vectors, `NormType.NORM_FROBENIUS` for matrices.

    See Also
    --------
    PETSc.NormType, petsc.NormType

"""

# =============================================================================
# Matrix-Related Types
# =============================================================================

MatAssemblySpec = int | bool | None
"""Matrix assembly specification.

   Possible values are:
     - `Mat.AssemblyType.FINAL`
     - `Mat.AssemblyType.FLUSH`
     - `None` as `Mat.AssemblyType.FINAL`
     - `False` as `Mat.AssemblyType.FINAL`
     - `True` as `Mat.AssemblyType.FLUSH`

   See Also
   --------
   petsc.MatAssemblyType

"""

MatSizeSpec = int | tuple[int, int] | tuple[tuple[int, int], tuple[int, int]]
"""`int` or (nested) `tuple` of `int` describing the matrix sizes.

   If `int` then rows = columns.
   A single `tuple` of `int` indicates ``(rows, columns)``.
   A nested `tuple` of `int` indicates ``((local_rows, rows), (local_columns, columns))``.

   See Also
   --------
   Sys.splitOwnership

"""

MatBlockSizeSpec = int | tuple[int, int]
"""The row and column block sizes.

   If a single `int` is provided then rows and columns share the same block size.

"""

CSRIndicesSpec = tuple[Sequence[int], Sequence[int]]
"""CSR indices format specification.

   A 2-tuple carrying the ``(row_start, col_indices)`` information.

"""

CSRSpec = tuple[Sequence[int], Sequence[int], Sequence[float | complex]]
"""CSR format specification.

   A 3-tuple carrying the ``(row_start, col_indices, values)`` information.

"""

NNZSpec = int | Sequence[int] | tuple[Sequence[int], Sequence[int]]
"""Nonzero pattern specification.

   A single `int` corresponds to fixed number of non-zeros per row.
   A `Sequence` of `int` indicates different non-zeros per row.
   If a 2-`tuple` is used, the elements of the tuple corresponds
   to the on-process and off-process parts of the matrix.

   See Also
   --------
   petsc.MatSeqAIJSetPreallocation, petsc.MatMPIAIJSetPreallocation

"""

# =============================================================================
# Callback Function Types
# =============================================================================

# --- PetscObject ---

PetscOptionsHandlerFunction = Callable[[Object], None]
"""Callback for processing extra options."""

# --- MatNullSpace ---

MatNullFunction = Callable[[NullSpace, Vec], None]
"""`PETSc.NullSpace` callback."""

# --- DM ---

DMCoarsenHookFunction = Callable[[DM, DM], None]
"""`PETSc.DM` coarsening hook callback."""

DMRestrictHookFunction = Callable[[DM, Mat, Vec, Mat, DM], None]
"""`PETSc.DM` restriction hook callback."""

# --- KSP ---

KSPRHSFunction = Callable[[KSP, Vec], None]
"""`PETSc.KSP` right-hand side function callback."""

KSPOperatorsFunction = Callable[[KSP, Mat, Mat], None]
"""`PETSc.KSP` operators function callback."""

KSPConvergenceTestFunction = Callable[[KSP, int, float], KSP.ConvergedReason]
"""`PETSc.KSP` convergence test callback.
Returns KSP.ConvergedReason.
"""

KSPMonitorFunction = Callable[[KSP, int, float], None]
"""`PETSc.KSP` monitor callback."""

KSPPreSolveFunction = Callable[[KSP, Vec, Vec], None]
"""`PETSc.KSP` pre solve callback."""

KSPPostSolveFunction = Callable[[KSP, Vec, Vec], None]
"""`PETSc.KSP` post solve callback."""

# --- SNES ---

SNESMonitorFunction = Callable[[SNES, int, float], None]
"""`SNES` monitor callback."""

SNESObjFunction = Callable[[SNES, Vec], None]
"""`SNES` objective function callback."""

SNESFunction = Callable[[SNES, Vec, Vec], None]
"""`SNES` residual function callback."""

SNESJacobianFunction = Callable[[SNES, Vec, Mat, Mat], None]
"""`SNES` Jacobian callback."""

SNESGuessFunction = Callable[[SNES, Vec], None]
"""`SNES` initial guess callback."""

SNESUpdateFunction = Callable[[SNES, int], None]
"""`SNES` step update callback."""

SNESLSPreFunction = Callable[[Vec, Vec], None]
"""`SNES` linesearch pre-check update callback."""

SNESNGSFunction = Callable[[SNES, Vec, Vec], None]
"""`SNES` nonlinear Gauss-Seidel callback."""

SNESConvergedFunction = Callable[[SNES, int, tuple[float, float, float]], int]
"""`SNES` convergence test callback.
Returns SNES.ConvergedReason.
"""
# --- TS ---

TSRHSFunction = Callable[[TS, float, Vec, Vec], None]
"""`TS` right-hand side function callback."""

TSRHSJacobian = Callable[[TS, float, Vec, Mat, Mat], None]
"""`TS` right-hand side Jacobian callback."""

TSRHSJacobianP = Callable[[TS, float, Vec, Mat], None]
"""`TS` right-hand side parameter Jacobian callback."""

TSIFunction = Callable[[TS, float, Vec, Vec, Vec], None]
"""`TS` implicit function callback."""

TSIJacobian = Callable[[TS, float, Vec, Vec, float, Mat, Mat], None]
"""`TS` implicit Jacobian callback."""

TSIJacobianP = Callable[[TS, float, Vec, Vec, float, Mat], None]
"""`TS` implicit parameter Jacobian callback."""

TSI2Function = Callable[[TS, float, Vec, Vec, Vec, Vec], None]
"""`TS` implicit 2nd order function callback."""

TSI2Jacobian = Callable[[TS, float, Vec, Vec, Vec, float, float, Mat, Mat], None]
"""`TS` implicit 2nd order Jacobian callback."""

TSI2JacobianP = Callable[[TS, float, Vec, Vec, Vec, float, float, Mat], None]
"""`TS` implicit 2nd order parameter Jacobian callback."""

TSMonitorFunction = Callable[[TS, int, float, Vec], None]
"""`TS` monitor callback."""

TSPreStepFunction = Callable[[TS], None]
"""`TS` pre-step callback."""

TSPostStepFunction = Callable[[TS], None]
"""`TS` post-step callback."""

TSIndicatorFunction = Callable[[TS, float, Vec, ArrayReal], None]
"""`TS` event indicator callback."""

TSPostEventFunction = Callable[[TS, ArrayInt, float, Vec, bool], None]
"""`TS` post-event callback."""

# --- TAO ---

TAOObjectiveFunction = Callable[[TAO, Vec], float]
"""`TAO` objective function callback."""

TAOGradientFunction = Callable[[TAO, Vec, Vec], None]
"""`TAO` objective gradient callback."""

TAOObjectiveGradientFunction = Callable[[TAO, Vec, Vec], float]
"""`TAO` objective function and gradient callback."""

TAOHessianFunction = Callable[[TAO, Vec, Mat, Mat], None]
"""`TAO` objective Hessian callback."""

TAOUpdateFunction = Callable[[TAO, int], None]
"""`TAO` update callback."""

TAOMonitorFunction = Callable[[TAO], None]
"""`TAO` monitor callback."""

TAOConvergedFunction = Callable[[TAO], None]
"""`TAO` convergence test callback."""

TAOJacobianFunction = Callable[[TAO, Vec, Mat, Mat], None]
"""`TAO` Jacobian callback."""

TAOResidualFunction = Callable[[TAO, Vec, Vec], None]
"""`TAO` residual callback."""

TAOJacobianResidualFunction = Callable[[TAO, Vec, Mat, Mat], None]
"""`TAO` Jacobian residual callback."""

TAOVariableBoundsFunction = Callable[[TAO, Vec, Vec], None]
"""`TAO` variable bounds callback."""

TAOConstraintsFunction = Callable[[TAO, Vec, Vec], None]
"""`TAO` constraints callback."""

TAOConstraintsJacobianFunction = Callable[[TAO, Vec, Mat, Mat], None]
"""`TAO` constraints Jacobian callback."""

TAOLSObjectiveFunction = Callable[[TAOLineSearch, Vec], float]
"""`TAOLineSearch` objective function callback."""

TAOLSGradientFunction = Callable[[TAOLineSearch, Vec, Vec], None]
"""`TAOLineSearch` objective gradient callback."""

TAOLSObjectiveGradientFunction = Callable[[TAOLineSearch, Vec, Vec], float]
"""`TAOLineSearch` objective function and gradient callback."""

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Scalar type
    "Scalar",
    # Array types
    "ArrayBool",
    "ArrayInt",
    "ArrayReal",
    "ArrayComplex",
    "ArrayScalar",
    # Specification types
    "DimsSpec",
    "AccessModeSpec",
    "InsertModeSpec",
    "ScatterModeSpec",
    "LayoutSizeSpec",
    "NormTypeSpec",
    "MatAssemblySpec",
    "MatSizeSpec",
    "MatBlockSizeSpec",
    "CSRIndicesSpec",
    "CSRSpec",
    "NNZSpec",
    # Callback function types
    "PetscOptionsHandlerFunction",
    "MatNullFunction",
    "DMCoarsenHookFunction",
    "DMRestrictHookFunction",
    "KSPRHSFunction",
    "KSPOperatorsFunction",
    "KSPConvergenceTestFunction",
    "KSPMonitorFunction",
    "KSPPreSolveFunction",
    "KSPPostSolveFunction",
    "SNESMonitorFunction",
    "SNESObjFunction",
    "SNESFunction",
    "SNESJacobianFunction",
    "SNESGuessFunction",
    "SNESUpdateFunction",
    "SNESLSPreFunction",
    "SNESNGSFunction",
    "SNESConvergedFunction",
    "TSRHSFunction",
    "TSRHSJacobian",
    "TSRHSJacobianP",
    "TSIFunction",
    "TSIJacobian",
    "TSIJacobianP",
    "TSI2Function",
    "TSI2Jacobian",
    "TSI2JacobianP",
    "TSMonitorFunction",
    "TSPreStepFunction",
    "TSPostStepFunction",
    "TSIndicatorFunction",
    "TSPostEventFunction",
    "TAOObjectiveFunction",
    "TAOGradientFunction",
    "TAOObjectiveGradientFunction",
    "TAOHessianFunction",
    "TAOUpdateFunction",
    "TAOMonitorFunction",
    "TAOConvergedFunction",
    "TAOJacobianFunction",
    "TAOResidualFunction",
    "TAOJacobianResidualFunction",
    "TAOVariableBoundsFunction",
    "TAOConstraintsFunction",
    "TAOConstraintsJacobianFunction",
    "TAOLSObjectiveFunction",
    "TAOLSGradientFunction",
    "TAOLSObjectiveGradientFunction",
]
