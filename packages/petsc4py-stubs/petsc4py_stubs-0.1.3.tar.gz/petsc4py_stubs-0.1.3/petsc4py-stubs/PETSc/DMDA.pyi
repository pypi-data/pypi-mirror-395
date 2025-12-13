"""Type stubs for PETSc DMDA module."""


from typing import Any, Sequence, Self

# Import types from other modules
from .DM import DM, DMBoundaryType, InsertModeSpec
from .Comm import Comm
from .Vec import Vec
from .Scatter import Scatter
from .AO import AO

# Import types from typing module
from petsc4py.typing import ArrayInt, DimsSpec

class DMDAStencilType:
    """DMDA Stencil types."""

    STAR: int
    BOX: int

class DMDAInterpolationType:
    """DMDA Interpolation types."""

    Q0: int
    Q1: int

class DMDAElementType:
    """DMDA Element types."""

    P1: int
    Q1: int

class DMDA(DM):
    """A DM object that is used to manage data for a structured grid.

    DMDA is used for working with structured grids (arrays) in parallel.
    It manages the ghost point communication needed for finite difference
    or finite element stencil operations.
    """

    StencilType = DMDAStencilType
    InterpolationType = DMDAInterpolationType
    ElementType = DMDAElementType

    def create(
        self,
        dim: int | Sequence[int] | None = None,
        dof: int | None = None,
        sizes: DimsSpec | None = None,
        proc_sizes: DimsSpec | None = None,
        boundary_type: Sequence[DMBoundaryType | int | str | bool] | None = None,
        stencil_type: DMDAStencilType | int | str | None = None,
        stencil_width: int | None = None,
        setup: bool = True,
        ownership_ranges: Sequence[Sequence[int]] | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a DMDA object.

        Parameters
        ----------
        dim
            The number of dimensions.
        dof
            The number of degrees of freedom.
        sizes
            The number of elements in each dimension.
        proc_sizes
            The number of processes in x, y, z dimensions.
        boundary_type
            The boundary types.
        stencil_type
            The ghost/halo stencil type.
        stencil_width
            The width of the ghost/halo region.
        setup
            Whether to call the setup routine after creating the object.
        ownership_ranges
            Local x, y, z element counts, of length equal to ``proc_sizes``,
            summing to ``sizes``.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def duplicate(
        self,
        dof: int | None = None,
        boundary_type: tuple[DMBoundaryType | int | str | bool, ...] | None = None,
        stencil_type: DMDAStencilType | int | str | None = None,
        stencil_width: int | None = None,
    ) -> DMDA:
        """Duplicate a DMDA.

        Parameters
        ----------
        dof
            The number of degrees of freedom.
        boundary_type
            Boundary types.
        stencil_type
            The ghost/halo stencil type.
        stencil_width
            The width of the ghost/halo region.
        """
        ...

    def setDim(self, dim: int) -> None:
        """Set the topological dimension."""
        ...

    def getDim(self) -> int:
        """Return the topological dimension."""
        ...

    def setDof(self, dof: int) -> None:
        """Set the number of degrees of freedom per vertex."""
        ...

    def getDof(self) -> int:
        """Return the number of degrees of freedom per node."""
        ...

    def setSizes(self, sizes: DimsSpec) -> None:
        """Set the number of grid points in each dimension."""
        ...

    def getSizes(self) -> tuple[int, ...]:
        """Return the number of grid points in each dimension."""
        ...

    def setProcSizes(self, proc_sizes: DimsSpec) -> None:
        """Set the number of processes in each dimension."""
        ...

    def getProcSizes(self) -> tuple[int, ...]:
        """Return the number of processes in each dimension."""
        ...

    def setBoundaryType(
        self, boundary_type: tuple[DMBoundaryType | int | str | bool, ...]
    ) -> None:
        """Set the type of ghost nodes on domain boundaries."""
        ...

    def getBoundaryType(self) -> tuple[int, ...]:
        """Return the type of ghost nodes at boundary in each dimension."""
        ...

    def setStencilType(self, stencil_type: DMDAStencilType | int | str) -> None:
        """Set the stencil type."""
        ...

    def getStencilType(self) -> int:
        """Return the stencil type."""
        ...

    def setStencilWidth(self, stencil_width: int) -> None:
        """Set the stencil width."""
        ...

    def getStencilWidth(self) -> int:
        """Return the stencil width."""
        ...

    def setStencil(
        self, stencil_type: DMDAStencilType | int | str, stencil_width: int
    ) -> None:
        """Set the stencil type and width."""
        ...

    def getStencil(self) -> tuple[int, int]:
        """Return the stencil type and width."""
        ...

    def getRanges(self) -> tuple[tuple[int, int], ...]:
        """Return the ranges of the owned local region in each dimension.

        Excluding ghost nodes.
        """
        ...

    def getGhostRanges(self) -> tuple[tuple[int, int], ...]:
        """Return the ranges of the local region in each dimension, including ghost nodes."""
        ...

    def getOwnershipRanges(self) -> tuple[ArrayInt, ...]:
        """Return the ranges of indices in each dimension owned by each process."""
        ...

    def getCorners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Return the lower left corner and the sizes of the owned local region.

        Returns the global (x,y,z) indices of the lower left corner (first
        tuple) and size of the local region (second tuple).
        Excluding ghost points.
        """
        ...

    def getGhostCorners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Return the lower left corner and the size of the ghosted local region.

        Returns the global (x,y,z) indices of the lower left corner (first
        tuple) and size of the local region (second tuple).
        """
        ...

    def setFieldName(self, field: int, name: str) -> None:
        """Set the name of individual field components.

        Parameters
        ----------
        field
            The field number for the DMDA (0, 1, ..., dof-1).
        name
            The name of the field (component).
        """
        ...

    def getFieldName(self, field: int) -> str:
        """Return the name of an individual field component.

        Parameters
        ----------
        field
            The field number for the DMDA (0, 1, ..., dof-1).
        """
        ...

    def getVecArray(self, vec: Vec, readonly: bool = False) -> Any:
        """Get access to the vector as laid out on a N-d grid.

        Parameters
        ----------
        vec
            The vector to which access is being requested.
        readonly
            Request read-only access.
        """
        ...

    def setUniformCoordinates(
        self,
        xmin: float = 0,
        xmax: float = 1,
        ymin: float = 0,
        ymax: float = 1,
        zmin: float = 0,
        zmax: float = 1,
    ) -> None:
        """Set the DMDA coordinates to be a uniform grid.

        Parameters
        ----------
        xmin
            The minimum in the x dimension.
        xmax
            The maximum in the x dimension.
        ymin
            The minimum in the y dimension.
        ymax
            The maximum in the y dimension.
        zmin
            The minimum in the z dimension.
        zmax
            The maximum in the z dimension.
        """
        ...

    def setCoordinateName(self, index: int, name: str) -> None:
        """Set the name of the coordinate dimension.

        Parameters
        ----------
        index
            The coordinate number for the DMDA (0, 1, ..., dim-1).
        name
            The name of the coordinate.
        """
        ...

    def getCoordinateName(self, index: int) -> str:
        """Return the name of a coordinate dimension.

        Parameters
        ----------
        index
            The coordinate number for the DMDA (0, 1, ..., dim-1).
        """
        ...

    def createNaturalVec(self) -> Vec:
        """Create a vector that will hold values in the natural numbering."""
        ...

    def globalToNatural(self, vg: Vec, vn: Vec, addv: InsertModeSpec = None) -> None:
        """Map values to the "natural" grid ordering.

        Parameters
        ----------
        vg
            The global vector in a grid ordering.
        vn
            The global vector in a "natural" ordering.
        addv
            The insertion mode.
        """
        ...

    def naturalToGlobal(self, vn: Vec, vg: Vec, addv: InsertModeSpec = None) -> None:
        """Map values the to grid ordering.

        Parameters
        ----------
        vn
            The global vector in a natural ordering.
        vg
            the global vector in a grid ordering.
        addv
            The insertion mode.
        """
        ...

    def getAO(self) -> AO:
        """Return the application ordering context for a distributed array."""
        ...

    def getScatter(self) -> tuple[Scatter, Scatter]:
        """Return the global-to-local, and local-to-local scatter contexts."""
        ...

    def setRefinementFactor(
        self, refine_x: int = 2, refine_y: int = 2, refine_z: int = 2
    ) -> None:
        """Set the ratios for the DMDA grid refinement.

        Parameters
        ----------
        refine_x
            Ratio of fine grid to coarse in x dimension.
        refine_y
            Ratio of fine grid to coarse in y dimension.
        refine_z
            Ratio of fine grid to coarse in z dimension.
        """
        ...

    def getRefinementFactor(self) -> tuple[int, ...]:
        """Return the ratios that the DMDA grid is refined in each dimension."""
        ...

    def setInterpolationType(
        self, interp_type: DMDAInterpolationType | int | str
    ) -> None:
        """Set the type of interpolation.

        Parameters
        ----------
        interp_type
            The interpolation type.
        """
        ...

    def getInterpolationType(self) -> int:
        """Return the type of interpolation."""
        ...

    def setElementType(self, elem_type: DMDAElementType | int | str) -> None:
        """Set the element type to be returned by getElements."""
        ...

    def getElementType(self) -> int:
        """Return the element type to be returned by getElements."""
        ...

    def getElements(
        self, elem_type: DMDAElementType | int | str | None = None
    ) -> ArrayInt:
        """Return an array containing the indices of all the local elements.

        Parameters
        ----------
        elem_type
            The element type.
        """
        ...

    # Properties
    @property
    def dim(self) -> int:
        """The grid dimension."""
        ...

    @property
    def dof(self) -> int:
        """The number of DOFs associated with each stratum of the grid."""
        ...

    @property
    def sizes(self) -> tuple[int, ...]:
        """The global dimension."""
        ...

    @property
    def proc_sizes(self) -> tuple[int, ...]:
        """The number of processes in each dimension in the global decomposition."""
        ...

    @property
    def boundary_type(self) -> tuple[int, ...]:
        """Boundary types in each dimension."""
        ...

    @property
    def stencil(self) -> tuple[int, int]:
        """Stencil type and width."""
        ...

    @property
    def stencil_type(self) -> int:
        """Stencil type."""
        ...

    @property
    def stencil_width(self) -> int:
        """Elementwise stencil width."""
        ...

    @property
    def ranges(self) -> tuple[tuple[int, int], ...]:
        """Ranges of the local region in each dimension."""
        ...

    @property
    def ghost_ranges(self) -> tuple[tuple[int, int], ...]:
        """Ranges of local region, including ghost nodes."""
        ...

    @property
    def corners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """The lower left corner and size of local region in each dimension."""
        ...

    @property
    def ghost_corners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """The lower left corner and size of local region in each dimension."""
        ...

    # Backward compatibility alias
    createNaturalVector = createNaturalVec

# Backward compatibility alias
DA = DMDA
