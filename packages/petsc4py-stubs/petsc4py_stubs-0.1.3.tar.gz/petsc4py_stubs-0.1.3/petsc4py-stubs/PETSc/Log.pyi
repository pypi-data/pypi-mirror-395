"""Type stubs for PETSc Log module."""


from typing import Any, Callable

from .Viewer import Viewer


class Log:
    """Logging support."""

    @classmethod
    def Stage(cls, name: str) -> LogStage:
        """Create a log stage.

        Not collective.

        Parameters
        ----------
        name
            Stage name.

        Returns
        -------
        stage : LogStage
            The log stage. If a stage already exists with name ``name`` then
            it is reused.

        See Also
        --------
        petsc.PetscLogStageRegister
        """
        ...

    @classmethod
    def Class(cls, name: str) -> LogClass:
        """Create a log class.

        Not collective.

        Parameters
        ----------
        name
            Class name.

        Returns
        -------
        klass : LogClass
            The log class. If a class already exists with name ``name`` then
            it is reused.

        See Also
        --------
        petsc.PetscClassIdRegister
        """
        ...

    @classmethod
    def Event(cls, name: str, klass: LogClass | None = None) -> LogEvent:
        """Create a log event.

        Not collective.

        Parameters
        ----------
        name
            Event name.
        klass
            Log class. If `None`, defaults to ``PETSC_OBJECT_CLASSID``.

        Returns
        -------
        event : LogEvent
            The log event. If an event already exists with name ``name`` then
            it is reused.

        See Also
        --------
        petsc.PetscLogEventRegister
        """
        ...

    @classmethod
    def begin(cls) -> None:
        """Turn on logging of objects and events.

        Collective.

        See Also
        --------
        petsc.PetscLogDefaultBegin
        """
        ...

    @classmethod
    def view(cls, viewer: Viewer | None = None) -> None:
        """Print the log.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc_options, petsc.PetscLogView
        """
        ...

    @classmethod
    def logFlops(cls, flops: float) -> None:
        """Add floating point operations to the current event.

        Not collective.

        Parameters
        ----------
        flops
            The number of flops to log.

        See Also
        --------
        petsc.PetscLogFlops
        """
        ...

    @classmethod
    def addFlops(cls, flops: float) -> None:
        """Add floating point operations to the current event.

        Not collective.

        Parameters
        ----------
        flops
            The number of flops to log.

        Notes
        -----
        This method exists for backward compatibility.

        See Also
        --------
        logFlops, petsc.PetscLogFlops
        """
        ...

    @classmethod
    def getFlops(cls) -> float:
        """Return the number of flops used on this processor since the program began.

        Not collective.

        Returns
        -------
        float
            Number of floating point operations.

        See Also
        --------
        petsc.PetscGetFlops
        """
        ...

    @classmethod
    def getTime(cls) -> float:
        """Return the current time of day in seconds.

        Collective.

        Returns
        -------
        wctime : float
            Current time.

        See Also
        --------
        petsc.PetscTime
        """
        ...

    @classmethod
    def getCPUTime(cls) -> float:
        """Return the CPU time."""
        ...

    @classmethod
    def EventDecorator(
        cls, name: str | None = None, klass: LogClass | None = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorate a function with a `PETSc` event."""
        ...

    @classmethod
    def isActive(cls) -> bool:
        """Return whether logging is currently in progress.

        Not collective.

        See Also
        --------
        petsc.PetscLogIsActive
        """
        ...


class LogStage:
    """Logging support for different stages."""

    @property
    def id(self) -> int:
        """The log stage identifier."""
        ...

    def __int__(self) -> int:
        ...

    def __enter__(self) -> LogStage:
        ...

    def __exit__(self, *exc: Any) -> None:
        ...

    def push(self) -> None:
        """Push a stage on the logging stack.

        Logically collective.

        See Also
        --------
        LogStage.pop, petsc.PetscLogStagePush
        """
        ...

    def pop(self) -> None:
        """Pop a stage from the logging stack.

        Logically collective.

        See Also
        --------
        LogStage.push, petsc.PetscLogStagePop
        """
        ...

    def getName(self) -> str:
        """Return the current stage name."""
        ...

    @property
    def name(self) -> str:
        """The current stage name."""
        ...

    def activate(self) -> None:
        """Activate the stage.

        Logically collective.

        See Also
        --------
        petsc.PetscLogStageSetActive
        """
        ...

    def deactivate(self) -> None:
        """Deactivate the stage.

        Logically collective.

        See Also
        --------
        petsc.PetscLogStageSetActive
        """
        ...

    def getActive(self) -> bool:
        """Check if the stage is activated.

        Not collective.

        See Also
        --------
        petsc.PetscLogStageGetActive
        """
        ...

    def setActive(self, flag: bool) -> None:
        """Activate or deactivate the current stage.

        Logically collective.

        See Also
        --------
        petsc.PetscLogStageSetActive
        """
        ...

    @property
    def active(self) -> bool:
        """Whether the stage is activate."""
        ...

    @active.setter
    def active(self, value: bool) -> None:
        ...

    def getVisible(self) -> bool:
        """Return whether the stage is visible.

        Not collective.

        See Also
        --------
        LogStage.setVisible, petsc.PetscLogStageSetVisible
        """
        ...

    def setVisible(self, flag: bool) -> None:
        """Set the visibility of the stage.

        Logically collective.

        Parameters
        ----------
        flag
            `True` to make the stage visible, `False` otherwise.

        See Also
        --------
        LogStage.getVisible, petsc.PetscLogStageSetVisible
        """
        ...

    @property
    def visible(self) -> bool:
        """Whether the stage is visible."""
        ...

    @visible.setter
    def visible(self, value: bool) -> None:
        ...


class LogClass:
    """Logging support."""

    @property
    def id(self) -> int:
        """The log class identifier."""
        ...

    def __int__(self) -> int:
        ...

    def getName(self) -> str:
        """Return the log class name."""
        ...

    @property
    def name(self) -> str:
        """The log class name."""
        ...

    def activate(self) -> None:
        """Activate the log class."""
        ...

    def deactivate(self) -> None:
        """Deactivate the log class."""
        ...

    def getActive(self) -> bool:
        """Not implemented."""
        ...

    def setActive(self, flag: bool) -> None:
        """Activate or deactivate the log class."""
        ...

    @property
    def active(self) -> bool:
        """Log class activation."""
        ...

    @active.setter
    def active(self, value: bool) -> None:
        ...


class LogEvent:
    """Logging support."""

    @property
    def id(self) -> int:
        """The log event identifier."""
        ...

    def __int__(self) -> int:
        ...

    def __enter__(self) -> LogEvent:
        ...

    def __exit__(self, *exc: Any) -> None:
        ...

    def begin(self, *objs: Any) -> None:
        """Log the beginning of a user event.

        Collective.

        Parameters
        ----------
        *objs
            objects associated with the event

        See Also
        --------
        petsc.PetscLogEventBegin
        """
        ...

    def end(self, *objs: Any) -> None:
        """Log the end of a user event.

        Collective.

        Parameters
        ----------
        *objs
            Objects associated with the event.

        See Also
        --------
        petsc.PetscLogEventEnd
        """
        ...

    def getName(self) -> str:
        """The current event name."""
        ...

    @property
    def name(self) -> str:
        """The current event name."""
        ...

    def activate(self) -> None:
        """Indicate that the event should be logged.

        Logically collective.

        See Also
        --------
        petsc.PetscLogEventActivate
        """
        ...

    def deactivate(self) -> None:
        """Indicate that the event should not be logged.

        Logically collective.

        See Also
        --------
        petsc.PetscLogEventDeactivate
        """
        ...

    def getActive(self) -> bool:
        """Not implemented."""
        ...

    def setActive(self, flag: bool) -> None:
        """Indicate whether or not the event should be logged.

        Logically collective.

        Parameters
        ----------
        flag
            Activate or deactivate the event.

        See Also
        --------
        petsc.PetscLogEventDeactivate, petsc.PetscLogEventActivate
        """
        ...

    @property
    def active(self) -> bool:
        """Event activation."""
        ...

    @active.setter
    def active(self, value: bool) -> None:
        ...

    def getActiveAll(self) -> bool:
        """Not implemented."""
        ...

    def setActiveAll(self, flag: bool) -> None:
        """Turn on logging of all events.

        Logically collective.

        Parameters
        ----------
        flag
            Activate (if `True`) or deactivate (if `False`) the logging of all events.

        See Also
        --------
        petsc.PetscLogEventSetActiveAll
        """
        ...

    @property
    def active_all(self) -> bool:
        """All events activation."""
        ...

    @active_all.setter
    def active_all(self, value: bool) -> None:
        ...

    def getPerfInfo(self, stage: int | None = None) -> dict[str, Any]:
        """Get the performance information about the given event in the given event.

        Not collective.

        Parameters
        ----------
        stage
            The stage number.

        Returns
        -------
        info : dict
            This structure is filled with the performance information.

        See Also
        --------
        petsc.PetscLogEventGetPerfInfo
        """
        ...
