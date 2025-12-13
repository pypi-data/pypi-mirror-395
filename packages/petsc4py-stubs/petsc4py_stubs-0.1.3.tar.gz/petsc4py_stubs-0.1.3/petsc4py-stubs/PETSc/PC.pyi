"""Type stubs for PETSc PC module."""


from typing import (
    Any,
    Callable,
    Sequence,
    Self
)

from .Object import Object
from .IS import IS
from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .DM import DM
from .Section import Section
from .KSP import KSP

# Import types from typing module
from petsc4py.typing import (
    ArrayInt,
    CSRIndicesSpec,
)


# Callback type aliases
PCApplyFunction = Callable[["PC", Vec, Vec, Any], None]
PCSetUpFunction = Callable[["PC", Any], None]
PCPatchComputeOperatorFunction = Callable[
    ["PC", int, Vec, Mat, IS, int, Sequence[int], Sequence[int], Any], None
]
PCPatchComputeFunction = Callable[
    ["PC", int, Vec, Vec, IS, int, Sequence[int], Sequence[int], Any], None
]


class PCType:
    """The preconditioner method."""

    NONE: str
    JACOBI: str
    SOR: str
    LU: str
    QR: str
    SHELL: str
    BJACOBI: str
    VPBJACOBI: str
    MG: str
    EISENSTAT: str
    ILU: str
    ICC: str
    ASM: str
    GASM: str
    KSP: str
    COMPOSITE: str
    REDUNDANT: str
    SPAI: str
    NN: str
    CHOLESKY: str
    PBJACOBI: str
    MAT: str
    HYPRE: str
    PARMS: str
    FIELDSPLIT: str
    TFS: str
    ML: str
    GALERKIN: str
    EXOTIC: str
    CP: str
    LSC: str
    PYTHON: str
    PFMG: str
    SYSPFMG: str
    REDISTRIBUTE: str
    SVD: str
    GAMG: str
    CHOWILUVIENNACL: str
    ROWSCALINGVIENNACL: str
    SAVIENNACL: str
    BDDC: str
    KACZMARZ: str
    TELESCOPE: str
    PATCH: str
    LMVM: str
    HMG: str
    DEFLATION: str
    HPDDM: str
    H2OPUS: str


class PCSide:
    """The manner in which the preconditioner is applied."""

    # native
    LEFT: int
    RIGHT: int
    SYMMETRIC: int
    # aliases
    L: int
    R: int
    S: int


class PCASMType:
    """The ASM subtype."""

    NONE: int
    BASIC: int
    RESTRICT: int
    INTERPOLATE: int


class PCGASMType:
    """The GASM subtype."""

    NONE: int
    BASIC: int
    RESTRICT: int
    INTERPOLATE: int


class PCMGType:
    """The MG subtype."""

    MULTIPLICATIVE: int
    ADDITIVE: int
    FULL: int
    KASKADE: int


class PCMGCycleType:
    """The MG cycle type."""

    V: int
    W: int


class PCGAMGType:
    """The GAMG subtype."""

    AGG: str
    GEO: str
    CLASSICAL: str


class PCCompositeType:
    """The composite type."""

    ADDITIVE: int
    MULTIPLICATIVE: int
    SYMMETRIC_MULTIPLICATIVE: int
    SPECIAL: int
    SCHUR: int


class PCFieldSplitSchurPreType:
    """The field split Schur subtype."""

    SELF: int
    SELFP: int
    A11: int
    USER: int
    FULL: int


class PCFieldSplitSchurFactType:
    """The field split Schur factorization type."""

    DIAG: int
    LOWER: int
    UPPER: int
    FULL: int


class PCPatchConstructType:
    """The patch construction type."""

    STAR: int
    VANKA: int
    PARDECOMP: int
    USER: int
    PYTHON: int


class PCHPDDMCoarseCorrectionType:
    """The HPDDM coarse correction type."""

    DEFLATED: int
    ADDITIVE: int
    BALANCED: int
    NONE: int


class PCDeflationSpaceType:
    """The deflation space subtype."""

    HAAR: int
    DB2: int
    DB4: int
    DB8: int
    DB16: int
    BIORTH22: int
    MEYER: int
    AGGREGATION: int
    USER: int


class PCFailedReason:
    """The reason the preconditioner has failed."""

    SETUP_ERROR: int
    NOERROR: int
    FACTOR_STRUCT_ZEROPIVOT: int
    FACTOR_NUMERIC_ZEROPIVOT: int
    FACTOR_OUTMEMORY: int
    FACTOR_OTHER: int
    SUBPC_ERROR: int


