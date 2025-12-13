"""Type stubs for PETSc AO (Application Ordering) module."""


from typing import Sequence, Self

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .IS import IS

class AOType:
    """The application ordering types."""

    BASIC: str
    ADVANCED: str
    MAPPING: str
    MEMORYSCALABLE: str

class AO(Object):
    """Application ordering object.

    AO objects map between an application-defined ordering and a PETSc ordering.
    This allows application code to work with a natural ordering while PETSc uses
    a different ordering that may be more efficient for computations.

    See Also
    --------
    petsc.AO
    """

    Type = AOType

    def view(self, viewer: Viewer | None = None) -> None:
        """Display the application ordering.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the ordering.

        See Also
        --------
        petsc.AOView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the application ordering.

        Collective.

        See Also
        --------
        petsc.AODestroy
        """
        ...

    def createBasic(
        self,
        app: Sequence[int] | IS,
        petsc: Sequence[int] | IS | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Return a basic application ordering using two orderings.

        Collective.

        The arrays/indices ``app`` and ``petsc`` must contain all the integers
        ``0`` to ``len(app)-1`` with no duplicates; that is there cannot be any
        "holes" in the indices. Use ``createMapping`` if you wish to have
        "holes" in the indices.

        Parameters
        ----------
        app
            The application ordering.
        petsc
            Another ordering (may be `None` to indicate the natural ordering,
            that is 0, 1, 2, 3, ...).
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        createMemoryScalable, createMapping, petsc.AOCreateBasicIS
        petsc.AOCreateBasic
        """
        ...

    def createMemoryScalable(
        self,
        app: Sequence[int] | IS,
        petsc: Sequence[int] | IS | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Return a memory scalable application ordering using two orderings.

        Collective.

        The arrays/indices ``app`` and ``petsc`` must contain all the integers
        ``0`` to ``len(app)-1`` with no duplicates; that is there cannot be any
        "holes" in the indices. Use ``createMapping`` if you wish to have
        "holes" in the indices.

        Comparing with ``createBasic``, this routine trades memory with message
        communication.

        Parameters
        ----------
        app
            The application ordering.
        petsc
            Another ordering (may be `None` to indicate the natural ordering,
            that is 0, 1, 2, 3, ...).
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        createBasic, createMapping, petsc.AOCreateMemoryScalableIS
        petsc.AOCreateMemoryScalable
        """
        ...

    def createMapping(
        self,
        app: Sequence[int] | IS,
        petsc: Sequence[int] | IS | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Return an application mapping using two orderings.

        Collective.

        The arrays ``app`` and ``petsc`` need NOT contain all the integers
        ``0`` to ``len(app)-1``, that is there CAN be "holes" in the indices.
        Use ``createBasic`` if they do not have holes for better performance.

        Parameters
        ----------
        app
            The application ordering.
        petsc
            Another ordering. May be `None` to indicate the identity ordering.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        createBasic, petsc.AOCreateMappingIS, petsc.AOCreateMapping
        """
        ...

    def getType(self) -> str:
        """Return the application ordering type.

        Not collective.

        See Also
        --------
        petsc.AOGetType
        """
        ...

    def app2petsc(self, indices: Sequence[int] | IS) -> Sequence[int] | IS:
        """Map an application-defined ordering to the PETSc ordering.

        Collective.

        Any integers in ``indices`` that are negative are left unchanged. This
        allows one to convert, for example, neighbor lists that use negative
        entries to indicate nonexistent neighbors due to boundary conditions,
        etc.

        Integers that are out of range are mapped to -1.

        If ``IS`` is used, it cannot be of type stride or block.

        Parameters
        ----------
        indices
            The indices; to be replaced with their mapped values.

        See Also
        --------
        petsc2app, petsc.AOApplicationToPetscIS, petsc.AOApplicationToPetsc
        """
        ...

    def petsc2app(self, indices: Sequence[int] | IS) -> Sequence[int] | IS:
        """Map a PETSc ordering to the application-defined ordering.

        Collective.

        Any integers in ``indices`` that are negative are left unchanged. This
        allows one to convert, for example, neighbor lists that use negative
        entries to indicate nonexistent neighbors due to boundary conditions,
        etc.

        Integers that are out of range are mapped to -1.

        If ``IS`` is used, it cannot be of type stride or block.

        Parameters
        ----------
        indices
            The indices; to be replaced with their mapped values.

        See Also
        --------
        app2petsc, petsc.AOPetscToApplicationIS, petsc.AOPetscToApplication
        """
        ...

__all__ = [
    "AO",
    "AOType",
]
