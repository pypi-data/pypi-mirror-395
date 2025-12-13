"""Type stubs for PETSc DMComposite module."""


from typing import (
    Any,
    Literal,
    Sequence,
    Self
)

# Import types from other modules
from .DM import DM
from .IS import IS, LGMap

from .Comm import Comm
from .Vec import Vec

# Import types from typing module
from petsc4py.typing import InsertModeSpec


class DMComposite(DM):
    """A DM object that is used to manage data for a collection of DMs.
    
    DMComposite is used to couple multiple DM objects together, typically
    for multi-physics simulations where different fields may live on
    different meshes or have different discretizations.
    """

    def create(self, comm: Comm | None = None) -> Self:
        """Create a composite object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def addDM(self, dm: DM, *args: DM) -> None:
        """Add a DM vector to the composite.

        Collective.

        Parameters
        ----------
        dm
            The DM object.
        *args
            Additional DM objects.
        """
        ...

    def getNumber(self) -> int:
        """Get number of sub-DMs contained in the composite.

        Not collective.
        """
        ...

    # Alias for getNumber
    getNumberDM = getNumber

    def getEntries(self) -> list[DM]:
        """Return sub-DMs contained in the composite.

        Not collective.
        """
        ...

    def scatter(self, gvec: Vec, lvecs: Sequence[Vec]) -> None:
        """Scatter coupled global vector into split local vectors.

        Collective.

        Parameters
        ----------
        gvec
            The global vector.
        lvecs
            Array of local vectors.

        See Also
        --------
        gather
        """
        ...

    def gather(self, gvec: Vec, imode: InsertModeSpec, lvecs: Sequence[Vec]) -> None:
        """Gather split local vectors into a coupled global vector.

        Collective.

        Parameters
        ----------
        gvec
            The global vector.
        imode
            The insertion mode.
        lvecs
            The individual sequential vectors.

        See Also
        --------
        scatter
        """
        ...

    def getGlobalISs(self) -> list[IS]:
        """Return the index sets for each composed object in the composite.

        Collective.

        These could be used to extract a subset of vector entries for a
        "multi-physics" preconditioner.

        Use getLocalISs for index sets in the packed local numbering, and
        getLGMaps for to map local sub-DM (including ghost) indices to packed
        global indices.

        See Also
        --------
        getLocalISs, getLGMaps
        """
        ...

    def getLocalISs(self) -> list[IS]:
        """Return index sets for each component of a composite local vector.

        Not collective.

        To get the composite global indices at all local points (including
        ghosts), use getLGMaps.

        To get index sets for pieces of the composite global vector, use
        getGlobalISs.

        See Also
        --------
        getGlobalISs, getLGMaps
        """
        ...

    def getLGMaps(self) -> list[LGMap]:
        """Return a local-to-global mapping for each DM in the composite.

        Collective.

        Note that this includes all the ghost points that individual ghosted
        DMDA may have.

        See Also
        --------
        getGlobalISs, getLocalISs
        """
        ...

    def getAccess(self, gvec: Vec, locs: Sequence[int] | None = None) -> Any:
        """Get access to the individual vectors from the global vector.

        Not collective.

        Use via ``with`` context manager (PEP 343).

        Parameters
        ----------
        gvec
            The global vector.
        locs
            Indices of vectors wanted, or None to get all vectors.

        Examples
        --------
        >>> with composite.getAccess(gvec) as vecs:
        ...     # vecs is a list of individual Vec objects
        ...     for vec in vecs:
        ...         # process each vector
        ...         pass
        """
        ...
