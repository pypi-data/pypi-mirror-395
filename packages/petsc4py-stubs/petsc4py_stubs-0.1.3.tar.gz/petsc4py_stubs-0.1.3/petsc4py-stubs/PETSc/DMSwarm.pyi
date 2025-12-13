"""Type stubs for PETSc DMSwarm module."""


from typing import Sequence, Self
from numpy import ndarray, dtype

# Import types from other modules
from .DM import DM, InsertModeSpec
from .Object import Object
from .Comm import Comm
from .Vec import Vec
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import ScatterModeSpec

class DMSwarmType:
    """Swarm types."""

    BASIC: int
    PIC: int

class DMSwarmMigrateType:
    """Swarm migration types."""

    MIGRATE_BASIC: int
    MIGRATE_DMCELLNSCATTER: int
    MIGRATE_DMCELLEXACT: int
    MIGRATE_USER: int

class DMSwarmCollectType:
    """Swarm collection types."""

    COLLECT_BASIC: int
    COLLECT_DMDABOUNDINGBOX: int
    COLLECT_GENERAL: int
    COLLECT_USER: int

class DMSwarmPICLayoutType:
    """Swarm PIC layout types."""

    LAYOUT_REGULAR: int
    LAYOUT_GAUSS: int
    LAYOUT_SUBDIVISION: int

class CellDM(Object):
    """CellDM object.

    Used for managing cell data in a DMSwarm.
    """

    def view(self, viewer: Viewer | None = None) -> None:
        """View the cell DM.

        Collective.

        Parameters
        ----------
        viewer
            A Viewer instance or None for the default viewer.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the cell DM.

        Collective.
        """
        ...

    def create(self, dm: DM, fields: Sequence[str], coords: Sequence[str]) -> Self:
        """Create the cell DM.

        Collective.

        Parameters
        ----------
        dm
            The underlying DM on which to place particles.
        fields
            The swarm fields represented on the DM.
        coords
            The swarm fields to use as coordinates in the DM.
        """
        ...

    def getDM(self) -> DM:
        """Return the underlying DM.

        Not collective.
        """
        ...

    def getCellID(self) -> str:
        """Return the cellid field for this cell DM.

        Not collective.
        """
        ...

    def getBlockSize(self, sw: DM) -> int:
        """Return the block size for this cell DM.

        Not collective.

        Parameters
        ----------
        sw
            The DMSwarm object.
        """
        ...

    def getFields(self) -> list[str]:
        """Return the swarm fields defined on this cell DM.

        Not collective.
        """
        ...

    def getCoordinateFields(self) -> list[str]:
        """Return the swarm fields used as coordinates on this cell DM.

        Not collective.
        """
        ...

