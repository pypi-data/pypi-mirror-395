"""Type stubs for PETSc Error module."""




class Error(RuntimeError):
    """PETSc Error.

    Attributes
    ----------
    ierr : int
        PETSc error code.

    See Also
    --------
    petsc.PetscError
    """

    ierr: int
    """PETSc error code."""

    _traceback: list[str]
    """List of traceback entries."""

    def __init__(self, ierr: int = 0) -> None:
        """Initialize a PETSc error.

        Parameters
        ----------
        ierr
            PETSc error code.
        """
        ...

    def __bool__(self) -> bool:
        """Return whether the error code is non-zero."""
        ...

    def __repr__(self) -> str:
        """Return the representation of the error."""
        ...

    def __str__(self) -> str:
        """Return the string representation of the error."""
        ...
