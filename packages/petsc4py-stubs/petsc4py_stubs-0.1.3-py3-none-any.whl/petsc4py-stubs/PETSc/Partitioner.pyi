"""Type stubs for PETSc Partitioner module."""


from typing import Sequence, Self

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer


class PartitionerType:
    """The partitioner types."""

    PARMETIS: str
    PTSCOTCH: str
    CHACO: str
    SIMPLE: str
    SHELL: str
    GATHER: str
    MATPARTITIONING: str
    MULTISTAGE: str


class Partitioner(Object):
    """A graph partitioner.

    See Also
    --------
    petsc.PetscPartitioner
    """

    Type = PartitionerType

    def view(self, viewer: Viewer | None = None) -> None:
        """View the partitioner.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the graph.

        See Also
        --------
        petsc.PetscPartitionerView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the partitioner object.

        Collective.

        See Also
        --------
        petsc.PetscPartitionerDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty partitioner object.

        Collective.

        The type can be set with `setType`.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        setType, petsc.PetscPartitionerCreate
        """
        ...

    def setType(self, part_type: PartitionerType | str) -> None:
        """Build a particular type of the partitioner.

        Collective.

        Parameters
        ----------
        part_type
            The kind of partitioner.

        See Also
        --------
        getType, petsc.PetscPartitionerSetType
        """
        ...

    def getType(self) -> str:
        """Return the partitioner type.

        Not collective.

        See Also
        --------
        setType, petsc.PetscPartitionerGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Set parameters in the partitioner from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.PetscPartitionerSetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Construct data structures for the partitioner.

        Collective.

        See Also
        --------
        petsc.PetscPartitionerSetUp
        """
        ...

    def reset(self) -> None:
        """Reset data structures of the partitioner.

        Collective.

        See Also
        --------
        petsc.PetscPartitionerReset
        """
        ...

    def setShellPartition(
        self,
        numProcs: int,
        sizes: Sequence[int] | None = None,
        points: Sequence[int] | None = None,
    ) -> None:
        """Set a custom partition for a mesh.

        Collective.

        Parameters
        ----------
        numProcs
            The number of partitions.
        sizes
            The number of points in each partition.
        points
            A permutation of the points that groups those assigned to each
            partition in order (i.e., partition 0 first, partition 1 next,
            etc.).

        See Also
        --------
        petsc.PetscPartitionerShellSetPartition
        """
        ...
