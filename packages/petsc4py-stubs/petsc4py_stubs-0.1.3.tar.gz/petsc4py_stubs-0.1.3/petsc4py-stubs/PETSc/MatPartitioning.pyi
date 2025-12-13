"""Type stubs for PETSc MatPartitioning module."""


from typing import Self

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .Mat import Mat
from .IS import IS


class MatPartitioningType:
    """The partitioning types."""

    PARTITIONINGCURRENT: str
    PARTITIONINGAVERAGE: str
    PARTITIONINGSQUARE: str
    PARTITIONINGPARMETIS: str
    PARTITIONINGCHACO: str
    PARTITIONINGPARTY: str
    PARTITIONINGPTSCOTCH: str
    PARTITIONINGHIERARCH: str


class MatPartitioning(Object):
    """Object for managing the partitioning of a matrix or graph.

    See Also
    --------
    petsc.MatPartitioning
    """

    Type = MatPartitioningType

    def __call__(self) -> IS:
        """Return the partitioning result."""
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the partitioning data structure.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the graph.

        See Also
        --------
        petsc.MatPartitioningView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the partitioning context.

        Collective.

        See Also
        --------
        create, petsc.MatPartitioningDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a partitioning context.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        destroy, petsc.MatPartitioningCreate
        """
        ...

    def setType(self, matpartitioning_type: MatPartitioningType | str) -> None:
        """Set the type of the partitioner to use.

        Collective.

        Parameters
        ----------
        matpartitioning_type
            The partitioner type.

        See Also
        --------
        getType, petsc.MatPartitioningSetType
        """
        ...

    def getType(self) -> str:
        """Return the partitioning method.

        Not collective.

        See Also
        --------
        setType, petsc.MatPartitioningGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Set parameters in the partitioner from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.MatPartitioningSetFromOptions
        """
        ...

    def setAdjacency(self, adj: Mat) -> None:
        """Set the adjacency graph (matrix) of the thing to be partitioned.

        Collective.

        Parameters
        ----------
        adj
            The adjacency matrix, this can be any `Mat.Type` but the natural
            representation is `Mat.Type.MPIADJ`.

        See Also
        --------
        petsc.MatPartitioningSetAdjacency
        """
        ...

    def apply(self, partitioning: IS) -> None:
        """Return a partitioning for the graph represented by a sparse matrix.

        Collective.

        For each local node this tells the processor number that that node is
        assigned to.

        Parameters
        ----------
        partitioning
            The IS to store the partitioning result.

        See Also
        --------
        petsc.MatPartitioningApply
        """
        ...
