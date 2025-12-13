"""Type stubs for PETSc IS (Index Set) module."""


from typing import Any, Sequence, Self

from .Object import Object

from .Comm import Comm
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import ArrayInt

class ISType:
    """The index set types."""

    GENERAL: str
    BLOCK: str
    STRIDE: str

class IS(Object):
    """A collection of indices.

    IS objects are used to index into vectors and matrices and to set up vector
    scatters.

    See Also
    --------
    petsc.IS
    """

    Type = ISType

    def __len__(self) -> int:
        """Return the local size of the index set."""
        ...

    def __getitem__(self, i: int) -> int:
        """Return the i-th index."""
        ...

    def __iter__(self) -> Any:
        """Return an iterator over the indices."""
        ...

    def __enter__(self) -> ArrayInt:
        """Return the indices array for the context manager."""
        ...

    def __exit__(self, *exc: Any) -> None:
        """Exit the context manager."""
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """Display the index set.

        Collective.

        Parameters
        ----------
        viewer
            Viewer used to display the IS.

        See Also
        --------
        petsc.ISView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the index set.

        Collective.

        See Also
        --------
        petsc.ISDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an IS.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.

        See Also
        --------
        petsc.ISCreate
        """
        ...

    def setType(self, is_type: ISType | str) -> None:
        """Set the type of the index set.

        Collective.

        Parameters
        ----------
        is_type
            The index set type.

        See Also
        --------
        petsc.ISSetType
        """
        ...

    def getType(self) -> str:
        """Return the index set type associated with the IS.

        Not collective.

        See Also
        --------
        petsc.ISGetType
        """
        ...

    def createGeneral(self, indices: Sequence[int], comm: Comm | None = None) -> Self:
        """Create an IS with indices.

        Collective.

        Parameters
        ----------
        indices
            Integer array.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.

        See Also
        --------
        petsc.ISCreateGeneral
        """
        ...

    def createBlock(
        self, bsize: int, indices: Sequence[int], comm: Comm | None = None
    ) -> Self:
        """Create a blocked index set.

        Collective.

        Parameters
        ----------
        bsize
            Block size.
        indices
            Integer array of indices.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.

        See Also
        --------
        petsc.ISCreateBlock
        """
        ...

    def createStride(
        self, size: int, first: int = 0, step: int = 1, comm: Comm | None = None
    ) -> Self:
        """Create an index set consisting of evenly spaced values.

        Collective.

        Parameters
        ----------
        size
            The length of the locally owned portion of the index set.
        first
            The first element of the index set.
        step
            The difference between adjacent indices.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.

        See Also
        --------
        petsc.ISCreateStride
        """
        ...

    def duplicate(self) -> IS:
        """Create a copy of the index set.

        Collective.

        See Also
        --------
        IS.copy, petsc.ISDuplicate
        """
        ...

    def copy(self, result: IS | None = None) -> IS:
        """Copy the index set.

        Collective.

        Parameters
        ----------
        result
            The target IS. If None, a new IS is created.

        See Also
        --------
        petsc.ISCopy
        """
        ...

    def load(self, viewer: Viewer) -> Self:
        """Load an index set from a viewer.

        Collective.

        Parameters
        ----------
        viewer
            The viewer to load from.

        See Also
        --------
        petsc.ISLoad
        """
        ...

    def allGather(self) -> IS:
        """Gather all indices to all processors.

        Collective.

        See Also
        --------
        petsc.ISAllGather
        """
        ...

    def toGeneral(self) -> Self:
        """Convert the IS type to general.

        Collective.

        See Also
        --------
        petsc.ISToGeneral
        """
        ...

    def buildTwoSided(self, toindx: IS | None = None) -> IS:
        """Create an index set describing a global pairing.

        Collective.

        Parameters
        ----------
        toindx
            The index set describing the matching indices.

        See Also
        --------
        petsc.ISBuildTwoSided
        """
        ...

    def invertPermutation(self, nlocal: int | None = None) -> IS:
        """Create the inverse of an index set permutation.

        Collective.

        Parameters
        ----------
        nlocal
            The number of indices on this processor in result.

        See Also
        --------
        petsc.ISInvertPermutation
        """
        ...

    def getSize(self) -> int:
        """Return the global length of the index set.

        Not collective.

        See Also
        --------
        petsc.ISGetSize
        """
        ...

    def getLocalSize(self) -> int:
        """Return the local length of the index set.

        Not collective.

        See Also
        --------
        petsc.ISGetLocalSize
        """
        ...

    def getSizes(self) -> tuple[int, int]:
        """Return the local and global sizes of the index set.

        Not collective.

        Returns
        -------
        tuple[int, int]
            The local and global sizes.
        """
        ...

    def getBlockSize(self) -> int:
        """Return the block size of the index set.

        Not collective.

        See Also
        --------
        petsc.ISGetBlockSize
        """
        ...

    def setBlockSize(self, bs: int) -> None:
        """Set the block size of the index set.

        Logically collective.

        Parameters
        ----------
        bs
            The block size.

        See Also
        --------
        petsc.ISSetBlockSize
        """
        ...

    def sort(self) -> Self:
        """Sort the indices of the index set.

        Collective.

        See Also
        --------
        petsc.ISSort
        """
        ...

    def sortRemoveDups(self) -> Self:
        """Sort the indices and remove duplicates.

        Collective.

        See Also
        --------
        petsc.ISSortRemoveDups
        """
        ...

    def isSorted(self) -> bool:
        """Return whether the indices are sorted.

        Not collective.

        See Also
        --------
        petsc.ISSorted
        """
        ...

    def setPermutation(self) -> Self:
        """Mark the index set as being a permutation.

        Logically collective.

        See Also
        --------
        petsc.ISSetPermutation
        """
        ...

    def isPermutation(self) -> bool:
        """Return whether the index set is a permutation.

        Not collective.

        See Also
        --------
        petsc.ISPermutation
        """
        ...

    def setIdentity(self) -> Self:
        """Mark the index set as being an identity.

        Logically collective.

        See Also
        --------
        petsc.ISSetIdentity
        """
        ...

    def isIdentity(self) -> bool:
        """Return whether the index set is an identity.

        Not collective.

        See Also
        --------
        petsc.ISIdentity
        """
        ...

    def equal(self, iset: IS) -> bool:
        """Return whether two index sets are equal.

        Collective.

        Parameters
        ----------
        iset
            The other index set.

        See Also
        --------
        petsc.ISEqual
        """
        ...

    def sum(self, iset: IS) -> IS:
        """Return the union of two index sets.

        Collective.

        Parameters
        ----------
        iset
            The other index set.

        See Also
        --------
        petsc.ISSum
        """
        ...

    def expand(self, iset: IS) -> IS:
        """Return the union of two index sets (alias for sum).

        Collective.

        Parameters
        ----------
        iset
            The other index set.

        See Also
        --------
        petsc.ISExpand
        """
        ...

    def union(self, iset: IS) -> IS:
        """Return the union of two index sets.

        Collective.

        Parameters
        ----------
        iset
            The other index set.
        """
        ...

    def difference(self, iset: IS) -> IS:
        """Return the difference of two index sets.

        Collective.

        Parameters
        ----------
        iset
            The other index set.

        See Also
        --------
        petsc.ISDifference
        """
        ...

    def complement(self, nmin: int, nmax: int) -> IS:
        """Return the complement of the index set.

        Collective.

        Parameters
        ----------
        nmin
            The minimum index.
        nmax
            The maximum index.

        See Also
        --------
        petsc.ISComplement
        """
        ...

    def embed(self, iset: IS, drop: bool) -> IS:
        """Embed the index set in a new index set.

        Not collective.

        Parameters
        ----------
        iset
            The containing index set.
        drop
            Whether to drop indices not in the containing set.

        See Also
        --------
        petsc.ISEmbed
        """
        ...

    def renumber(self, mult: IS | None = None) -> tuple[int, IS]:
        """Renumber the indices.

        Collective.

        Parameters
        ----------
        mult
            Multiplicity index set.

        See Also
        --------
        petsc.ISRenumber
        """
        ...

    def setIndices(self, indices: Sequence[int]) -> None:
        """Set the indices of the index set.

        Logically collective.

        Parameters
        ----------
        indices
            The indices.

        See Also
        --------
        petsc.ISGeneralSetIndices
        """
        ...

    def getIndices(self) -> ArrayInt:
        """Return the indices of the index set.

        Not collective.

        See Also
        --------
        petsc.ISGetIndices
        """
        ...

    def setBlockIndices(self, bsize: int, indices: Sequence[int]) -> None:
        """Set the indices for a blocked index set.

        Logically collective.

        Parameters
        ----------
        bsize
            The block size.
        indices
            The block indices.

        See Also
        --------
        petsc.ISBlockSetIndices
        """
        ...

    def getBlockIndices(self) -> ArrayInt:
        """Return the block indices of a blocked index set.

        Not collective.

        See Also
        --------
        petsc.ISBlockGetIndices
        """
        ...

    def setStride(self, size: int, first: int = 0, step: int = 1) -> None:
        """Set the stride parameters for a stride index set.

        Logically collective.

        Parameters
        ----------
        size
            The length of the index set.
        first
            The first element.
        step
            The step between elements.

        See Also
        --------
        petsc.ISStrideSetStride
        """
        ...

    def getStride(self) -> tuple[int, int, int]:
        """Return the stride parameters.

        Not collective.

        Returns
        -------
        tuple[int, int, int]
            The size, first element, and step.

        See Also
        --------
        petsc.ISStrideGetInfo
        """
        ...

    def getInfo(self) -> tuple[int, int, int]:
        """Return the stride parameters (alias for getStride).

        Not collective.
        """
        ...

    # Properties

    @property
    def sizes(self) -> tuple[int, int]:
        """The local and global sizes."""
        ...

    @property
    def size(self) -> int:
        """The global size."""
        ...

    @property
    def local_size(self) -> int:
        """The local size."""
        ...

    @property
    def block_size(self) -> int:
        """The block size."""
        ...

    @property
    def indices(self) -> ArrayInt:
        """The indices."""
        ...

    @property
    def array(self) -> ArrayInt:
        """The indices as an array (alias for indices)."""
        ...

