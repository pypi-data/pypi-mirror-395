"""Type stubs for PETSc Const module."""


# Basic constants
DECIDE: int
"""Use a default value for an `int` or `float` parameter."""

DEFAULT: int
"""Use a default value chosen by PETSc."""

DETERMINE: int
"""Compute a default value for an `int` or `float` parameter.
For tolerances this uses the default value from when
the object's type was set."""

CURRENT: int
"""Do not change the current value that is set."""

UNLIMITED: int
"""For a parameter that is a bound, such as the maximum
number of iterations, do not bound the value."""

# Float constants
INFINITY: float
"""Very large real value."""

NINFINITY: float
"""Very large negative real value."""

PINFINITY: float
"""Very large positive real value, same as `INFINITY`."""


class InsertMode:
    """Insertion mode.

    Most commonly used insertion modes are:

    `INSERT`
        Insert provided value/s discarding previous value/s.
    `ADD`
        Add provided value/s to current value/s.
    `MAX`
        Insert the maximum of provided value/s and current value/s.

    See Also
    --------
    petsc.InsertMode
    """

    # native
    NOT_SET_VALUES: int
    INSERT_VALUES: int
    ADD_VALUES: int
    MAX_VALUES: int
    INSERT_ALL_VALUES: int
    ADD_ALL_VALUES: int
    INSERT_BC_VALUES: int
    ADD_BC_VALUES: int

    # aliases
    INSERT: int
    ADD: int
    MAX: int
    INSERT_ALL: int
    ADD_ALL: int
    INSERT_BC: int
    ADD_BC: int


class ScatterMode:
    """Scatter mode.

    Most commonly used scatter modes are:

    `FORWARD`
        Scatter values in the forward direction.
    `REVERSE`
        Scatter values in the reverse direction.

    See Also
    --------
    Scatter.create, Scatter.begin, Scatter.end
    petsc.ScatterMode
    """

    # native
    SCATTER_FORWARD: int
    SCATTER_REVERSE: int
    SCATTER_FORWARD_LOCAL: int
    SCATTER_REVERSE_LOCAL: int

    # aliases
    FORWARD: int
    REVERSE: int
    FORWARD_LOCAL: int
    REVERSE_LOCAL: int


class NormType:
    """Norm type.

    Commonly used norm types:

    `N1`
        The one norm.
    `N2`
        The two norm.
    `FROBENIUS`
        The Frobenius norm.
    `INFINITY`
        The infinity norm.

    See Also
    --------
    petsc.NormType
    """

    # native
    NORM_1: int
    NORM_2: int
    NORM_1_AND_2: int
    NORM_FROBENIUS: int
    NORM_INFINITY: int
    NORM_MAX: int

    # aliases
    N1: int
    N2: int
    N12: int
    MAX: int
    FROBENIUS: int
    INFINITY: int

    # extra aliases
    FRB: int
    INF: int
