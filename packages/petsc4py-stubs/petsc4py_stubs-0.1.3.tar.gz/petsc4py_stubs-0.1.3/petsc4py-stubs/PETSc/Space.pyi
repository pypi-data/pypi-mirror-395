"""Type stubs for PETSc Space module."""


from typing import Self

from .Object import Object
from .Comm import Comm
from .Viewer import Viewer
from .DM import DM
from .DT import Quad

# Import types from typing module
from petsc4py.typing import ArrayInt

class SpaceType:
    """The function space types."""

    POLYNOMIAL: str
    PTRIMMED: str
    TENSOR: str
    SUM: str
    POINT: str
    SUBSPACE: str
    WXY: str

class DualSpaceType:
    """The dual space types."""

    LAGRANGE: str
    SIMPLE: str
    REFINED: str
    BDM: str

class Space(Object):
    """Function space object.

    See Also
    --------
    petsc.PetscSpace
    """

    Type = SpaceType

    def setUp(self) -> None:
        """Construct data structures for the `Space`.

        Collective.

        See Also
        --------
        petsc.PetscSpaceSetUp
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty `Space` object.

        Collective.

        The type can then be set with `setType`.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscSpaceCreate
        """
        ...

    def destroy(self) -> Self:
        """Destroy the `Space` object.

        Collective.

        See Also
        --------
        petsc.PetscSpaceDestroy
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View a `Space`.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the `Space`.

        See Also
        --------
        petsc.PetscSpaceView
        """
        ...

    def setFromOptions(self) -> None:
        """Set parameters in `Space` from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.PetscSpaceSetFromOptions
        """
        ...

    def getDimension(self) -> int:
        """Return the number of basis vectors.

        Not collective.

        See Also
        --------
        petsc.PetscSpaceGetDimension
        """
        ...

    def getDegree(self) -> tuple[int, int]:
        """Return the polynomial degrees that characterize this space.

        Not collective.

        Returns
        -------
        minDegree : int
            The degree of the largest polynomial space contained in the space.
        maxDegree : int
            The degree of the smallest polynomial space containing the space.

        See Also
        --------
        setDegree, petsc.PetscSpaceGetDegree
        """
        ...

    def setDegree(self, degree: int | None, maxDegree: int | None) -> None:
        """Set the degree of approximation for this space.

        Logically collective.

        One of ``degree`` and ``maxDegree`` can be `None`.

        Parameters
        ----------
        degree
            The degree of the largest polynomial space contained in the space.
        maxDegree
            The degree of the largest polynomial space containing the space.

        See Also
        --------
        getDegree, petsc.PetscSpaceSetDegree
        """
        ...

    def getNumVariables(self) -> int:
        """Return the number of variables for this space.

        Not collective.

        See Also
        --------
        setNumVariables, petsc.PetscSpaceGetNumVariables
        """
        ...

    def setNumVariables(self, n: int) -> None:
        """Set the number of variables for this space.

        Logically collective.

        Parameters
        ----------
        n
            The number of variables (``x``, ``y``, ``z`` etc.).

        See Also
        --------
        getNumVariables, petsc.PetscSpaceSetNumVariables
        """
        ...

    def getNumComponents(self) -> int:
        """Return the number of components for this space.

        Not collective.

        See Also
        --------
        setNumComponents, petsc.PetscSpaceGetNumComponents
        """
        ...

    def setNumComponents(self, nc: int) -> None:
        """Set the number of components for this space.

        Logically collective.

        Parameters
        ----------
        nc
            The number of components.

        See Also
        --------
        getNumComponents, petsc.PetscSpaceSetNumComponents
        """
        ...

    def getType(self) -> str:
        """Return the type of the space object.

        Not collective.

        See Also
        --------
        setType, petsc.PetscSpaceGetType
        """
        ...

    def setType(self, space_type: SpaceType | str) -> Self:
        """Build a particular type of space.

        Collective.

        Parameters
        ----------
        space_type
            The kind of space.

        See Also
        --------
        getType, petsc.PetscSpaceSetType
        """
        ...

    def getSumConcatenate(self) -> bool:
        """Return the concatenate flag for this space.

        Not collective.

        A concatenated sum space will have the number of components equal to
        the sum of the number of components of all subspaces.
        A non-concatenated, or direct sum space will have the same number of
        components as its subspaces.

        See Also
        --------
        setSumConcatenate, petsc.PetscSpaceSumGetConcatenate
        """
        ...

    def setSumConcatenate(self, concatenate: bool) -> None:
        """Set the concatenate flag for this space.

        Logically collective.

        A concatenated sum space will have the number of components equal to
        the sum of the number of components of all subspaces.
        A non-concatenated, or direct sum space will have the same number of
        components as its subspaces.

        Parameters
        ----------
        concatenate
            `True` if subspaces are concatenated components,
            `False` if direct summands.

        See Also
        --------
        getSumConcatenate, petsc.PetscSpaceSumSetConcatenate
        """
        ...

    def getSumNumSubspaces(self) -> int:
        """Return the number of spaces in the sum.

        Not collective.

        See Also
        --------
        setSumNumSubspaces, petsc.PetscSpaceSumGetNumSubspaces
        """
        ...

    def getSumSubspace(self, s: int) -> Space:
        """Return a space in the sum.

        Not collective.

        Parameters
        ----------
        s
            The space number.

        See Also
        --------
        setSumSubspace, petsc.PetscSpaceSumGetSubspace
        """
        ...

    def setSumSubspace(self, s: int, subsp: Space) -> None:
        """Set a space in the sum.

        Logically collective.

        Parameters
        ----------
        s
            The space number.
        subsp
            The number of spaces.

        See Also
        --------
        getSumSubspace, petsc.PetscSpaceSumSetSubspace
        """
        ...

    def setSumNumSubspaces(self, numSumSpaces: int) -> None:
        """Set the number of spaces in the sum.

        Logically collective.

        Parameters
        ----------
        numSumSpaces
            The number of spaces.

        See Also
        --------
        getSumNumSubspaces, petsc.PetscSpaceSumSetNumSubspaces
        """
        ...

    def getTensorNumSubspaces(self) -> int:
        """Return the number of spaces in the tensor product.

        Not collective.

        See Also
        --------
        setTensorNumSubspaces, petsc.PetscSpaceTensorGetNumSubspaces
        """
        ...

    def setTensorSubspace(self, s: int, subsp: Space) -> None:
        """Set a space in the tensor product.

        Logically collective.

        Parameters
        ----------
        s
            The space number.
        subsp
            The number of spaces.

        See Also
        --------
        getTensorSubspace, petsc.PetscSpaceTensorSetSubspace
        """
        ...

    def getTensorSubspace(self, s: int) -> Space:
        """Return a space in the tensor product.

        Not collective.

        Parameters
        ----------
        s
            The space number.

        See Also
        --------
        setTensorSubspace, petsc.PetscSpaceTensorGetSubspace
        """
        ...

    def setTensorNumSubspaces(self, numTensSpaces: int) -> None:
        """Set the number of spaces in the tensor product.

        Logically collective.

        Parameters
        ----------
        numTensSpaces
            The number of spaces.

        See Also
        --------
        getTensorNumSubspaces, petsc.PetscSpaceTensorSetNumSubspaces
        """
        ...

    def getPolynomialTensor(self) -> bool:
        """Return whether a function space is a space of tensor polynomials.

        Not collective.

        Return `True` if a function space is a space of tensor polynomials
        (the space is spanned by polynomials whose degree in each variable is
        bounded by the given order), as opposed to polynomials (the space is
        spanned by polynomials whose total degree—summing over all variables
        is bounded by the given order).

        See Also
        --------
        setPolynomialTensor, petsc.PetscSpacePolynomialGetTensor
        """
        ...

    def setPolynomialTensor(self, tensor: bool) -> None:
        """Set whether a function space is a space of tensor polynomials.

        Logically collective.

        Set to `True` for a function space which is a space of tensor
        polynomials (the space is spanned by polynomials whose degree in each
        variable is bounded by the given order), as opposed to polynomials
        (the space is spanned by polynomials whose total degree—summing over
        all variables is bounded by the given order).

        Parameters
        ----------
        tensor
            `True` for a tensor polynomial space, `False` for a polynomial
            space.

        See Also
        --------
        getPolynomialTensor, petsc.PetscSpacePolynomialSetTensor
        """
        ...

    def setPointPoints(self, quad: Quad) -> None:
        """Set the evaluation points for the space to be based on a quad.

        Logically collective.

        Sets the evaluation points for the space to coincide with the points
        of a quadrature rule.

        Parameters
        ----------
        quad
            The `Quad` defining the points.

        See Also
        --------
        getPointPoints, petsc.PetscSpacePointSetPoints
        """
        ...

    def getPointPoints(self) -> Quad:
        """Return the evaluation points for the space as the points of a quad.

        Logically collective.

        See Also
        --------
        setPointPoints, petsc.PetscSpacePointGetPoints
        """
        ...

    def setPTrimmedFormDegree(self, formDegree: int) -> None:
        """Set the form degree of the trimmed polynomials.

        Logically collective.

        Parameters
        ----------
        formDegree
            The form degree.

        See Also
        --------
        getPTrimmedFormDegree, petsc.PetscSpacePTrimmedSetFormDegree
        """
        ...

    def getPTrimmedFormDegree(self) -> int:
        """Return the form degree of the trimmed polynomials.

        Not collective.

        See Also
        --------
        setPTrimmedFormDegree, petsc.PetscSpacePTrimmedGetFormDegree
        """
        ...

