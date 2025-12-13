"""Type stubs for PETSc DS (Discrete System) module."""


from typing import (
    Self
)

# Import types from other modules
from .Object import Object
from .Comm import Comm
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import ArrayInt


class DSType:
    """The Discrete System types."""
    BASIC: str


class DS(Object):
    """Discrete System object.
    
    The DS (Discrete System) is used to encapsulate a discrete system,
    which is a collection of fields discretized over a mesh.
    """

    Type = DSType

    def view(self, viewer: Viewer | None = None) -> None:
        """View a discrete system.

        Collective.

        Parameters
        ----------
        viewer
            A Viewer to display the system.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the discrete system.

        Collective.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty DS.

        Collective.

        The type can then be set with setType.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setType(self, ds_type: DSType | str) -> None:
        """Build a particular type of a discrete system.

        Collective.

        Parameters
        ----------
        ds_type
            The type of the discrete system.
        """
        ...

    def getType(self) -> str:
        """Return the type of the discrete system.

        Not collective.
        """
        ...

    def setFromOptions(self) -> None:
        """Set parameters in a DS from the options database.

        Collective.
        """
        ...

    def setUp(self) -> Self:
        """Construct data structures for the discrete system.

        Collective.
        """
        ...

    def getSpatialDimension(self) -> int:
        """Return the spatial dimension of the DS.

        Not collective.

        The spatial dimension of the DS is the topological dimension of the
        discretizations.
        """
        ...

    def getCoordinateDimension(self) -> int:
        """Return the coordinate dimension of the DS.

        Not collective.

        The coordinate dimension of the DS is the dimension of the space into
        which the discretizations are embedded.
        """
        ...

    def getNumFields(self) -> int:
        """Return the number of fields in the DS.

        Not collective.
        """
        ...

    def getFieldIndex(self, disc: Object) -> int:
        """Return the index of the given field.

        Not collective.

        Parameters
        ----------
        disc
            The discretization object.
        """
        ...

    def getTotalDimensions(self) -> int:
        """Return the total size of the approximation space for this system.

        Not collective.
        """
        ...

    def getTotalComponents(self) -> int:
        """Return the total number of components in this system.

        Not collective.
        """
        ...

    def getDimensions(self) -> ArrayInt:
        """Return the size of the space for each field on an evaluation point.

        Not collective.
        """
        ...

    def getComponents(self) -> ArrayInt:
        """Return the number of components for each field on an evaluation point.

        Not collective.
        """
        ...

    def setDiscretisation(self, f: int, disc: Object) -> None:
        """Set the discretization object for the given field.

        Not collective.

        Parameters
        ----------
        f
            The field number.
        disc
            The discretization object.
        """
        ...
