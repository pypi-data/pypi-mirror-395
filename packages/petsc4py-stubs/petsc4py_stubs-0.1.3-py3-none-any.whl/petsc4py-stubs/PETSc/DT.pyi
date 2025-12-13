"""Type stubs for PETSc DT (Discretization Technology) module."""


from typing import Self

# Import types from other modules
from .Object import Object
from .Comm import Comm
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import ArrayReal

class Quad(Object):
    """Quadrature rule for integration.

    The Quad object encapsulates a quadrature rule, which is a method for
    numerical integration. It stores quadrature points and weights.
    """

    def view(self, viewer: Viewer | None = None) -> None:
        """View a Quad object.

        Collective.

        Parameters
        ----------
        viewer
            A Viewer to display the graph.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a Quad object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def duplicate(self) -> Quad:
        """Create a deep copy of the Quad object.

        Collective.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the Quad object.

        Collective.
        """
        ...

    def getData(self) -> tuple[ArrayReal, ArrayReal]:
        """Return the data defining the Quad.

        Not collective.

        Returns
        -------
        tuple[ArrayReal, ArrayReal]
            A tuple of (points, weights) where points are the coordinates of
            the quadrature points and weights are the quadrature weights.
        """
        ...

    def getNumComponents(self) -> int:
        """Return the number of components for functions to be integrated.

        Not collective.
        """
        ...

    def setNumComponents(self, nc: int) -> None:
        """Set the number of components for functions to be integrated.

        Not collective.

        Parameters
        ----------
        nc
            The number of components.
        """
        ...

    def getOrder(self) -> int:
        """Return the order of the method in the Quad.

        Not collective.
        """
        ...

    def setOrder(self, order: int) -> None:
        """Set the order of the method in the Quad.

        Not collective.

        Parameters
        ----------
        order
            The order of the quadrature, i.e. the highest degree polynomial
            that is exactly integrated.
        """
        ...