class DMSwarm(DM):
    """A DM object used to represent arrays of data (fields) of arbitrary type.

    DMSwarm is used for particle methods such as PIC (particle-in-cell).
    """

    Type = DMSwarmType
    MigrateType = DMSwarmMigrateType
    CollectType = DMSwarmCollectType
    PICLayoutType = DMSwarmPICLayoutType

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty DM object and set its type to DM.Type.SWARM.

        Collective.

        DMs are the abstract objects in PETSc that mediate between meshes and
        discretizations and the algebraic solvers, time integrators, and
        optimization algorithms.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createGlobalVectorFromField(self, fieldname: str) -> Vec:
        """Create a global Vec object associated with a given field.

        Collective.

        The vector must be returned to the DMSwarm using a matching call to
        destroyGlobalVectorFromField.

        Parameters
        ----------
        fieldname
            The textual name given to a registered field.
        """
        ...

    def destroyGlobalVectorFromField(self, fieldname: str) -> None:
        """Destroy the global Vec object associated with a given field.

        Collective.

        Parameters
        ----------
        fieldname
            The textual name given to a registered field.
        """
        ...

    def createGlobalVectorFromFields(self, fieldnames: Sequence[str]) -> Vec:
        """Create a global Vec object associated with a given set of fields.

        Collective.

        The vector must be returned to the DMSwarm using a matching call to
        destroyGlobalVectorFromFields.

        Parameters
        ----------
        fieldnames
            The textual name given to each registered field.
        """
        ...

    def destroyGlobalVectorFromFields(self, fieldnames: Sequence[str]) -> None:
        """Destroy the global Vec object associated with a given set of fields.

        Collective.

        Parameters
        ----------
        fieldnames
            The textual name given to each registered field.
        """
        ...

    def createLocalVectorFromField(self, fieldname: str) -> Vec:
        """Create a local Vec object associated with a given field.

        Collective.

        The vector must be returned to the DMSwarm using a matching call
        to destroyLocalVectorFromField.

        Parameters
        ----------
        fieldname
            The textual name given to a registered field.
        """
        ...

    def destroyLocalVectorFromField(self, fieldname: str) -> None:
        """Destroy the local Vec object associated with a given field.

        Collective.

        Parameters
        ----------
        fieldname
            The textual name given to a registered field.
        """
        ...

    def createLocalVectorFromFields(self, fieldnames: Sequence[str]) -> Vec:
        """Create a local Vec object associated with a given set of fields.

        Collective.

        The vector must be returned to the DMSwarm using a matching call to
        destroyLocalVectorFromFields.

        Parameters
        ----------
        fieldnames
            The textual name given to each registered field.
        """
        ...

    def destroyLocalVectorFromFields(self, fieldnames: Sequence[str]) -> None:
        """Destroy the local Vec object associated with a given set of fields.

        Collective.

        Parameters
        ----------
        fieldnames
            The textual name given to each registered field.
        """
        ...

    def initializeFieldRegister(self) -> None:
        """Initiate the registration of fields to a DMSwarm.

        Collective.

        After all fields have been registered, you must call finalizeFieldRegister.
        """
        ...

    def finalizeFieldRegister(self) -> None:
        """Finalize the registration of fields to a DMSwarm.

        Collective.
        """
        ...

    def setLocalSizes(self, nlocal: int, buffer: int) -> Self:
        """Set the length of all registered fields on the DMSwarm.

        Not collective.

        Parameters
        ----------
        nlocal
            The length of each registered field.
        buffer
            The length of the buffer used for efficient dynamic resizing.
        """
        ...

    def registerField(
        self, fieldname: str, blocksize: int, dtype: type | dtype = ...
    ) -> None:
        """Register a field to a DMSwarm with a native PETSc data type.

        Collective.

        Parameters
        ----------
        fieldname
            The textual name to identify this field.
        blocksize
            The number of each data type.
        dtype
            A valid PETSc data type.
        """
        ...

    def getField(self, fieldname: str) -> ndarray:
        """Return arrays storing all entries associated with a field.

        Not collective.

        The returned array contains underlying values of the field.
        The array must be returned to the DMSwarm using a matching call to
        restoreField.

        Parameters
        ----------
        fieldname
            The textual name to identify this field.

        Returns
        -------
        ndarray
            The type of the entries in the array will match the type of the
            field. The array is two dimensional with shape (num_points, blocksize).
        """
        ...

    def restoreField(self, fieldname: str) -> None:
        """Restore accesses associated with a registered field.

        Not collective.

        Parameters
        ----------
        fieldname
            The textual name to identify this field.
        """
        ...

    def vectorDefineField(self, fieldname: str) -> None:
        """Set the fields from which to define a Vec object.

        Collective.

        The field will be used when DM.createLocalVec, or
        DM.createGlobalVec is called.

        Parameters
        ----------
        fieldname
            The textual names given to a registered field.
        """
        ...

    def addPoint(self) -> None:
        """Add space for one new point in the DMSwarm.

        Not collective.
        """
        ...

    def addNPoints(self, npoints: int) -> None:
        """Add space for a number of new points in the DMSwarm.

        Not collective.

        Parameters
        ----------
        npoints
            The number of new points to add.
        """
        ...

    def removePoint(self) -> None:
        """Remove the last point from the DMSwarm.

        Not collective.
        """
        ...

    def removePointAtIndex(self, index: int) -> None:
        """Remove a specific point from the DMSwarm.

        Not collective.

        Parameters
        ----------
        index
            Index of point to remove.
        """
        ...

    def copyPoint(self, pi: int, pj: int) -> None:
        """Copy point pi to point pj in the DMSwarm.

        Not collective.

        Parameters
        ----------
        pi
            The index of the point to copy (source).
        pj
            The point index where the copy should be located (destination).
        """
        ...

    def getLocalSize(self) -> int:
        """Return the local length of fields registered.

        Not collective.
        """
        ...

    def getSize(self) -> int:
        """Return the total length of fields registered.

        Collective.
        """
        ...

    def migrate(self, remove_sent_points: bool = False) -> None:
        """Relocate points defined in the DMSwarm to other MPI ranks.

        Collective.

        Parameters
        ----------
        remove_sent_points
            Flag indicating if sent points should be removed from the current
            MPI rank.
        """
        ...

    def collectViewCreate(self) -> None:
        """Apply a collection method and gather points in neighbor ranks.

        Collective.
        """
        ...

    def collectViewDestroy(self) -> None:
        """Reset the DMSwarm to the size prior to calling collectViewCreate.

        Collective.
        """
        ...

    def setCellDM(self, dm: DM) -> None:
        """Attach a DM to a DMSwarm.

        Collective.

        Parameters
        ----------
        dm
            The DM to attach to the DMSwarm.
        """
        ...

    def getCellDM(self) -> DM:
        """Return DM cell attached to DMSwarm.

        Collective.
        """
        ...

    def setType(self, dmswarm_type: DMSwarmType | int | str) -> None:
        """Set particular flavor of DMSwarm.

        Collective.

        Parameters
        ----------
        dmswarm_type
            The DMSwarm type.
        """
        ...

    def setPointsUniformCoordinates(
        self,
        min: Sequence[float],
        max: Sequence[float],
        npoints: Sequence[int],
        mode: InsertModeSpec = None,
    ) -> Self:
        """Set point coordinates in a DMSwarm on a regular (ijk) grid.

        Collective.

        Parameters
        ----------
        min
            Minimum coordinate values in the x, y, z directions (array of
            length dim).
        max
            Maximum coordinate values in the x, y, z directions (array of
            length dim).
        npoints
            Number of points in each spatial direction (array of length dim).
        mode
            Indicates whether to append points to the swarm (InsertMode.ADD),
            or override existing points (InsertMode.INSERT).
        """
        ...

    def setPointCoordinates(
        self,
        coordinates: Sequence[float],
        redundant: bool = False,
        mode: InsertModeSpec = None,
    ) -> None:
        """Set point coordinates in a DMSwarm from a user-defined list.

        Collective.

        Parameters
        ----------
        coordinates
            The coordinate values.
        redundant
            If set to True, it is assumed that coordinates are only valid on
            rank 0 and should be broadcast to other ranks.
        mode
            Indicates whether to append points to the swarm (InsertMode.ADD),
            or override existing points (InsertMode.INSERT).
        """
        ...

    def insertPointUsingCellDM(
        self, layoutType: DMSwarmPICLayoutType | int, fill_param: int
    ) -> None:
        """Insert point coordinates within each cell.

        Not collective.

        Parameters
        ----------
        layoutType
            Method used to fill each cell with the cell DM.
        fill_param
            Parameter controlling how many points per cell are added (the
            meaning of this parameter is dependent on the layout type).
        """
        ...

    def setPointCoordinatesCellwise(self, coordinates: Sequence[float]) -> None:
        """Insert point coordinates within each cell.

        Not collective.

        Point coordinates are defined over the reference cell.

        Parameters
        ----------
        coordinates
            The coordinates (defined in the local coordinate system for each
            cell) to insert.
        """
        ...

    def viewFieldsXDMF(self, filename: str, fieldnames: Sequence[str]) -> None:
        """Write a selection of DMSwarm fields to an XDMF3 file.

        Collective.

        Parameters
        ----------
        filename
            The file name of the XDMF file (must have the extension .xmf).
        fieldnames
            Array containing the textual names of fields to write.
        """
        ...

    def viewXDMF(self, filename: str) -> None:
        """Write this DMSwarm fields to an XDMF3 file.

        Collective.

        Parameters
        ----------
        filename
            The file name of the XDMF file (must have the extension .xmf).
        """
        ...

    def sortGetAccess(self) -> None:
        """Setup up a DMSwarm point sort context.

        Not collective.

        The point sort context is used for efficient traversal of points within
        a cell.

        You must call sortRestoreAccess when you no longer need access to the
        sort context.
        """
        ...

    def sortRestoreAccess(self) -> None:
        """Invalidate the DMSwarm point sorting context.

        Not collective.
        """
        ...

    def sortGetPointsPerCell(self, e: int) -> list[int]:
        """Create an array of point indices for all points in a cell.

        Not collective.

        Parameters
        ----------
        e
            The index of the cell.
        """
        ...

    def sortGetNumberOfPointsPerCell(self, e: int) -> int:
        """Return the number of points in a cell.

        Not collective.

        Parameters
        ----------
        e
            The index of the cell.
        """
        ...

    def sortGetIsValid(self) -> bool:
        """Return whether the sort context is up-to-date.

        Not collective.

        Returns the flag associated with a DMSwarm point sorting context.
        """
        ...

    def sortGetSizes(self) -> tuple[int, int]:
        """Return the sizes associated with a DMSwarm point sorting context.

        Not collective.

        Returns
        -------
        tuple[int, int]
            A tuple of (ncells, npoints) where ncells is the number of cells
            within the sort context and npoints is the number of points used
            to create the sort context.
        """
        ...

    def projectFields(
        self,
        dm: DM,
        fieldnames: Sequence[str],
        vecs: Sequence[Vec],
        mode: ScatterModeSpec = None,
    ) -> None:
        """Project a set of DMSwarm fields onto the cell DM.

        Collective.

        Parameters
        ----------
        dm
            The continuum DM.
        fieldnames
            The textual names of the swarm fields to project.
        vecs
            The vectors to hold the projected fields.
        mode
            The scatter mode.
        """
        ...

    def addCellDM(self, celldm: CellDM) -> None:
        """Add a cell DM to the DMSwarm.

        Logically collective.

        Parameters
        ----------
        celldm
            The cell DM object.
        """
        ...

    def setCellDMActive(self, name: str) -> None:
        """Activate a cell DM in the DMSwarm.

        Logically collective.

        Parameters
        ----------
        name
            The name of the cell DM to activate.
        """
        ...

    def getCellDMActive(self) -> CellDM:
        """Return the active cell DM in the DMSwarm.

        Not collective.
        """
        ...

    def getCellDMByName(self, name: str) -> CellDM:
        """Return the cell DM with the given name in the DMSwarm.

        Not collective.

        Parameters
        ----------
        name
            The name of the cell DM.
        """
        ...

    def getCellDMNames(self) -> list[str]:
        """Return the names of all cell DMs in the DMSwarm.

        Not collective.
        """
        ...

    def computeMoments(self, coord: str, weight: str) -> list[float]:
        """Return the moments defined in the active cell DM.

        Collective.

        Parameters
        ----------
        coord
            The coordinate field name.
        weight
            The weight field name.

        Notes
        -----
        We integrate the given weight field over the given coordinate.
        """
        ...