class LGMap(Object):
    """Local-to-global mapping.

    Mapping from a local ordering (on individual processes) to a global PETSc ordering.

    See Also
    --------
    petsc.ISLocalToGlobalMapping
    """

    class MapMode:
        """Mapping mode."""

        BASIC: int
        MASK: int
        DROP: int

    Mode = MapMode

    def view(self, viewer: Viewer | None = None) -> None:
        """View the local-to-global mapping.

        Collective.

        Parameters
        ----------
        viewer
            Viewer used to display the mapping.

        See Also
        --------
        petsc.ISLocalToGlobalMappingView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the local-to-global mapping.

        Collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingDestroy
        """
        ...

    def create(
        self, indices: Sequence[int], bsize: int = 1, comm: Comm | None = None
    ) -> Self:
        """Create a local-to-global mapping.

        Collective.

        Parameters
        ----------
        indices
            The global index for each local element.
        bsize
            The block size.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.

        See Also
        --------
        petsc.ISLocalToGlobalMappingCreate
        """
        ...

    def createIS(self, iset: IS) -> Self:
        """Create a local-to-global mapping from an index set.

        Collective.

        Parameters
        ----------
        iset
            The index set that defines the mapping.

        See Also
        --------
        petsc.ISLocalToGlobalMappingCreateIS
        """
        ...

    def createSF(self, sf: Any, start: int) -> Self:
        """Create a local-to-global mapping from a star forest.

        Collective.

        Parameters
        ----------
        sf
            The star forest.
        start
            The first global index on this process.

        See Also
        --------
        petsc.ISLocalToGlobalMappingCreateSF
        """
        ...

    def getSize(self) -> int:
        """Return the local size of the local-to-global mapping.

        Not collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetSize
        """
        ...

    def getBlockSize(self) -> int:
        """Return the block size of the local-to-global mapping.

        Not collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetBlockSize
        """
        ...

    def getIndices(self) -> ArrayInt:
        """Return the global indices for the local-to-global mapping.

        Not collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetIndices
        """
        ...

    def getBlockIndices(self) -> ArrayInt:
        """Return the block indices for the local-to-global mapping.

        Not collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetBlockIndices
        """
        ...

    def getInfo(self) -> tuple[ArrayInt, ArrayInt]:
        """Return the mapping info.

        Collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetInfo
        """
        ...

    def getBlockInfo(self) -> tuple[ArrayInt, ArrayInt]:
        """Return the block mapping info.

        Collective.

        See Also
        --------
        petsc.ISLocalToGlobalMappingGetBlockInfo
        """
        ...

    def apply(self, indices: Sequence[int], result: ArrayInt | None = None) -> ArrayInt:
        """Apply the local-to-global mapping to an index array.

        Not collective.

        Parameters
        ----------
        indices
            The local indices.
        result
            The array to store the global indices.

        See Also
        --------
        petsc.ISLocalToGlobalMappingApply
        """
        ...

    def applyBlock(
        self, indices: Sequence[int], result: ArrayInt | None = None
    ) -> ArrayInt:
        """Apply the local-to-global block mapping.

        Not collective.

        Parameters
        ----------
        indices
            The local block indices.
        result
            The array to store the global block indices.

        See Also
        --------
        petsc.ISLocalToGlobalMappingApplyBlock
        """
        ...

    def applyInverse(
        self, indices: Sequence[int], mode: MapMode | int | None = None
    ) -> ArrayInt:
        """Apply the inverse of the local-to-global mapping.

        Not collective.

        Parameters
        ----------
        indices
            The global indices.
        mode
            The mapping mode.

        See Also
        --------
        petsc.ISGlobalToLocalMappingApply
        """
        ...

    def applyBlockInverse(
        self, indices: Sequence[int], mode: MapMode | int | None = None
    ) -> ArrayInt:
        """Apply the inverse of the local-to-global block mapping.

        Not collective.

        Parameters
        ----------
        indices
            The global block indices.
        mode
            The mapping mode.

        See Also
        --------
        petsc.ISGlobalToLocalMappingApplyBlock
        """
        ...

    # Properties

    @property
    def size(self) -> int:
        """The local size of the mapping."""
        ...

    @property
    def block_size(self) -> int:
        """The block size of the mapping."""
        ...

    @property
    def indices(self) -> ArrayInt:
        """The global indices."""
        ...

    @property
    def block_indices(self) -> ArrayInt:
        """The block indices."""
        ...

# Type alias exports
__all__ = [
    "IS",
    "ISType",
    "LGMap",
]
