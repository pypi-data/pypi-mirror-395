"""Type stubs for PETSc Scatter module."""


from typing import Self, Literal

from .Object import Object
from .IS import IS

from .Vec import Vec
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    InsertModeSpec,
    ScatterModeSpec,
)

class ScatterType:
    """Scatter type.

    See Also
    --------
    petsc.VecScatterType
    """

    BASIC: str
    NEIGHBOR: str
    ALLGATHERV: str
    ALLGATHER: str
    GATHERV: str
    GATHER: str
    ALLTOALL: str
    WINDOW: str

class ScatterMode:
    """Scatter mode."""

    FORWARD: int
    REVERSE: int
    FORWARD_LOCAL: int
    REVERSE_LOCAL: int

class Scatter(Object):
    """Scatter object.

    The object used to perform data movement between vectors.
    Scatter is described in the PETSc manual.

    See Also
    --------
    Vec, SF, petsc.VecScatter
    """

    Type = ScatterType
    Mode = ScatterMode

    def __init__(self) -> None: ...
    def __call__(
        self,
        x: Vec,
        y: Vec,
        addv: InsertModeSpec = None,
        mode: ScatterModeSpec = None,
    ) -> None:
        """Perform the scatter.

        Collective.

        See Also
        --------
        scatter
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the scatter.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.VecScatterView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the scatter.

        Collective.

        See Also
        --------
        petsc.VecScatterDestroy
        """
        ...

    def create(
        self,
        vec_from: Vec,
        is_from: IS | None,
        vec_to: Vec,
        is_to: IS | None,
    ) -> Self:
        """Create a scatter object.

        Collective.

        Parameters
        ----------
        vec_from
            Representative vector from which to scatter the data.
        is_from
            Indices of ``vec_from`` to scatter. If `None`, use all indices.
        vec_to
            Representative vector to which scatter the data.
        is_to
            Indices of ``vec_to`` where to receive. If `None`, use all indices.

        See Also
        --------
        IS, petsc.VecScatterCreate
        """
        ...

    def setType(self, scatter_type: ScatterType | str) -> None:
        """Set the type of the scatter.

        Logically collective.

        See Also
        --------
        getType, petsc.VecScatterSetType
        """
        ...

    def getType(self) -> str:
        """Return the type of the scatter.

        Not collective.

        See Also
        --------
        setType, petsc.VecScatterGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the scatter from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.VecScatterSetFromOptions
        """
        ...

    def setUp(self) -> Self:
        """Set up the internal data structures for using the scatter.

        Collective.

        See Also
        --------
        petsc.VecScatterSetUp
        """
        ...

    def copy(self) -> Scatter:
        """Return a copy of the scatter."""
        ...

    @classmethod
    def toAll(cls, vec: Vec) -> tuple[Scatter, Vec]:
        """Create a scatter that communicates a vector to all sharing processes.

        Collective.

        Parameters
        ----------
        vec
            The vector to scatter from.

        Notes
        -----
        The created scatter will have the same communicator of ``vec``.
        The method also returns an output vector of appropriate size to
        contain the result of the operation.

        See Also
        --------
        toZero, petsc.VecScatterCreateToAll
        """
        ...

    @classmethod
    def toZero(cls, vec: Vec) -> tuple[Scatter, Vec]:
        """Create a scatter that communicates a vector to rank zero.

        Collective.

        Parameters
        ----------
        vec
            The vector to scatter from.

        Notes
        -----
        The created scatter will have the same communicator of ``vec``.
        The method also returns an output vector of appropriate size to
        contain the result of the operation.

        See Also
        --------
        toAll, petsc.VecScatterCreateToZero
        """
        ...

    def begin(
        self,
        vec_from: Vec,
        vec_to: Vec,
        addv: InsertModeSpec = None,
        mode: ScatterModeSpec = None,
    ) -> None:
        """Begin a generalized scatter from one vector into another.

        Collective.

        This call has to be concluded with a call to `end`.
        For additional details on the Parameters, see `scatter`.

        See Also
        --------
        create, end, petsc.VecScatterBegin
        """
        ...

    def end(
        self,
        vec_from: Vec,
        vec_to: Vec,
        addv: InsertModeSpec = None,
        mode: ScatterModeSpec = None,
    ) -> None:
        """Complete a generalized scatter from one vector into another.

        Collective.

        This call has to be preceded by a call to `begin`.
        For additional details on the Parameters, see `scatter`.

        See Also
        --------
        create, begin, petsc.VecScatterEnd
        """
        ...

    def scatter(
        self,
        vec_from: Vec,
        vec_to: Vec,
        addv: InsertModeSpec = None,
        mode: ScatterModeSpec = None,
    ) -> None:
        """Perform a generalized scatter from one vector into another.

        Collective.

        Parameters
        ----------
        vec_from
            The source vector.
        vec_to
            The destination vector.
        addv
            Insertion mode.
        mode
            Scatter mode.

        See Also
        --------
        create, begin, end, petsc.VecScatterBegin, petsc.VecScatterEnd
        """
        ...

    # Aliases
    scatterBegin = begin
    scatterEnd = end
