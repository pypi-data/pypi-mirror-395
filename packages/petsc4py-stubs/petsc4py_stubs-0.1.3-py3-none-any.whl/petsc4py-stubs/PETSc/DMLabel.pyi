"""Type stubs for PETSc DMLabel module."""


from typing import Sequence, Self

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .IS import IS
from .SF import SF
from .Section import Section

class DMLabel(Object):
    """An object representing a subset of mesh entities from a `DM`.

    A DMLabel marks mesh entities (points) with integer values, allowing you to
    identify subsets of the mesh such as boundary conditions, material regions,
    etc. Points may have multiple labels, and labels can be distributed across
    processors.

    See Also
    --------
    petsc.DMLabel
    """

    def destroy(self) -> Self:
        """Destroy the label.

        Collective.

        See Also
        --------
        petsc.DMLabelDestroy
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the label.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the graph.

        See Also
        --------
        petsc.DMLabelView
        """
        ...

    def create(self, name: str, comm: Comm | None = None) -> Self:
        """Create a `DMLabel` object, which is a multimap.

        Collective.

        Parameters
        ----------
        name
            The label name.
        comm
            MPI communicator, defaults to `COMM_SELF`.

        See Also
        --------
        petsc.DMLabelCreate
        """
        ...

    def duplicate(self) -> DMLabel:
        """Duplicate the `DMLabel`.

        Collective.

        See Also
        --------
        petsc.DMLabelDuplicate
        """
        ...

    def reset(self) -> None:
        """Destroy internal data structures in the `DMLabel`.

        Not collective.

        See Also
        --------
        petsc.DMLabelReset
        """
        ...

    def insertIS(self, iset: IS, value: int) -> Self:
        """Set all points in the `IS` to a value.

        Not collective.

        Parameters
        ----------
        iset
            The point IS.
        value
            The point value.

        See Also
        --------
        petsc.DMLabelInsertIS
        """
        ...

    def setValue(self, point: int, value: int) -> None:
        """Set the value a label assigns to a point.

        Not collective.

        If the value is the same as the label's default value (which is
        initially ``-1``, and can be changed with `setDefaultValue`), this
        function will do nothing.

        Parameters
        ----------
        point
            The point.
        value
            The point value.

        See Also
        --------
        getValue, setDefaultValue, petsc.DMLabelSetValue
        """
        ...

    def getValue(self, point: int) -> int:
        """Return the value a label assigns to a point.

        Not collective.

        If no value was assigned, a default value will be returned.
        The default value, initially ``-1``, can be changed with
        `setDefaultValue`.

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        setValue, setDefaultValue, petsc.DMLabelGetValue
        """
        ...

    def getDefaultValue(self) -> int:
        """Return the default value returned by `getValue`.

        Not collective.

        The default value is returned if a point has not been explicitly given
        a value. When a label is created, it is initialized to ``-1``.

        See Also
        --------
        setDefaultValue, petsc.DMLabelGetDefaultValue
        """
        ...

    def setDefaultValue(self, value: int) -> None:
        """Set the default value returned by `getValue`.

        Not collective.

        The value is used if a point has not been explicitly given a value.
        When a label is created, the default value is initialized to ``-1``.

        Parameters
        ----------
        value
            The default value.

        See Also
        --------
        getDefaultValue, petsc.DMLabelSetDefaultValue
        """
        ...

    def clearValue(self, point: int, value: int) -> None:
        """Clear the value a label assigns to a point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        value
            The point value.

        See Also
        --------
        petsc.DMLabelClearValue
        """
        ...

    def addStratum(self, value: int) -> None:
        """Add a new stratum value in a `DMLabel`.

        Not collective.

        Parameters
        ----------
        value
            The stratum value.

        See Also
        --------
        addStrata, addStrataIS, petsc.DMLabelAddStratum
        """
        ...

    def addStrata(self, strata: Sequence[int]) -> None:
        """Add new stratum values in a `DMLabel`.

        Not collective.

        Parameters
        ----------
        strata
            The stratum values.

        See Also
        --------
        addStrataIS, addStratum, petsc.DMLabelAddStrata
        """
        ...

    def addStrataIS(self, iset: IS) -> None:
        """Add new stratum values in a `DMLabel`.

        Not collective.

        Parameters
        ----------
        iset
            Index set with stratum values.

        See Also
        --------
        addStrata, addStratum, petsc.DMLabelAddStrataIS
        """
        ...

    def getNumValues(self) -> int:
        """Return the number of values that the `DMLabel` takes.

        Not collective.

        See Also
        --------
        petsc.DMLabelGetNumValues
        """
        ...

    def getValueIS(self) -> IS:
        """Return an `IS` of all values that the `DMLabel` takes.

        Not collective.

        See Also
        --------
        petsc.DMLabelGetValueIS
        """
        ...

    def stratumHasPoint(self, value: int, point: int) -> bool:
        """Return whether the stratum contains a point.

        Not collective.

        Parameters
        ----------
        value
            The stratum value.
        point
            The point.

        See Also
        --------
        petsc.DMLabelStratumHasPoint
        """
        ...

    def hasStratum(self, value: int) -> bool:
        """Determine whether points exist with the given value.

        Not collective.

        Parameters
        ----------
        value
            The stratum value.

        See Also
        --------
        petsc.DMLabelHasStratum
        """
        ...

    def getStratumSize(self, stratum: int) -> int:
        """Return the size of a stratum.

        Not collective.

        Parameters
        ----------
        stratum
            The stratum value.

        See Also
        --------
        petsc.DMLabelGetStratumSize
        """
        ...

    def getStratumIS(self, stratum: int) -> IS:
        """Return an `IS` with the stratum points.

        Not collective.

        Parameters
        ----------
        stratum
            The stratum value.

        See Also
        --------
        setStratumIS, petsc.DMLabelGetStratumIS
        """
        ...

    def setStratumIS(self, stratum: int, iset: IS) -> None:
        """Set the stratum points using an `IS`.

        Not collective.

        Parameters
        ----------
        stratum
            The stratum value.
        iset
            The stratum points.

        See Also
        --------
        getStratumIS, petsc.DMLabelSetStratumIS
        """
        ...

    def clearStratum(self, stratum: int) -> None:
        """Remove a stratum.

        Not collective.

        Parameters
        ----------
        stratum
            The stratum value.

        See Also
        --------
        petsc.DMLabelClearStratum
        """
        ...

    def computeIndex(self) -> None:
        """Create an index structure for membership determination.

        Not collective.

        Automatically determines the bounds.

        See Also
        --------
        petsc.DMLabelComputeIndex
        """
        ...

    def createIndex(self, pStart: int, pEnd: int) -> None:
        """Create an index structure for membership determination.

        Not collective.

        Parameters
        ----------
        pStart
            The smallest point.
        pEnd
            The largest point + 1.

        See Also
        --------
        destroyIndex, petsc.DMLabelCreateIndex
        """
        ...

    def destroyIndex(self) -> None:
        """Destroy the index structure.

        Not collective.

        See Also
        --------
        createIndex, petsc.DMLabelDestroyIndex
        """
        ...

    def hasValue(self, value: int) -> bool:
        """Determine whether a label assigns the value to any point.

        Not collective.

        Parameters
        ----------
        value
            The value.

        See Also
        --------
        hasPoint, petsc.DMLabelHasValue
        """
        ...

    def hasPoint(self, point: int) -> bool:
        """Determine whether the label contains a point.

        Not collective.

        The user must call `createIndex` before this function.

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        hasValue, petsc.DMLabelHasPoint
        """
        ...

    def getBounds(self) -> tuple[int, int]:
        """Return the smallest and largest point in the label.

        Not collective.

        The returned values are the smallest point and the largest point + 1.

        See Also
        --------
        petsc.DMLabelGetBounds
        """
        ...

    def filter(self, start: int, end: int) -> None:
        """Remove all points outside of [start, end).

        Not collective.

        Parameters
        ----------
        start
            The first point kept.
        end
            One more than the last point kept.

        See Also
        --------
        petsc.DMLabelFilter
        """
        ...

    def permute(self, permutation: IS) -> DMLabel:
        """Create a new label with permuted points.

        Not collective.

        Parameters
        ----------
        permutation
            The point permutation.

        See Also
        --------
        petsc.DMLabelPermute
        """
        ...

    def distribute(self, sf: SF) -> DMLabel:
        """Create a new label pushed forward over the `SF`.

        Collective.

        Parameters
        ----------
        sf
            The map from old to new distribution.

        See Also
        --------
        gather, petsc.DMLabelDistribute
        """
        ...

    def gather(self, sf: SF) -> DMLabel:
        """Gather all label values from leaves into roots.

        Collective.

        This is the inverse operation to `distribute`.

        Parameters
        ----------
        sf
            The `SF` communication map.

        See Also
        --------
        distribute, petsc.DMLabelGather
        """
        ...

    def convertToSection(self) -> tuple[Section, IS]:
        """Return a `Section` and `IS` that encode the label.

        Not collective.

        See Also
        --------
        petsc.DMLabelConvertToSection
        """
        ...

    def getNonEmptyStratumValuesIS(self) -> IS:
        """Return an `IS` of all values that the `DMLabel` takes.

        Not collective.

        See Also
        --------
        petsc.DMLabelGetNonEmptyStratumValuesIS
        """
        ...

__all__ = [
    "DMLabel",
]
