"""Type stubs for PETSc Mat module."""


from typing import (
    Any,
    Callable,
    Literal,
    Sequence,
    overload,
    Self
)
from numpy import ndarray, dtype

from .Object import Object
from .IS import IS, LGMap

from .Comm import Comm
from .Vec import Vec
from .Viewer import Viewer
from .Scatter import Scatter
from .DM import DM
from .KSP import KSP
from .Random import Random

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    ArrayBool,
    LayoutSizeSpec,
    MatSizeSpec,
    MatBlockSizeSpec,
    NNZSpec,
    CSRIndicesSpec,
    CSRSpec,
    InsertModeSpec,
    MatAssemblySpec,
    AccessModeSpec,
    NormTypeSpec,
    DimsSpec,
    MatNullFunction,
)




class MatType:
    """Matrix type."""
    SAME: str
    MAIJ: str
    SEQMAIJ: str
    MPIMAIJ: str
    KAIJ: str
    SEQKAIJ: str
    MPIKAIJ: str
    IS: str
    AIJ: str
    SEQAIJ: str
    MPIAIJ: str
    AIJCRL: str
    SEQAIJCRL: str
    MPIAIJCRL: str
    AIJCUSPARSE: str
    SEQAIJCUSPARSE: str
    MPIAIJCUSPARSE: str
    AIJVIENNACL: str
    SEQAIJVIENNACL: str
    MPIAIJVIENNACL: str
    AIJPERM: str
    SEQAIJPERM: str
    MPIAIJPERM: str
    AIJSELL: str
    SEQAIJSELL: str
    MPIAIJSELL: str
    AIJMKL: str
    SEQAIJMKL: str
    MPIAIJMKL: str
    BAIJMKL: str
    SEQBAIJMKL: str
    MPIBAIJMKL: str
    SHELL: str
    DENSE: str
    DENSECUDA: str
    DENSEHIP: str
    SEQDENSE: str
    SEQDENSECUDA: str
    SEQDENSEHIP: str
    MPIDENSE: str
    MPIDENSECUDA: str
    MPIDENSEHIP: str
    ELEMENTAL: str
    BAIJ: str
    SEQBAIJ: str
    MPIBAIJ: str
    MPIADJ: str
    SBAIJ: str
    SEQSBAIJ: str
    MPISBAIJ: str
    MFFD: str
    NORMAL: str
    NORMALHERMITIAN: str
    LRC: str
    SCATTER: str
    BLOCKMAT: str
    COMPOSITE: str
    FFT: str
    FFTW: str
    SEQCUFFT: str
    TRANSPOSE: str
    HERMITIANTRANSPOSE: str
    SCHURCOMPLEMENT: str
    PYTHON: str
    HYPRE: str
    HYPRESTRUCT: str
    HYPRESSTRUCT: str
    SUBMATRIX: str
    LOCALREF: str
    NEST: str
    PREALLOCATOR: str
    SELL: str
    SEQSELL: str
    MPISELL: str
    DUMMY: str
    LMVM: str
    LMVMDFP: str
    LMVMDDFP: str
    LMVMBFGS: str
    LMVMDBFGS: str
    LMVMDQN: str
    LMVMSR1: str
    LMVMBROYDEN: str
    LMVMBADBROYDEN: str
    LMVMSYMBROYDEN: str
    LMVMSYMBADBROYDEN: str
    LMVMDIAGBBROYDEN: str
    CONSTANTDIAGONAL: str
    DIAGONAL: str
    H2OPUS: str


class MatOption:
    """Matrix option."""
    OPTION_MIN: int
    UNUSED_NONZERO_LOCATION_ERR: int
    ROW_ORIENTED: int
    SYMMETRIC: int
    STRUCTURALLY_SYMMETRIC: int
    FORCE_DIAGONAL_ENTRIES: int
    IGNORE_OFF_PROC_ENTRIES: int
    USE_HASH_TABLE: int
    KEEP_NONZERO_PATTERN: int
    IGNORE_ZERO_ENTRIES: int
    USE_INODES: int
    HERMITIAN: int
    SYMMETRY_ETERNAL: int
    NEW_NONZERO_LOCATION_ERR: int
    IGNORE_LOWER_TRIANGULAR: int
    ERROR_LOWER_TRIANGULAR: int
    GETROW_UPPERTRIANGULAR: int
    SPD: int
    NO_OFF_PROC_ZERO_ROWS: int
    NO_OFF_PROC_ENTRIES: int
    NEW_NONZERO_LOCATIONS: int
    NEW_NONZERO_ALLOCATION_ERR: int
    SUBSET_OFF_PROC_ENTRIES: int
    SUBMAT_SINGLEIS: int
    STRUCTURE_ONLY: int
    SORTED_FULL: int
    OPTION_MAX: int


class MatAssemblyType:
    """Matrix assembly type."""
    FINAL_ASSEMBLY: int
    FLUSH_ASSEMBLY: int
    FINAL: int
    FLUSH: int


class MatInfoType:
    """Matrix info type."""
    LOCAL: int
    GLOBAL_MAX: int
    GLOBAL_SUM: int


class MatStructure:
    """Matrix modification structure."""
    SAME_NONZERO_PATTERN: int
    DIFFERENT_NONZERO_PATTERN: int
    SUBSET_NONZERO_PATTERN: int
    UNKNOWN_NONZERO_PATTERN: int
    SAME: int
    SAME_NZ: int
    SUBSET: int
    SUBSET_NZ: int
    DIFFERENT: int
    DIFFERENT_NZ: int
    UNKNOWN: int
    UNKNOWN_NZ: int


class MatDuplicateOption:
    """Matrix duplicate option."""
    DO_NOT_COPY_VALUES: int
    COPY_VALUES: int
    SHARE_NONZERO_PATTERN: int


class MatOrderingType:
    """Factored matrix ordering type."""
    NATURAL: str
    ND: str
    OWD: str
    RCM: str
    QMD: str
    ROWLENGTH: str
    WBM: str
    SPECTRAL: str
    AMD: str
    METISND: str


