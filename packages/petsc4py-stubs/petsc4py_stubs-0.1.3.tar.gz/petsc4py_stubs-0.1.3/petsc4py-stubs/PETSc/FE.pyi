"""Type stubs for PETSc FE module."""


from typing import Self

from numpy import ndarray

from .Object import Object

from .Comm import Comm
from .Viewer import Viewer
from .Space import Space, DualSpace
from .DT import Quad


class FEType:
    """The finite element types."""

    BASIC: str
    OPENCL: str
    COMPOSITE: str


class FE(Object):
    """A PETSc object that manages a finite element space.

    See Also
    --------
    petsc.PetscFE
    """

    Type = FEType

    def view(self, viewer: Viewer | None = None) -> None:
        """View a `FE` object.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` to display the graph.

        See Also
        --------
        petsc.PetscFEView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the `FE` object.

        Collective.

        See Also
        --------
        petsc.PetscFEDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty `FE` object.

        Collective.

        The type can then be set with `setType`.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        setType, petsc.PetscFECreate
        """
        ...

    def createDefault(
        self,
        dim: int,
        nc: int,
        isSimplex: bool,
        qorder: int = ...,
        prefix: str | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `FE` for basic FEM computation.

        Collective.

        Parameters
        ----------
        dim
            The spatial dimension.
        nc
            The number of components.
        isSimplex
            Flag for simplex reference cell, otherwise it's a tensor product.
        qorder
            The quadrature order or `DETERMINE` to use `Space` polynomial
            degree.
        prefix
            The options prefix, or `None`.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscFECreateDefault
        """
        ...

    def createLagrange(
        self,
        dim: int,
        nc: int,
        isSimplex: bool,
        k: int,
        qorder: int = ...,
        comm: Comm | None = None,
    ) -> Self:
        """Create a `FE` for the basic Lagrange space of degree k.

        Collective.

        Parameters
        ----------
        dim
            The spatial dimension.
        nc
            The number of components.
        isSimplex
            Flag for simplex reference cell, otherwise it's a tensor product.
        k
            The degree of the space.
        qorder
            The quadrature order or `DETERMINE` to use `Space` polynomial
            degree.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc.PetscFECreateLagrange
        """
        ...

    def getQuadrature(self) -> Quad:
        """Return the `Quad` used to calculate inner products.

        Not collective.

        See Also
        --------
        setQuadrature, petsc.PetscFEGetQuadrature
        """
        ...

    def getDimension(self) -> int:
        """Return the dimension of the finite element space on a cell.

        Not collective.

        See Also
        --------
        petsc.PetscFEGetDimension
        """
        ...

    def getSpatialDimension(self) -> int:
        """Return the spatial dimension of the element.

        Not collective.

        See Also
        --------
        petsc.PetscFEGetSpatialDimension
        """
        ...

    def getNumComponents(self) -> int:
        """Return the number of components in the element.

        Not collective.

        See Also
        --------
        setNumComponents, petsc.PetscFEGetNumComponents
        """
        ...

    def setNumComponents(self, comp: int) -> None:
        """Set the number of field components in the element.

        Not collective.

        Parameters
        ----------
        comp
            The number of field components.

        See Also
        --------
        getNumComponents, petsc.PetscFESetNumComponents
        """
        ...

    def getNumDof(self) -> ndarray:
        """Return the number of DOFs.

        Not collective.

        Return the number of DOFs (dual basis vectors) associated with mesh
        points on the reference cell of a given dimension.

        See Also
        --------
        petsc.PetscFEGetNumDof
        """
        ...

    def getTileSizes(self) -> tuple[int, int, int, int]:
        """Return the tile sizes for evaluation.

        Not collective.

        Returns
        -------
        blockSize : int
            The number of elements in a block.
        numBlocks : int
            The number of blocks in a batch.
        batchSize : int
            The number of elements in a batch.
        numBatches : int
            The number of batches in a chunk.

        See Also
        --------
        setTileSizes, petsc.PetscFEGetTileSizes
        """
        ...

    def setTileSizes(
        self,
        blockSize: int,
        numBlocks: int,
        batchSize: int,
        numBatches: int,
    ) -> None:
        """Set the tile sizes for evaluation.

        Not collective.

        Parameters
        ----------
        blockSize
            The number of elements in a block.
        numBlocks
            The number of blocks in a batch.
        batchSize
            The number of elements in a batch.
        numBatches
            The number of batches in a chunk.

        See Also
        --------
        getTileSizes, petsc.PetscFESetTileSizes
        """
        ...

    def getFaceQuadrature(self) -> Quad:
        """Return the `Quad` used to calculate inner products on faces.

        Not collective.

        See Also
        --------
        setFaceQuadrature, petsc.PetscFEGetFaceQuadrature
        """
        ...

    def setQuadrature(self, quad: Quad) -> Self:
        """Set the `Quad` used to calculate inner products.

        Not collective.

        Parameters
        ----------
        quad
            The `Quad` object.

        See Also
        --------
        getQuadrature, petsc.PetscFESetQuadrature
        """
        ...

    def setFaceQuadrature(self, quad: Quad) -> Quad:
        """Set the `Quad` used to calculate inner products on faces.

        Not collective.

        Parameters
        ----------
        quad
            The `Quad` object.

        See Also
        --------
        getFaceQuadrature, petsc.PetscFESetFaceQuadrature
        """
        ...

    def setType(self, fe_type: FEType | str) -> Self:
        """Build a particular `FE`.

        Collective.

        Parameters
        ----------
        fe_type
            The kind of FEM space.

        See Also
        --------
        petsc.PetscFESetType
        """
        ...

    def getBasisSpace(self) -> Space:
        """Return the `Space` used for the approximation of the `FE` solution.

        Not collective.

        See Also
        --------
        setBasisSpace, petsc.PetscFEGetBasisSpace
        """
        ...

    def setBasisSpace(self, sp: Space) -> None:
        """Set the `Space` used for the approximation of the solution.

        Not collective.

        Parameters
        ----------
        sp
            The `Space` object.

        See Also
        --------
        getBasisSpace, petsc.PetscFESetBasisSpace
        """
        ...

    def setFromOptions(self) -> None:
        """Set parameters in a `FE` from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.PetscFESetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Construct data structures for the `FE` after the `Type` has been set.

        Collective.

        See Also
        --------
        petsc.PetscFESetUp
        """
        ...

    def getDualSpace(self) -> DualSpace:
        """Return the `DualSpace` used to define the inner product for the `FE`.

        Not collective.

        See Also
        --------
        setDualSpace, DualSpace, petsc.PetscFEGetDualSpace
        """
        ...

    def setDualSpace(self, dspace: DualSpace) -> None:
        """Set the `DualSpace` used to define the inner product.

        Not collective.

        Parameters
        ----------
        dspace
            The `DualSpace` object.

        See Also
        --------
        getDualSpace, DualSpace, petsc.PetscFESetDualSpace
        """
        ...