class PC(Object):
    """Preconditioners.

    PC is described in the PETSc manual.
    Calling the PC with a vector as an argument will apply the
    preconditioner as shown in the example below.

    Examples
    --------
    >>> from petsc4py import PETSc
    >>> v = PETSc.Vec().createWithArray([1, 2])
    >>> m = PETSc.Mat().createDense(2, array=[[1, 0], [0, 1]])
    >>> pc = PETSc.PC().create()
    >>> pc.setOperators(m)
    >>> u = pc(v)  # u is created internally
    >>> pc.apply(v, u)  # u can also be passed as second argument
    """

    Type = PCType
    Side = PCSide

    ASMType = PCASMType
    GASMType = PCGASMType
    MGType = PCMGType
    MGCycleType = PCMGCycleType
    GAMGType = PCGAMGType
    CompositeType = PCCompositeType
    FieldSplitSchurFactType = PCFieldSplitSchurFactType
    FieldSplitSchurPreType = PCFieldSplitSchurPreType
    PatchConstructType = PCPatchConstructType
    HPDDMCoarseCorrectionType = PCHPDDMCoarseCorrectionType
    DeflationSpaceType = PCDeflationSpaceType
    FailedReason = PCFailedReason
    # Backward compatibility
    SchurFactType = PCFieldSplitSchurFactType
    SchurPreType = PCFieldSplitSchurPreType

    def __call__(self, x: Vec, y: Vec | None = None) -> Vec:
        """Apply the preconditioner.

        Parameters
        ----------
        x
            The input vector.
        y
            The output vector. If None, created internally.

        Returns
        -------
        Vec
            The output vector.
        """
        ...

    # --- View and lifecycle ---

    def view(self, viewer: Viewer | None = None) -> None:
        """View the PC object.

        Parameters
        ----------
        viewer
            The visualization context.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the PC that was created with create."""
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty PC.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    # --- Type and options ---

    def setType(self, pc_type: Type | str) -> None:
        """Set the preconditioner type.

        Parameters
        ----------
        pc_type
            The preconditioner type.
        """
        ...

    def getType(self) -> str:
        """Return the preconditioner type."""
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for all the PC options.

        Parameters
        ----------
        prefix
            The prefix to prepend to all option names.
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for all the PC options."""
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for all the PC options.

        Parameters
        ----------
        prefix
            The prefix to append to the current prefix.
        """
        ...

    def setFromOptions(self) -> None:
        """Set various PC parameters from user options."""
        ...

    # --- Operators ---

    def setOperators(self, A: Mat | None = None, P: Mat | None = None) -> None:
        """Set the matrices associated with the linear system.

        Parameters
        ----------
        A
            The matrix which defines the linear system.
        P
            The matrix to be used in constructing the preconditioner,
            usually the same as A.
        """
        ...

    def getOperators(self) -> tuple[Mat, Mat]:
        """Return the matrices associated with a linear system."""
        ...

    def setUseAmat(self, flag: bool) -> None:
        """Set to indicate to apply PC to A and not P.

        Parameters
        ----------
        flag
            Set True to use A and False to use P.
        """
        ...

    def getUseAmat(self) -> bool:
        """Return the flag to indicate if PC is applied to A or P."""
        ...

    def setReusePreconditioner(self, flag: bool) -> None:
        """Set to indicate the preconditioner is to be reused.

        Parameters
        ----------
        flag
            Set to True to use the reuse the current preconditioner
            and False to recompute on changes to the matrix.
        """
        ...

    # --- Failed reason ---

    def setFailedReason(self, reason: FailedReason | int) -> None:
        """Set the reason the PC terminated.

        Parameters
        ----------
        reason
            The reason the PC terminated.
        """
        ...

    def getFailedReason(self) -> FailedReason:
        """Return the reason the PC terminated."""
        ...

    # --- Setup and apply ---

    def setUp(self) -> None:
        """Set up the internal data structures for the PC."""
        ...

    def reset(self) -> None:
        """Reset the PC, removing any allocated vectors and matrices."""
        ...

    def setUpOnBlocks(self) -> None:
        """Set up the PC for each block."""
        ...

    def apply(self, x: Vec, y: Vec) -> None:
        """Apply the PC to a vector.

        Parameters
        ----------
        x
            The input vector.
        y
            The output vector, cannot be the same as x.
        """
        ...

    def matApply(self, x: Mat, y: Mat) -> None:
        """Apply the PC to many vectors stored as Mat.Type.DENSE.

        Parameters
        ----------
        x
            The input matrix.
        y
            The output matrix, cannot be the same as x.
        """
        ...

    def applyTranspose(self, x: Vec, y: Vec) -> None:
        """Apply the transpose of the PC to a vector.

        Parameters
        ----------
        x
            The input vector.
        y
            The output vector, cannot be the same as x.
        """
        ...

    def matApplyTranspose(self, x: Mat, y: Mat) -> None:
        """Apply the transpose of the PC to many vectors stored as Mat.Type.DENSE.

        Parameters
        ----------
        x
            The input matrix.
        y
            The output matrix, cannot be the same as x.
        """
        ...

    def applySymmetricLeft(self, x: Vec, y: Vec) -> None:
        """Apply the left part of a symmetric PC to a vector.

        Parameters
        ----------
        x
            The input vector.
        y
            The output vector, cannot be the same as x.
        """
        ...

    def applySymmetricRight(self, x: Vec, y: Vec) -> None:
        """Apply the right part of a symmetric PC to a vector.

        Parameters
        ----------
        x
            The input vector.
        y
            The output vector, cannot be the same as x.
        """
        ...

    # --- Discretization space ---

    def getDM(self) -> DM:
        """Return the DM associated with the PC."""
        ...

    def setDM(self, dm: DM) -> None:
        """Set the DM that may be used by some preconditioners.

        Parameters
        ----------
        dm
            The DM object.
        """
        ...

    def setCoordinates(self, coordinates: Sequence[Sequence[float]]) -> None:
        """Set the coordinates for the nodes on the local process.

        Parameters
        ----------
        coordinates
            The two dimensional coordinate array.
        """
        ...

    # --- Python ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create a preconditioner of Python type.

        Parameters
        ----------
        context
            An instance of the Python class implementing the required methods.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setPythonContext(self, context: Any) -> None:
        """Set the instance of the class implementing the required Python methods."""
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing the required Python methods."""
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used."""
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the preconditioner."""
        ...

    # --- Block Jacobi ---

    def getBJacobiSubKSP(self) -> list[KSP]:
        """Return the local KSP object for all blocks on this process."""
        ...

    # --- ASM ---

    def setASMType(self, asmtype: ASMType) -> None:
        """Set the type of restriction and interpolation.

        Parameters
        ----------
        asmtype
            The type of ASM you wish to use.
        """
        ...

    def setASMOverlap(self, overlap: int) -> None:
        """Set the overlap between a pair of subdomains.

        Parameters
        ----------
        overlap
            The amount of overlap between subdomains.
        """
        ...

    def setASMLocalSubdomains(
        self,
        nsd: int,
        is_sub: Sequence[IS] | None = None,
        is_local: Sequence[IS] | None = None,
    ) -> None:
        """Set the local subdomains.

        Parameters
        ----------
        nsd
            The number of subdomains for this process.
        is_sub
            Defines the subdomains for this process or None to determine
            internally.
        is_local
            Defines the local part of the subdomains for this process,
            only used for PC.ASMType.RESTRICT.
        """
        ...

    def setASMTotalSubdomains(
        self,
        nsd: int,
        is_sub: Sequence[IS] | None = None,
        is_local: Sequence[IS] | None = None,
    ) -> None:
        """Set the subdomains for all processes.

        Parameters
        ----------
        nsd
            The number of subdomains for all processes.
        is_sub
            Defines the subdomains for all processes or None to determine
            internally.
        is_local
            Defines the local part of the subdomains for this process,
            only used for PC.ASMType.RESTRICT.
        """
        ...

    def getASMSubKSP(self) -> list[KSP]:
        """Return the local KSP object for all blocks on this process."""
        ...

    def setASMSortIndices(self, dosort: bool) -> None:
        """Set to sort subdomain indices.

        Parameters
        ----------
        dosort
            Set to True to sort indices.
        """
        ...

    # --- GASM ---

    def setGASMType(self, gasmtype: GASMType) -> None:
        """Set the type of restriction and interpolation.

        Parameters
        ----------
        gasmtype
            The type of GASM.
        """
        ...

    def setGASMOverlap(self, overlap: int) -> None:
        """Set the overlap between a pair of subdomains.

        Parameters
        ----------
        overlap
            The amount of overlap between subdomains.
        """
        ...

    # --- GAMG ---

    def setGAMGType(self, gamgtype: GAMGType | str) -> None:
        """Set the type of algorithm.

        Parameters
        ----------
        gamgtype
            The type of GAMG.
        """
        ...

    def setGAMGLevels(self, levels: int) -> None:
        """Set the maximum number of levels.

        Parameters
        ----------
        levels
            The maximum number of levels to use.
        """
        ...

    def setGAMGSmooths(self, smooths: int) -> None:
        """Set the number of smoothing steps used on all levels.

        Parameters
        ----------
        smooths
            The maximum number of smooths.
        """
        ...

    # --- Hypre ---

    def getHYPREType(self) -> str:
        """Return the Type.HYPRE type."""
        ...

    def setHYPREType(self, hypretype: str) -> None:
        """Set the Type.HYPRE type.

        Parameters
        ----------
        hypretype
            The name of the type, one of "euclid", "pilut",
            "parasails", "boomeramg", "ams", "ads".
        """
        ...

    def setHYPREDiscreteCurl(self, mat: Mat) -> None:
        """Set the discrete curl matrix.

        Parameters
        ----------
        mat
            The discrete curl.
        """
        ...

    def setHYPREDiscreteGradient(self, mat: Mat) -> None:
        """Set the discrete gradient matrix.

        Parameters
        ----------
        mat
            The discrete gradient.
        """
        ...

    def setHYPRESetAlphaPoissonMatrix(self, mat: Mat) -> None:
        """Set the vector Poisson matrix.

        Parameters
        ----------
        mat
            The vector Poisson matrix.
        """
        ...

    def setHYPRESetBetaPoissonMatrix(self, mat: Mat | None = None) -> None:
        """Set the Poisson matrix.

        Parameters
        ----------
        mat
            The Poisson matrix or None to turn off.
        """
        ...

    def setHYPRESetInterpolations(
        self,
        dim: int,
        RT_Pi_Full: Mat | None = None,
        RT_Pi: Sequence[Mat] | None = None,
        ND_Pi_Full: Mat | None = None,
        ND_Pi: Sequence[Mat] | None = None,
    ) -> None:
        """Set the interpolation matrices.

        Parameters
        ----------
        dim
            The dimension of the problem.
        RT_Pi_Full
            The Raviart-Thomas interpolation matrix or None to omit.
        RT_Pi
            The xyz components of the Raviart-Thomas interpolation matrix,
            or None to omit.
        ND_Pi_Full
            The Nedelec interpolation matrix or None to omit.
        ND_Pi
            The xyz components of the Nedelec interpolation matrix,
            or None to omit.
        """
        ...

    def setHYPRESetEdgeConstantVectors(
        self, ozz: Vec, zoz: Vec, zzo: Vec | None = None
    ) -> None:
        """Set the representation of the constant vector fields in the edge element basis.

        Parameters
        ----------
        ozz
            A vector representing [1, 0, 0] or [1, 0] in 2D.
        zoz
            A vector representing [0, 1, 0] or [0, 1] in 2D.
        zzo
            A vector representing [0, 0, 1] or None in 2D.
        """
        ...

    def setHYPREAMSSetInteriorNodes(self, interior: Vec) -> None:
        """Set the list of interior nodes to a zero conductivity region.

        Parameters
        ----------
        interior
            A vector where a value of 1.0 indicates an interior node.
        """
        ...

    # --- Factor ---

    def setFactorSolverType(self, solver: Mat.SolverType | str) -> None:
        """Set the solver package used to perform the factorization.

        Parameters
        ----------
        solver
            The solver package used to factorize.
        """
        ...

    def getFactorSolverType(self) -> str:
        """Return the solver package used to perform the factorization."""
        ...

    def setFactorSetUpSolverType(self) -> None:
        """Set up the factorization solver."""
        ...

    def setFactorOrdering(
        self,
        ord_type: str | None = None,
        nzdiag: float | None = None,
        reuse: bool | None = None,
    ) -> None:
        """Set options for the matrix factorization reordering.

        Parameters
        ----------
        ord_type
            The name of the matrix ordering or None to leave unchanged.
        nzdiag
            Threshold to consider diagonal entries in the matrix as zero.
        reuse
            Enable to reuse the ordering of a factored matrix.
        """
        ...

    def setFactorPivot(
        self, zeropivot: float | None = None, inblocks: bool | None = None
    ) -> None:
        """Set options for matrix factorization pivoting.

        Parameters
        ----------
        zeropivot
            The size at which smaller pivots are treated as zero.
        inblocks
            Enable to allow pivoting while factoring in blocks.
        """
        ...

    def setFactorShift(
        self,
        shift_type: Mat.FactorShiftType | None = None,
        amount: float | None = None,
    ) -> None:
        """Set options for shifting diagonal entries of a matrix.

        Parameters
        ----------
        shift_type
            The type of shift, or None to leave unchanged.
        amount
            The amount of shift. Specify DEFAULT to determine internally
            or None to leave unchanged.
        """
        ...

    def setFactorLevels(self, levels: int) -> None:
        """Set the number of levels of fill.

        Parameters
        ----------
        levels
            The number of levels to fill.
        """
        ...

    def getFactorMatrix(self) -> Mat:
        """Return the factored matrix."""
        ...

    # --- FieldSplit ---

    def setFieldSplitType(self, ctype: CompositeType) -> None:
        """Set the type of composition of a field split preconditioner.

        Parameters
        ----------
        ctype
            The type of composition.
        """
        ...

    def setFieldSplitIS(self, *fields: tuple[str, IS]) -> None:
        """Set the elements for the field split by IS.

        Parameters
        ----------
        fields
            A sequence of tuples containing the split name and the IS
            that defines the elements in the split.
        """
        ...

    def setFieldSplitFields(
        self, bsize: int, *fields: tuple[str, Sequence[int]]
    ) -> None:
        """Sets the elements for the field split.

        Parameters
        ----------
        bsize
            The block size.
        fields
            A sequence of tuples containing the split name and a sequence
            of integers that define the elements in the split.
        """
        ...

    def getFieldSplitSubKSP(self) -> list[KSP]:
        """Return the KSP for all splits."""
        ...

    def getFieldSplitSchurGetSubKSP(self) -> list[KSP]:
        """Return the KSP for the Schur complement based splits."""
        ...

    def getFieldSplitSubIS(self, splitname: str) -> IS:
        """Return the IS associated with a given name.

        Parameters
        ----------
        splitname
            The name of the split.
        """
        ...

    def setFieldSplitSchurFactType(self, ctype: FieldSplitSchurFactType) -> None:
        """Set the type of approximate block factorization.

        Parameters
        ----------
        ctype
            The type indicating which blocks to retain.
        """
        ...

    def setFieldSplitSchurPreType(
        self, ptype: FieldSplitSchurPreType, pre: Mat | None = None
    ) -> None:
        """Set from what operator the PC is constructed.

        Parameters
        ----------
        ptype
            The type of matrix to use for preconditioning the Schur complement.
        pre
            The optional matrix to use for preconditioning.
        """
        ...

    # --- Composite ---

    def setCompositeType(self, ctype: CompositeType) -> None:
        """Set the type of composite preconditioner.

        Parameters
        ----------
        ctype
            The type of composition.
        """
        ...

    def getCompositePC(self, n: int) -> "PC":
        """Return a component of the composite PC.

        Parameters
        ----------
        n
            The index of the PC in the composition.
        """
        ...

    def addCompositePCType(self, pc_type: Type | str) -> None:
        """Add a PC of the given type to the composite PC.

        Parameters
        ----------
        pc_type
            The type of the preconditioner to add.
        """
        ...

    # --- KSP ---

    def getKSP(self) -> KSP:
        """Return the KSP if the PC is Type.KSP."""
        ...

    # --- MG ---

    def getMGType(self) -> MGType:
        """Return the form of multigrid."""
        ...

    def setMGType(self, mgtype: MGType) -> None:
        """Set the form of multigrid.

        Parameters
        ----------
        mgtype
            The type of multigrid.
        """
        ...

    def getMGLevels(self) -> int:
        """Return the number of MG levels."""
        ...

    def setMGLevels(self, levels: int) -> None:
        """Set the number of MG levels.

        Parameters
        ----------
        levels
            The number of levels.
        """
        ...

    def getMGCoarseSolve(self) -> KSP:
        """Return the KSP used on the coarse grid."""
        ...

    def setMGInterpolation(self, level: int, mat: Mat) -> None:
        """Set the interpolation operator for the given level.

        Parameters
        ----------
        level
            The level where interpolation is defined from level-1 to level.
        mat
            The interpolation operator.
        """
        ...

    def getMGInterpolation(self, level: int) -> Mat:
        """Return the interpolation operator for the given level.

        Parameters
        ----------
        level
            The level where interpolation is defined from level-1 to level.
        """
        ...

    def setMGRestriction(self, level: int, mat: Mat) -> None:
        """Set the restriction operator for the given level.

        Parameters
        ----------
        level
            The level where restriction is defined from level to level-1.
        mat
            The restriction operator.
        """
        ...

    def getMGRestriction(self, level: int) -> Mat:
        """Return the restriction operator for the given level.

        Parameters
        ----------
        level
            The level where restriction is defined from level to level-1.
        """
        ...

    def setMGRScale(self, level: int, rscale: Vec) -> None:
        """Set the pointwise scaling for the restriction operator on the given level.

        Parameters
        ----------
        level
            The level where restriction is defined from level to level-1.
        rscale
            The scaling vector.
        """
        ...

    def getMGRScale(self, level: int) -> Vec:
        """Return the pointwise scaling for the restriction operator on the given level.

        Parameters
        ----------
        level
            The level where restriction is defined from level to level-1.
        """
        ...

    def getMGSmoother(self, level: int) -> KSP:
        """Return the KSP to be used as a smoother.

        Parameters
        ----------
        level
            The level of the smoother.
        """
        ...

    def getMGSmootherDown(self, level: int) -> KSP:
        """Return the KSP to be used as a smoother before coarse grid correction.

        Parameters
        ----------
        level
            The level of the smoother.
        """
        ...

    def getMGSmootherUp(self, level: int) -> KSP:
        """Return the KSP to be used as a smoother after coarse grid correction.

        Parameters
        ----------
        level
            The level of the smoother.
        """
        ...

    def setMGCycleType(self, cycle_type: MGCycleType) -> None:
        """Set the type of cycles.

        Parameters
        ----------
        cycle_type
            The type of multigrid cycles to use.
        """
        ...

    def setMGCycleTypeOnLevel(self, level: int, cycle_type: MGCycleType) -> None:
        """Set the type of cycle on the given level.

        Parameters
        ----------
        level
            The level on which to set the cycle type.
        cycle_type
            The type of multigrid cycles to use.
        """
        ...

    def setMGRhs(self, level: int, rhs: Vec) -> None:
        """Set the vector where the right-hand side is stored.

        Parameters
        ----------
        level
            The level on which to set the right-hand side.
        rhs
            The vector where the right-hand side is stored.
        """
        ...

    def setMGX(self, level: int, x: Vec) -> None:
        """Set the vector where the solution is stored.

        Parameters
        ----------
        level
            The level on which to set the solution.
        x
            The vector where the solution is stored.
        """
        ...

    def setMGR(self, level: int, r: Vec) -> None:
        """Set the vector where the residual is stored.

        Parameters
        ----------
        level
            The level on which to set the residual.
        r
            The vector where the residual is stored.
        """
        ...

    # --- BDDC ---

    def setBDDCLocalAdjacency(self, csr: CSRIndicesSpec) -> None:
        """Provide a custom connectivity graph for local dofs.

        Parameters
        ----------
        csr
            Compressed sparse row layout information.
        """
        ...

    def setBDDCDivergenceMat(
        self, div: Mat, trans: bool = False, l2l: IS | None = None
    ) -> None:
        """Set the linear operator representing ∫ div(u)•p dx.

        Parameters
        ----------
        div
            The matrix in Mat.Type.IS format.
        trans
            If True, the pressure/velocity is in the trial/test space
            respectively. If False the pressure/velocity is in the test/trial
            space.
        l2l
            Optional IS describing the local to local map for velocities.
        """
        ...

    def setBDDCDiscreteGradient(
        self,
        G: Mat,
        order: int = 1,
        field: int = 1,
        gord: bool = True,
        conforming: bool = True,
    ) -> None:
        """Set the discrete gradient.

        Parameters
        ----------
        G
            The discrete gradient matrix in Mat.Type.AIJ format.
        order
            The order of the Nedelec space.
        field
            The field number of the Nedelec degrees of freedom.
        gord
            Enable to use global ordering in the rows of G.
        conforming
            Enable if the mesh is conforming.
        """
        ...

    def setBDDCChangeOfBasisMat(self, T: Mat, interior: bool = False) -> None:
        """Set a user defined change of basis for degrees of freedom.

        Parameters
        ----------
        T
            The matrix representing the change of basis.
        interior
            Enable to indicate the change of basis affects interior degrees
            of freedom.
        """
        ...

    def setBDDCPrimalVerticesIS(self, primv: IS) -> None:
        """Set additional user defined primal vertices.

        Parameters
        ----------
        primv
            The IS of primal vertices in global numbering.
        """
        ...

    def setBDDCPrimalVerticesLocalIS(self, primv: IS) -> None:
        """Set additional user defined primal vertices.

        Parameters
        ----------
        primv
            The IS of primal vertices in local numbering.
        """
        ...

    def setBDDCCoarseningRatio(self, cratio: int) -> None:
        """Set the coarsening ratio used in the multilevel version.

        Parameters
        ----------
        cratio
            The coarsening ratio at the coarse level.
        """
        ...

    def setBDDCLevels(self, levels: int) -> None:
        """Set the maximum number of additional levels allowed.

        Parameters
        ----------
        levels
            The maximum number of levels.
        """
        ...

    def setBDDCDirichletBoundaries(self, bndr: IS) -> None:
        """Set the IS defining Dirichlet boundaries for the global problem.

        Parameters
        ----------
        bndr
            The parallel IS defining Dirichlet boundaries.
        """
        ...

    def setBDDCDirichletBoundariesLocal(self, bndr: IS) -> None:
        """Set the IS defining Dirichlet boundaries in local ordering.

        Parameters
        ----------
        bndr
            The parallel IS defining Dirichlet boundaries in local ordering.
        """
        ...

    def setBDDCNeumannBoundaries(self, bndr: IS) -> None:
        """Set the IS defining Neumann boundaries for the global problem.

        Parameters
        ----------
        bndr
            The parallel IS defining Neumann boundaries.
        """
        ...

    def setBDDCNeumannBoundariesLocal(self, bndr: IS) -> None:
        """Set the IS defining Neumann boundaries in local ordering.

        Parameters
        ----------
        bndr
            The parallel IS defining Neumann boundaries in local ordering.
        """
        ...

    def setBDDCDofsSplitting(self, isfields: IS | Sequence[IS]) -> None:
        """Set the index set(s) defining fields of the global matrix.

        Parameters
        ----------
        isfields
            The sequence of IS describing the fields in global ordering.
        """
        ...

    def setBDDCDofsSplittingLocal(self, isfields: IS | Sequence[IS]) -> None:
        """Set the index set(s) defining fields of the local subdomain matrix.

        Parameters
        ----------
        isfields
            The sequence of IS describing the fields in local ordering.
        """
        ...

    # --- Patch ---

    def getPatchSubKSP(self) -> list[KSP]:
        """Return the local KSP object for all blocks on this process."""
        ...

    def setPatchCellNumbering(self, sec: Section) -> None:
        """Set the cell numbering.

        Parameters
        ----------
        sec
            The section describing cell numbering.
        """
        ...

    def setPatchDiscretisationInfo(
        self,
        dms: Sequence[DM],
        bs: Sequence[int],
        cellNodeMaps: Sequence[ArrayInt],
        subspaceOffsets: Sequence[int],
        ghostBcNodes: Sequence[int],
        globalBcNodes: Sequence[int],
    ) -> None:
        """Set discretisation info.

        Parameters
        ----------
        dms
            The sequence of DMs.
        bs
            The block sizes.
        cellNodeMaps
            The cell node maps.
        subspaceOffsets
            The subspace offsets.
        ghostBcNodes
            The ghost BC nodes.
        globalBcNodes
            The global BC nodes.
        """
        ...

    def setPatchComputeOperator(
        self,
        operator: Callable[..., None],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set compute operator callbacks.

        Parameters
        ----------
        operator
            The operator callback function.
        args
            Positional arguments for callback.
        kargs
            Keyword arguments for callback.
        """
        ...

    def setPatchComputeOperatorInteriorFacets(
        self,
        operator: Callable[..., None],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set compute operator callbacks for interior facets.

        Parameters
        ----------
        operator
            The operator callback function.
        args
            Positional arguments for callback.
        kargs
            Keyword arguments for callback.
        """
        ...

    def setPatchComputeFunction(
        self,
        function: Callable[..., None],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set compute function callbacks.

        Parameters
        ----------
        function
            The function callback.
        args
            Positional arguments for callback.
        kargs
            Keyword arguments for callback.
        """
        ...

    def setPatchComputeFunctionInteriorFacets(
        self,
        function: Callable[..., None],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set compute function callbacks for interior facets.

        Parameters
        ----------
        function
            The function callback.
        args
            Positional arguments for callback.
        kargs
            Keyword arguments for callback.
        """
        ...

    def setPatchConstructType(
        self,
        typ: PatchConstructType,
        operator: Callable[..., None] | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set patch construction type.

        Parameters
        ----------
        typ
            The type of patch construction.
        operator
            The construction operator callback (required for USER or PYTHON type).
        args
            Positional arguments for callback.
        kargs
            Keyword arguments for callback.
        """
        ...

    # --- HPDDM ---

    def setHPDDMAuxiliaryMat(self, uis: IS, uaux: Mat) -> None:
        """Set the auxiliary matrix used by the preconditioner.

        Parameters
        ----------
        uis
            The IS of the local auxiliary matrix.
        uaux
            The auxiliary sequential matrix.
        """
        ...

    def setHPDDMRHSMat(self, B: Mat) -> None:
        """Set the right-hand side matrix of the preconditioner.

        Parameters
        ----------
        B
            The right-hand side sequential matrix.
        """
        ...

    def getHPDDMComplexities(self) -> tuple[float, float]:
        """Compute the grid and operator complexities."""
        ...

    def setHPDDMHasNeumannMat(self, has: bool) -> None:
        """Set to indicate that the Mat passed to the PC is the local Neumann matrix.

        Parameters
        ----------
        has
            Enable to indicate the matrix is the local Neumann matrix.
        """
        ...

    def setHPDDMCoarseCorrectionType(
        self, correction_type: HPDDMCoarseCorrectionType
    ) -> None:
        """Set the coarse correction type.

        Parameters
        ----------
        correction_type
            The type of coarse correction to apply.
        """
        ...

    def getHPDDMCoarseCorrectionType(self) -> HPDDMCoarseCorrectionType:
        """Return the coarse correction type."""
        ...

    def getHPDDMSTShareSubKSP(self) -> bool:
        """Return true if the KSP in SLEPc ST and the subdomain solver is shared."""
        ...

    def setHPDDMDeflationMat(self, uis: IS, U: Mat) -> None:
        """Set the deflation space used to assemble a coarse operator.

        Parameters
        ----------
        uis
            The IS of the local deflation matrix.
        U
            The deflation sequential matrix of type Mat.Type.DENSE.
        """
        ...

    # --- SPAI ---

    def setSPAIEpsilon(self, val: float) -> None:
        """Set the tolerance for the preconditioner.

        Parameters
        ----------
        val
            The tolerance, defaults to 0.4.
        """
        ...

    def setSPAINBSteps(self, nbsteps: int) -> None:
        """Set the maximum number of improvement steps per row.

        Parameters
        ----------
        nbsteps
            The number of steps, defaults to 5.
        """
        ...

    def setSPAIMax(self, maxval: int) -> None:
        """Set the size of working buffers in the preconditioner.

        Parameters
        ----------
        maxval
            Number of entries in the work arrays to be allocated, defaults to 5000.
        """
        ...

    def setSPAIMaxNew(self, maxval: int) -> None:
        """Set the maximum number of new non-zero candidates per step.

        Parameters
        ----------
        maxval
            Number of entries allowed, defaults to 5.
        """
        ...

    def setSPAIBlockSize(self, n: int) -> None:
        """Set the block size of the preconditioner.

        Parameters
        ----------
        n
            The block size, defaults to 1.
        """
        ...

    def setSPAICacheSize(self, size: int) -> None:
        """Set the cache size.

        Parameters
        ----------
        size
            The size of the cache, defaults to 5.
        """
        ...

    def setSPAIVerbose(self, level: int) -> None:
        """Set the verbosity level.

        Parameters
        ----------
        level
            The level of verbosity, defaults to 1.
        """
        ...

    def setSPAISp(self, sym: int) -> None:
        """Set to specify a symmetric sparsity pattern.

        Parameters
        ----------
        sym
            Enable to indicate the matrix is symmetric.
        """
        ...

    # --- Deflation ---

    def setDeflationInitOnly(self, flg: bool) -> None:
        """Set to only perform the initialization.

        Parameters
        ----------
        flg
            Enable to only initialize the preconditioner.
        """
        ...

    def setDeflationLevels(self, levels: int) -> None:
        """Set the maximum level of deflation nesting.

        Parameters
        ----------
        levels
            The maximum deflation level.
        """
        ...

    def setDeflationReductionFactor(self, red: int) -> None:
        """Set the reduction factor for the preconditioner.

        Parameters
        ----------
        red
            The reduction factor or DEFAULT.
        """
        ...

    def setDeflationCorrectionFactor(self, fact: float) -> None:
        """Set the coarse problem correction factor.

        Parameters
        ----------
        fact
            The correction factor.
        """
        ...

    def setDeflationSpaceToCompute(
        self, space_type: DeflationSpaceType, size: int
    ) -> None:
        """Set the deflation space type.

        Parameters
        ----------
        space_type
            The deflation space type.
        size
            The size of the space to compute.
        """
        ...

    def setDeflationSpace(self, W: Mat, transpose: bool) -> None:
        """Set the deflation space matrix or its (Hermitian) transpose.

        Parameters
        ----------
        W
            The deflation matrix.
        transpose
            Enable to indicate that W is an explicit transpose of the
            deflation matrix.
        """
        ...

    def setDeflationProjectionNullSpaceMat(self, mat: Mat) -> None:
        """Set the projection null space matrix.

        Parameters
        ----------
        mat
            The projection null space matrix.
        """
        ...

    def setDeflationCoarseMat(self, mat: Mat) -> None:
        """Set the coarse problem matrix.

        Parameters
        ----------
        mat
            The coarse problem matrix.
        """
        ...

    def getDeflationCoarseKSP(self) -> KSP:
        """Return the coarse problem KSP."""
        ...

    def getDeflationPC(self) -> "PC":
        """Return the additional preconditioner."""
        ...
