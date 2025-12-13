"""Type stubs for PETSc DM module."""


from typing import Any, Callable, Literal, Sequence, Self
from numpy import ndarray, dtype

from .Object import Object
from .IS import IS, LGMap
from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .Section import Section
from .SF import SF
from .FE import FE
from .DMLabel import DMLabel
from .DS import DS

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    InsertModeSpec,
    SNESFunction,
    SNESJacobianFunction,
    DMCoarsenHookFunction,
    DMRestrictHookFunction,
)

class DMType:
    """DM types."""

    DA: str
    COMPOSITE: str
    SLICED: str
    SHELL: str
    PLEX: str
    REDUNDANT: str
    PATCH: str
    MOAB: str
    NETWORK: str
    FOREST: str
    P4EST: str
    P8EST: str
    SWARM: str
    PRODUCT: str
    STAG: str

class DMBoundaryType:
    """DM Boundary types."""

    NONE: int
    GHOSTED: int
    MIRROR: int
    PERIODIC: int
    TWIST: int

class DMPolytopeType:
    """The DM cell types."""

    POINT: int
    SEGMENT: int
    POINT_PRISM_TENSOR: int
    TRIANGLE: int
    QUADRILATERAL: int
    SEG_PRISM_TENSOR: int
    TETRAHEDRON: int
    HEXAHEDRON: int
    TRI_PRISM: int
    TRI_PRISM_TENSOR: int
    QUAD_PRISM_TENSOR: int
    PYRAMID: int
    FV_GHOST: int
    INTERIOR_GHOST: int
    UNKNOWN: int
    UNKNOWN_CELL: int
    UNKNOWN_FACE: int

class DMReorderDefaultFlag:
    """The DM reordering default flags."""

    NOTSET: int
    FALSE: int
    TRUE: int