class DualSpace(Object):
    """Dual space to a linear space.

    See Also
    --------
    petsc.PetscDualSpace
    """

    Type = DualSpaceType

    def setUp(self) -> None:
        """Construct a basis for a `DualSpace`.

        Collective.

        See Also
        --------
        petsc.PetscDualSpaceSetUp
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty `DualSpace` object.

        Collective.

        The type can then be set with `setType`.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscDualSpaceCreate
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View a `DualSpace`.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the `DualSpace`.

        See Also
        --------
        petsc.PetscDualSpaceView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the `DualSpace` object.

        Collective.

        See Also
        --------
        petsc.PetscDualSpaceDestroy
        """
        ...

    def duplicate(self) -> DualSpace:
        """Create a duplicate `DualSpace` object that is not set up.

        Collective.

        See Also
        --------
        petsc.PetscDualSpaceDuplicate
        """
        ...

    def getDM(self) -> DM:
        """Return the `DM` representing the reference cell of a `DualSpace`.

        Not collective.

        See Also
        --------
        setDM, petsc.PetscDualSpaceGetDM
        """
        ...

    def setDM(self, dm: DM) -> None:
        """Set the `DM` representing the reference cell.

        Not collective.

        Parameters
        ----------
        dm
            The reference cell.

        See Also
        --------
        getDM, petsc.PetscDualSpaceSetDM
        """
        ...

    def getDimension(self) -> int:
        """Return the dimension of the dual space.

        Not collective.

        The dimension of the dual space, i.e. the number of basis functionals.

        See Also
        --------
        petsc.PetscDualSpaceGetDimension
        """
        ...

    def getNumComponents(self) -> int:
        """Return the number of components for this space.

        Not collective.

        See Also
        --------
        setNumComponents, petsc.PetscDualSpaceGetNumComponents
        """
        ...

    def setNumComponents(self, nc: int) -> None:
        """Set the number of components for this space.

        Logically collective.

        Parameters
        ----------
        nc
            The number of components

        See Also
        --------
        getNumComponents, petsc.PetscDualSpaceSetNumComponents
        """
        ...

    def getType(self) -> str:
        """Return the type of the dual space object.

        Not collective.

        See Also
        --------
        setType, petsc.PetscDualSpaceGetType
        """
        ...

    def setType(self, dualspace_type: DualSpaceType | str) -> Self:
        """Build a particular type of dual space.

        Collective.

        Parameters
        ----------
        dualspace_type
            The kind of space.

        See Also
        --------
        getType, petsc.PetscDualSpaceSetType
        """
        ...

    def getOrder(self) -> int:
        """Return the order of the dual space.

        Not collective.

        See Also
        --------
        setOrder, petsc.PetscDualSpaceGetOrder
        """
        ...

    def setOrder(self, order: int) -> None:
        """Set the order of the dual space.

        Not collective.

        Parameters
        ----------
        order
            The order.

        See Also
        --------
        getOrder, petsc.PetscDualSpaceSetOrder
        """
        ...

    def getNumDof(self) -> ArrayInt:
        """Return the number of degrees of freedom for each spatial dimension.

        Not collective.

        See Also
        --------
        petsc.PetscDualSpaceGetNumDof
        """
        ...

    def getFunctional(self, i: int) -> Quad:
        """Return the i-th basis functional in the dual space.

        Not collective.

        Parameters
        ----------
        i
            The basis number.

        See Also
        --------
        petsc.PetscDualSpaceGetFunctional
        """
        ...

    def getInteriorDimension(self) -> int:
        """Return the interior dimension of the dual space.

        Not collective.

        The interior dimension of the dual space, i.e. the number of basis
        functionals assigned to the interior of the reference domain.

        See Also
        --------
        petsc.PetscDualSpaceGetInteriorDimension
        """
        ...

    def getLagrangeContinuity(self) -> bool:
        """Return whether the element is continuous.

        Not collective.

        See Also
        --------
        setLagrangeContinuity, petsc.PetscDualSpaceLagrangeGetContinuity
        """
        ...

    def setLagrangeContinuity(self, continuous: bool) -> None:
        """Indicate whether the element is continuous.

        Not collective.

        Parameters
        ----------
        continuous
            The flag for element continuity.

        See Also
        --------
        getLagrangeContinuity, petsc.PetscDualSpaceLagrangeSetContinuity
        """
        ...

    def getLagrangeTensor(self) -> bool:
        """Return the tensor nature of the dual space.

        Not collective.

        See Also
        --------
        setLagrangeTensor, petsc.PetscDualSpaceLagrangeGetTensor
        """
        ...

    def setLagrangeTensor(self, tensor: bool) -> None:
        """Set the tensor nature of the dual space.

        Not collective.

        Parameters
        ----------
        tensor
            Whether the dual space has tensor layout (vs. simplicial).

        See Also
        --------
        getLagrangeTensor, petsc.PetscDualSpaceLagrangeSetTensor
        """
        ...

    def getLagrangeTrimmed(self) -> bool:
        """Return the trimmed nature of the dual space.

        Not collective.

        See Also
        --------
        setLagrangeTrimmed, petsc.PetscDualSpaceLagrangeGetTrimmed
        """
        ...

    def setLagrangeTrimmed(self, trimmed: bool) -> None:
        """Set the trimmed nature of the dual space.

        Not collective.

        Parameters
        ----------
        trimmed
            Whether the dual space represents to dual basis of a trimmed
            polynomial space (e.g. Raviart-Thomas and higher order /
            other form degree variants).

        See Also
        --------
        getLagrangeTrimmed, petsc.PetscDualSpaceLagrangeSetTrimmed
        """
        ...

    def setSimpleDimension(self, dim: int) -> None:
        """Set the number of functionals in the dual space basis.

        Logically collective.

        Parameters
        ----------
        dim
            The basis dimension.

        See Also
        --------
        petsc.PetscDualSpaceSimpleSetDimension
        """
        ...

    def setSimpleFunctional(self, func: int, functional: Quad) -> None:
        """Set the given basis element for this dual space.

        Not collective.

        Parameters
        ----------
        func
            The basis index.
        functional
            The basis functional.

        See Also
        --------
        petsc.PetscDualSpaceSimpleSetFunctional
        """
        ...
