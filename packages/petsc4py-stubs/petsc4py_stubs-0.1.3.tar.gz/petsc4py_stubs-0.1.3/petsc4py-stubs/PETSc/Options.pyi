"""Type stubs for PETSc Options module."""


from typing import Sequence, Self

from .Object import Object
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    ArrayBool,
)

class Options:
    """The options database object.

    A dictionary-like object to store and operate with
    command line options.

    Parameters
    ----------
    prefix : str, optional
        Optional string to prepend to all the options.

    Examples
    --------
    Create an option database and operate with it.

    >>> from petsc4py import PETSc
    >>> opts = PETSc.Options()
    >>> opts['a'] = 1 # insert the command-line option '-a 1'
    >>> if 'a' in opts: # if the option is present
    >>>     val = opts['a'] # return the option value as 'str'
    >>> a_int = opts.getInt('a') # return the option value as 'int'
    >>> a_bool = opts.getBool('a') # return the option value as 'bool'

    Read command line and use default values.

    >>> from petsc4py import PETSc
    >>> opts = PETSc.Options()
    >>> b_float = opts.getReal('b', 1) # return the value or 1.0 if not present

    Read command line options prepended with a prefix.

    >>> from petsc4py import PETSc
    >>> opts = PETSc.Options('prefix_')
    >>> opts.getString('b', 'some_default_string') # read -prefix_b xxx

    See Also
    --------
    petsc_options

    """

    def __init__(self, prefix: str | None = None) -> None: ...
    def __contains__(self, item: str) -> bool: ...
    def __getitem__(self, item: str) -> str: ...
    def __setitem__(
        self,
        item: str,
        value: bool
        | int
        | float
        | Scalar
        | Sequence[bool]
        | Sequence[int]
        | Sequence[float]
        | Sequence[Scalar]
        | str,
    ) -> None: ...
    def __delitem__(self, item: str) -> None: ...
    @property
    def prefix(self) -> str | None:
        """Prefix for options."""
        ...

    @prefix.setter
    def prefix(self, prefix: str | None) -> None: ...
    @prefix.deleter
    def prefix(self) -> None: ...
    def create(self) -> Self:
        """Create an options database."""
        ...

    def destroy(self) -> Self:
        """Destroy an options database."""
        ...

    def clear(self) -> Self:
        """Clear an options database."""
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the options database.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        Viewer, petsc.PetscOptionsView

        """
        ...

    def prefixPush(self, prefix: str | Options | Object | None) -> None:
        """Push a prefix for the options database.

        Logically collective.

        See Also
        --------
        prefixPop, petsc.PetscOptionsPrefixPush

        """
        ...

    def prefixPop(self) -> None:
        """Pop a prefix for the options database.

        Logically collective.

        See Also
        --------
        prefixPush, petsc.PetscOptionsPrefixPop

        """
        ...

    def hasName(self, name: str) -> bool:
        """Return the boolean indicating if the option is in the database."""
        ...

    def used(self, name: str) -> bool:
        """Return the boolean indicating if the option was queried from the database."""
        ...

    def setValue(
        self,
        name: str,
        value: bool
        | int
        | float
        | Scalar
        | Sequence[bool]
        | Sequence[int]
        | Sequence[float]
        | Sequence[Scalar]
        | str,
    ) -> None:
        """Set a value for an option.

        Logically collective.

        Parameters
        ----------
        name
            The string identifying the option.
        value
            The option value.

        See Also
        --------
        delValue, petsc.PetscOptionsSetValue

        """
        ...

    def delValue(self, name: str) -> None:
        """Delete an option from the database.

        Logically collective.

        See Also
        --------
        setValue, petsc.PetscOptionsClearValue

        """
        ...

    def getBool(self, name: str, default: bool | None = None) -> bool:
        """Return the boolean value associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getBoolArray, petsc.PetscOptionsGetBool

        """
        ...

    def getBoolArray(
        self, name: str, default: Sequence[bool] | None = None
    ) -> ArrayBool:
        """Return the boolean values associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getBool, petsc.PetscOptionsGetBoolArray

        """
        ...

    def getInt(self, name: str, default: int | None = None) -> int:
        """Return the integer value associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getIntArray, petsc.PetscOptionsGetInt

        """
        ...

    def getIntArray(self, name: str, default: Sequence[int] | None = None) -> ArrayInt:
        """Return the integer array associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getInt, petsc.PetscOptionsGetIntArray

        """
        ...

    def getReal(self, name: str, default: float | None = None) -> float:
        """Return the real value associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getRealArray, petsc.PetscOptionsGetReal

        """
        ...

    def getRealArray(
        self, name: str, default: Sequence[float] | None = None
    ) -> ArrayReal:
        """Return the real array associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getReal, petsc.PetscOptionsGetRealArray

        """
        ...

    def getScalar(self, name: str, default: Scalar | None = None) -> Scalar:
        """Return the scalar value associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getScalarArray, petsc.PetscOptionsGetScalar

        """
        ...

    def getScalarArray(
        self, name: str, default: Sequence[Scalar] | None = None
    ) -> ArrayScalar:
        """Return the scalar array associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        getScalar, petsc.PetscOptionsGetScalarArray

        """
        ...

    def getString(self, name: str, default: str | None = None) -> str:
        """Return the string associated with the option.

        Not collective.

        Parameters
        ----------
        name
            The option name.
        default
            The default value.
            If `None`, it raises a `KeyError` if the option is not found.

        See Also
        --------
        petsc.PetscOptionsGetString

        """
        ...

    def insertString(self, string: str) -> None:
        """Insert a string in the options database.

        Logically collective.

        See Also
        --------
        petsc.PetscOptionsInsertString

        """
        ...

    def getAll(self) -> dict[str, str]:
        """Return all the options and their values.

        Not collective.

        See Also
        --------
        petsc.PetscOptionsGetAll

        """
        ...