class DM(Object):
    """An object describing a computational grid or mesh."""

    Type = DMType
    BoundaryType = DMBoundaryType
    PolytopeType = DMPolytopeType
    ReorderDefaultFlag = DMReorderDefaultFlag

    # --- view/load/destroy/create/clone ---

    def view(self, viewer: Viewer | None = None) -> None:
        """View the DM.

        Collective.

        Parameters
        ----------
        viewer
            The DM viewer.
        """
        ...

    def load(self, viewer: Viewer) -> Self:
        """Return a DM stored in binary.

        Collective.

        Parameters
        ----------
        viewer
            Viewer used to store the DM,
            like Viewer.Type.BINARY or Viewer.Type.HDF5.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the object.

        Collective.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Return an empty DM.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def clone(self) -> DM:
        """Return the cloned DM.

        Collective.
        """
        ...

    # --- type management ---

    def setType(self, dm_type: DMType | str) -> None:
        """Build a DM.

        Collective.

        Parameters
        ----------
        dm_type
            The type of DM.
        """
        ...

    def getType(self) -> str:
        """Return the DM type name.

        Not collective.
        """
        ...

    # --- dimension management ---

    def getDimension(self) -> int:
        """Return the topological dimension of the DM.

        Not collective.
        """
        ...

    def setDimension(self, dim: int) -> None:
        """Set the topological dimension of the DM.

        Collective.

        Parameters
        ----------
        dim
            Topological dimension.
        """
        ...

    def getCoordinateDim(self) -> int:
        """Return the dimension of embedding space for coordinates values.

        Not collective.
        """
        ...

    def setCoordinateDim(self, dim: int) -> None:
        """Set the dimension of embedding space for coordinates values.

        Not collective.

        Parameters
        ----------
        dim
            The embedding dimension.
        """
        ...

    # --- options management ---

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for searching for options in the database.

        Logically collective.
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database.

        Not collective.
        """
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for searching for options in the database.

        Logically collective.
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the object from the options database.

        Collective.
        """
        ...

    def setUp(self) -> Self:
        """Return the data structure.

        Collective.
        """
        ...

    # --- application context ---

    def setAppCtx(self, appctx: Any) -> None:
        """Set the application context."""
        ...

    def getAppCtx(self) -> Any:
        """Return the application context."""
        ...

    # --- adjacency ---

    def setBasicAdjacency(self, useCone: bool, useClosure: bool) -> None:
        """Set the flags for determining variable influence.

        Not collective.

        Parameters
        ----------
        useCone
            Whether adjacency uses cone information.
        useClosure
            Whether adjacency is computed using full closure information.
        """
        ...

    def getBasicAdjacency(self) -> tuple[bool, bool]:
        """Return the flags for determining variable influence.

        Not collective.

        Returns
        -------
        useCone : bool
            Whether adjacency uses cone information.
        useClosure : bool
            Whether adjacency is computed using full closure information.
        """
        ...

    def setFieldAdjacency(self, field: int, useCone: bool, useClosure: bool) -> None:
        """Set the flags for determining variable influence.

        Not collective.

        Parameters
        ----------
        field
            The field number.
        useCone
            Whether adjacency uses cone information.
        useClosure
            Whether adjacency is computed using full closure information.
        """
        ...

    def getFieldAdjacency(self, field: int) -> tuple[bool, bool]:
        """Return the flags for determining variable influence.

        Not collective.

        Parameters
        ----------
        field
            The field number.

        Returns
        -------
        useCone : bool
            Whether adjacency uses cone information.
        useClosure : bool
            Whether adjacency is computed using full closure information.
        """
        ...

    # --- subproblem ---

    def createSubDM(self, fields: Sequence[int]) -> tuple[IS, DM]:
        """Return IS and DM encapsulating a subproblem.

        Not collective.

        Returns
        -------
        iset : IS
            The global indices for all the degrees of freedom.
        subdm : DM
            The DM for the subproblem.
        """
        ...

    # --- auxiliary vectors ---

    def setAuxiliaryVec(
        self, aux: Vec, label: DMLabel | None, value: int = 0, part: int = 0
    ) -> None:
        """Set an auxiliary vector for a specific region.

        Not collective.

        Parameters
        ----------
        aux
            The auxiliary vector.
        label
            The name of the DMLabel.
        value
            Indicate the region.
        part
            The equation part, or 0 is unused.
        """
        ...

    def getAuxiliaryVec(
        self, label: str | None = None, value: int = 0, part: int = 0
    ) -> Vec:
        """Return an auxiliary vector for region.

        Not collective.

        Parameters
        ----------
        label
            The name of the DMLabel.
        value
            Indicate the region.
        part
            The equation part, or 0 is unused.
        """
        ...

    # --- field management ---

    def setNumFields(self, numFields: int) -> None:
        """Set the number of fields in the DM.

        Logically collective.
        """
        ...

    def getNumFields(self) -> int:
        """Return the number of fields in the DM.

        Not collective.
        """
        ...

    def setField(self, index: int, field: Object, label: str | None = None) -> None:
        """Set the discretization object for a given DM field.

        Logically collective.

        Parameters
        ----------
        index
            The field number.
        field
            The discretization object.
        label
            The name of the label indicating the support of the field,
            or None for the entire mesh.
        """
        ...

    def getField(self, index: int) -> tuple[Object, None]:
        """Return the discretization object for a given DM field.

        Not collective.

        Parameters
        ----------
        index
            The field number.
        """
        ...

    def addField(self, field: Object, label: str | None = None) -> None:
        """Add a field to a DM object.

        Logically collective.

        Parameters
        ----------
        field
            The discretization object.
        label
            The name of the label indicating the support of the field,
            or None for the entire mesh.
        """
        ...

    def clearFields(self) -> None:
        """Remove all fields from the DM.

        Logically collective.
        """
        ...

    def copyFields(
        self, dm: DM, minDegree: int | None = None, maxDegree: int | None = None
    ) -> None:
        """Copy the discretizations of this DM into another DM.

        Collective.

        Parameters
        ----------
        dm
            The DM that the fields are copied into.
        minDegree
            The minimum polynomial degree for the discretization,
            or None for no limit.
        maxDegree
            The maximum polynomial degree for the discretization,
            or None for no limit.
        """
        ...

    # --- discrete systems ---

    def createDS(self) -> None:
        """Create discrete systems.

        Collective.
        """
        ...

    def clearDS(self) -> None:
        """Remove all discrete systems from the DM.

        Logically collective.
        """
        ...

    def getDS(self) -> DS:
        """Return default DS.

        Not collective.
        """
        ...

    def setDS(self, ds: DS) -> None:
        """Set the DS.

        Not collective.
        """
        ...

    def copyDS(
        self, dm: DM, minDegree: int | None = None, maxDegree: int | None = None
    ) -> None:
        """Copy the discrete systems for this DM into another DM.

        Collective.

        Parameters
        ----------
        dm
            The DM that the discrete fields are copied into.
        minDegree
            The minimum polynomial degree for the discretization,
            or None for no limit.
        maxDegree
            The maximum polynomial degree for the discretization,
            or None for no limit.
        """
        ...

    def copyDisc(self, dm: DM) -> None:
        """Copy fields and discrete systems of a DM into another DM.

        Collective.

        Parameters
        ----------
        dm
            The DM that the fields and discrete systems are copied into.
        """
        ...

    # --- block size ---

    def getBlockSize(self) -> int:
        """Return the inherent block size associated with a DM.

        Not collective.
        """
        ...

    # --- vector management ---

    def setVecType(self, vec_type: str) -> None:
        """Set the type of vector.

        Logically collective.
        """
        ...

    def createGlobalVec(self) -> Vec:
        """Return a global vector.

        Collective.
        """
        ...

    def createLocalVec(self) -> Vec:
        """Return a local vector.

        Not collective.
        """
        ...

    def getGlobalVec(self, name: str | None = None) -> Vec:
        """Return a global vector.

        Collective.

        Parameters
        ----------
        name
            The optional name to retrieve a persistent vector.

        Notes
        -----
        When done with the vector, it must be restored using restoreGlobalVec.
        """
        ...

    def restoreGlobalVec(self, vg: Vec, name: str | None = None) -> None:
        """Restore a global vector obtained with getGlobalVec.

        Logically collective.

        Parameters
        ----------
        vg
            The global vector.
        name
            The name used to retrieve the persistent vector, if any.
        """
        ...

    def getLocalVec(self, name: str | None = None) -> Vec:
        """Return a local vector.

        Not collective.

        Parameters
        ----------
        name
            The optional name to retrieve a persistent vector.

        Notes
        -----
        When done with the vector, it must be restored using restoreLocalVec.
        """
        ...

    def restoreLocalVec(self, vl: Vec, name: str | None = None) -> None:
        """Restore a local vector obtained with getLocalVec.

        Not collective.

        Parameters
        ----------
        vl
            The local vector.
        name
            The name used to retrieve the persistent vector, if any.
        """
        ...

    # --- global/local conversions ---

    def globalToLocal(self, vg: Vec, vl: Vec, addv: InsertModeSpec = None) -> None:
        """Update local vectors from global vector.

        Neighborwise collective.

        Parameters
        ----------
        vg
            The global vector.
        vl
            The local vector.
        addv
            Insertion mode.
        """
        ...

    def localToGlobal(self, vl: Vec, vg: Vec, addv: InsertModeSpec = None) -> None:
        """Update global vectors from local vector.

        Neighborwise collective.

        Parameters
        ----------
        vl
            The local vector.
        vg
            The global vector.
        addv
            Insertion mode.
        """
        ...

    def localToLocal(self, vl: Vec, vlg: Vec, addv: InsertModeSpec = None) -> None:
        """Map the values from a local vector to another local vector.

        Neighborwise collective.

        Parameters
        ----------
        vl
            The local vector.
        vlg
            The global vector.
        addv
            Insertion mode.
        """
        ...

    def getLGMap(self) -> LGMap:
        """Return local mapping to global mapping.

        Collective.
        """
        ...

    # --- coarse DM ---

    def getCoarseDM(self) -> DM:
        """Return the coarse DM.

        Collective.
        """
        ...

    def setCoarseDM(self, dm: DM) -> None:
        """Set the coarse DM.

        Collective.
        """
        ...

    # --- coordinate management ---

    def getCoordinateDM(self) -> DM:
        """Return the coordinate DM.

        Collective.
        """
        ...

    def getCoordinateSection(self) -> Section:
        """Return coordinate values layout over the mesh.

        Collective.
        """
        ...

    def setCoordinates(self, c: Vec) -> None:
        """Set a global vector that holds the coordinates.

        Collective.

        Parameters
        ----------
        c
            Coordinate Vector.
        """
        ...

    def getCoordinates(self) -> Vec:
        """Return a global vector with the coordinates associated.

        Collective.
        """
        ...

    def setCoordinatesLocal(self, c: Vec) -> None:
        """Set a local vector with the ghost point holding the coordinates.

        Not collective.

        Parameters
        ----------
        c
            Coordinate Vector.
        """
        ...

    def getCoordinatesLocal(self) -> Vec:
        """Return a local vector with the coordinates associated.

        Collective the first time it is called.
        """
        ...

    # --- cell coordinate management ---

    def setCellCoordinateDM(self, dm: DM) -> None:
        """Set the cell coordinate DM.

        Collective.

        Parameters
        ----------
        dm
            The cell coordinate DM.
        """
        ...

    def getCellCoordinateDM(self) -> DM:
        """Return the cell coordinate DM.

        Collective.
        """
        ...

    def setCellCoordinateSection(self, dim: int, sec: Section) -> None:
        """Set the cell coordinate layout over the DM.

        Collective.

        Parameters
        ----------
        dim
            The embedding dimension, or DETERMINE.
        sec
            The cell coordinate Section.
        """
        ...

    def getCellCoordinateSection(self) -> Section:
        """Return the cell coordinate layout over the DM.

        Collective.
        """
        ...

    def setCellCoordinates(self, c: Vec) -> None:
        """Set a global vector with the cellwise coordinates.

        Collective.

        Parameters
        ----------
        c
            The global cell coordinate vector.
        """
        ...

    def getCellCoordinates(self) -> Vec:
        """Return a global vector with the cellwise coordinates.

        Collective.
        """
        ...

    def setCellCoordinatesLocal(self, c: Vec) -> None:
        """Set a local vector with the cellwise coordinates.

        Not collective.

        Parameters
        ----------
        c
            The local cell coordinate vector.
        """
        ...

    def getCellCoordinatesLocal(self) -> Vec:
        """Return a local vector with the cellwise coordinates.

        Collective.
        """
        ...

    def setCoordinateDisc(self, disc: FE, localized: bool, project: bool) -> Self:
        """Project coordinates to a different space.

        Collective.

        Parameters
        ----------
        disc
            The new coordinates discretization.
        localized
            Set a localized (DG) coordinate space.
        project
            Project coordinates to new discretization.
        """
        ...

    def getCoordinatesLocalized(self) -> bool:
        """Check if the coordinates have been localized for cells.

        Not collective.
        """
        ...

    def getBoundingBox(self) -> tuple[tuple[float, float], ...]:
        """Return the dimension of embedding space for coordinates values.

        Not collective.
        """
        ...

    def getLocalBoundingBox(self) -> tuple[tuple[float, float], ...]:
        """Return the bounding box for the piece of the DM.

        Not collective.
        """
        ...

    def localizeCoordinates(self) -> None:
        """Create local coordinates for cells having periodic faces.

        Collective.

        Notes
        -----
        Used if the mesh is periodic.
        """
        ...

    # --- periodicity ---

    def getPeriodicity(self) -> tuple[ArrayReal, ArrayReal, ArrayReal]:
        """Return the description of mesh periodicity.

        Not collective.

        Returns
        -------
        maxCell
            The longest allowable cell dimension in each direction.
        Lstart
            The start of each coordinate direction, usually [0, 0, 0].
        L
            The periodic length of each coordinate direction, or -1 for non-periodic.
        """
        ...

    def setPeriodicity(
        self, maxCell: Sequence[float], Lstart: Sequence[float], L: Sequence[float]
    ) -> None:
        """Set the description of mesh periodicity.

        Logically collective.

        Parameters
        ----------
        maxCell
            The longest allowable cell dimension in each direction.
        Lstart
            The start of each coordinate direction, usually [0, 0, 0].
        L
            The periodic length of each coordinate direction, or -1 for non-periodic.
        """
        ...

    # --- matrix management ---

    def setMatType(self, mat_type: Mat.Type | str) -> None:
        """Set matrix type to be used by DM.createMat.

        Logically collective.

        Parameters
        ----------
        mat_type
            The matrix type.

        Notes
        -----
        The option ``-dm_mat_type`` is used to set the matrix type.
        """
        ...

    def createMat(self) -> Mat:
        """Return an empty matrix.

        Collective.
        """
        ...

    def createMassMatrix(self, dmf: DM) -> Mat:
        """Return the mass matrix between this DM and the given DM.

        Collective.

        Parameters
        ----------
        dmf
            The second DM.
        """
        ...

    def createInterpolation(self, dm: DM) -> tuple[Mat, Vec]:
        """Return the interpolation matrix to a finer DM.

        Collective.

        Parameters
        ----------
        dm
            The second, finer DM.
        """
        ...

    def createInjection(self, dm: DM) -> Mat:
        """Return the injection matrix into a finer DM.

        Collective.

        Parameters
        ----------
        dm
            The second, finer DM object.
        """
        ...

    def createRestriction(self, dm: DM) -> Mat:
        """Return the restriction matrix between this DM and the given DM.

        Collective.

        Parameters
        ----------
        dm
            The second, finer DM object.
        """
        ...

    # --- conversion ---

    def convert(self, dm_type: DMType | str) -> DM:
        """Return a DM converted to another DM.

        Collective.

        Parameters
        ----------
        dm_type
            The new DM.Type, use "same" for the same type.
        """
        ...

    # --- refinement/coarsening ---

    def refine(self, comm: Comm | None = None) -> DM:
        """Return a refined DM object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def coarsen(self, comm: Comm | None = None) -> DM:
        """Return a coarsened DM object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def refineHierarchy(self, nlevels: int) -> list[DM]:
        """Refine this DM and return the refined DM hierarchy.

        Collective.

        Parameters
        ----------
        nlevels
            The number of levels of refinement.
        """
        ...

    def coarsenHierarchy(self, nlevels: int) -> list[DM]:
        """Coarsen this DM and return the coarsened DM hierarchy.

        Collective.

        Parameters
        ----------
        nlevels
            The number of levels of coarsening.
        """
        ...

    def getRefineLevel(self) -> int:
        """Return the refinement level.

        Not collective.
        """
        ...

    def setRefineLevel(self, level: int) -> None:
        """Set the number of refinements.

        Not collective.

        Parameters
        ----------
        level
            The number of refinement.
        """
        ...

    def getCoarsenLevel(self) -> int:
        """Return the number of coarsenings.

        Not collective.
        """
        ...

    # --- adaptation ---

    def adaptLabel(self, label: str) -> DM:
        """Adapt a DM based on a DMLabel.

        Collective.

        Parameters
        ----------
        label
            The name of the DMLabel.
        """
        ...

    def adaptMetric(
        self, metric: Vec, bdLabel: str | None = None, rgLabel: str | None = None
    ) -> DM:
        """Return a mesh adapted to the specified metric field.

        Collective.

        Parameters
        ----------
        metric
            The metric to which the mesh is adapted, defined vertex-wise.
        bdLabel
            Label for boundary tags.
        rgLabel
            Label for cell tag.
        """
        ...

    # --- labels ---

    def getLabel(self, name: str) -> DMLabel:
        """Return the label of a given name.

        Not collective.
        """
        ...

    def getNumLabels(self) -> int:
        """Return the number of labels defined by on the DM.

        Not collective.
        """
        ...

    def getLabelName(self, index: int) -> str:
        """Return the name of nth label.

        Not collective.

        Parameters
        ----------
        index
            The label number.
        """
        ...

    def hasLabel(self, name: str) -> bool:
        """Determine whether the DM has a label.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    def createLabel(self, name: str) -> None:
        """Create a label of the given name if it does not already exist.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    def removeLabel(self, name: str) -> None:
        """Remove and destroy the label by name.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    def getLabelValue(self, name: str, point: int) -> int:
        """Return the value in DMLabel for the given point.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        point
            The mesh point.
        """
        ...

    def setLabelValue(self, name: str, point: int, value: int) -> None:
        """Set a point to a DMLabel with a given value.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        point
            The mesh point.
        value
            The label value for the point.
        """
        ...

    def clearLabelValue(self, name: str, point: int, value: int) -> None:
        """Remove a point from a DMLabel with given value.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        point
            The mesh point.
        value
            The label value for the point.
        """
        ...

    def getLabelSize(self, name: str) -> int:
        """Return the number of values that the DMLabel takes.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    def getLabelIdIS(self, name: str) -> IS:
        """Return an IS of all values that the DMLabel takes.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    def getStratumSize(self, name: str, value: int) -> int:
        """Return the number of points in a label stratum.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        value
            The stratum value.
        """
        ...

    def getStratumIS(self, name: str, value: int) -> IS:
        """Return the points in a label stratum.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        value
            The stratum value.
        """
        ...

    def clearLabelStratum(self, name: str, value: int) -> None:
        """Remove all points from a stratum.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        value
            The stratum value.
        """
        ...

    def setLabelOutput(self, name: str, output: bool) -> None:
        """Set if a given label should be saved to a view.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        output
            If True, the label is saved to the viewer.
        """
        ...

    def getLabelOutput(self, name: str) -> bool:
        """Return the output flag for a given label.

        Not collective.

        Parameters
        ----------
        name
            The label name.
        """
        ...

    # --- section management ---

    def setLocalSection(self, sec: Section) -> None:
        """Set the Section encoding the local data layout for the DM.

        Collective.
        """
        ...

    def getLocalSection(self) -> Section:
        """Return the Section encoding the local data layout for the DM.

        Not collective.
        """
        ...

    def setGlobalSection(self, sec: Section) -> None:
        """Set the Section encoding the global data layout for the DM.

        Collective.
        """
        ...

    def getGlobalSection(self) -> Section:
        """Return the Section encoding the global data layout for the DM.

        Collective the first time it is called.
        """
        ...

    # Backward compatibility aliases for sections
    setSection = setLocalSection
    getSection = getLocalSection
    setDefaultSection = setLocalSection
    getDefaultSection = getLocalSection
    setDefaultLocalSection = setLocalSection
    getDefaultLocalSection = getLocalSection
    setDefaultGlobalSection = setGlobalSection
    getDefaultGlobalSection = getGlobalSection

    # --- section SF ---

    def createSectionSF(self, localsec: Section, globalsec: Section) -> None:
        """Create the SF encoding the parallel DOF overlap for the DM.

        Collective.

        Parameters
        ----------
        localsec
            Describe the local data layout.
        globalsec
            Describe the global data layout.

        Notes
        -----
        Encoding based on the Section describing the data layout.
        """
        ...

    def getSectionSF(self) -> SF:
        """Return the Section encoding the parallel DOF overlap.

        Collective the first time it is called.
        """
        ...

    def setSectionSF(self, sf: SF) -> None:
        """Set the Section encoding the parallel DOF overlap for the DM.

        Logically collective.
        """
        ...

    # Backward compatibility aliases
    createDefaultSF = createSectionSF
    getDefaultSF = getSectionSF
    setDefaultSF = setSectionSF

    # --- point SF ---

    def getPointSF(self) -> SF:
        """Return the SF encoding the parallel DOF overlap for the DM.

        Not collective.
        """
        ...

    def setPointSF(self, sf: SF) -> None:
        """Set the SF encoding the parallel DOF overlap for the DM.

        Logically collective.
        """
        ...

    # --- KSP/SNES callbacks ---

    def setKSPComputeOperators(
        self,
        operators: Callable[..., None],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Matrix associated with the linear system.

        Collective.

        Parameters
        ----------
        operators
            Callback function to compute the operators.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def createFieldDecomposition(
        self,
    ) -> tuple[list[str | None], list[IS], list[DM | None]]:
        """Return field splitting information.

        Collective.
        """
        ...

    def setSNESFunction(
        self,
        function: SNESFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set SNES residual evaluation function.

        Not collective.

        Parameters
        ----------
        function
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def setSNESJacobian(
        self,
        jacobian: SNESJacobianFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the SNES Jacobian evaluation function.

        Not collective.

        Parameters
        ----------
        jacobian
            The Jacobian callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def addCoarsenHook(
        self,
        coarsenhook: DMCoarsenHookFunction,
        restricthook: DMRestrictHookFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Add a callback to be executed when restricting to a coarser grid.

        Logically collective.

        Parameters
        ----------
        coarsenhook
            The coarsen hook function.
        restricthook
            The restrict hook function.
        args
            Positional arguments for the hooks.
        kargs
            Keyword arguments for the hooks.
        """
        ...

    # --- backward compatibility ---

    # Aliases for vector creation
    createGlobalVector = createGlobalVec
    createLocalVector = createLocalVec
    getMatrix = createMat
    createMatrix = createMat

    # --- properties ---

    @property
    def appctx(self) -> Any:
        """Application context."""
        ...

    @appctx.setter
    def appctx(self, value: Any) -> None: ...
    @property
    def ds(self) -> DS:
        """Discrete space."""
        ...

    @ds.setter
    def ds(self, value: DS) -> None: ...
