"""Type stubs for PETSc Object module - base class for all PETSc objects."""


from typing import Any, Self

from .Comm import Comm
from .Viewer import Viewer

class Object:
    """Base class wrapping a PETSc object.

    See Also
    --------
    petsc.PetscObject
    """

    def __bool__(self) -> bool:
        """Return whether the object has been created."""
        ...

    def __eq__(self, other: object) -> bool:
        """Return whether two objects are the same."""
        ...

    def __ne__(self, other: object) -> bool:
        """Return whether two objects are different."""
        ...

    def __copy__(self) -> Object:
        """Return a shallow copy of the object."""
        ...

    def __deepcopy__(self, memo: dict[Any, Any]) -> Object:
        """Return a deep copy of the object."""
        ...

    # --- attribute management ---

    def get_attr(self, name: str) -> Any:
        """Get an attribute from the object."""
        ...

    def set_attr(self, name: str, value: Any) -> Any:
        """Set an attribute on the object."""
        ...

    # --- view/destroy ---

    def view(self, viewer: Viewer | None = None) -> None:
        """Display the object.

        Collective.

        Parameters
        ----------
        viewer
            A Viewer instance or None for the default viewer.

        See Also
        --------
        petsc.PetscObjectView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the object.

        Collective.

        See Also
        --------
        petsc.PetscObjectDestroy
        """
        ...

    def getType(self) -> str:
        """Return the object type name.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetType
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for this object in option queries.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetOptionsPrefix
        """
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for this object in option queries.

        Collective.

        Parameters
        ----------
        prefix
            The prefix to prepend to all option names.

        See Also
        --------
        petsc.PetscObjectSetOptionsPrefix
        """
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for this object in option queries.

        Collective.

        Parameters
        ----------
        prefix
            The prefix to append to the current prefix.

        See Also
        --------
        petsc.PetscObjectAppendOptionsPrefix
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the object from the options database.

        Collective.

        See Also
        --------
        petsc.PetscObjectSetFromOptions
        """
        ...

    def getComm(self) -> Comm:
        """Return the MPI communicator associated with the object.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetComm
        """
        ...

    def getName(self) -> str:
        """Return the object name.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetName
        """
        ...

    def setName(self, name: str | None) -> None:
        """Set the object name.

        Collective.

        Parameters
        ----------
        name
            The object name.

        See Also
        --------
        petsc.PetscObjectSetName
        """
        ...

    def getClassId(self) -> int:
        """Return the class identifier of the object.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetClassId
        """
        ...

    def getClassName(self) -> str:
        """Return the class name of the object.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetClassName
        """
        ...

    def getRefCount(self) -> int:
        """Return the reference count of the object.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetReference
        """
        ...

    def incrementTabLevel(self, tab: int, parent: Object | None = None) -> None:
        """Increment the tab level used for viewing.

        Not collective.

        Parameters
        ----------
        tab
            The tab level increment.
        parent
            The parent object (for indentation purposes).

        See Also
        --------
        petsc.PetscObjectIncrementTabLevel
        """
        ...

    def compose(self, name: str, obj: Object | None) -> None:
        """Associate another object with this object.

        Not collective.

        Parameters
        ----------
        name
            The name associated with the child object.
        obj
            The child object, or None to remove.

        See Also
        --------
        petsc.PetscObjectCompose
        """
        ...

    def query(self, name: str) -> Object | None:
        """Return the object associated with a given name.

        Not collective.

        Parameters
        ----------
        name
            The name associated with the child object.

        See Also
        --------
        petsc.PetscObjectQuery
        """
        ...

    def getTabLevel(self) -> int:
        """Return the object tab level for viewing.

        Not collective.

        See Also
        --------
        petsc.PetscObjectGetTabLevel
        """
        ...

    def setTabLevel(self, level: int) -> None:
        """Set the object tab level for viewing.

        Not collective.

        Parameters
        ----------
        level
            The tab level.

        See Also
        --------
        petsc.PetscObjectSetTabLevel
        """
        ...

    def stateIncrease(self) -> None:
        """Increment the object state.

        Logically collective.

        See Also
        --------
        petsc.PetscObjectStateIncrease
        """
        ...

    def getDict(self) -> dict[str, Any]:
        """Return the dictionary for the object.

        Not collective.
        """
        ...

    # Properties

    @property
    def handle(self) -> int:
        """The object handle."""
        ...

    @property
    def klass(self) -> str:
        """The class name."""
        ...

    @property
    def type(self) -> str:
        """The object type."""
        ...

    @type.setter
    def type(self, value: str) -> None: ...
    @property
    def prefix(self) -> str:
        """The options prefix."""
        ...

    @prefix.setter
    def prefix(self, value: str | None) -> None: ...
    @property
    def name(self) -> str:
        """The object name."""
        ...

    @name.setter
    def name(self, value: str | None) -> None: ...
    @property
    def comm(self) -> Comm:
        """The object communicator."""
        ...

    @property
    def refcount(self) -> int:
        """The reference count."""
        ...

    @property
    def id(self) -> int:
        """The object identifier."""
        ...

    @property
    def classid(self) -> int:
        """The class identifier."""
        ...

    @property
    def fortran(self) -> int:
        """The Fortran handle."""
        ...
