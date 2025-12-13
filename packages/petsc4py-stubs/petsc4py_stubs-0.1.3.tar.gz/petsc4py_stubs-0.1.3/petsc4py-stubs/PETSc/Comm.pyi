"""Type stubs for PETSc Comm module."""


from typing import Any
from mpi4py.MPI import Intracomm

class Comm:
    """Communicator object.

    Predefined instances:

    `COMM_NULL`
        The *null* (or invalid) communicator.
    `COMM_SELF`
        The *self* communicator.
    `COMM_WORLD`
        The *world* communicator.

    See Also
    --------
    Sys.setDefaultComm, Sys.getDefaultComm

    """

    def __init__(self, comm: Comm | Any | None = None) -> None: ...
    def __bool__(self) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def destroy(self) -> None:
        """Destroy the communicator.

        Collective.

        See Also
        --------
        petsc.PetscCommDestroy

        """
        ...

    def duplicate(self) -> Comm:
        """Duplicate the communicator.

        Collective.

        See Also
        --------
        petsc.PetscCommDuplicate

        """
        ...

    def getSize(self) -> int:
        """Return the number of processes in the communicator.

        Not collective.

        """
        ...

    def getRank(self) -> int:
        """Return the rank of the calling processes in the communicator.

        Not collective.

        """
        ...

    def barrier(self) -> None:
        """Barrier synchronization.

        Collective.

        """
        ...

    # --- properties ---

    @property
    def size(self) -> int:
        """Communicator size."""
        ...

    @property
    def rank(self) -> int:
        """Communicator rank."""
        ...

    @property
    def fortran(self) -> int:
        """Fortran handle."""
        ...

    # --- mpi4py support ---

    def tompi4py(self) -> Intracomm:
        """Convert communicator to `mpi4py`.

        Not collective.

        See Also
        --------
        mpi4py.MPI.Comm, mpi4py.MPI.Intracomm

        """
        ...

    # --- mpi4py compatibility API ---

    Free = destroy
    Clone = duplicate
    Dup = duplicate
    Get_size = getSize
    Get_rank = getRank
    Barrier = barrier

# Predefined communicators
COMM_NULL: Comm
COMM_SELF: Comm
COMM_WORLD: Comm