class MatSolverType:
    """Factored matrix solver type."""
    SUPERLU: str
    SUPERLU_DIST: str
    STRUMPACK: str
    UMFPACK: str
    CHOLMOD: str
    KLU: str
    ELEMENTAL: str
    SCALAPACK: str
    ESSL: str
    LUSOL: str
    MUMPS: str
    MKL_PARDISO: str
    MKL_CPARDISO: str
    PASTIX: str
    MATLAB: str
    PETSC: str
    BAS: str
    CUSPARSE: str
    CUDA: str
    SPQR: str


class MatFactorShiftType:
    """Factored matrix shift type."""
    NONE: int
    NONZERO: int
    POSITIVE_DEFINITE: int
    INBLOCKS: int
    NZ: int
    PD: int


class MatSORType:
    """Matrix SOR type."""
    FORWARD_SWEEP: int
    BACKWARD_SWEEP: int
    SYMMETRY_SWEEP: int
    LOCAL_FORWARD_SWEEP: int
    LOCAL_BACKWARD_SWEEP: int
    LOCAL_SYMMETRIC_SWEEP: int
    ZERO_INITIAL_GUESS: int
    EISENSTAT: int
    APPLY_UPPER: int
    APPLY_LOWER: int


class MatStencil:
    """Associate structured grid coordinates with matrix indices."""
    
    @property
    def i(self) -> int:
        """First logical grid coordinate."""
        ...
    
    @i.setter
    def i(self, value: int) -> None: ...
    
    @property
    def j(self) -> int:
        """Second logical grid coordinate."""
        ...
    
    @j.setter
    def j(self, value: int) -> None: ...
    
    @property
    def k(self) -> int:
        """Third logical grid coordinate."""
        ...
    
    @k.setter
    def k(self, value: int) -> None: ...
    
    @property
    def c(self) -> int:
        """Field component."""
        ...
    
    @c.setter
    def c(self, value: int) -> None: ...
    
    @property
    def index(self) -> tuple[int, int, int]:
        """Logical grid coordinates ``(i, j, k)``."""
        ...
    
    @index.setter
    def index(self, value: Sequence[int]) -> None: ...
    
    @property
    def field(self) -> int:
        """Field component."""
        ...
    
    @field.setter
    def field(self, value: int) -> None: ...


