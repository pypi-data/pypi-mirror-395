"""Type stubs for PETSc DMStag module."""


from typing import Sequence, Self

# Import types from other modules
from .DM import DM, DMBoundaryType
from .DMDA import DMDA
from .Comm import Comm
from .Vec import Vec

class DMStagStencilType:
    """Stencil types for DMStag."""

    STAR: int
    BOX: int
    NONE: int

class DMStagStencilLocation:
    """Stencil location types for DMStag."""

    NULLLOC: int
    BACK_DOWN_LEFT: int
    BACK_DOWN: int
    BACK_DOWN_RIGHT: int
    BACK_LEFT: int
    BACK: int
    BACK_RIGHT: int
    BACK_UP_LEFT: int
    BACK_UP: int
    BACK_UP_RIGHT: int
    DOWN_LEFT: int
    DOWN: int
    DOWN_RIGHT: int
    LEFT: int
    ELEMENT: int
    RIGHT: int
    UP_LEFT: int
    UP: int
    UP_RIGHT: int
    FRONT_DOWN_LEFT: int
    FRONT_DOWN: int
    FRONT_DOWN_RIGHT: int
    FRONT_LEFT: int
    FRONT: int
    FRONT_RIGHT: int
    FRONT_UP_LEFT: int
    FRONT_UP: int
    FRONT_UP_RIGHT: int

