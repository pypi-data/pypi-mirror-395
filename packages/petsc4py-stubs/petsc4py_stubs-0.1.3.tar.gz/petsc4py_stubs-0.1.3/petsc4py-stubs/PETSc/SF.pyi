"""Type stubs for PETSc SF (Star Forest) module."""

from typing import Any, Sequence, Self
from numpy import ndarray

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .Section import Section

# Import types from typing module
from petsc4py.typing import ArrayInt
from mpi4py.MPI import Datatype, Op

class SFType:
    """The star forest types."""

    BASIC: str
    NEIGHBOR: str
    ALLGATHERV: str
    ALLGATHER: str
    GATHERV: str
    GATHER: str
    ALLTOALL: str
    WINDOW: str

class SF(Object):
    """Star Forest object for communication.

    SF is used for setting up and managing the communication of certain
    entries of arrays and `Vec` between MPI processes.

    See Also
    --------
    petsc.PetscSF
    """

    Type = SFType

    def view(self, viewer: Viewer | None = None) -> None:
        """View a star forest.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the graph.

        See Also
        --------
        petsc.PetscSFView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the star forest.

        Collective.

        See Also
        --------
        petsc.PetscSFDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a star forest communication context.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscSFCreate
        """
        ...

    def setType(self, sf_type: SFType | str) -> None:
        """Set the type of the star forest.

        Collective.

        Parameters
        ----------
        sf_type
            The star forest type.

        See Also
        --------
        petsc.PetscSFSetType
        """
        ...

    def getType(self) -> str:
        """Return the type name of the star forest.

        Collective.

        See Also
        --------
        petsc.PetscSFGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Set options using the options database.

        Logically collective.

        See Also
        --------
        petsc_options, petsc.PetscSFSetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Set up communication structures.

        Collective.

        See Also
        --------
        petsc.PetscSFSetUp
        """
        ...

    def reset(self) -> None:
        """Reset a star forest so that different sizes or neighbors can be used.

        Collective.

        See Also
        --------
        petsc.PetscSFReset
        """
        ...

    def getGraph(self) -> tuple[int, ArrayInt, ArrayInt]:
        """Return star forest graph.

        Not collective.

        The number of leaves can be determined from the size of ``ilocal``.

        Returns
        -------
        nroots : int
            Number of root vertices on the current process (these are possible
            targets for other process to attach leaves).
        ilocal : ArrayInt
            Locations of leaves in leafdata buffers.
        iremote : ArrayInt
            Remote locations of root vertices for each leaf on the current
            process.

        See Also
        --------
        petsc.PetscSFGetGraph
        """
        ...

    def setGraph(
        self, nroots: int, local: Sequence[int] | None, remote: Sequence[int]
    ) -> None:
        """Set star forest graph.

        Collective.

        The number of leaves argument can be determined from the size of
        ``local`` and/or ``remote``.

        Parameters
        ----------
        nroots
            Number of root vertices on the current process (these are possible
            targets for other process to attach leaves).
        local
            Locations of leaves in leafdata buffers, pass `None` for contiguous
            storage.
        remote
            Remote locations of root vertices for each leaf on the current
            process. Should be ``2*nleaves`` long as (rank, index) pairs.

        See Also
        --------
        petsc.PetscSFSetGraph
        """
        ...

    def setRankOrder(self, flag: bool) -> None:
        """Sort multi-points for gathers and scatters by rank order.

        Logically collective.

        Parameters
        ----------
        flag
            `True` to sort, `False` to skip sorting.

        See Also
        --------
        petsc.PetscSFSetRankOrder
        """
        ...

    def getMulti(self) -> SF:
        """Return the inner SF implementing gathers and scatters.

        Collective.

        See Also
        --------
        petsc.PetscSFGetMultiSF
        """
        ...

    def createInverse(self) -> SF:
        """Create the inverse map.

        Collective.

        Create the inverse map given a PetscSF in which all vertices have
        degree 1.

        See Also
        --------
        petsc.PetscSFCreateInverseSF
        """
        ...

    def computeDegree(self) -> ArrayInt:
        """Compute and return the degree of each root vertex.

        Collective.

        See Also
        --------
        petsc.PetscSFComputeDegreeBegin, petsc.PetscSFComputeDegreeEnd
        """
        ...

    def createEmbeddedRootSF(self, selected: Sequence[int]) -> SF:
        """Remove edges from all but the selected roots.

        Collective.

        Does not remap indices.

        Parameters
        ----------
        selected
            Indices of the selected roots on this process.

        See Also
        --------
        petsc.PetscSFCreateEmbeddedRootSF
        """
        ...

    def createEmbeddedLeafSF(self, selected: Sequence[int]) -> SF:
        """Remove edges from all but the selected leaves.

        Collective.

        Does not remap indices.

        Parameters
        ----------
        selected
            Indices of the selected roots on this process.

        See Also
        --------
        petsc.PetscSFCreateEmbeddedLeafSF
        """
        ...

    def createSectionSF(
        self,
        rootSection: Section,
        remoteOffsets: Sequence[int] | None,
        leafSection: Section,
    ) -> SF:
        """Create an expanded `SF` of DOFs.

        Collective.

        Assumes the input `SF` relates points.

        Parameters
        ----------
        rootSection
            Data layout of remote points for outgoing data (this is usually
            the serial section).
        remoteOffsets
            Offsets for point data on remote processes (these are offsets from
            the root section), or `None`.
        leafSection
            Data layout of local points for incoming data (this is the
            distributed section).

        See Also
        --------
        petsc.PetscSFCreateSectionSF
        """
        ...

    def distributeSection(
        self, rootSection: Section, leafSection: Section | None = None
    ) -> tuple[ArrayInt, Section]:
        """Create a new, reorganized `Section`.

        Collective.

        Moves from the root to the leaves of the `SF`.

        Parameters
        ----------
        rootSection
            Section defined on root space.
        leafSection
            Section defined on the leaf space.

        See Also
        --------
        petsc.PetscSFDistributeSection
        """
        ...

    def compose(self, sf: SF) -> SF:
        """Compose a new `SF`.

        Collective.

        Puts the ``sf`` under this object in a top (roots) down (leaves) view.

        Parameters
        ----------
        sf
            `SF` to put under this object.

        See Also
        --------
        petsc.PetscSFCompose
        """
        ...

    def bcastBegin(
        self, unit: Datatype, rootdata: ndarray, leafdata: ndarray, op: Op
    ) -> None:
        """Begin pointwise broadcast.

        Collective.

        Root values are reduced to leaf values. This call has to be concluded
        with a call to `bcastEnd`.

        Parameters
        ----------
        unit
            MPI datatype.
        rootdata
            Buffer to broadcast.
        leafdata
            Buffer to be reduced with values from each leaf's respective root.
        op
            MPI reduction operation.

        See Also
        --------
        bcastEnd, petsc.PetscSFBcastBegin
        """
        ...

    def bcastEnd(
        self, unit: Datatype, rootdata: ndarray, leafdata: ndarray, op: Op
    ) -> None:
        """End a broadcast & reduce operation started with `bcastBegin`.

        Collective.

        Parameters
        ----------
        unit
            MPI datatype.
        rootdata
            Buffer to broadcast.
        leafdata
            Buffer to be reduced with values from each leaf's respective root.
        op
            MPI reduction operation.

        See Also
        --------
        bcastBegin, petsc.PetscSFBcastEnd
        """
        ...

    def reduceBegin(
        self, unit: Datatype, leafdata: ndarray, rootdata: ndarray, op: Op
    ) -> None:
        """Begin reduction of leafdata into rootdata.

        Collective.

        This call has to be completed with call to `reduceEnd`.

        Parameters
        ----------
        unit
            MPI datatype.
        leafdata
            Values to reduce.
        rootdata
            Result of reduction of values from all leaves of each root.
        op
            MPI reduction operation.

        See Also
        --------
        reduceEnd, petsc.PetscSFReduceBegin
        """
        ...

    def reduceEnd(
        self, unit: Datatype, leafdata: ndarray, rootdata: ndarray, op: Op
    ) -> None:
        """End a reduction operation started with `reduceBegin`.

        Collective.

        Parameters
        ----------
        unit
            MPI datatype.
        leafdata
            Values to reduce.
        rootdata
            Result of reduction of values from all leaves of each root.
        op
            MPI reduction operation.

        See Also
        --------
        reduceBegin, petsc.PetscSFReduceEnd
        """
        ...

    def scatterBegin(
        self, unit: Datatype, multirootdata: ndarray, leafdata: ndarray
    ) -> None:
        """Begin pointwise scatter operation.

        Collective.

        Operation is from multi-roots to leaves.
        This call has to be completed with `scatterEnd`.

        Parameters
        ----------
        unit
            MPI datatype.
        multirootdata
            Root buffer to send to each leaf, one unit of data per leaf.
        leafdata
            Leaf data to be updated with personal data from each respective root.

        See Also
        --------
        scatterEnd, petsc.PetscSFScatterBegin
        """
        ...

    def scatterEnd(
        self, unit: Datatype, multirootdata: ndarray, leafdata: ndarray
    ) -> None:
        """End scatter operation that was started with `scatterBegin`.

        Collective.

        Parameters
        ----------
        unit
            MPI datatype.
        multirootdata
            Root buffer to send to each leaf, one unit of data per leaf.
        leafdata
            Leaf data to be updated with personal data from each respective root.

        See Also
        --------
        scatterBegin, petsc.PetscSFScatterEnd
        """
        ...

    def gatherBegin(
        self, unit: Datatype, leafdata: ndarray, multirootdata: ndarray
    ) -> None:
        """Begin pointwise gather of all leaves into multi-roots.

        Collective.

        This call has to be completed with `gatherEnd`.

        Parameters
        ----------
        unit
            MPI datatype.
        leafdata
            Leaf data to gather to roots.
        multirootdata
            Root buffer to gather into, amount of space per root is
            equal to its degree.

        See Also
        --------
        gatherEnd, petsc.PetscSFGatherBegin
        """
        ...

    def gatherEnd(
        self, unit: Datatype, leafdata: ndarray, multirootdata: ndarray
    ) -> None:
        """End gather operation that was started with `gatherBegin`.

        Collective.

        Parameters
        ----------
        unit
            MPI datatype.
        leafdata
            Leaf data to gather to roots.
        multirootdata
            Root buffer to gather into, amount of space per root is
            equal to its degree.

        See Also
        --------
        gatherBegin, petsc.PetscSFGatherEnd
        """
        ...

    def fetchAndOpBegin(
        self,
        unit: Datatype,
        rootdata: ndarray,
        leafdata: ndarray,
        leafupdate: ndarray,
        op: Op,
    ) -> None:
        """Begin fetch and update operation.

        Collective.

        This operation fetches values from root and updates atomically
        by applying an operation using the leaf value.

        This call has to be completed with `fetchAndOpEnd`.

        Parameters
        ----------
        unit
            MPI datatype.
        rootdata
            Root values to be updated, input state is seen by first process
            to perform an update.
        leafdata
            Leaf values to use in reduction.
        leafupdate
            State at each leaf's respective root immediately prior to my atomic
            update.
        op
            MPI reduction operation.

        See Also
        --------
        fetchAndOpEnd, petsc.PetscSFFetchAndOpBegin
        """
        ...

    def fetchAndOpEnd(
        self,
        unit: Datatype,
        rootdata: ndarray,
        leafdata: ndarray,
        leafupdate: ndarray,
        op: Op,
    ) -> None:
        """End operation started in a matching call to `fetchAndOpBegin`.

        Collective.

        Parameters
        ----------
        unit
            MPI datatype.
        rootdata
            Root values to be updated, input state is seen by first process
            to perform an update.
        leafdata
            Leaf values to use in reduction.
        leafupdate
            State at each leaf's respective root immediately prior to my atomic
            update.
        op
            MPI reduction operation.

        See Also
        --------
        fetchAndOpBegin, petsc.PetscSFFetchAndOpEnd
        """
        ...

__all__ = [
    "SF",
    "SFType",
]
