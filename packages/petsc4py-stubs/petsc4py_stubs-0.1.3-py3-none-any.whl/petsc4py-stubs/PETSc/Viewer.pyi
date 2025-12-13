"""Type stubs for PETSc Viewer module."""


from typing import Any, Literal, Self

from .Object import Object

from .Comm import Comm

class ViewerType:
    """Viewer type."""

    SOCKET: str
    ASCII: str
    BINARY: str
    STRING: str
    DRAW: str
    VU: str
    MATHEMATICA: str
    HDF5: str
    VTK: str
    MATLAB: str
    SAWS: str
    GLVIS: str
    ADIOS: str
    EXODUSII: str
    PYTHON: str
    PYVISTA: str

class ViewerFormat:
    """Viewer format."""

    DEFAULT: int
    ASCII_MATLAB: int
    ASCII_MATHEMATICA: int
    ASCII_IMPL: int
    ASCII_INFO: int
    ASCII_INFO_DETAIL: int
    ASCII_COMMON: int
    ASCII_SYMMODU: int
    ASCII_INDEX: int
    ASCII_DENSE: int
    ASCII_MATRIXMARKET: int
    ASCII_PCICE: int
    ASCII_PYTHON: int
    ASCII_FACTOR_INFO: int
    ASCII_LATEX: int
    ASCII_XML: int
    ASCII_GLVIS: int
    ASCII_CSV: int
    DRAW_BASIC: int
    DRAW_LG: int
    DRAW_LG_XRANGE: int
    DRAW_CONTOUR: int
    DRAW_PORTS: int
    VTK_VTS: int
    VTK_VTR: int
    VTK_VTU: int
    BINARY_MATLAB: int
    NATIVE: int
    HDF5_PETSC: int
    HDF5_VIZ: int
    HDF5_XDMF: int
    HDF5_MAT: int
    NOFORMAT: int
    LOAD_BALANCE: int
    FAILED: int

class ViewerFileMode:
    """Viewer file mode."""

    # native
    READ: int
    WRITE: int
    APPEND: int
    UPDATE: int
    APPEND_UPDATE: int
    # aliases
    R: int
    W: int
    A: int
    U: int
    AU: int
    UA: int

class ViewerDrawSize:
    """Window size."""

    # native
    FULL_SIZE: int
    HALF_SIZE: int
    THIRD_SIZE: int
    QUARTER_SIZE: int
    # aliases
    FULL: int
    HALF: int
    THIRD: int
    QUARTER: int

# Type aliases for convenience
FileMode = ViewerFileMode
Format = ViewerFormat
Type = ViewerType
DrawSize = ViewerDrawSize

# Mode string specifications
FileModeSpec = (
    Literal["r", "w", "a", "r+", "w+", "a+", "u", "au", "ua"]
    | ViewerFileMode
    | int
    | None
)