class DMStag(DM):
    """A DM object representing a "staggered grid" or a structured cell complex.

    DMStag is used for working with staggered grids where different variables
    live on different parts of the grid (vertices, edges, faces, elements).
    """

    StencilType = DMStagStencilType
    StencilLocation = DMStagStencilLocation

    def create(
        self,
        dim: int,
        dofs: tuple[int, ...] | None = None,
        sizes: tuple[int, ...] | None = None,
        boundary_types: tuple[DMBoundaryType | int | str | bool, ...] | None = None,
        stencil_type: DMStagStencilType | int | str | None = None,
        stencil_width: int | None = None,
        proc_sizes: tuple[int, ...] | None = None,
        ownership_ranges: tuple[Sequence[int], ...] | None = None,
        comm: Comm | None = None,
        setUp: bool | None = False,
    ) -> Self:
        """Create a DMStag object.

        Collective.

        Creates an object to manage data living on the elements and vertices /
        the elements, faces, and vertices / the elements, faces, edges, and
        vertices of a parallelized regular 1D / 2D / 3D grid.

        Parameters
        ----------
        dim
            The number of dimensions.
        dofs
            The number of degrees of freedom per vertex, element (1D); vertex,
            face, element (2D); or vertex, edge, face, element (3D).
        sizes
            The number of elements in each dimension.
        boundary_types
            The boundary types.
        stencil_type
            The ghost/halo stencil type.
        stencil_width
            The width of the ghost/halo region.
        proc_sizes
            The number of processes in x, y, z dimensions.
        ownership_ranges
            Local x, y, z element counts, of length equal to ``proc_sizes``,
            summing to ``sizes``.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        setUp
            Whether to call the setup routine after creating the object.
        """
        ...

    # Setters

    def setStencilWidth(self, swidth: int) -> None:
        """Set elementwise stencil width.

        Logically collective.

        The width value is not used when StencilType.NONE is specified.

        Parameters
        ----------
        swidth
            Stencil/halo/ghost width in elements.
        """
        ...

    def setStencilType(self, stenciltype: DMStagStencilType | int | str) -> None:
        """Set elementwise ghost/halo stencil type.

        Logically collective.

        Parameters
        ----------
        stenciltype
            The elementwise ghost stencil type.
        """
        ...

    def setBoundaryTypes(
        self, boundary_types: tuple[DMBoundaryType | int | str | bool, ...]
    ) -> None:
        """Set the boundary types.

        Logically collective.

        Parameters
        ----------
        boundary_types
            Boundary types for one/two/three dimensions.
        """
        ...

    def setDof(self, dofs: tuple[int, ...]) -> None:
        """Set DOFs/stratum.

        Logically collective.

        Parameters
        ----------
        dofs
            The number of points per 0-cell (vertex/node), 1-cell (element in
            1D, edge in 2D and 3D), 2-cell (element in 2D, face in 3D), or
            3-cell (element in 3D).
        """
        ...

    def setGlobalSizes(self, sizes: tuple[int, ...]) -> None:
        """Set global element counts in each dimension.

        Logically collective.

        Parameters
        ----------
        sizes
            Global elementwise size in the one/two/three dimensions.
        """
        ...

    def setProcSizes(self, sizes: tuple[int, ...]) -> None:
        """Set the number of processes in each dimension in the global process grid.

        Logically collective.

        Parameters
        ----------
        sizes
            Number of processes in one/two/three dimensions.
        """
        ...

    def setOwnershipRanges(self, ranges: tuple[Sequence[int], ...]) -> None:
        """Set elements per process in each dimension.

        Logically collective.

        Parameters
        ----------
        ranges
            Element counts for each process in one/two/three dimensions.
        """
        ...

    # Getters

    def getDim(self) -> int:
        """Return the number of dimensions.

        Not collective.
        """
        ...

    def getEntriesPerElement(self) -> int:
        """Return the number of entries per element in the local representation.

        Not collective.

        This is the natural block size for most local operations.
        """
        ...

    def getStencilWidth(self) -> int:
        """Return elementwise stencil width.

        Not collective.
        """
        ...

    def getDof(self) -> tuple[int, ...]:
        """Get number of DOFs associated with each stratum of the grid.

        Not collective.
        """
        ...

    def getCorners(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        """Return starting element index, width and number of partial elements.

        Not collective.

        The returned value is calculated excluding ghost points.

        The number of extra partial elements is either 1 or 0. The value is 1
        on right, top, and front non-periodic domain ("physical") boundaries,
        in the x, y, and z dimensions respectively, and otherwise 0.
        """
        ...

    def getGhostCorners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Return starting element index and width of local region.

        Not collective.
        """
        ...

    def getLocalSizes(self) -> tuple[int, ...]:
        """Return local elementwise sizes in each dimension.

        Not collective.

        The returned value is calculated excluding ghost points.
        """
        ...

    def getGlobalSizes(self) -> tuple[int, ...]:
        """Return global element counts in each dimension.

        Not collective.
        """
        ...

    def getProcSizes(self) -> tuple[int, ...]:
        """Return number of processes in each dimension.

        Not collective.
        """
        ...

    def getStencilType(self) -> str:
        """Return elementwise ghost/halo stencil type.

        Not collective.
        """
        ...

    def getOwnershipRanges(self) -> tuple[Sequence[int], ...]:
        """Return elements per process in each dimension.

        Not collective.
        """
        ...

    def getBoundaryTypes(self) -> tuple[str, ...]:
        """Return boundary types in each dimension.

        Not collective.
        """
        ...

    def getIsFirstRank(self) -> tuple[int, ...]:
        """Return whether this process is first in each dimension in the process grid.

        Not collective.
        """
        ...

    def getIsLastRank(self) -> tuple[int, ...]:
        """Return whether this process is last in each dimension in the process grid.

        Not collective.
        """
        ...

    # Coordinate-related functions

    def setUniformCoordinatesExplicit(
        self,
        xmin: float = 0,
        xmax: float = 1,
        ymin: float = 0,
        ymax: float = 1,
        zmin: float = 0,
        zmax: float = 1,
    ) -> None:
        """Set coordinates to be a uniform grid, storing all values.

        Collective.

        Parameters
        ----------
        xmin
            The minimum global coordinate value in the x dimension.
        xmax
            The maximum global coordinate value in the x dimension.
        ymin
            The minimum global coordinate value in the y dimension.
        ymax
            The maximum global coordinate value in the y dimension.
        zmin
            The minimum global coordinate value in the z dimension.
        zmax
            The maximum global coordinate value in the z dimension.
        """
        ...

    def setUniformCoordinatesProduct(
        self,
        xmin: float = 0,
        xmax: float = 1,
        ymin: float = 0,
        ymax: float = 1,
        zmin: float = 0,
        zmax: float = 1,
    ) -> None:
        """Create uniform coordinates, as a product of 1D arrays.

        Collective.

        The per-dimension 1-dimensional DMStag objects that comprise the
        product always have active 0-cells (vertices, element boundaries) and
        1-cells (element centers).

        Parameters
        ----------
        xmin
            The minimum global coordinate value in the x dimension.
        xmax
            The maximum global coordinate value in the x dimension.
        ymin
            The minimum global coordinate value in the y dimension.
        ymax
            The maximum global coordinate value in the y dimension.
        zmin
            The minimum global coordinate value in the z dimension.
        zmax
            The maximum global coordinate value in the z dimension.
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
        """Set the coordinates to be a uniform grid.

        Collective.

        Local coordinates are populated, linearly extrapolated to ghost cells,
        including those outside the physical domain. This is also done in case
        of periodic boundaries, meaning that the same global point may have
        different coordinates in different local representations.

        Parameters
        ----------
        xmin
            The minimum global coordinate value in the x dimension.
        xmax
            The maximum global coordinate value in the x dimension.
        ymin
            The minimum global coordinate value in the y dimension.
        ymax
            The maximum global coordinate value in the y dimension.
        zmin
            The minimum global coordinate value in the z dimension.
        zmax
            The maximum global coordinate value in the z dimension.
        """
        ...

    def setCoordinateDMType(self, dmtype: str) -> None:
        """Set the type to store coordinates.

        Logically collective.

        Parameters
        ----------
        dmtype
            The type to store coordinates.
        """
        ...

    # Location slot related functions

    def getLocationSlot(self, loc: DMStagStencilLocation | int | str, c: int) -> int:
        """Return index to use in accessing raw local arrays.

        Not collective.

        Parameters
        ----------
        loc
            Location relative to an element.
        c
            Component.
        """
        ...

    def getProductCoordinateLocationSlot(
        self, loc: DMStagStencilLocation | int | str
    ) -> int:
        """Return slot for use with local product coordinate arrays.

        Not collective.

        Parameters
        ----------
        loc
            The grid location.
        """
        ...

    def getLocationDof(self, loc: DMStagStencilLocation | int | str) -> int:
        """Return number of DOFs associated with a given point on the grid.

        Not collective.

        Parameters
        ----------
        loc
            The grid point.
        """
        ...

    # Other functions

    def migrateVec(self, vec: Vec, dmTo: DM, vecTo: Vec) -> None:
        """Transfer a vector between two DMStag objects.

        Collective.

        Currently only implemented to migrate global vectors to global vectors.

        Parameters
        ----------
        vec
            The source vector.
        dmTo
            The compatible destination object.
        vecTo
            The destination vector.
        """
        ...

    def createCompatibleDMStag(self, dofs: tuple[int, ...]) -> DMStag:
        """Create a compatible DMStag with different DOFs/stratum.

        Collective.

        Parameters
        ----------
        dofs
            The number of DOFs on the strata in the new DMStag.
        """
        ...

    def VecSplitToDMDA(
        self, vec: Vec, loc: DMStagStencilLocation | int | str, c: int
    ) -> tuple[DMDA, Vec]:
        """Return DMDA, Vec from a subgrid of a DMStag, its Vec.

        Collective.

        If a ``c`` value of ``-k`` is provided, the first ``k`` DOFs for that
        position are extracted, padding with zero values if needed. If a
        non-negative value is provided, a single DOF is extracted.

        Parameters
        ----------
        vec
            The Vec object.
        loc
            Which subgrid to extract.
        c
            Which component to extract.
        """
        ...

    def getVecArray(self, vec: Vec) -> None:
        """Not implemented."""
        ...

    def get1dCoordinatecArrays(self) -> None:
        """Not implemented."""
        ...

    # Properties

    @property
    def dim(self) -> int:
        """The dimension."""
        ...

    @property
    def dofs(self) -> tuple[int, ...]:
        """The number of DOFs associated with each stratum of the grid."""
        ...

    @property
    def entries_per_element(self) -> int:
        """The number of entries per element in the local representation."""
        ...

    @property
    def global_sizes(self) -> tuple[int, ...]:
        """Global element counts in each dimension."""
        ...

    @property
    def local_sizes(self) -> tuple[int, ...]:
        """Local elementwise sizes in each dimension."""
        ...

    @property
    def proc_sizes(self) -> tuple[int, ...]:
        """The number of processes in each dimension in the global decomposition."""
        ...

    @property
    def boundary_types(self) -> tuple[str, ...]:
        """Boundary types in each dimension."""
        ...

    @property
    def stencil_type(self) -> str:
        """Stencil type."""
        ...

    @property
    def stencil_width(self) -> int:
        """Elementwise stencil width."""
        ...

    @property
    def corners(self) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        """The lower left corner, size, and extra elements of local region."""
        ...

    @property
    def ghost_corners(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """The lower left corner and size of local region including ghosts."""
        ...
