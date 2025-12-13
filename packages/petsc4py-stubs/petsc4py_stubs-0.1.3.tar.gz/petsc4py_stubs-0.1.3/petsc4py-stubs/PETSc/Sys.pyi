"""Type stubs for PETSc Sys module."""


from typing import Any

from .Comm import Comm

class Sys:
    """System utilities.

    See Also
    --------
    petsc.PetscSys
    """

    @classmethod
    def getVersion(
        cls,
        devel: bool = False,
        date: bool = False,
        author: bool = False,
    ) -> tuple[int, int, int] | tuple[tuple[int, int, int], ...]:
        """Return PETSc version information.

        Not collective.

        Parameters
        ----------
        devel
            Additionally, return whether using an in-development version.
        date
            Additionally, return date information.
        author
            Additionally, return author information.

        Returns
        -------
        major : int
            Major version number.
        minor : int
            Minor version number.
        micro : int
            Micro (or patch) version number.

        See Also
        --------
        petsc.PetscGetVersion, petsc.PetscGetVersionNumber
        """
        ...

    @classmethod
    def getVersionInfo(cls) -> dict[str, bool | int | str | tuple[str, ...]]:
        """Return PETSc version information.

        Not collective.

        Returns
        -------
        info : dict
            Dictionary with version information.

        See Also
        --------
        petsc.PetscGetVersion, petsc.PetscGetVersionNumber
        """
        ...

    @classmethod
    def isInitialized(cls) -> bool:
        """Return whether PETSc has been initialized.

        Not collective.

        See Also
        --------
        isFinalized
        """
        ...

    @classmethod
    def isFinalized(cls) -> bool:
        """Return whether PETSc has been finalized.

        Not collective.

        See Also
        --------
        isInitialized
        """
        ...

    @classmethod
    def getDefaultComm(cls) -> Comm:
        """Get the default MPI communicator used to create PETSc objects.

        Not collective.

        See Also
        --------
        setDefaultComm
        """
        ...

    @classmethod
    def setDefaultComm(cls, comm: Comm | None) -> None:
        """Set the default MPI communicator used to create PETSc objects.

        Logically collective.

        Parameters
        ----------
        comm
            MPI communicator. If set to `None`, uses `COMM_WORLD`.

        See Also
        --------
        getDefaultComm
        """
        ...

    @classmethod
    def Print(
        cls,
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        comm: Comm | None = None,
        **kwargs: Any,
    ) -> None:
        """Print output from the first processor of a communicator.

        Collective.

        Parameters
        ----------
        *args
            Positional arguments.
        sep
            String inserted between values, by default a space.
        end
            String appended after the last value, by default a newline.
        comm
            MPI communicator, defaults to `getDefaultComm`.
        **kwargs
            Keyword arguments.

        See Also
        --------
        petsc.PetscPrintf
        """
        ...

    @classmethod
    def syncPrint(
        cls,
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
        comm: Comm | None = None,
        **kwargs: Any,
    ) -> None:
        """Print synchronized output from several processors of a communicator.

        Not collective.

        Parameters
        ----------
        *args
            Positional arguments.
        sep
            String inserted between values, by default a space.
        end
            String appended after the last value, by default a newline.
        flush
            Whether to flush output with `syncFlush`.
        comm
            MPI communicator, defaults to `getDefaultComm`.
        **kwargs
            Keyword arguments.

        See Also
        --------
        petsc.PetscSynchronizedPrintf, petsc.PetscSynchronizedFlush
        """
        ...

    @classmethod
    def syncFlush(cls, comm: Comm | None = None) -> None:
        """Flush output from previous `syncPrint` calls.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `getDefaultComm`.

        See Also
        --------
        petsc.PetscSynchronizedPrintf, petsc.PetscSynchronizedFlush
        """
        ...

    @classmethod
    def splitOwnership(
        cls,
        size: int | tuple[int, int],
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> tuple[int, int]:
        """Given a global (or local) size determines a local (or global) size.

        Collective.

        Parameters
        ----------
        size
            Global size ``N`` or 2-tuple ``(n, N)`` with local and global
            sizes. Either of ``n`` or ``N`` (but not both) can be `None`.
        bsize
            Block size, defaults to ``1``.
        comm
            MPI communicator, defaults to `getDefaultComm`.

        Returns
        -------
        n : int
            The local size.
        N : int
            The global size.

        Notes
        -----
        The ``size`` argument corresponds to the full size of the
        vector. That is, an array with 10 blocks and a block size of 3 will
        have a ``size`` of 30, not 10.

        See Also
        --------
        petsc.PetscSplitOwnership
        """
        ...

    @classmethod
    def sleep(cls, seconds: float = 1.0) -> None:
        """Sleep some number of seconds.

        Not collective.

        Parameters
        ----------
        seconds
            Time to sleep in seconds.

        See Also
        --------
        petsc.PetscSleep
        """
        ...

    @classmethod
    def pushErrorHandler(cls, errhandler: str) -> None:
        """Set the current error handler.

        Logically collective.

        Parameters
        ----------
        errhandler
            The name of the error handler. Supported values are:
            ``"python"``, ``"debugger"``, ``"emacs"``, ``"traceback"``,
            ``"ignore"``, ``"mpiabort"``, ``"abort"``.

        See Also
        --------
        petsc.PetscPushErrorHandler
        """
        ...

    @classmethod
    def popErrorHandler(cls) -> None:
        """Remove the current error handler.

        Logically collective.

        See Also
        --------
        petsc.PetscPopErrorHandler
        """
        ...

    @classmethod
    def popSignalHandler(cls) -> None:
        """Remove the current signal handler.

        Logically collective.

        See Also
        --------
        petsc.PetscPopSignalHandler
        """
        ...

    @classmethod
    def infoAllow(
        cls,
        flag: bool,
        filename: str | None = None,
        mode: str = "w",
    ) -> None:
        """Enables or disables PETSc info messages.

        Not collective.

        Parameters
        ----------
        flag
            Whether to enable info messages.
        filename
            Name of a file where to dump output.
        mode
            Write mode for file, by default ``"w"``.

        See Also
        --------
        petsc.PetscInfoAllow, petsc.PetscInfoSetFile
        """
        ...

    @classmethod
    def registerCitation(cls, citation: str) -> None:
        """Register BibTeX citation.

        Not collective.

        Parameters
        ----------
        citation
            The BibTex citation entry to register.

        See Also
        --------
        petsc.PetscCitationsRegister
        """
        ...

    @classmethod
    def hasExternalPackage(cls, package: str) -> bool:
        """Return whether PETSc has support for external package.

        Not collective.

        Parameters
        ----------
        package
            The external package name.

        See Also
        --------
        petsc.PetscHasExternalPackage
        """
        ...