class Viewer(Object):
    """Viewer object.

    Viewer is described in the PETSc manual.

    Viewers can be called as functions where the argument specified
    is the PETSc object to be viewed.
    """

    Type = ViewerType
    Format = ViewerFormat
    FileMode = ViewerFileMode
    DrawSize = ViewerDrawSize

    # backward compatibility
    Mode = ViewerFileMode
    Size = ViewerFileMode

    def __call__(self, obj: Object) -> None:
        """View a generic object."""
        ...

    def view(self, obj: Viewer | Object | None = None) -> None:
        """View the viewer.

        Collective.

        Parameters
        ----------
        obj
            A `Viewer` instance or `None` for the default viewer.
            If none of the above applies, it assumes ``obj`` is an instance of `Object`
            and it calls the generic view for ``obj``.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the viewer.

        Collective.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a viewer.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createASCII(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a viewer of type `Type.ASCII`.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createBinary(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a viewer of type `Type.BINARY`.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createMPIIO(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a viewer of type `Type.BINARY` supporting MPI-IO.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createVTK(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a viewer of type `Type.VTK`.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createHDF5(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> ViewerHDF5:
        """Create a viewer of type `Type.HDF5`.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def createDraw(
        self,
        display: str | None = None,
        title: str | None = None,
        position: tuple[int, int] | None = None,
        size: tuple[int, int] | int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `Type.DRAW` viewer.

        Collective.

        Parameters
        ----------
        display
            The X display to use or `None` for the local machine.
        title
            The window title or `None` for no title.
        position
            Screen coordinates of the upper left corner, or `None` for default.
        size
            Window size or `None` for default.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def setType(self, vwr_type: Type | str) -> None:
        """Set the type of the viewer.

        Logically collective.

        Parameters
        ----------
        vwr_type
            The type of the viewer.
        """
        ...

    def getType(self) -> str:
        """Return the type of the viewer.

        Not collective.
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the object from the options database.

        Collective.
        """
        ...

    def setUp(self) -> Self:
        """Set up the internal data structures for using the viewer.

        Collective.
        """
        ...

    def getFormat(self) -> Format:
        """Return the format of the viewer.

        Not collective.
        """
        ...

    def pushFormat(self, format: Format) -> None:
        """Push format to the viewer.

        Collective.
        """
        ...

    def popFormat(self) -> None:
        """Pop format from the viewer.

        Collective.
        """
        ...

    def getSubViewer(self, comm: Comm | None = None) -> Viewer:
        """Return a viewer defined on a subcommunicator.

        Collective.

        Parameters
        ----------
        comm
            The subcommunicator. If `None`, uses `COMM_SELF`.

        Notes
        -----
        Users must call `restoreSubViewer` when done.
        """
        ...

    def restoreSubViewer(self, sub: Viewer) -> None:
        """Restore a viewer defined on a subcommunicator.

        Collective.

        Parameters
        ----------
        sub
            The subviewer obtained from `getSubViewer`.
        """
        ...

    @classmethod
    def STDOUT(cls, comm: Comm | None = None) -> Viewer:
        """Return the standard output viewer associated with the communicator.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    @classmethod
    def STDERR(cls, comm: Comm | None = None) -> Viewer:
        """Return the standard error viewer associated with the communicator.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    @classmethod
    def ASCII(cls, name: str, comm: Comm | None = None) -> Viewer:
        """Return an ASCII viewer associated with the communicator.

        Collective.

        Parameters
        ----------
        name
            The filename.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    @classmethod
    def BINARY(cls, comm: Comm | None = None) -> Viewer:
        """Return the default `Type.BINARY` viewer associated with the communicator.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    @classmethod
    def DRAW(cls, comm: Comm | None = None) -> Viewer:
        """Return the default `Type.DRAW` viewer associated with the communicator.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    # --- ASCII viewers ---

    def setASCIITab(self, tabs: int) -> None:
        """Set ASCII tab level.

        Collective.
        """
        ...

    def getASCIITab(self) -> int:
        """Return the ASCII tab level.

        Not collective.
        """
        ...

    def addASCIITab(self, tabs: int) -> None:
        """Increment the ASCII tab level.

        Collective.
        """
        ...

    def subtractASCIITab(self, tabs: int) -> None:
        """Decrement the ASCII tab level.

        Collective.
        """
        ...

    def pushASCIISynchronized(self) -> None:
        """Allow ASCII synchronized calls.

        Collective.
        """
        ...

    def popASCIISynchronized(self) -> None:
        """Disallow ASCII synchronized calls.

        Collective.
        """
        ...

    def pushASCIITab(self) -> None:
        """Push an additional tab level.

        Collective.
        """
        ...

    def popASCIITab(self) -> None:
        """Pop an additional tab level pushed via `pushASCIITab`.

        Collective.
        """
        ...

    def useASCIITabs(self, flag: bool) -> None:
        """Enable/disable the use of ASCII tabs.

        Collective.
        """
        ...

    def printfASCII(self, msg: str) -> None:
        """Print a message.

        Collective.
        """
        ...

    def printfASCIISynchronized(self, msg: str) -> None:
        """Print a synchronized message.

        Collective.
        """
        ...

    # --- methods specific to file viewers ---

    def flush(self) -> None:
        """Flush the viewer.

        Collective.
        """
        ...

    def setFileMode(self, mode: FileModeSpec) -> None:
        """Set file mode.

        Collective.
        """
        ...

    def getFileMode(self) -> FileMode:
        """Return the file mode.

        Not collective.
        """
        ...

    def setFileName(self, name: str) -> None:
        """Set file name.

        Collective.
        """
        ...

    def getFileName(self) -> str:
        """Return file name.

        Not collective.
        """
        ...

    # --- methods specific to draw viewers ---

    def setDrawInfo(
        self,
        display: str | None = None,
        title: str | None = None,
        position: tuple[int, int] | None = None,
        size: tuple[int, int] | int | None = None,
    ) -> None:
        """Set window information for a `Type.DRAW` viewer.

        Collective.

        Parameters
        ----------
        display
            The X display to use or `None` for the local machine.
        title
            The window title or `None` for no title.
        position
            Screen coordinates of the upper left corner, or `None` for default.
        size
            Window size or `None` for default.
        """
        ...

    def clearDraw(self) -> None:
        """Reset graphics.

        Not collective.
        """
        ...

    # --- Python viewer methods ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create a `Type.PYTHON` viewer.

        Collective.

        Parameters
        ----------
        context
            An instance of the Python class implementing the required methods.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def setPythonContext(self, context: Any) -> None:
        """Set the instance of the class implementing the required Python methods.

        Logically collective.
        """
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing the required Python methods.

        Not collective.
        """
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used.

        Collective.
        """
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the viewer.

        Not collective.
        """
        ...

    def viewObjectPython(self, obj: Object) -> None:
        """View a generic `Object`.

        Collective.
        """
        ...

class ViewerHDF5(Viewer):
    """Viewer object for HDF5 file formats.

    Viewer is described in the PETSc manual.
    """

    def create(
        self,
        name: str,
        mode: FileModeSpec = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a viewer of type `Type.HDF5`.

        Collective.

        Parameters
        ----------
        name
            The filename associated with the viewer.
        mode
            The mode type.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.
        """
        ...

    def pushTimestepping(self) -> None:
        """Activate the timestepping mode.

        Logically collective.
        """
        ...

    def popTimestepping(self) -> None:
        """Deactivate the timestepping mode.

        Logically collective.
        """
        ...

    def getTimestep(self) -> int:
        """Return the current time step.

        Not collective.
        """
        ...

    def setTimestep(self, timestep: int) -> None:
        """Set the current time step.

        Logically collective.
        """
        ...

    def incrementTimestep(self) -> None:
        """Increment the time step.

        Logically collective.
        """
        ...

    def pushGroup(self, group: str) -> None:
        """Set the current group.

        Logically collective.
        """
        ...

    def popGroup(self) -> None:
        """Pop the current group from the stack.

        Logically collective.
        """
        ...

    def getGroup(self) -> str:
        """Return the current group.

        Not collective.
        """
        ...

__all__ = [
    "Viewer",
    "ViewerType",
    "ViewerFormat",
    "ViewerFileMode",
    "ViewerDrawSize",
    "ViewerHDF5",
    # Aliases
    "Type",
    "Format",
    "FileMode",
    "DrawSize",
    "FileModeSpec",
]