class Mat(Object):
    """Matrix object.
    
    Mat is described in the PETSc manual.
    """

    Type = MatType
    Option = MatOption
    AssemblyType = MatAssemblyType
    InfoType = MatInfoType
    Structure = MatStructure
    DuplicateOption = MatDuplicateOption
    OrderingType = MatOrderingType
    SolverType = MatSolverType
    FactorShiftType = MatFactorShiftType
    SORType = MatSORType
    Stencil = MatStencil

    # Unary operations
    def __pos__(self) -> Mat: ...
    def __neg__(self) -> Mat: ...

    # In-place binary operations
    def __iadd__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __isub__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __imul__(self, other: Scalar | tuple[Vec, Vec]) -> Mat: ...
    def __idiv__(self, other: Scalar | tuple[Vec, Vec]) -> Mat: ...
    def __itruediv__(self, other: Scalar | tuple[Vec, Vec]) -> Mat: ...

    # Binary operations
    def __add__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __radd__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __sub__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __rsub__(self, other: Mat | Vec | Scalar | tuple[Scalar, Mat]) -> Mat: ...
    def __mul__(self, other: Vec | Mat | Scalar) -> Mat | Vec: ...
    def __rmul__(self, other: Vec | Mat | Scalar) -> Mat | Vec: ...
    def __div__(self, other: Scalar | tuple[Vec, Vec]) -> Mat: ...
    def __rdiv__(self, other: Any) -> Any: ...
    def __truediv__(self, other: Scalar | tuple[Vec, Vec]) -> Mat: ...
    def __rtruediv__(self, other: Any) -> Any: ...
    def __matmul__(self, other: Vec | Mat) -> Vec | Mat: ...

    # Indexing
    def __getitem__(self, ij: tuple[int | slice, int | slice]) -> ArrayScalar: ...
    def __setitem__(self, ij: tuple[int | slice, int | slice], v: Scalar | Sequence[Scalar]) -> None: ...
    def __call__(self, x: Vec, y: Vec | None = None) -> Vec: ...

    # View and lifecycle
    def view(self, viewer: Viewer | None = None) -> None:
        """View the matrix."""
        ...

    def destroy(self) -> Self:
        """Destroy the matrix."""
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create the matrix."""
        ...

    # Type and sizes
    def setType(self, mat_type: type | str) -> None:
        """Set the matrix type."""
        ...

    def setSizes(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None
    ) -> None:
        """Set the local, global and block sizes."""
        ...

    def setBlockSize(self, bsize: int) -> None:
        """Set the matrix block size (same for rows and columns)."""
        ...

    def setBlockSizes(self, row_bsize: int, col_bsize: int) -> None:
        """Set the row and column block sizes."""
        ...

    def setVariableBlockSizes(self, blocks: Sequence[int]) -> None:
        """Set diagonal point-blocks of the matrix."""
        ...

    def setVecType(self, vec_type: str) -> None:
        """Set the vector type."""
        ...

    def getVecType(self) -> str:
        """Return the vector type used by the matrix."""
        ...

    def setNestVecType(self, vec_type: str) -> None:
        """Set the vector type for a NEST matrix."""
        ...

    # Creation methods
    def createAIJ(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None,
        nnz: NNZSpec | None = None,
        csr: CSRIndicesSpec | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a sparse AIJ matrix, optionally preallocating."""
        ...

    def createBAIJ(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec,
        nnz: NNZSpec | None = None,
        csr: CSRIndicesSpec | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a sparse blocked BAIJ matrix, optionally preallocating."""
        ...

    def createSBAIJ(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec,
        nnz: NNZSpec | None = None,
        csr: CSRIndicesSpec | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a sparse SBAIJ matrix in symmetric block format."""
        ...

    def createAIJCRL(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None,
        nnz: NNZSpec | None = None,
        csr: CSRIndicesSpec | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a sparse AIJCRL matrix."""
        ...

    def setPreallocationNNZ(self, nnz: NNZSpec) -> Self:
        """Preallocate memory for the matrix with a non-zero pattern."""
        ...

    def setPreallocationCOO(self, coo_i: Sequence[int], coo_j: Sequence[int]) -> Self:
        """Set preallocation using coordinate format with global indices."""
        ...

    def setPreallocationCOOLocal(self, coo_i: Sequence[int], coo_j: Sequence[int]) -> Self:
        """Set preallocation using coordinate format with local indices."""
        ...

    def setPreallocationCSR(self, csr: CSRIndicesSpec) -> Self:
        """Preallocate memory for the matrix with a CSR layout."""
        ...

    def preallocatorPreallocate(self, A: Mat, fill: bool = True) -> None:
        """Preallocate memory for a matrix using a preallocator matrix."""
        ...

    def createAIJWithArrays(
        self,
        size: MatSizeSpec,
        csr: CSRSpec | tuple[CSRSpec, CSRSpec],
        bsize: MatBlockSizeSpec = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a sparse AIJ matrix with data in CSR format."""
        ...

    def createDense(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None,
        array: Sequence[Scalar] | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a DENSE matrix."""
        ...

    def createDenseCUDA(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None,
        array: Sequence[Scalar] | None = None,
        cudahandle: int | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a DENSECUDA matrix with optional host and device data."""
        ...

    def setPreallocationDense(self, array: Sequence[Scalar]) -> Self:
        """Set the array used for storing matrix elements for a dense matrix."""
        ...

    def createScatter(self, scatter: Scatter, comm: Comm | None = None) -> Self:
        """Create a SCATTER matrix from a vector scatter."""
        ...

    def createNormal(self, mat: Mat) -> Self:
        """Create a NORMAL matrix representing AᵀA."""
        ...

    def createTranspose(self, mat: Mat) -> Self:
        """Create a TRANSPOSE matrix that behaves like Aᵀ."""
        ...

    def getTransposeMat(self) -> Mat:
        """Return the internal matrix of a TRANSPOSE matrix."""
        ...

    def createNormalHermitian(self, mat: Mat) -> Self:
        """Create a NORMALHERMITIAN matrix representing (A*)ᵀA."""
        ...

    def createHermitianTranspose(self, mat: Mat) -> Self:
        """Create a HERMITIANTRANSPOSE matrix that behaves like (A*)ᵀ."""
        ...

    def createLRC(
        self,
        A: Mat | None,
        U: Mat,
        c: Vec | None,
        V: Mat | None
    ) -> Self:
        """Create a low-rank correction LRC matrix representing A + UCVᵀ."""
        ...

    def createSubMatrixVirtual(self, A: Mat, isrow: IS, iscol: IS | None = None) -> Self:
        """Create a SUBMATRIX matrix that acts as a submatrix."""
        ...

    def createNest(
        self,
        mats: Sequence[Sequence[Mat | None]],
        isrows: Sequence[IS] | None = None,
        iscols: Sequence[IS] | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a NEST matrix containing multiple submatrices."""
        ...

    def createH2OpusFromMat(
        self,
        A: Mat,
        coordinates: Sequence[Scalar] | None = None,
        dist: bool | None = None,
        eta: float | None = None,
        leafsize: int | None = None,
        maxrank: int | None = None,
        bs: int | None = None,
        rtol: float | None = None
    ) -> Self:
        """Create a hierarchical H2OPUS matrix sampling from a provided operator."""
        ...

    def createIS(
        self,
        size: MatSizeSpec,
        bsize: MatBlockSizeSpec = None,
        lgmapr: LGMap | None = None,
        lgmapc: LGMap | None = None,
        comm: Comm | None = None
    ) -> Self:
        """Create an IS matrix representing globally unassembled operators."""
        ...

    def createConstantDiagonal(
        self,
        size: MatSizeSpec,
        diag: float,
        comm: Comm | None = None
    ) -> Self:
        """Create a diagonal matrix of type CONSTANTDIAGONAL."""
        ...

    def createDiagonal(self, diag: Vec) -> Self:
        """Create a diagonal matrix of type DIAGONAL."""
        ...

    def createPython(
        self,
        size: MatSizeSpec,
        context: Any = None,
        comm: Comm | None = None
    ) -> Self:
        """Create a PYTHON matrix."""
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
        """Return the fully qualified Python name of the class used by the matrix."""
        ...

    # Options
    def setOptionsPrefix(self, prefix: str | None = None) -> None:
        """Set the prefix used for searching for options in the database."""
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database."""
        ...

    def appendOptionsPrefix(self, prefix: str | None = None) -> None:
        """Append to the prefix used for searching for options in the database."""
        ...

    def setFromOptions(self) -> None:
        """Configure the matrix from the options database."""
        ...

    def setUp(self) -> Self:
        """Set up the internal data structures for using the matrix."""
        ...

    def setOption(self, option: int, flag: bool) -> None:
        """Set option."""
        ...

    def getOption(self, option: int) -> bool:
        """Return the option value."""
        ...

    def getType(self) -> str:
        """Return the type of the matrix."""
        ...

    def getSize(self) -> tuple[int, int]:
        """Return the global number of rows and columns."""
        ...

    def getLocalSize(self) -> tuple[int, int]:
        """Return the local number of rows and columns."""
        ...

    def getSizes(self) -> tuple[LayoutSizeSpec, LayoutSizeSpec]:
        """Return the tuple of matrix layouts."""
        ...

    def getBlockSize(self) -> int:
        """Return the matrix block size."""
        ...

    def getBlockSizes(self) -> tuple[int, int]:
        """Return the row and column block sizes."""
        ...

    def getOwnershipRange(self) -> tuple[int, int]:
        """Return the locally owned range of rows."""
        ...

    def getOwnershipRanges(self) -> ArrayInt:
        """Return the range of rows owned by each process."""
        ...

    def getOwnershipRangeColumn(self) -> tuple[int, int]:
        """Return the locally owned range of columns."""
        ...

    def getOwnershipRangesColumn(self) -> ArrayInt:
        """Return the range of columns owned by each process."""
        ...

    def getOwnershipIS(self) -> tuple[IS, IS]:
        """Return the ranges of rows and columns owned by each process as index sets."""
        ...

    def getInfo(self, info: int | None = None) -> dict[str, float]:
        """Return summary information."""
        ...

    # Duplication and copying
    def duplicate(self, copy: int | bool = False) -> Mat:
        """Return a clone of the matrix."""
        ...

    def copy(self, result: Mat | None = None, structure: int | None = None) -> Mat:
        """Return a copy of the matrix."""
        ...

    def load(self, viewer: Viewer) -> Self:
        """Load a matrix."""
        ...

    def convert(self, mat_type: type | str | None = None, out: Mat | None = None) -> Mat:
        """Convert the matrix type."""
        ...

    def transpose(self, out: Mat | None = None) -> Mat:
        """Return the transposed matrix."""
        ...

    def setTransposePrecursor(self, out: Mat) -> None:
        """Set transpose precursor."""
        ...

    def hermitianTranspose(self, out: Mat | None = None) -> Mat:
        """Return the transposed Hermitian matrix."""
        ...

    def realPart(self, out: Mat | None = None) -> Mat:
        """Return the real part of the matrix."""
        ...

    def imagPart(self, out: Mat | None = None) -> Mat:
        """Return the imaginary part of the matrix."""
        ...

    def conjugate(self, out: Mat | None = None) -> Mat:
        """Return the conjugate matrix."""
        ...

    def permute(self, row: IS, col: IS) -> Mat:
        """Return the permuted matrix."""
        ...

    def equal(self, mat: Mat) -> bool:
        """Return the result of matrix comparison."""
        ...

    def isTranspose(self, mat: Mat | None = None, tol: float = 0) -> bool:
        """Return the result of matrix comparison with transposition."""
        ...

    def isSymmetric(self, tol: float = 0) -> bool:
        """Return the boolean indicating if the matrix is symmetric."""
        ...

    def isSymmetricKnown(self) -> tuple[bool, bool]:
        """Return the 2-tuple indicating if the matrix is known to be symmetric."""
        ...

    def isHermitian(self, tol: float = 0) -> bool:
        """Return the boolean indicating if the matrix is Hermitian."""
        ...

    def isHermitianKnown(self) -> tuple[bool, bool]:
        """Return the 2-tuple indicating if the matrix is known to be Hermitian."""
        ...

    def isStructurallySymmetric(self) -> bool:
        """Return the boolean indicating if the matrix is structurally symmetric."""
        ...

    def isLinear(self, n: int = 1) -> bool:
        """Return whether the Mat is a linear operator."""
        ...

    def zeroEntries(self) -> None:
        """Zero the entries of the matrix."""
        ...

    # Getting/setting values
    def getValue(self, row: int, col: int) -> Scalar:
        """Return the value in the (row, col) position."""
        ...

    def getValues(
        self,
        rows: Sequence[int],
        cols: Sequence[int],
        values: ArrayScalar | None = None
    ) -> ArrayScalar:
        """Return the values in the zip(rows, cols) positions."""
        ...

    def getValuesCSR(self) -> tuple[ArrayInt, ArrayInt, ArrayScalar]:
        """Return the CSR representation of the local part of the matrix."""
        ...

    def getRow(self, row: int) -> tuple[ArrayInt, ArrayScalar]:
        """Return the column indices and values for the requested row."""
        ...

    def getRowIJ(
        self,
        symmetric: bool = False,
        compressed: bool = False
    ) -> tuple[ArrayInt, ArrayInt]:
        """Return the CSR representation of the local sparsity pattern."""
        ...

    def getColumnIJ(
        self,
        symmetric: bool = False,
        compressed: bool = False
    ) -> tuple[ArrayInt, ArrayInt]:
        """Return the CSC representation of the local sparsity pattern."""
        ...

    def setValue(
        self,
        row: int,
        col: int,
        value: Scalar,
        addv: InsertModeSpec = None
    ) -> None:
        """Set a value to the (row, col) entry of the matrix."""
        ...

    def setValues(
        self,
        rows: Sequence[int],
        cols: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values to the rows ⊗ cols entries of the matrix."""
        ...

    def setValuesRCV(self, R: Any, C: Any, V: Any, addv: InsertModeSpec = None) -> None:
        """Undocumented."""
        ...

    def setValuesIJV(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None,
        rowmap: Sequence[int] | None = None
    ) -> None:
        """Set a subset of values stored in CSR format."""
        ...

    def setValuesCOO(
        self,
        coo_v: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values after preallocation with coordinate format."""
        ...

    def setValuesCSR(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values stored in CSR format."""
        ...

    def setValuesBlocked(
        self,
        rows: Sequence[int],
        cols: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values to the rows ⊗ col block entries of the matrix."""
        ...

    def setValuesBlockedRCV(self, R: Any, C: Any, V: Any, addv: InsertModeSpec = None) -> None:
        """Undocumented."""
        ...

    def setValuesBlockedIJV(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None,
        rowmap: Sequence[int] | None = None
    ) -> None:
        """Set a subset of values stored in block CSR format."""
        ...

    def setValuesBlockedCSR(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values stored in block CSR format."""
        ...

    def setLGMap(self, rmap: LGMap, cmap: LGMap | None = None) -> None:
        """Set the local-to-global mappings."""
        ...

    def getLGMap(self) -> tuple[LGMap, LGMap]:
        """Return the local-to-global mappings."""
        ...

    def setValueLocal(
        self,
        row: int,
        col: int,
        value: Scalar,
        addv: InsertModeSpec = None
    ) -> None:
        """Set a value to the (row, col) entry of the matrix in local ordering."""
        ...

    def setValuesLocal(
        self,
        rows: Sequence[int],
        cols: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values to the rows ⊗ col entries of the matrix in local ordering."""
        ...

    def setValuesLocalRCV(self, R: Any, C: Any, V: Any, addv: InsertModeSpec = None) -> None:
        """Undocumented."""
        ...

    def setValuesLocalIJV(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None,
        rowmap: Sequence[int] | None = None
    ) -> None:
        """Set a subset of values stored in CSR format."""
        ...

    def setValuesLocalCSR(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values stored in CSR format."""
        ...

    def setValuesBlockedLocal(
        self,
        rows: Sequence[int],
        cols: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values to the rows ⊗ col block entries of the matrix in local ordering."""
        ...

    def setValuesBlockedLocalRCV(self, R: Any, C: Any, V: Any, addv: InsertModeSpec = None) -> None:
        """Undocumented."""
        ...

    def setValuesBlockedLocalIJV(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None,
        rowmap: Sequence[int] | None = None
    ) -> None:
        """Set a subset of values stored in block CSR format."""
        ...

    def setValuesBlockedLocalCSR(
        self,
        I: Sequence[int],
        J: Sequence[int],
        V: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set values stored in block CSR format."""
        ...

    # Stencil
    def setStencil(self, dims: DimsSpec, starts: DimsSpec | None = None, dof: int = 1) -> None:
        """Set matrix stencil."""
        ...

    def setValueStencil(
        self,
        row: MatStencil,
        col: MatStencil,
        value: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set a value to row and col stencil."""
        ...

    def setValueStagStencil(self, row: Any, col: Any, value: Any, addv: InsertModeSpec = None) -> None:
        """Not implemented."""
        ...

    def setValueBlockedStencil(
        self,
        row: MatStencil,
        col: MatStencil,
        value: Sequence[Scalar],
        addv: InsertModeSpec = None
    ) -> None:
        """Set a block of values to row and col stencil."""
        ...

    def setValueBlockedStagStencil(self, row: Any, col: Any, value: Any, addv: InsertModeSpec = None) -> None:
        """Not implemented."""
        ...

    # Zero rows
    def zeroRows(
        self,
        rows: IS | Sequence[int],
        diag: Scalar = 1.0,
        x: Vec | None = None,
        b: Vec | None = None
    ) -> None:
        """Zero selected rows of the matrix."""
        ...

    def zeroRowsLocal(
        self,
        rows: IS | Sequence[int],
        diag: Scalar = 1.0,
        x: Vec | None = None,
        b: Vec | None = None
    ) -> None:
        """Zero selected rows of the matrix in local ordering."""
        ...

    def zeroRowsColumns(
        self,
        rows: IS | Sequence[int],
        diag: Scalar = 1.0,
        x: Vec | None = None,
        b: Vec | None = None
    ) -> None:
        """Zero selected rows and columns of the matrix."""
        ...

    def zeroRowsColumnsLocal(
        self,
        rows: IS | Sequence[int],
        diag: Scalar = 1.0,
        x: Vec | None = None,
        b: Vec | None = None
    ) -> None:
        """Zero selected rows and columns of the matrix in local ordering."""
        ...

    def zeroRowsColumnsStencil(
        self,
        rows: Sequence[MatStencil],
        diag: Scalar = 1.0,
        x: Vec | None = None,
        b: Vec | None = None
    ) -> None:
        """Zero selected rows and columns of the matrix."""
        ...

    def storeValues(self) -> None:
        """Stash a copy of the matrix values."""
        ...

    def retrieveValues(self) -> None:
        """Retrieve a copy of the matrix values previously stored with storeValues."""
        ...

    # Assembly
    def assemblyBegin(self, assembly: MatAssemblySpec = None) -> None:
        """Begin an assembling stage of the matrix."""
        ...

    def assemblyEnd(self, assembly: MatAssemblySpec = None) -> None:
        """Complete an assembling stage of the matrix initiated with assemblyBegin."""
        ...

    def assemble(self, assembly: MatAssemblySpec = None) -> None:
        """Assemble the matrix."""
        ...

    def isAssembled(self) -> bool:
        """The boolean flag indicating if the matrix is assembled."""
        ...

    def findZeroRows(self) -> IS:
        """Return the index set of empty rows."""
        ...

    # Vector creation
    @overload
    def createVecs(self, side: None = None) -> tuple[Vec, Vec]: ...
    @overload
    def createVecs(self, side: Literal['r', 'R', 'right', 'Right', 'RIGHT']) -> Vec: ...
    @overload
    def createVecs(self, side: Literal['l', 'L', 'left', 'Left', 'LEFT']) -> Vec: ...

    def createVecRight(self) -> Vec:
        """Return a right vector, a vector that the matrix can be multiplied against."""
        ...

    def createVecLeft(self) -> Vec:
        """Return a left vector, a vector that the matrix vector product can be stored in."""
        ...

    getVecs = createVecs
    getVecRight = createVecRight
    getVecLeft = createVecLeft

    def getColumnVector(self, column: int, result: Vec | None = None) -> Vec:
        """Return the columnᵗʰ column vector of the matrix."""
        ...

    def getRedundantMatrix(
        self,
        nsubcomm: int,
        subcomm: Comm | None = None,
        out: Mat | None = None
    ) -> Mat:
        """Return redundant matrices on subcommunicators."""
        ...

    def getDiagonal(self, result: Vec | None = None) -> Vec:
        """Return the diagonal of the matrix."""
        ...

    def getRowSum(self, result: Vec | None = None) -> Vec:
        """Return the row-sum vector."""
        ...

    def setDiagonal(self, diag: Vec, addv: InsertModeSpec = None) -> None:
        """Set the diagonal values of the matrix."""
        ...

    def diagonalScale(self, L: Vec | None = None, R: Vec | None = None) -> None:
        """Perform left and/or right diagonal scaling of the matrix."""
        ...

    def invertBlockDiagonal(self) -> ArrayScalar:
        """Return the inverse of the block-diagonal entries."""
        ...

    # Null space
    def setNullSpace(self, nsp: NullSpace) -> None:
        """Set the nullspace."""
        ...

    def getNullSpace(self) -> NullSpace:
        """Return the nullspace."""
        ...

    def setTransposeNullSpace(self, nsp: NullSpace) -> None:
        """Set the transpose nullspace."""
        ...

    def getTransposeNullSpace(self) -> NullSpace:
        """Return the transpose nullspace."""
        ...

    def setNearNullSpace(self, nsp: NullSpace) -> None:
        """Set the near-nullspace."""
        ...

    def getNearNullSpace(self) -> NullSpace:
        """Return the near-nullspace."""
        ...

    # Matrix-vector product
    def mult(self, x: Vec, y: Vec) -> None:
        """Perform the matrix vector product y = A @ x."""
        ...

    def multAdd(self, x: Vec, v: Vec, y: Vec) -> None:
        """Perform the matrix vector product with addition y = A @ x + v."""
        ...

    def multTranspose(self, x: Vec, y: Vec) -> None:
        """Perform the transposed matrix vector product y = A^T @ x."""
        ...

    def multTransposeAdd(self, x: Vec, v: Vec, y: Vec) -> None:
        """Perform the transposed matrix vector product with addition y = A^T @ x + v."""
        ...

    def multHermitian(self, x: Vec, y: Vec) -> None:
        """Perform the Hermitian matrix vector product y = A^H @ x."""
        ...

    def multHermitianAdd(self, x: Vec, v: Vec, y: Vec) -> None:
        """Perform the Hermitian matrix vector product with addition y = A^H @ x + v."""
        ...

    # SOR
    def SOR(
        self,
        b: Vec,
        x: Vec,
        omega: float = 1.0,
        sortype: int | None = None,
        shift: float = 0.0,
        its: int = 1,
        lits: int = 1
    ) -> None:
        """Compute relaxation (SOR, Gauss-Seidel) sweeps."""
        ...

    def getDiagonalBlock(self) -> Mat:
        """Return the part of the matrix associated with the on-process coupling."""
        ...

    def increaseOverlap(self, iset: IS, overlap: int = 1) -> None:
        """Increase the overlap of a index set."""
        ...

    def createSubMatrix(
        self,
        isrow: IS,
        iscol: IS | None = None,
        submat: Mat | None = None
    ) -> Mat:
        """Return a submatrix."""
        ...

    def createSubMatrices(
        self,
        isrows: IS | Sequence[IS],
        iscols: IS | Sequence[IS] | None = None,
        submats: Mat | Sequence[Mat] | None = None
    ) -> Sequence[Mat]:
        """Return several sequential submatrices."""
        ...

    def createSchurComplement(
        self,
        A00: Mat,
        Ap00: Mat,
        A01: Mat,
        A10: Mat,
        A11: Mat | None = None
    ) -> Self:
        """Create a SCHURCOMPLEMENT matrix."""
        ...

    def getSchurComplementSubMatrices(self) -> tuple[Mat, Mat, Mat, Mat, Mat]:
        """Return Schur complement sub-matrices."""
        ...

    def getLocalSubMatrix(
        self,
        isrow: IS,
        iscol: IS,
        submat: Mat | None = None
    ) -> Mat:
        """Return a reference to a submatrix specified in local numbering."""
        ...

    def restoreLocalSubMatrix(self, isrow: IS, iscol: IS, submat: Mat) -> None:
        """Restore a reference to a submatrix obtained with getLocalSubMatrix."""
        ...

    def norm(self, norm_type: NormTypeSpec = None) -> float | tuple[float, float]:
        """Compute the requested matrix norm."""
        ...

    def scale(self, alpha: Scalar) -> None:
        """Scale the matrix."""
        ...

    def shift(self, alpha: Scalar) -> None:
        """Shift the matrix."""
        ...

    def chop(self, tol: float) -> None:
        """Set entries smallest of tol (in absolute values) to zero."""
        ...

    def setRandom(self, random: Random | None = None) -> None:
        """Set random values in the matrix."""
        ...

    def axpy(self, alpha: Scalar, X: Mat, structure: int | None = None) -> None:
        """Perform the matrix summation self += ɑ·X."""
        ...

    def aypx(self, alpha: Scalar, X: Mat, structure: int | None = None) -> None:
        """Perform the matrix summation self = ɑ·self + X."""
        ...

    # Matrix-matrix product
    def matMult(
        self,
        mat: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Perform matrix-matrix multiplication C=AB."""
        ...

    def matTransposeMult(
        self,
        mat: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Perform matrix-matrix multiplication C=ABᵀ."""
        ...

    def transposeMatMult(
        self,
        mat: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Perform matrix-matrix multiplication C=AᵀB."""
        ...

    def ptap(
        self,
        P: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Creates the matrix product C = PᵀAP."""
        ...

    def rart(
        self,
        R: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Create the matrix product C = RARᵀ."""
        ...

    def matMatMult(
        self,
        B: Mat,
        C: Mat,
        result: Mat | None = None,
        fill: float | None = None
    ) -> Mat:
        """Perform matrix-matrix-matrix multiplication D=ABC."""
        ...

    def kron(self, mat: Mat, result: Mat | None = None) -> Mat:
        """Compute C, the Kronecker product of A and B."""
        ...

    def bindToCPU(self, flg: bool) -> None:
        """Mark a matrix to temporarily stay on the CPU."""
        ...

    def boundToCPU(self) -> bool:
        """Query if a matrix is bound to the CPU."""
        ...

    # Factorization
    def getOrdering(self, ord_type: str) -> tuple[IS, IS]:
        """Return a reordering for a matrix to improve a LU factorization."""
        ...

    def reorderForNonzeroDiagonal(
        self,
        isrow: IS,
        iscol: IS,
        atol: float = 0
    ) -> None:
        """Change a matrix ordering to remove zeros from the diagonal."""
        ...

    def factorLU(
        self,
        isrow: IS,
        iscol: IS,
        options: dict[str, Any] | None = None
    ) -> None:
        """Perform an in-place LU factorization."""
        ...

    def factorSymbolicLU(self, mat: Mat, isrow: IS, iscol: IS, options: Any = None) -> None:
        """Not implemented."""
        ...

    def factorNumericLU(self, mat: Mat, options: Any = None) -> None:
        """Not implemented."""
        ...

    def factorILU(
        self,
        isrow: IS,
        iscol: IS,
        options: dict[str, Any] | None = None
    ) -> None:
        """Perform an in-place ILU factorization."""
        ...

    def factorSymbolicILU(self, isrow: IS, iscol: IS, options: Any = None) -> None:
        """Not implemented."""
        ...

    def factorCholesky(
        self,
        isperm: IS,
        options: dict[str, Any] | None = None
    ) -> None:
        """Perform an in-place Cholesky factorization."""
        ...

    def factorSymbolicCholesky(self, isperm: IS, options: Any = None) -> None:
        """Not implemented."""
        ...

    def factorNumericCholesky(self, mat: Mat, options: Any = None) -> None:
        """Not implemented."""
        ...

    def factorICC(
        self,
        isperm: IS,
        options: dict[str, Any] | None = None
    ) -> None:
        """Perform an in-place an incomplete Cholesky factorization."""
        ...

    def factorSymbolicICC(self, isperm: IS, options: Any = None) -> None:
        """Not implemented."""
        ...

    def getInertia(self) -> tuple[int, int, int]:
        """Return the inertia from a factored matrix."""
        ...

    def setUnfactored(self) -> None:
        """Set a factored matrix to be treated as unfactored."""
        ...

    # IS matrix methods
    def setISAllowRepeated(self, allow: bool = True) -> None:
        """Allow repeated entries in the local to global map."""
        ...

    def getISAllowRepeated(self) -> bool:
        """Get the flag for repeated entries in the local to global map."""
        ...

    def fixISLocalEmpty(self, fix: bool = True) -> None:
        """Compress out zero local rows from the local matrices."""
        ...

    def getISLocalMat(self) -> Mat:
        """Return the local matrix stored inside an IS matrix."""
        ...

    def restoreISLocalMat(self, local: Mat) -> None:
        """Restore the local matrix obtained with getISLocalMat."""
        ...

    def setISLocalMat(self, local: Mat) -> None:
        """Set the local matrix stored inside a Type.IS."""
        ...

    def setISPreallocation(
        self,
        nnz: Sequence[int],
        onnz: Sequence[int]
    ) -> Self:
        """Preallocate memory for an IS parallel matrix."""
        ...

    # LRC methods
    def getLRCMats(self) -> tuple[Mat, Mat, Vec, Mat]:
        """Return the constituents of an LRC matrix."""
        ...

    def setLRCMats(
        self,
        A: Mat | None,
        U: Mat,
        c: Vec | None = None,
        V: Mat | None = None
    ) -> None:
        """Set the constituents of an LRC matrix."""
        ...

    # H2Opus methods
    def H2OpusOrthogonalize(self) -> Self:
        """Orthogonalize the basis tree of a hierarchical matrix."""
        ...

    def H2OpusCompress(self, tol: float) -> Self:
        """Compress a hierarchical matrix."""
        ...

    def H2OpusLowRankUpdate(
        self,
        U: Mat,
        V: Mat | None = None,
        s: float = 1.0
    ) -> Self:
        """Perform a low-rank update of the form self += sUVᵀ."""
        ...

    # LMVM methods
    def getLMVMJ0(self) -> Mat:
        """Get the initial Jacobian of the LMVM matrix."""
        ...

    def setLMVMJ0(self, J0: Mat) -> None:
        """Set the initial Jacobian of the LMVM matrix."""
        ...

    def getLMVMJ0KSP(self) -> KSP:
        """Get the KSP of the LMVM matrix."""
        ...

    def setLMVMJ0KSP(self, ksp: KSP) -> None:
        """Set the KSP of the LMVM matrix."""
        ...

    def allocateLMVM(self, x: Vec, f: Vec) -> None:
        """Allocate all necessary common memory LMVM matrix."""
        ...

    def updateLMVM(self, x: Vec, f: Vec) -> None:
        """Adds (X-Xprev) and (F-Fprev) updates to LMVM matrix."""
        ...

    def resetLMVM(self, destructive: bool = False) -> None:
        """Flushes all of the accumulated updates out of the LMVM matrix."""
        ...

    # MUMPS methods
    def setMumpsIcntl(self, icntl: int, ival: int) -> None:
        """Set a MUMPS parameter, ICNTL[icntl] = ival."""
        ...

    def getMumpsIcntl(self, icntl: int) -> int:
        """Return the MUMPS parameter, ICNTL[icntl]."""
        ...

    def setMumpsCntl(self, icntl: int, val: float) -> None:
        """Set a MUMPS parameter, CNTL[icntl] = val."""
        ...

    def getMumpsCntl(self, icntl: int) -> float:
        """Return the MUMPS parameter, CNTL[icntl]."""
        ...

    def getMumpsInfo(self, icntl: int) -> int:
        """Return the MUMPS parameter, INFO[icntl]."""
        ...

    def getMumpsInfog(self, icntl: int) -> int:
        """Return the MUMPS parameter, INFOG[icntl]."""
        ...

    def getMumpsRinfo(self, icntl: int) -> float:
        """Return the MUMPS parameter, RINFO[icntl]."""
        ...

    def getMumpsRinfog(self, icntl: int) -> float:
        """Return the MUMPS parameter, RINFOG[icntl]."""
        ...

    # Solve methods
    def solveForward(self, b: Vec, x: Vec) -> None:
        """Solve Lx = b, given a factored matrix A = LU."""
        ...

    def solveBackward(self, b: Vec, x: Vec) -> None:
        """Solve Ux=b, given a factored matrix A=LU."""
        ...

    def solve(self, b: Vec, x: Vec) -> None:
        """Solve Ax=b, given a factored matrix."""
        ...

    def solveTranspose(self, b: Vec, x: Vec) -> None:
        """Solve Aᵀx=b, given a factored matrix."""
        ...

    def solveAdd(self, b: Vec, y: Vec, x: Vec) -> None:
        """Solve x=y+A⁻¹b, given a factored matrix."""
        ...

    def solveTransposeAdd(self, b: Vec, y: Vec, x: Vec) -> None:
        """Solve x=y+A⁻ᵀb, given a factored matrix."""
        ...

    def matSolve(self, B: Mat, X: Mat) -> None:
        """Solve AX=B, given a factored matrix A."""
        ...

    # Dense matrix methods
    def setDenseLDA(self, lda: int) -> None:
        """Set the leading dimension of the array used by the dense matrix."""
        ...

    def getDenseLDA(self) -> int:
        """Return the leading dimension of the array used by the dense matrix."""
        ...

    def getDenseArray(self, readonly: bool = False) -> ArrayScalar:
        """Return the array where the data is stored."""
        ...

    def getDenseLocalMatrix(self) -> Mat:
        """Return the local part of the dense matrix."""
        ...

    def getDenseSubMatrix(
        self,
        rbegin: int = -1,
        rend: int = -1,
        cbegin: int = -1,
        cend: int = -1
    ) -> Mat:
        """Get access to a submatrix of a DENSE matrix."""
        ...

    def restoreDenseSubMatrix(self, mat: Mat) -> None:
        """Restore access to a submatrix of a DENSE matrix."""
        ...

    def getDenseColumnVec(self, i: int, mode: AccessModeSpec = 'rw') -> Vec:
        """Return the iᵗʰ column vector of the dense matrix."""
        ...

    def restoreDenseColumnVec(
        self,
        i: int,
        mode: AccessModeSpec = 'rw',
        V: Vec | None = None
    ) -> None:
        """Restore the iᵗʰ column vector of the dense matrix."""
        ...

    # Nest matrix methods
    def getNestSize(self) -> tuple[int, int]:
        """Return the number of rows and columns of the matrix."""
        ...

    def getNestISs(self) -> tuple[list[IS], list[IS]]:
        """Return the index sets representing the row and column spaces."""
        ...

    def getNestLocalISs(self) -> tuple[list[IS], list[IS]]:
        """Return the local index sets representing the row and column spaces."""
        ...

    def getNestSubMatrix(self, i: int, j: int) -> Mat:
        """Return a single submatrix."""
        ...

    # DM methods
    def getDM(self) -> DM:
        """Return the DM defining the data layout of the matrix."""
        ...

    def setDM(self, dm: DM) -> None:
        """Set the DM defining the data layout of the matrix."""
        ...

    # Backward compatibility
    PtAP = ptap

    # Properties
    @property
    def sizes(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Matrix local and global sizes."""
        ...

    @sizes.setter
    def sizes(self, value: MatSizeSpec) -> None: ...

    @property
    def size(self) -> tuple[int, int]:
        """Matrix global size."""
        ...

    @property
    def local_size(self) -> tuple[int, int]:
        """Matrix local size."""
        ...

    @property
    def block_size(self) -> int:
        """Matrix block size."""
        ...

    @property
    def block_sizes(self) -> tuple[int, int]:
        """Matrix row and column block sizes."""
        ...

    @property
    def owner_range(self) -> tuple[int, int]:
        """Matrix local row range."""
        ...

    @property
    def owner_ranges(self) -> ArrayInt:
        """Matrix row ranges."""
        ...

    @property
    def assembled(self) -> bool:
        """The boolean flag indicating if the matrix is assembled."""
        ...

    @property
    def symmetric(self) -> bool:
        """The boolean flag indicating if the matrix is symmetric."""
        ...

    @property
    def hermitian(self) -> bool:
        """The boolean flag indicating if the matrix is Hermitian."""
        ...

    @property
    def structsymm(self) -> bool:
        """The boolean flag indicating if the matrix is structurally symmetric."""
        ...

    # DLPack support
    def __dlpack__(self, stream: int = -1) -> Any:
        """Return a DLPack PyCapsule wrapping the matrix data."""
        ...

    def __dlpack_device__(self) -> tuple[int, int]:
        """Return the device type and ID for DLPack."""
        ...

    def toDLPack(self, mode: AccessModeSpec = 'rw') -> Any:
        """Return a DLPack PyCapsule wrapping the matrix data."""
        ...


class NullSpace(Object):
    """Nullspace object."""

    def view(self, viewer: Viewer | None = None) -> None:
        """View the null space."""
        ...

    def destroy(self) -> Self:
        """Destroy the null space."""
        ...

    def create(
        self,
        constant: bool = False,
        vectors: Sequence[Vec] = (),
        comm: Comm | None = None
    ) -> Self:
        """Create the null space."""
        ...

    def createRigidBody(self, coords: Vec) -> Self:
        """Create rigid body modes from coordinates."""
        ...

    def setFunction(
        self,
        function: Callable[[NullSpace, Vec], None] | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None
    ) -> None:
        """Set the callback to remove the nullspace."""
        ...

    def hasConstant(self) -> bool:
        """Return whether the null space contains the constant."""
        ...

    def getVecs(self) -> list[Vec]:
        """Return the vectors defining the null space."""
        ...

    def getFunction(self) -> Callable[[NullSpace, Vec], None] | None:
        """Return the callback to remove the nullspace."""
        ...

    def remove(self, vec: Vec) -> None:
        """Remove all components of a null space from a vector."""
        ...

    def test(self, mat: Mat) -> bool:
        """Return if the claimed null space is valid for a matrix."""
        ...


# Type aliases for callback functions
MatNullFunction = Callable[[NullSpace, Vec], None]
