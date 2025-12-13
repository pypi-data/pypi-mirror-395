"""Type stubs for PETSc DMPlex module."""


from typing import Sequence, Self

from .DM import DM, InsertModeSpec
from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .Section import Section
from .SF import SF
from .IS import IS
from .DMLabel import DMLabel
from .Partitioner import Partitioner

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
)

class DMPlex(DM):
    """Encapsulate an unstructured mesh.

    DMPlex encapsulates both topology and geometry.
    It is capable of parallel refinement and coarsening (using Pragmatic or ParMmg)
    and parallel redistribution for load balancing.
    """

    def create(self, comm: Comm | None = None) -> Self:
        """Create a `DMPlex` object, which encapsulates an unstructured mesh.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createFromCellList(
        self,
        dim: int,
        cells: Sequence[int],
        coords: Sequence[float],
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` from a list of vertices for each cell on process 0.

        Collective.

        Parameters
        ----------
        dim
            The topological dimension of the mesh.
        cells
            An array of number of cells times number of vertices on each cell.
        coords
            An array of number of vertices times spatial dimension for coordinates.
        interpolate
            Flag to interpolate the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createBoxMesh(
        self,
        faces: Sequence[int],
        lower: Sequence[float] | None = (0, 0, 0),
        upper: Sequence[float] | None = (1, 1, 1),
        simplex: bool | None = True,
        periodic: Sequence | str | int | bool | None = False,
        interpolate: bool | None = True,
        localizationHeight: int | None = 0,
        sparseLocalize: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a mesh on the tensor product of intervals.

        Collective.

        Parameters
        ----------
        faces
            Number of faces per dimension, or `None` for the default.
        lower
            The lower left corner.
        upper
            The upper right corner.
        simplex
            `True` for simplices, `False` for tensor cells.
        periodic
            The boundary type for the X, Y, Z direction,
            or `None` for `DM.BoundaryType.NONE`.
        interpolate
            Flag to create intermediate mesh entities (edges, faces).
        localizationHeight
            Flag to localize edges and faces in addition to cells;
            only significant for periodic meshes.
        sparseLocalize
            Flag to localize coordinates only for cells near the
            periodic boundary; only significant for periodic meshes.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createBoxSurfaceMesh(
        self,
        faces: Sequence[int],
        lower: Sequence[float] | None = (0, 0, 0),
        upper: Sequence[float] | None = (1, 1, 1),
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a mesh on the surface of a box mesh using tensor cells.

        Collective.

        Parameters
        ----------
        faces
            Number of faces per dimension, or `None` for the default.
        lower
            The lower left corner.
        upper
            The upper right corner.
        interpolate
            Flag to create intermediate mesh pieces (edges, faces).
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createFromFile(
        self,
        filename: str,
        plexname: str | None = "unnamed",
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create `DMPlex` from a file.

        Collective.

        Parameters
        ----------
        filename
            A file name.
        plexname
            The name of the resulting `DMPlex`,
            also used for intra-datafile lookup by some formats.
        interpolate
            Flag to create intermediate mesh pieces (edges, faces).
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createCGNS(
        self,
        cgid: int,
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` mesh from a CGNS file.

        Collective.

        Parameters
        ----------
        cgid
            The CG id associated with a file and obtained using cg_open.
        interpolate
            Create faces and edges in the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createCGNSFromFile(
        self,
        filename: str,
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` mesh from a CGNS file.

        Collective.

        Parameters
        ----------
        filename
            The name of the CGNS file.
        interpolate
            Create faces and edges in the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createExodusFromFile(
        self,
        filename: str,
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` mesh from an ExodusII file.

        Collective.

        Parameters
        ----------
        filename
            The name of the ExodusII file.
        interpolate
            Create faces and edges in the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createExodus(
        self,
        exoid: int,
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` mesh from an ExodusII file ID.

        Collective.

        Parameters
        ----------
        exoid
            The ExodusII id associated with a file obtained using ``ex_open``.
        interpolate
            Create faces and edges in the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createGmsh(
        self,
        viewer: Viewer,
        interpolate: bool | None = True,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `DMPlex` mesh from a Gmsh file viewer.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` associated with a Gmsh file.
        interpolate
            Create faces and edges in the mesh.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createCoordinateSpace(
        self,
        degree: int,
        localized: bool,
        project: bool,
    ) -> None:
        """Create a finite element space for the coordinates.

        Collective.

        Parameters
        ----------
        degree
            The degree of the finite element.
        localized
            Flag to create a localized (DG) coordinate space.
        project
            Flag to project current coordinates into the space.
        """
        ...

    def createCohesiveSubmesh(self, hasLagrange: bool, value: int) -> DMPlex:
        """Extract the hypersurface defined by one face of the cohesive cells.

        Collective.

        Parameters
        ----------
        hasLagrange
            Flag indicating whether the mesh has Lagrange dofs in the cohesive cells.
        value
            A label value.
        """
        ...

    def getChart(self) -> tuple[int, int]:
        """Return the interval for all mesh points [``pStart``, ``pEnd``).

        Not collective.

        Returns
        -------
        pStart : int
            The first mesh point.
        pEnd : int
            The upper bound for mesh points.
        """
        ...

    def setChart(self, pStart: int, pEnd: int) -> None:
        """Set the interval for all mesh points [``pStart``, ``pEnd``).

        Not collective.

        Parameters
        ----------
        pStart
            The first mesh point.
        pEnd
            The upper bound for mesh points.
        """
        ...

    def getConeSize(self, p: int) -> int:
        """Return the number of in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        """
        ...

    def setConeSize(self, p: int, size: int) -> None:
        """Set the number of in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        size
            The cone size for point ``p``.
        """
        ...

    def getCone(self, p: int) -> ArrayInt:
        """Return the points on the in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        """
        ...

    def setCone(
        self,
        p: int,
        cone: Sequence[int],
        orientation: Sequence[int] | None = None,
    ) -> None:
        """Set the points on the in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        cone
            An array of points which are on the in-edges for point ``p``.
        orientation
            An array of orientations, defaults to `None`.
        """
        ...

    def insertCone(self, p: int, conePos: int, conePoint: int) -> None:
        """Insert a point into the in-edges for the point p in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        conePos
            The local index in the cone where the point should be put.
        conePoint
            The mesh point to insert.
        """
        ...

    def insertConeOrientation(
        self,
        p: int,
        conePos: int,
        coneOrientation: int,
    ) -> None:
        """Insert a point orientation for the in-edge for the point p in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`
        conePos
            The local index in the cone where the point should be put.
        coneOrientation
            The point orientation to insert.
        """
        ...

    def getConeOrientation(self, p: int) -> ArrayInt:
        """Return the orientations on the in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        """
        ...

    def setConeOrientation(self, p: int, orientation: Sequence[int]) -> None:
        """Set the orientations on the in-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        orientation
            An array of orientations.
        """
        ...

    def setCellType(self, p: int, ctype: DM.PolytopeType) -> None:
        """Set the polytope type of a given cell.

        Not collective.

        Parameters
        ----------
        p
            The cell.
        ctype
            The polytope type of the cell.
        """
        ...

    def getCellType(self, p: int) -> DM.PolytopeType:
        """Return the polytope type of a given cell.

        Not collective.

        Parameters
        ----------
        p
            The cell.
        """
        ...

    def getCellTypeLabel(self) -> DMLabel:
        """Return the `DMLabel` recording the polytope type of each cell.

        Not collective.
        """
        ...

    def getSupportSize(self, p: int) -> int:
        """Return the number of out-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        """
        ...

    def setSupportSize(self, p: int, size: int) -> None:
        """Set the number of out-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        size
            The support size for point ``p``.
        """
        ...

    def getSupport(self, p: int) -> ArrayInt:
        """Return the points on the out-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        """
        ...

    def setSupport(self, p: int, supp: Sequence[int]) -> None:
        """Set the points on the out-edges for this point in the DAG.

        Not collective.

        Parameters
        ----------
        p
            The point, which must lie in the chart set with `DMPlex.setChart`.
        supp
            An array of points which are on the out-edges for point ``p``.
        """
        ...

    def getMaxSizes(self) -> tuple[int, int]:
        """Return the maximum number of in-edges and out-edges of the DAG.

        Not collective.

        Returns
        -------
        maxConeSize : int
            The maximum number of in-edges.
        maxSupportSize : int
            The maximum number of out-edges.
        """
        ...

    def symmetrize(self) -> None:
        """Create support (out-edge) information from cone (in-edge) information.

        Not collective.
        """
        ...

    def stratify(self) -> None:
        """Calculate the strata of DAG.

        Collective.
        """
        ...

    def orient(self) -> None:
        """Give a consistent orientation to the input mesh.

        Collective.
        """
        ...

    def getCellNumbering(self) -> IS:
        """Return a global cell numbering for all cells on this process.

        Collective the first time it is called.
        """
        ...

    def getVertexNumbering(self) -> IS:
        """Return a global vertex numbering for all vertices on this process.

        Collective the first time it is called.
        """
        ...

    def createPointNumbering(self) -> IS:
        """Create a global numbering for all points.

        Collective.
        """
        ...

    def getDepth(self) -> int:
        """Return the depth of the DAG representing this mesh.

        Not collective.
        """
        ...

    def getDepthStratum(self, svalue: int) -> tuple[int, int]:
        """Return the bounds [``start``, ``end``) for all points at a certain depth.

        Not collective.

        Parameters
        ----------
        svalue
            The requested depth.

        Returns
        -------
        pStart : int
            The first stratum point.
        pEnd : int
            The upper bound for stratum points.
        """
        ...

    def getHeightStratum(self, svalue: int) -> tuple[int, int]:
        """Return the bounds [``start``, ``end``) for all points at a certain height.

        Not collective.

        Parameters
        ----------
        svalue
            The requested height.

        Returns
        -------
        pStart : int
            The first stratum point.
        pEnd : int
            The upper bound for stratum points.
        """
        ...

    def getPointDepth(self, point: int) -> int:
        """Return the *depth* of a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        """
        ...

    def getPointHeight(self, point: int) -> int:
        """Return the *height* of a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        """
        ...

    def getMeet(self, points: Sequence[int]) -> ArrayInt:
        """Return an array for the meet of the set of points.

        Not collective.

        Parameters
        ----------
        points
            The input points.
        """
        ...

    def getJoin(self, points: Sequence[int]) -> ArrayInt:
        """Return an array for the join of the set of points.

        Not collective.

        Parameters
        ----------
        points
            The input points.
        """
        ...

    def getFullJoin(self, points: Sequence[int]) -> ArrayInt:
        """Return an array for the join of the set of points.

        Not collective.

        Parameters
        ----------
        points
            The input points.
        """
        ...

    def getTransitiveClosure(
        self,
        p: int,
        useCone: bool | None = True,
    ) -> tuple[ArrayInt, ArrayInt]:
        """Return the points and orientations on the transitive closure of this point.

        Not collective.

        Parameters
        ----------
        p
            The mesh point.
        useCone
            `True` for the closure, otherwise return the star.

        Returns
        -------
        points : ArrayInt
            The points.
        orientations : ArrayInt
            The orientations.
        """
        ...

    def vecGetClosure(self, sec: Section, vec: Vec, p: int) -> ArrayScalar:
        """Return an array of values on the closure of ``p``.

        Not collective.

        Parameters
        ----------
        sec
            The section describing the layout in ``vec``.
        vec
            The local vector.
        p
            The point in the `DMPlex`.
        """
        ...

    def getVecClosure(
        self,
        sec: Section | None,
        vec: Vec,
        point: int,
    ) -> ArrayScalar:
        """Return an array of the values on the closure of a point.

        Not collective.

        Parameters
        ----------
        sec
            The `Section` describing the layout in ``vec``
            or `None` to use the default section.
        vec
            The local vector.
        point
            The point in the `DMPlex`.
        """
        ...

    def setVecClosure(
        self,
        sec: Section | None,
        vec: Vec,
        point: int,
        values: Sequence[Scalar],
        addv: InsertModeSpec | None = None,
    ) -> None:
        """Set an array of the values on the closure of ``point``.

        Not collective.

        Parameters
        ----------
        sec
            The section describing the layout in ``vec``,
            or `None` to use the default section.
        vec
            The local vector.
        point
            The point in the `DMPlex`.
        values
            The array of values.
        addv
            The insertion mode.
        """
        ...

    def setMatClosure(
        self,
        sec: Section | None,
        gsec: Section | None,
        mat: Mat,
        point: int,
        values: Sequence[Scalar],
        addv: InsertModeSpec | None = None,
    ) -> None:
        """Set an array of the values on the closure of ``point``.

        Not collective.

        Parameters
        ----------
        sec
            The section describing the layout in ``mat``,
            or `None` to use the default section.
        gsec
            The section describing the layout in ``mat``,
            or `None` to use the default global section.
        mat
            The matrix.
        point
            The point in the `DMPlex`.
        values
            The array of values.
        addv
            The insertion mode.
        """
        ...

    def generate(
        self,
        boundary: DMPlex,
        name: str | None = None,
        interpolate: bool | None = True,
    ) -> Self:
        """Generate a mesh.

        Not collective.

        Parameters
        ----------
        boundary
            The `DMPlex` boundary object.
        name
            The mesh generation package name.
        interpolate
            Flag to create intermediate mesh elements.
        """
        ...

    def setTriangleOptions(self, opts: str) -> None:
        """Set the options used for the Triangle mesh generator.

        Not collective.

        Parameters
        ----------
        opts
            The command line options.
        """
        ...

    def setTetGenOptions(self, opts: str) -> None:
        """Set the options used for the Tetgen mesh generator.

        Not collective.

        Parameters
        ----------
        opts
            The command line options.
        """
        ...

    def markBoundaryFaces(self, label: str, value: int | None = None) -> DMLabel:
        """Mark all faces on the boundary.

        Not collective.

        Parameters
        ----------
        label
            The label name.
        value
            The marker value, or `DETERMINE` or `None` to use some
            value in the closure (or 1 if none are found).
        """
        ...

    def labelComplete(self, label: DMLabel) -> None:
        """Add the transitive closure to the surface.

        Not collective.

        Parameters
        ----------
        label
            A `DMLabel` marking the surface points.
        """
        ...

    def labelCohesiveComplete(
        self,
        label: DMLabel,
        bdlabel: DMLabel,
        bdvalue: int,
        flip: bool,
        split: bool,
        subdm: DMPlex,
    ) -> None:
        """Add all other mesh pieces to complete the surface.

        Not collective.

        Parameters
        ----------
        label
            A `DMLabel` marking the surface.
        bdlabel
            A `DMLabel` marking the vertices on the boundary
            which will not be duplicated.
        bdvalue
            Value of `DMLabel` marking the vertices on the boundary.
        flip
            Flag to flip the submesh normal and replace points
            on the other side.
        split
            Flag to split faces incident on the surface boundary,
            rather than clamping those faces to the boundary
        subdm
            The `DMPlex` associated with the label.
        """
        ...

    def setAdjacencyUseAnchors(self, useAnchors: bool = True) -> None:
        """Define adjacency in the mesh using the point-to-point constraints.

        Logically collective.

        Parameters
        ----------
        useAnchors
            Flag to use the constraints.
            If `True`, then constrained points are omitted from `DMPlex.getAdjacency`,
            and their anchor points appear in their place.
        """
        ...

    def getAdjacencyUseAnchors(self) -> bool:
        """Query whether adjacency in the mesh uses the point-to-point constraints.

        Not collective.
        """
        ...

    def getAdjacency(self, p: int) -> ArrayInt:
        """Return all points adjacent to the given point.

        Not collective.

        Parameters
        ----------
        p
            The point.
        """
        ...

    def setPartitioner(self, part: Partitioner) -> None:
        """Set the mesh partitioner.

        Logically collective.

        Parameters
        ----------
        part
            The partitioner.
        """
        ...

    def getPartitioner(self) -> Partitioner:
        """Return the mesh partitioner.

        Not collective.
        """
        ...

    def rebalanceSharedPoints(
        self,
        entityDepth: int | None = 0,
        useInitialGuess: bool | None = True,
        parallel: bool | None = True,
    ) -> bool:
        """Redistribute shared points in order to achieve better balancing.

        Collective.

        Parameters
        ----------
        entityDepth
            Depth of the entity to balance (e.g., 0 -> balance vertices).
        useInitialGuess
            Whether to use the current distribution as initial guess.
        parallel
            Whether to use ParMETIS and do the partition in parallel
            or gather the graph onto a single process.

        Returns
        -------
        success : bool
            Whether the graph partitioning was successful or not.
            Unsuccessful simply means no change to the partitioning.
        """
        ...

    def distribute(self, overlap: int | None = 0) -> SF | None:
        """Distribute the mesh and any associated sections.

        Collective.

        Parameters
        ----------
        overlap
            The overlap of partitions.

        Returns
        -------
        sf : SF or None
            The `SF` used for point distribution, or `None` if not distributed.
        """
        ...

    def distributeOverlap(self, overlap: int | None = 0) -> SF:
        """Add partition overlap to a distributed non-overlapping `DMPlex`.

        Collective.

        Parameters
        ----------
        overlap
            The overlap of partitions (the same on all ranks).

        Returns
        -------
        sf : SF
            The `SF` used for point distribution.
        """
        ...

    def isDistributed(self) -> bool:
        """Return the flag indicating if the mesh is distributed.

        Collective.
        """
        ...

    def isSimplex(self) -> bool:
        """Return the flag indicating if the first cell is a simplex.

        Not collective.
        """
        ...

    def distributeGetDefault(self) -> bool:
        """Return a flag indicating whether the `DM` should be distributed by default.

        Not collective.

        Returns
        -------
        dist : bool
            Flag indicating whether the `DMPlex` should be distributed by default.
        """
        ...

    def distributeSetDefault(self, flag: bool) -> None:
        """Set flag indicating whether the `DMPlex` should be distributed by default.

        Logically collective.

        Parameters
        ----------
        flag
            Flag indicating whether the `DMPlex` should be distributed by default.
        """
        ...

    def distributionSetName(self, name: str) -> None:
        """Set the name of the specific parallel distribution.

        Logically collective.

        Parameters
        ----------
        name
            The name of the specific parallel distribution.
        """
        ...

    def distributionGetName(self) -> str:
        """Retrieve the name of the specific parallel distribution.

        Not collective.

        Returns
        -------
        name : str
            The name of the specific parallel distribution.
        """
        ...

    def interpolate(self) -> None:
        """Convert to a mesh with all intermediate faces, edges, etc.

        Collective.
        """
        ...

    def uninterpolate(self) -> None:
        """Convert to a mesh with only cells and vertices.

        Collective.
        """
        ...

    def distributeField(
        self,
        sf: SF,
        sec: Section,
        vec: Vec,
        newsec: Section | None = None,
        newvec: Vec | None = None,
    ) -> tuple[Section, Vec]:
        """Distribute field data with a with a given `SF`.

        Collective.

        Parameters
        ----------
        sf
            The `SF` describing the communication pattern.
        sec
            The `Section` for existing data layout.
        vec
            The existing data in a local vector.
        newsec
            The `SF` describing the new data layout.
        newvec
            The new data in a local vector.

        Returns
        -------
        newSection : Section
            The `SF` describing the new data layout.
        newVec : Vec
            The new data in a local vector.
        """
        ...

    def getMinRadius(self) -> float:
        """Return the minimum distance from any cell centroid to a face.

        Not collective.
        """
        ...

    def createCoarsePointIS(self) -> IS:
        """Create an `IS` covering the coarse `DMPlex` chart with the fine points as data.

        Collective.

        Returns
        -------
        fpointIS : IS
            The `IS` of all the fine points which exist in the original coarse mesh.
        """
        ...

    def createSection(
        self,
        numComp: Sequence[int],
        numDof: Sequence[int],
        bcField: Sequence[int] | None = None,
        bcComps: Sequence[IS] | None = None,
        bcPoints: Sequence[IS] | None = None,
        perm: IS | None = None,
    ) -> Section:
        """Create a `Section` based upon the DOF layout specification provided.

        Not collective.

        Parameters
        ----------
        numComp
            An array of size ``numFields`` holding the number of components per field.
        numDof
            An array of size ``numFields*(dim+1)`` holding the number of DOFs
            per field on a mesh piece of dimension ``dim``.
        bcField
            An array of size ``numBC`` giving the field number for each boundary
            condition, where ``numBC`` is the number of boundary conditions.
        bcComps
            An array of size ``numBC`` giving an `IS` holding the field
            components to which each boundary condition applies.
        bcPoints
            An array of size ``numBC`` giving an `IS` holding the `DMPlex` points
            to which each boundary condition applies.
        perm
            Permutation of the chart.
        """
        ...

    def getPointLocal(self, point: int) -> tuple[int, int]:
        """Return location of point data in local `Vec`.

        Not collective.

        Parameters
        ----------
        point
            The topological point.

        Returns
        -------
        start : int
            Start of point data.
        end : int
            End of point data.
        """
        ...

    def getPointLocalField(self, point: int, field: int) -> tuple[int, int]:
        """Return location of point field data in local `Vec`.

        Not collective.

        Parameters
        ----------
        point
            The topological point.
        field
            The field number.

        Returns
        -------
        start : int
            Start of point data.
        end : int
            End of point data.
        """
        ...

    def getPointGlobal(self, point: int) -> tuple[int, int]:
        """Return location of point data in global `Vec`.

        Not collective.

        Parameters
        ----------
        point
            The topological point.

        Returns
        -------
        start : int
            Start of point data.
        end : int
            End of point data.
        """
        ...

    def getPointGlobalField(self, point: int, field: int) -> tuple[int, int]:
        """Return location of point field data in global `Vec`.

        Not collective.

        Parameters
        ----------
        point
            The topological point.
        field
            The field number.

        Returns
        -------
        start : int
            Start of point data.
        end : int
            End of point data.
        """
        ...

    def createClosureIndex(self, sec: Section | None) -> None:
        """Calculate an index for ``sec`` for the closure operation.

        Not collective.

        Parameters
        ----------
        sec
            The `Section` describing the layout in the local vector,
            or `None` to use the default section.
        """
        ...

    def setRefinementUniform(self, refinementUniform: bool | None = True) -> None:
        """Set the flag for uniform refinement.

        Logically collective.

        Parameters
        ----------
        refinementUniform
            The flag for uniform refinement.
        """
        ...

    def getRefinementUniform(self) -> bool:
        """Retrieve the flag for uniform refinement.

        Not collective.

        Returns
        -------
        refinementUniform : bool
            The flag for uniform refinement.
        """
        ...

    def setRefinementLimit(self, refinementLimit: float) -> None:
        """Set the maximum cell volume for refinement.

        Logically collective.

        Parameters
        ----------
        refinementLimit
            The maximum cell volume in the refined mesh.
        """
        ...

    def getRefinementLimit(self) -> float:
        """Retrieve the maximum cell volume for refinement.

        Not collective.
        """
        ...

    def getOrdering(self, otype: Mat.OrderingType) -> IS:
        """Calculate a reordering of the mesh.

        Collective.

        Parameters
        ----------
        otype
            Type of reordering, see `Mat.OrderingType`.

        Returns
        -------
        perm : IS
            The point permutation.
        """
        ...

    def permute(self, perm: IS) -> DMPlex:
        """Reorder the mesh according to the input permutation.

        Collective.

        Parameters
        ----------
        perm
            The point permutation, ``perm[old point number] = new point number``.

        Returns
        -------
        pdm : DMPlex
            The permuted `DMPlex`.
        """
        ...

    def reorderGetDefault(self) -> DM.ReorderDefaultFlag:
        """Return flag indicating whether the `DMPlex` should be reordered by default.

        Not collective.
        """
        ...

    def reorderSetDefault(self, flag: DM.ReorderDefaultFlag) -> None:
        """Set flag indicating whether the DM should be reordered by default.

        Logically collective.

        Parameters
        ----------
        reorder
            Flag for reordering.
        """
        ...

    def computeCellGeometryFVM(self, cell: int) -> tuple[float, ArrayReal, ArrayReal]:
        """Compute the volume for a given cell.

        Not collective.

        Parameters
        ----------
        cell
            The cell.

        Returns
        -------
        volume : float
            The cell volume.
        centroid : ArrayReal
            The cell centroid.
        normal : ArrayReal
            The cell normal, if appropriate.
        """
        ...

    def constructGhostCells(self, labelName: str | None = None) -> int:
        """Construct ghost cells which connect to every boundary face.

        Collective.

        Parameters
        ----------
        labelName
            The name of the label specifying the boundary faces.
            Defaults to ``"Face Sets"``.

        Returns
        -------
        numGhostCells : int
            The number of ghost cells added to the `DMPlex`.
        """
        ...

    def getSubpointIS(self) -> IS:
        """Return an `IS` covering the entire subdm chart.

        Not collective.

        Returns
        -------
        iset : IS
            The `IS` containing subdm's parent's points.
        """
        ...

    def getSubpointMap(self) -> DMLabel:
        """Return a `DMLabel` with point dimension as values.

        Not collective.

        Returns
        -------
        label : DMLabel
            The `DMLabel` whose values are subdm's point dimensions.
        """
        ...

    # Metric

    def metricSetFromOptions(self) -> None:
        """Configure the object from the options database.

        Collective.
        """
        ...

    def metricSetUniform(self, uniform: bool) -> None:
        """Record whether the metric is uniform or not.

        Logically collective.

        Parameters
        ----------
        uniform
            Flag indicating whether the metric is uniform or not.
        """
        ...

    def metricIsUniform(self) -> bool:
        """Return the flag indicating whether the metric is uniform or not.

        Not collective.
        """
        ...

    def metricSetIsotropic(self, isotropic: bool) -> None:
        """Record whether the metric is isotropic or not.

        Logically collective.

        Parameters
        ----------
        isotropic
            Flag indicating whether the metric is isotropic or not.
        """
        ...

    def metricIsIsotropic(self) -> bool:
        """Return the flag indicating whether the metric is isotropic or not.

        Not collective.
        """
        ...

    def metricSetRestrictAnisotropyFirst(self, restrictAnisotropyFirst: bool) -> None:
        """Record whether anisotropy is be restricted before normalization or after.

        Logically collective.

        Parameters
        ----------
        restrictAnisotropyFirst
            Flag indicating if anisotropy is restricted before normalization or after.
        """
        ...

    def metricRestrictAnisotropyFirst(self) -> bool:
        """Return ``true`` if anisotropy is restricted before normalization.

        Not collective.
        """
        ...

    def metricSetNoInsertion(self, noInsert: bool) -> None:
        """Set the flag indicating whether node insertion should be turned off.

        Logically collective.

        Parameters
        ----------
        noInsert
            Flag indicating whether node insertion and deletion should be turned off.
        """
        ...

    def metricNoInsertion(self) -> bool:
        """Return the flag indicating whether node insertion and deletion are turned off.

        Not collective.
        """
        ...

    def metricSetNoSwapping(self, noSwap: bool) -> None:
        """Set the flag indicating whether facet swapping should be turned off.

        Logically collective.

        Parameters
        ----------
        noSwap
            Flag indicating whether facet swapping should be turned off.
        """
        ...

    def metricNoSwapping(self) -> bool:
        """Return the flag indicating whether facet swapping is turned off.

        Not collective.
        """
        ...

    def metricSetNoMovement(self, noMove: bool) -> None:
        """Set the flag indicating whether node movement should be turned off.

        Logically collective.

        Parameters
        ----------
        noMove
            Flag indicating whether node movement should be turned off.
        """
        ...

    def metricNoMovement(self) -> bool:
        """Return the flag indicating whether node movement is turned off.

        Not collective.
        """
        ...

    def metricSetNoSurf(self, noSurf: bool) -> None:
        """Set the flag indicating whether surface modification should be turned off.

        Logically collective.

        Parameters
        ----------
        noSurf
            Flag indicating whether surface modification should be turned off.
        """
        ...

    def metricNoSurf(self) -> bool:
        """Return the flag indicating whether surface modification is turned off.

        Not collective.
        """
        ...

    def metricSetVerbosity(self, verbosity: int) -> None:
        """Set the verbosity of the mesh adaptation package.

        Logically collective.

        Parameters
        ----------
        verbosity
            The verbosity, where -1 is silent and 10 is maximum.
        """
        ...

    def metricGetVerbosity(self) -> int:
        """Return the verbosity of the mesh adaptation package.

        Not collective.

        Returns
        -------
        verbosity : int
            The verbosity, where -1 is silent and 10 is maximum.
        """
        ...

    def metricSetNumIterations(self, numIter: int) -> None:
        """Set the number of parallel adaptation iterations.

        Logically collective.

        Parameters
        ----------
        numIter
            The number of parallel adaptation iterations.
        """
        ...

    def metricGetNumIterations(self) -> int:
        """Return the number of parallel adaptation iterations.

        Not collective.
        """
        ...

    def metricSetMinimumMagnitude(self, h_min: float) -> None:
        """Set the minimum tolerated metric magnitude.

        Logically collective.

        Parameters
        ----------
        h_min
            The minimum tolerated metric magnitude.
        """
        ...

    def metricGetMinimumMagnitude(self) -> float:
        """Return the minimum tolerated metric magnitude.

        Not collective.
        """
        ...

    def metricSetMaximumMagnitude(self, h_max: float) -> None:
        """Set the maximum tolerated metric magnitude.

        Logically collective.

        Parameters
        ----------
        h_max
            The maximum tolerated metric magnitude.
        """
        ...

    def metricGetMaximumMagnitude(self) -> float:
        """Return the maximum tolerated metric magnitude.

        Not collective.
        """
        ...

    def metricSetMaximumAnisotropy(self, a_max: float) -> None:
        """Set the maximum tolerated metric anisotropy.

        Logically collective.

        Parameters
        ----------
        a_max
            The maximum tolerated metric anisotropy.
        """
        ...

    def metricGetMaximumAnisotropy(self) -> float:
        """Return the maximum tolerated metric anisotropy.

        Not collective.
        """
        ...

    def metricSetTargetComplexity(self, targetComplexity: float) -> None:
        """Set the target metric complexity.

        Logically collective.

        Parameters
        ----------
        targetComplexity
            The target metric complexity.
        """
        ...

    def metricGetTargetComplexity(self) -> float:
        """Return the target metric complexity.

        Not collective.
        """
        ...

    def metricSetNormalizationOrder(self, p: float) -> None:
        """Set the order p for L-p normalization.

        Logically collective.

        Parameters
        ----------
        p
            The normalization order.
        """
        ...

    def metricGetNormalizationOrder(self) -> float:
        """Return the order p for L-p normalization.

        Not collective.
        """
        ...

    def metricSetGradationFactor(self, beta: float) -> None:
        """Set the metric gradation factor.

        Logically collective.

        Parameters
        ----------
        beta
            The metric gradation factor.
        """
        ...

    def metricGetGradationFactor(self) -> float:
        """Return the metric gradation factor.

        Not collective.
        """
        ...

    def metricSetHausdorffNumber(self, hausd: float) -> None:
        """Set the metric Hausdorff number.

        Logically collective.

        Parameters
        ----------
        hausd
            The metric Hausdorff number.
        """
        ...

    def metricGetHausdorffNumber(self) -> float:
        """Return the metric Hausdorff number.

        Not collective.
        """
        ...

    def metricCreate(self, field: int | None = 0) -> Vec:
        """Create a Riemannian metric field.

        Collective.

        Parameters
        ----------
        field
            The field number to use.
        """
        ...

    def metricCreateUniform(self, alpha: float, field: int | None = 0) -> Vec:
        """Construct a uniform isotropic metric.

        Collective.

        Parameters
        ----------
        alpha
            Scaling parameter for the diagonal.
        field
            The field number to use.
        """
        ...

    def metricCreateIsotropic(self, indicator: Vec, field: int | None = 0) -> Vec:
        """Construct an isotropic metric from an error indicator.

        Collective.

        Parameters
        ----------
        indicator
            The error indicator.
        field
            The field number to use.
        """
        ...

    def metricDeterminantCreate(self, field: int | None = 0) -> tuple[Vec, DM]:
        """Create the determinant field for a Riemannian metric.

        Collective.

        Parameters
        ----------
        field
            The field number to use.

        Returns
        -------
        determinant : Vec
            The determinant field.
        dmDet : DM
            The corresponding DM
        """
        ...

    def metricEnforceSPD(
        self,
        metric: Vec,
        ometric: Vec,
        determinant: Vec,
        restrictSizes: bool | None = False,
        restrictAnisotropy: bool | None = False,
    ) -> tuple[Vec, Vec]:
        """Enforce symmetric positive-definiteness of a metric.

        Collective.

        Parameters
        ----------
        metric
            The metric.
        ometric
            The output metric.
        determinant
            The output determinant.
        restrictSizes
            Flag indicating whether maximum/minimum magnitudes should be enforced.
        restrictAnisotropy
            Flag indicating whether maximum anisotropy should be enforced.

        Returns
        -------
        ometric : Vec
            The output metric.
        determinant : Vec
            The output determinant.
        """
        ...

    def metricNormalize(
        self,
        metric: Vec,
        ometric: Vec,
        determinant: Vec,
        restrictSizes: bool | None = True,
        restrictAnisotropy: bool | None = True,
    ) -> tuple[Vec, Vec]:
        """Apply L-p normalization to a metric.

        Collective.

        Parameters
        ----------
        metric
            The metric.
        ometric
            The output metric.
        determinant
            The output determinant.
        restrictSizes
            Flag indicating whether maximum/minimum magnitudes should be enforced.
        restrictAnisotropy
            Flag indicating whether maximum anisotropy should be enforced.

        Returns
        -------
        ometric : Vec
            The output normalized metric.
        determinant : Vec
            The output determinant.
        """
        ...

    def metricAverage2(self, metric1: Vec, metric2: Vec, metricAvg: Vec) -> Vec:
        """Compute and return the unweighted average of two metrics.

        Collective.

        Parameters
        ----------
        metric1
            The first metric to be averaged.
        metric2
            The second metric to be averaged.
        metricAvg
            The output averaged metric.
        """
        ...

    def metricAverage3(
        self,
        metric1: Vec,
        metric2: Vec,
        metric3: Vec,
        metricAvg: Vec,
    ) -> Vec:
        """Compute and return the unweighted average of three metrics.

        Collective.

        Parameters
        ----------
        metric1
            The first metric to be averaged.
        metric2
            The second metric to be averaged.
        metric3
            The third metric to be averaged.
        metricAvg
            The output averaged metric.
        """
        ...

    def metricIntersection2(self, metric1: Vec, metric2: Vec, metricInt: Vec) -> Vec:
        """Compute and return the intersection of two metrics.

        Collective.

        Parameters
        ----------
        metric1
            The first metric to be intersected.
        metric2
            The second metric to be intersected.
        metricInt
            The output intersected metric.
        """
        ...

    def metricIntersection3(
        self,
        metric1: Vec,
        metric2: Vec,
        metric3: Vec,
        metricInt: Vec,
    ) -> Vec:
        """Compute the intersection of three metrics.

        Collective.

        Parameters
        ----------
        metric1
            The first metric to be intersected.
        metric2
            The second metric to be intersected.
        metric3
            The third metric to be intersected.
        metricInt
            The output intersected metric.
        """
        ...

    def computeGradientClementInterpolant(self, locX: Vec, locC: Vec) -> Vec:
        """Return the L2 projection of the cellwise gradient of a function onto P1.

        Collective.

        Parameters
        ----------
        locX
            The coefficient vector of the function.
        locC
            The output `Vec` which holds the Clement interpolant of the gradient.
        """
        ...

    # View

    def topologyView(self, viewer: Viewer) -> None:
        """Save a `DMPlex` topology into a file.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for saving.
        """
        ...

    def coordinatesView(self, viewer: Viewer) -> None:
        """Save `DMPlex` coordinates into a file.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for saving.
        """
        ...

    def labelsView(self, viewer: Viewer) -> None:
        """Save `DMPlex` labels into a file.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for saving.
        """
        ...

    def sectionView(self, viewer: Viewer, sectiondm: DM) -> None:
        """Save a section associated with a `DMPlex`.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for saving.
        sectiondm
            The `DM` that contains the section to be saved.
        """
        ...

    def globalVectorView(self, viewer: Viewer, sectiondm: DM, vec: Vec) -> None:
        """Save a global vector.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` to save data with.
        sectiondm
            The `DM` containing the global section on which ``vec``
            is defined; may be the same as this `DMPlex` object.
        vec
            The global vector to be saved.
        """
        ...

    def localVectorView(self, viewer: Viewer, sectiondm: DM, vec: Vec) -> None:
        """Save a local vector.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` to save data with.
        sectiondm
            The `DM` that contains the local section on which ``vec`` is
            defined; may be the same as this `DMPlex` object.
        vec
            The local vector to be saved.
        """
        ...

    # Load

    def topologyLoad(self, viewer: Viewer) -> SF:
        """Load a topology into this `DMPlex` object.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for the saved topology

        Returns
        -------
        sfxc : SF
            The `SF` that pushes points in ``[0, N)`` to the associated points
            in the loaded `DMPlex`, where ``N`` is the global number of points.
        """
        ...

    def coordinatesLoad(self, viewer: Viewer, sfxc: SF) -> None:
        """Load coordinates into this `DMPlex` object.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for the saved coordinates.
        sfxc
            The `SF` returned by `topologyLoad`.
        """
        ...

    def labelsLoad(self, viewer: Viewer, sfxc: SF) -> None:
        """Load labels into this `DMPlex` object.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` for the saved labels.
        sfxc
            The `SF` returned by `topologyLoad`.
        """
        ...

    def sectionLoad(
        self,
        viewer: Viewer,
        sectiondm: DM,
        sfxc: SF,
    ) -> tuple[SF, SF]:
        """Load section into a `DM`.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` that represents the on-disk section (``sectionA``).
        sectiondm
            The `DM` into which the on-disk section (``sectionA``) is migrated.
        sfxc
            The `SF` returned by `topologyLoad`.

        Returns
        -------
        gsf : SF
            The `SF` that migrates any on-disk `Vec` data associated with
            ``sectionA`` into a global `Vec` associated with the
            ``sectiondm``'s global section (`None` if not needed).
        lsf : SF
            The `SF` that migrates any on-disk `Vec` data associated with
            ``sectionA`` into a local `Vec` associated with the ``sectiondm``'s
            local section (`None` if not needed).
        """
        ...

    def globalVectorLoad(
        self,
        viewer: Viewer,
        sectiondm: DM,
        sf: SF,
        vec: Vec,
    ) -> None:
        """Load on-disk vector data into a global vector.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` that represents the on-disk vector data.
        sectiondm
            The `DM` that contains the global section on which vec is defined.
        sf
            The `SF` that migrates the on-disk vector data into vec.
        vec
            The global vector to set values of.
        """
        ...

    def localVectorLoad(
        self,
        viewer: Viewer,
        sectiondm: DM,
        sf: SF,
        vec: Vec,
    ) -> None:
        """Load on-disk vector data into a local vector.

        Collective.

        Parameters
        ----------
        viewer
            The `Viewer` that represents the on-disk vector data.
        sectiondm
            The `DM` that contains the local section on which vec is defined.
        sf
            The `SF` that migrates the on-disk vector data into vec.
        vec
            The local vector to set values of.
        """
        ...


class DMPlexTransformType:
    """Transformation types."""

    REFINEREGULAR: str
    REFINEALFELD: str
    REFINEPOWELLSABIN: str
    REFINEBOUNDARYLAYER: str
    REFINESBR: str
    REFINETOBOX: str
    REFINETOSIMPLEX: str
    REFINE1D: str
    EXTRUDE: str
    TRANSFORMFILTER: str


class DMPlexTransform:
    """Mesh transformations."""

    def apply(self, dm: DM) -> DM:
        """Apply a mesh transformation.

        Collective.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a mesh transformation.

        Collective.
        """
        ...

    def destroy(self) -> Self:
        """Destroy a mesh transformation.

        Collective.
        """
        ...

    def getType(self) -> str:
        """Return the transformation type name.

        Not collective.
        """
        ...

    def setUp(self) -> Self:
        """Setup a mesh transformation.

        Collective.
        """
        ...

    def setType(self, tr_type: DMPlexTransformType | str) -> None:
        """Set the transformation type.

        Collective.
        """
        ...

    def setDM(self, dm: DM) -> None:
        """Set the `DM` for the transformation.

        Logically collective.
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the transformation from the options database.

        Collective.
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the mesh transformation.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.
        """
        ...
