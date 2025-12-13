"""Type stubs for PETSc DMShell module."""


from typing import Any, Callable, Sequence, Self

# Import types from other modules
from .DM import DM, InsertModeSpec
from .IS import IS
from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Scatter import Scatter

class DMShell(DM):
    """A shell DM object, used to manage user-defined problem data.

    DMShell is used to create a user-defined DM where the user provides
    the routines for creating vectors, matrices, and other operations.
    """

    def create(self, comm: Comm | None = None) -> Self:
        """Create a shell DM object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setMatrix(self, mat: Mat) -> None:
        """Set a template matrix.

        Collective.

        Parameters
        ----------
        mat
            The template matrix.
        """
        ...

    def setGlobalVector(self, gv: Vec) -> None:
        """Set a template global vector.

        Logically collective.

        Parameters
        ----------
        gv
            Template vector.
        """
        ...

    def setLocalVector(self, lv: Vec) -> None:
        """Set a template local vector.

        Logically collective.

        Parameters
        ----------
        lv
            Template vector.
        """
        ...

    def setCreateGlobalVector(
        self,
        create_gvec: Callable[[DM], Vec] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine to create a global vector.

        Logically collective.

        Parameters
        ----------
        create_gvec
            The creation routine.
        args
            Additional positional arguments for ``create_gvec``.
        kargs
            Additional keyword arguments for ``create_gvec``.
        """
        ...

    def setCreateLocalVector(
        self,
        create_lvec: Callable[[DM], Vec] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine to create a local vector.

        Logically collective.

        Parameters
        ----------
        create_lvec
            The creation routine.
        args
            Additional positional arguments for ``create_lvec``.
        kargs
            Additional keyword arguments for ``create_lvec``.
        """
        ...

    def setGlobalToLocal(
        self,
        begin: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        end: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        begin_args: tuple[Any, ...] | None = None,
        begin_kargs: dict[str, Any] | None = None,
        end_args: tuple[Any, ...] | None = None,
        end_kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routines used to perform a global to local scatter.

        Logically collective.

        Parameters
        ----------
        begin
            The routine which begins the global to local scatter.
        end
            The routine which ends the global to local scatter.
        begin_args
            Additional positional arguments for ``begin``.
        begin_kargs
            Additional keyword arguments for ``begin``.
        end_args
            Additional positional arguments for ``end``.
        end_kargs
            Additional keyword arguments for ``end``.
        """
        ...

    def setGlobalToLocalVecScatter(self, gtol: Scatter) -> None:
        """Set a Scatter context for global to local communication.

        Logically collective.

        Parameters
        ----------
        gtol
            The global to local Scatter context.
        """
        ...

    def setLocalToGlobal(
        self,
        begin: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        end: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        begin_args: tuple[Any, ...] | None = None,
        begin_kargs: dict[str, Any] | None = None,
        end_args: tuple[Any, ...] | None = None,
        end_kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routines used to perform a local to global scatter.

        Logically collective.

        Parameters
        ----------
        begin
            The routine which begins the local to global scatter.
        end
            The routine which ends the local to global scatter.
        begin_args
            Additional positional arguments for ``begin``.
        begin_kargs
            Additional keyword arguments for ``begin``.
        end_args
            Additional positional arguments for ``end``.
        end_kargs
            Additional keyword arguments for ``end``.
        """
        ...

    def setLocalToGlobalVecScatter(self, ltog: Scatter) -> None:
        """Set a Scatter context for local to global communication.

        Logically collective.

        Parameters
        ----------
        ltog
            The local to global Scatter context.
        """
        ...

    def setLocalToLocal(
        self,
        begin: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        end: Callable[[DM, Vec, InsertModeSpec, Vec], None] | None,
        begin_args: tuple[Any, ...] | None = None,
        begin_kargs: dict[str, Any] | None = None,
        end_args: tuple[Any, ...] | None = None,
        end_kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routines used to perform a local to local scatter.

        Logically collective.

        Parameters
        ----------
        begin
            The routine which begins the local to local scatter.
        end
            The routine which ends the local to local scatter.
        begin_args
            Additional positional arguments for ``begin``.
        begin_kargs
            Additional keyword arguments for ``begin``.
        end_args
            Additional positional arguments for ``end``.
        end_kargs
            Additional keyword arguments for ``end``.
        """
        ...

    def setLocalToLocalVecScatter(self, ltol: Scatter) -> None:
        """Set a Scatter context for local to local communication.

        Logically collective.

        Parameters
        ----------
        ltol
            The local to local Scatter context.
        """
        ...

    def setCreateMatrix(
        self,
        create_matrix: Callable[[DM], Mat] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine to create a matrix.

        Logically collective.

        Parameters
        ----------
        create_matrix
            The function to create a matrix.
        args
            Additional positional arguments for ``create_matrix``.
        kargs
            Additional keyword arguments for ``create_matrix``.
        """
        ...

    def setCoarsen(
        self,
        coarsen: Callable[[DM, Comm], DM] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to coarsen the DMShell.

        Logically collective.

        Parameters
        ----------
        coarsen
            The routine which coarsens the DM.
        args
            Additional positional arguments for ``coarsen``.
        kargs
            Additional keyword arguments for ``coarsen``.
        """
        ...

    def setRefine(
        self,
        refine: Callable[[DM, Comm], DM] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to refine the DMShell.

        Logically collective.

        Parameters
        ----------
        refine
            The routine which refines the DM.
        args
            Additional positional arguments for ``refine``.
        kargs
            Additional keyword arguments for ``refine``.
        """
        ...

    def setCreateInterpolation(
        self,
        create_interpolation: Callable[[DM, DM], tuple[Mat, Vec]] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create the interpolation operator.

        Logically collective.

        Parameters
        ----------
        create_interpolation
            The routine to create the interpolation.
        args
            Additional positional arguments for ``create_interpolation``.
        kargs
            Additional keyword arguments for ``create_interpolation``.
        """
        ...

    def setCreateInjection(
        self,
        create_injection: Callable[[DM, DM], Mat] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create the injection operator.

        Logically collective.

        Parameters
        ----------
        create_injection
            The routine to create the injection.
        args
            Additional positional arguments for ``create_injection``.
        kargs
            Additional keyword arguments for ``create_injection``.
        """
        ...

    def setCreateRestriction(
        self,
        create_restriction: Callable[[DM, DM], Mat] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create the restriction operator.

        Logically collective.

        Parameters
        ----------
        create_restriction
            The routine to create the restriction.
        args
            Additional positional arguments for ``create_restriction``.
        kargs
            Additional keyword arguments for ``create_restriction``.
        """
        ...

    def setCreateFieldDecomposition(
        self,
        decomp: Callable[
            [DM], tuple[list[str] | None, list[IS] | None, list[DM] | None]
        ]
        | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create a field decomposition.

        Logically collective.

        Parameters
        ----------
        decomp
            The routine to create the decomposition.
        args
            Additional positional arguments for ``decomp``.
        kargs
            Additional keyword arguments for ``decomp``.
        """
        ...

    def setCreateDomainDecomposition(
        self,
        decomp: Callable[
            [DM],
            tuple[list[str] | None, list[IS] | None, list[IS] | None, list[DM] | None],
        ]
        | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create a domain decomposition.

        Logically collective.

        Parameters
        ----------
        decomp
            The routine to create the decomposition.
        args
            Additional positional arguments for ``decomp``.
        kargs
            Additional keyword arguments for ``decomp``.
        """
        ...

    def setCreateDomainDecompositionScatters(
        self,
        scatter: Callable[
            [DM, list[DM]], tuple[list[Scatter], list[Scatter], list[Scatter]]
        ]
        | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create the scatter contexts for domain decomposition.

        Logically collective.

        Parameters
        ----------
        scatter
            The routine to create the scatters.
        args
            Additional positional arguments for ``scatter``.
        kargs
            Additional keyword arguments for ``scatter``.
        """
        ...

    def setCreateSubDM(
        self,
        create_subdm: Callable[[DM, Sequence[int]], tuple[IS, DM]] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine used to create a sub DM from the DMShell.

        Logically collective.

        Parameters
        ----------
        create_subdm
            The routine to create the sub DM.
        args
            Additional positional arguments for ``create_subdm``.
        kargs
            Additional keyword arguments for ``create_subdm``.
        """
        ...
