"""Type stubs for PETSc Section module."""


from typing import Self, Sequence

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .IS import IS
from .SF import SF

# Import types from typing module
from petsc4py.typing import ArrayInt

class Section(Object):
    """Mapping from integers in a range to unstructured set of integers.

    A `Section` describes the layout of data over a set of points. It is used to
    define the layout of DOFs for finite element problems. A section maps
    points to offsets and DOF counts.

    See Also
    --------
    petsc.PetscSection
    """

    def view(self, viewer: Viewer | None = None) -> None:
        """View the section.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the section.

        See Also
        --------
        petsc.PetscSectionView
        """
        ...

    def destroy(self) -> Self:
        """Destroy a section.

        Not collective.

        See Also
        --------
        petsc.PetscSectionDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Allocate a section and set the map contents to the default.

        Collective.

        Typical calling sequence:
        - `create`
        - `setNumFields`
        - `setChart`
        - `setDof`
        - `setUp`
        - `getOffset`
        - `destroy`

        The `Section` object and methods are intended to be used in the PETSc
        Vec and Mat implementations. The indices returned by the `Section` are
        appropriate for the kind of `Vec` it is associated with. For example,
        if the vector being indexed is a local vector, we call the section a
        local section. If the section indexes a global vector, we call it a
        global section. For parallel vectors, like global vectors, we use
        negative indices to indicate DOFs owned by other processes.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscSectionCreate
        """
        ...

    def clone(self) -> Section:
        """Return a copy of the section.

        Collective.

        The copy is shallow, if possible.

        See Also
        --------
        petsc.PetscSectionClone
        """
        ...

    def setUp(self) -> None:
        """Calculate offsets.

        Not collective.

        Offsets are based on the number of degrees of freedom for each point.

        See Also
        --------
        petsc.PetscSectionSetUp
        """
        ...

    def reset(self) -> None:
        """Free all section data.

        Not collective.

        See Also
        --------
        petsc.PetscSectionReset
        """
        ...

    def getNumFields(self) -> int:
        """Return the number of fields in a section.

        Not collective.

        Returns ``0`` if no fields were defined.

        See Also
        --------
        setNumFields, petsc.PetscSectionGetNumFields
        """
        ...

    def setNumFields(self, numFields: int) -> None:
        """Set the number of fields in a section.

        Not collective.

        Parameters
        ----------
        numFields
            The number of fields.

        See Also
        --------
        getNumFields, petsc.PetscSectionSetNumFields
        """
        ...

    def getFieldName(self, field: int) -> str:
        """Return the name of a field in the section.

        Not collective.

        Parameters
        ----------
        field
            The field number.

        See Also
        --------
        setFieldName, petsc.PetscSectionGetFieldName
        """
        ...

    def setFieldName(self, field: int, fieldName: str) -> None:
        """Set the name of a field in the section.

        Not collective.

        Parameters
        ----------
        field
            The field number.
        fieldName
            The field name.

        See Also
        --------
        getFieldName, petsc.PetscSectionSetFieldName
        """
        ...

    def getFieldComponents(self, field: int) -> int:
        """Return the number of field components for the given field.

        Not collective.

        Parameters
        ----------
        field
            The field number.

        See Also
        --------
        setFieldComponents, petsc.PetscSectionGetFieldComponents
        """
        ...

    def setFieldComponents(self, field: int, numComp: int) -> None:
        """Set the number of field components for the given field.

        Not collective.

        Parameters
        ----------
        field
            The field number.
        numComp
            The number of field components.

        See Also
        --------
        getFieldComponents, petsc.PetscSectionSetFieldComponents
        """
        ...

    def getChart(self) -> tuple[int, int]:
        """Return the range in which points (indices) lie for this section.

        Not collective.

        The range is [pStart, pEnd), i.e., from the first point to one past the
        last point.

        See Also
        --------
        petsc.PetscSectionGetChart
        """
        ...

    def setChart(self, pStart: int, pEnd: int) -> None:
        """Set the range in which points (indices) lie for this section.

        Not collective.

        The range is [pStart, pEnd), i.e., from the first point to one past the
        last point.

        Parameters
        ----------
        pStart
            The first point.
        pEnd
            One past the last point.

        See Also
        --------
        petsc.PetscSectionSetChart
        """
        ...

    def getPermutation(self) -> IS:
        """Return the permutation that was set with `setPermutation`.

        Not collective.

        See Also
        --------
        setPermutation, petsc.PetscSectionGetPermutation
        """
        ...

    def setPermutation(self, perm: IS) -> None:
        """Set the permutation for [0, pEnd - pStart).

        Not collective.

        Parameters
        ----------
        perm
            The permutation of points.

        See Also
        --------
        getPermutation, petsc.PetscSectionSetPermutation
        """
        ...

    def getDof(self, point: int) -> int:
        """Return the number of degrees of freedom for a given point.

        Not collective.

        In a global section, this value will be negative for points not owned
        by this process.

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        setDof, addDof, petsc.PetscSectionGetDof
        """
        ...

    def setDof(self, point: int, numDof: int) -> None:
        """Set the number of degrees of freedom associated with a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        numDof
            The number of DOFs.

        See Also
        --------
        getDof, addDof, petsc.PetscSectionSetDof
        """
        ...

    def addDof(self, point: int, numDof: int) -> None:
        """Add ``numDof`` degrees of freedom associated with a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        numDof
            The number of additional DOFs.

        See Also
        --------
        setDof, getDof, petsc.PetscSectionAddDof
        """
        ...

    def getFieldDof(self, point: int, field: int) -> int:
        """Return the number of DOFs associated with a field on a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.

        See Also
        --------
        setFieldDof, petsc.PetscSectionGetFieldDof
        """
        ...

    def setFieldDof(self, point: int, field: int, numDof: int) -> None:
        """Set the number of DOFs associated with a field on a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.
        numDof
            The number of DOFs.

        See Also
        --------
        getFieldDof, addFieldDof, petsc.PetscSectionSetFieldDof
        """
        ...

    def addFieldDof(self, point: int, field: int, numDof: int) -> None:
        """Add ``numDof`` DOFs associated with a field on a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.
        numDof
            The number of additional DOFs.

        See Also
        --------
        setFieldDof, getFieldDof, petsc.PetscSectionAddFieldDof
        """
        ...

    def getConstraintDof(self, point: int) -> int:
        """Return the number of constrained DOFs associated with a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        setConstraintDof, petsc.PetscSectionGetConstraintDof
        """
        ...

    def setConstraintDof(self, point: int, numDof: int) -> None:
        """Set the number of constrained DOFs associated with a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        numDof
            The number of DOFs which are fixed by constraints.

        See Also
        --------
        getConstraintDof, addConstraintDof, petsc.PetscSectionSetConstraintDof
        """
        ...

    def addConstraintDof(self, point: int, numDof: int) -> None:
        """Increment the number of constrained DOFs for a given point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        numDof
            The number of additional DOFs which are fixed by constraints.

        See Also
        --------
        setConstraintDof, getConstraintDof, petsc.PetscSectionAddConstraintDof
        """
        ...

    def getFieldConstraintDof(self, point: int, field: int) -> int:
        """Return the number of constrained DOFs for a given field on a point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.

        See Also
        --------
        setFieldConstraintDof, petsc.PetscSectionGetFieldConstraintDof
        """
        ...

    def setFieldConstraintDof(self, point: int, field: int, numDof: int) -> None:
        """Set the number of constrained DOFs for a given field on a point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.
        numDof
            The number of DOFs which are fixed by constraints.

        See Also
        --------
        getFieldConstraintDof, addFieldConstraintDof
        petsc.PetscSectionSetFieldConstraintDof
        """
        ...

    def addFieldConstraintDof(self, point: int, field: int, numDof: int) -> None:
        """Add ``numDof`` constrained DOFs for a given field on a point.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field.
        numDof
            The number of additional DOFs which are fixed by constraints.

        See Also
        --------
        setFieldConstraintDof, getFieldConstraintDof
        petsc.PetscSectionAddFieldConstraintDof
        """
        ...

    def getConstraintIndices(self, point: int) -> ArrayInt:
        """Return the point DOFs numbers which are constrained for a given point.

        Not collective.

        The range is in [0, DOFs).

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        setConstraintIndices, petsc.PetscSectionGetConstraintIndices
        """
        ...

    def setConstraintIndices(self, point: int, indices: Sequence[int]) -> None:
        """Set the point DOFs numbers, in [0, DOFs), which are constrained.

        Not collective.

        Parameters
        ----------
        point
            The point.
        indices
            The constrained DOFs.

        See Also
        --------
        getConstraintIndices, petsc.PetscSectionSetConstraintIndices
        """
        ...

    def getFieldConstraintIndices(self, point: int, field: int) -> ArrayInt:
        """Return the field DOFs numbers, in [0, DOFs), which are constrained.

        Not collective.

        The constrained DOFs are sorted in ascending order.

        Parameters
        ----------
        field
            The field number.
        point
            The point.

        See Also
        --------
        setFieldConstraintIndices, petsc.PetscSectionGetFieldConstraintIndices
        """
        ...

    def setFieldConstraintIndices(
        self, point: int, field: int, indices: Sequence[int]
    ) -> None:
        """Set the field DOFs numbers, in [0, DOFs), which are constrained.

        Not collective.

        Parameters
        ----------
        point
            The point.
        field
            The field number.
        indices
            The constrained DOFs.

        See Also
        --------
        getFieldConstraintIndices, petsc.PetscSectionSetFieldConstraintIndices
        """
        ...

    def getMaxDof(self) -> int:
        """Return the maximum number of DOFs for any point in the section.

        Not collective.

        See Also
        --------
        petsc.PetscSectionGetMaxDof
        """
        ...

    def getStorageSize(self) -> int:
        """Return the size capable of holding all the DOFs defined in a section.

        Not collective.

        See Also
        --------
        getConstrainedStorageSize, petsc.PetscSectionGetStorageSize
        """
        ...

    def getConstrainedStorageSize(self) -> int:
        """Return the size capable of holding all unconstrained DOFs in a section.

        Not collective.

        See Also
        --------
        getStorageSize, petsc.PetscSectionGetConstrainedStorageSize
        """
        ...

    def getOffset(self, point: int) -> int:
        """Return the offset for the DOFs associated with the given point.

        Not collective.

        In a global section, this offset will be negative for points not owned
        by this process.

        Parameters
        ----------
        point
            The point.

        See Also
        --------
        setOffset, petsc.PetscSectionGetOffset
        """
        ...

    def setOffset(self, point: int, offset: int) -> None:
        """Set the offset for the DOFs associated with the given point.

        Not collective.

        The user usually does not call this function, but uses `setUp`.

        Parameters
        ----------
        point
            The point.
        offset
            The offset.

        See Also
        --------
        getOffset, petsc.PetscSectionSetOffset
        """
        ...

    def getFieldOffset(self, point: int, field: int) -> int:
        """Return the offset for the field DOFs on the given point.

        Not collective.

        In a global section, this offset will be negative for points not owned
        by this process.

        Parameters
        ----------
        point
            The point.
        field
            The field.

        See Also
        --------
        setFieldOffset, petsc.PetscSectionGetFieldOffset
        """
        ...

    def setFieldOffset(self, point: int, field: int, offset: int) -> None:
        """Set the offset for the DOFs on the given field at a point.

        Not collective.

        The user usually does not call this function, but uses `setUp`.

        Parameters
        ----------
        point
            The point.
        field
            The field.
        offset
            The offset.

        See Also
        --------
        getFieldOffset, petsc.PetscSectionSetFieldOffset
        """
        ...

    def getOffsetRange(self) -> tuple[int, int]:
        """Return the full range of offsets, [start, end), for a section.

        Not collective.

        See Also
        --------
        petsc.PetscSectionGetOffsetRange
        """
        ...

    def createGlobalSection(self, sf: SF) -> Section:
        """Create a section describing the global field layout.

        Collective.

        The section describes the global field layout using the local section
        and an `SF` describing the section point overlap.

        If we have a set of local sections defining the layout of a set of
        local vectors, and also an `SF` to determine which section points are
        shared and the ownership, we can calculate a global section defining
        the parallel data layout, and the associated global vector.

        This gives negative sizes and offsets to points not owned by this
        process.

        ``includeConstraints`` and ``localOffsets`` parameters of the C API
        are always set to `False`.

        Parameters
        ----------
        sf
            The `SF` describing the parallel layout of the section points
            (leaves are unowned local points).

        See Also
        --------
        petsc.PetscSectionCreateGlobalSection
        """
        ...

__all__ = [
    "Section",
]
