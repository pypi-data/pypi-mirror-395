"""Type stubs for PETSc Device module."""

from typing import Self

from .Object import Object
from .Viewer import Viewer

from .Comm import Comm

class DeviceType:
    """The type of device.

    See Also
    --------
    Device, Device.create, Device.getDeviceType, Device.type, petsc.PetscDeviceType

    """

    HOST: int
    CUDA: int
    HIP: int
    SYCL: int
    DEFAULT: int

class StreamType:
    """The type of stream.

    See Also
    --------
    DeviceContext, DeviceContext.getStreamType
    DeviceContext.setStreamType, petsc.PetscStreamType

    """

    DEFAULT: int
    NONBLOCKING: int
    DEFAULT_WITH_BARRIER: int
    NONBLOCKING_WITH_BARRIER: int

class DeviceJoinMode:
    """The type of join to perform.

    See Also
    --------
    DeviceContext, DeviceContext.join, DeviceContext.fork
    petsc.PetscDeviceContextJoinMode

    """

    DESTROY: int
    SYNC: int
    NO_SYNC: int

class Device:
    """The device object.

    Represents a handle to an accelerator (which may be the host).

    See Also
    --------
    DeviceContext, petsc.PetscDevice

    """

    Type = DeviceType

    @classmethod
    def create(cls, dtype: DeviceType | None = None, device_id: int = ...) -> Device:
        """Create a device object.

        Not collective.

        Parameters
        ----------
        dtype
            The type of device to create (or `None` for the default).

        device_id
            The numeric id of the device to create.

        See Also
        --------
        destroy, petsc.PetscDeviceCreate

        """
        ...

    def destroy(self) -> None:
        """Destroy a device object.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceDestroy

        """
        ...

    def configure(self) -> None:
        """Configure and setup a device object.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceConfigure

        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View a device object.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.PetscDeviceView

        """
        ...

    def getDeviceType(self) -> str:
        """Return the type of the device.

        Not collective.

        See Also
        --------
        type, petsc.PetscDeviceGetType

        """
        ...

    def getDeviceId(self) -> int:
        """Return the device id.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceGetDeviceId

        """
        ...

    @staticmethod
    def setDefaultType(device_type: DeviceType | str) -> None:
        """Set the device type to be used as the default in subsequent calls to `create`.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceSetDefaultDeviceType

        """
        ...

    @property
    def type(self) -> str:
        """The device type."""
        ...

    @property
    def device_id(self) -> int:
        """The device id."""
        ...

class DeviceContext(Object):
    """DeviceContext object.

    Represents an abstract handle to a device context.

    See Also
    --------
    Device, petsc.PetscDeviceContext

    """

    JoinMode = DeviceJoinMode

    def create(self) -> Self:
        """Create an empty DeviceContext.

        Not collective.

        See Also
        --------
        destroy, Device, petsc.PetscDeviceContextCreate

        """
        ...

    def destroy(self) -> Self:
        """Destroy a device context.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceContextDestroy

        """
        ...

    def getStreamType(self) -> str:
        """Return the `StreamType`.

        Not collective.

        See Also
        --------
        stream_type, setStreamType, petsc.PetscDeviceContextGetStreamType

        """
        ...

    def setStreamType(self, stream_type: StreamType | str) -> None:
        """Set the `StreamType`.

        Not collective.

        Parameters
        ----------
        stream_type
            The type of stream to set

        See Also
        --------
        stream_type, getStreamType, petsc.PetscDeviceContextSetStreamType

        """
        ...

    def getDevice(self) -> Device:
        """Get the `Device` which this instance is attached to.

        Not collective.

        See Also
        --------
        setDevice, device, Device, petsc.PetscDeviceContextGetDevice

        """
        ...

    def setDevice(self, device: Device) -> None:
        """Set the `Device` which this `DeviceContext` is attached to.

        Collective.

        Parameters
        ----------
        device
            The `Device` to which this instance is attached to.

        See Also
        --------
        getDevice, device, Device, petsc.PetscDeviceContextSetDevice

        """
        ...

    def setUp(self) -> None:
        """Set up the internal data structures for using the device context.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceContextSetUp

        """
        ...

    def duplicate(self) -> DeviceContext:
        """Duplicate a the device context.

        Not collective.

        See Also
        --------
        create, petsc.PetscDeviceContextDuplicate

        """
        ...

    def idle(self) -> bool:
        """Return whether the underlying stream for the device context is idle.

        Not collective.

        See Also
        --------
        synchronize, petsc.PetscDeviceContextQueryIdle

        """
        ...

    def waitFor(self, other: DeviceContext | None) -> None:
        """Make this instance wait for ``other``.

        Not collective.

        Parameters
        ----------
        other
            The other `DeviceContext` to wait for

        See Also
        --------
        fork, join, petsc.PetscDeviceContextWaitForContext

        """
        ...

    def fork(
        self, n: int, stream_type: StreamType | str | None = None
    ) -> list[DeviceContext]:
        """Create multiple device contexts which are all logically dependent on this one.

        Not collective.

        Parameters
        ----------
        n
            The number of device contexts to create.
        stream_type
            The type of stream of the forked device context.

        Examples
        --------
        The device contexts created must be destroyed using `join`.

        >>> dctx = PETSc.DeviceContext().getCurrent()
        >>> dctxs = dctx.fork(4)
        >>> ... # perform computations
        >>> # we can mix various join modes
        >>> dctx.join(PETSc.DeviceContext.JoinMode.SYNC, dctxs[0:2])
        >>> dctx.join(PETSc.DeviceContext.JoinMode.SYNC, dctxs[2:])
        >>> ... # some more computations and joins
        >>> # dctxs must be all destroyed with joinMode.DESTROY
        >>> dctx.join(PETSc.DeviceContext.JoinMode.DESTROY, dctxs)

        See Also
        --------
        join, waitFor, petsc.PetscDeviceContextFork

        """
        ...

    def join(
        self, join_mode: DeviceJoinMode | str, py_sub_ctxs: list[DeviceContext]
    ) -> None:
        """Join a set of device contexts on this one.

        Not collective.

        Parameters
        ----------
        join_mode
            The type of join to perform.
        py_sub_ctxs
            The list of device contexts to join.

        See Also
        --------
        fork, waitFor, petsc.PetscDeviceContextJoin

        """
        ...

    def synchronize(self) -> None:
        """Synchronize a device context.

        Not collective.

        Notes
        -----
        The underlying stream is considered idle after this routine returns,
        i.e. `idle` will return ``True``.

        See Also
        --------
        idle, petsc.PetscDeviceContextSynchronize

        """
        ...

    def setFromOptions(self, comm: Comm | None = None) -> None:
        """Configure the `DeviceContext` from the options database.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        Sys.getDefaultComm, petsc.PetscDeviceContextSetFromOptions

        """
        ...

    @staticmethod
    def getCurrent() -> DeviceContext:
        """Return the current device context.

        Not collective.

        See Also
        --------
        current, setCurrent, petsc.PetscDeviceContextGetCurrentContext

        """
        ...

    @staticmethod
    def setCurrent(dctx: DeviceContext | None) -> None:
        """Set the current device context.

        Not collective.

        Parameters
        ----------
        dctx
            The `DeviceContext` to set as current (or `None` to use
            the default context).

        See Also
        --------
        current, getCurrent, petsc.PetscDeviceContextSetCurrentContext

        """
        ...

    @property
    def stream_type(self) -> str:
        """The stream type."""
        ...

    @stream_type.setter
    def stream_type(self, stype: StreamType | str) -> None: ...
    @property
    def device(self) -> Device:
        """The device associated to the device context."""
        ...

    @device.setter
    def device(self, device: Device) -> None: ...
    @property
    def current(self) -> DeviceContext:
        """The current global device context."""
        ...

    @current.setter
    def current(self, dctx: DeviceContext | None) -> None: ...
