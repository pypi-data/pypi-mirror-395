"""Type stubs for PETSc Vec module."""


from typing import Any, Literal, Sequence, Self
from numpy import ndarray, dtype

# Import types from other modules
from .Object import Object
from .IS import IS, LGMap
from .Viewer import Viewer
from .Random import Random

from .Comm import Comm
from .DM import DM

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    LayoutSizeSpec,
    InsertModeSpec,
    NormTypeSpec,
    ScatterModeSpec,
    AccessModeSpec,
)

class VecType:
    """The vector type."""

    SEQ: str
    MPI: str
    STANDARD: str
    SHARED: str
    SEQVIENNACL: str
    MPIVIENNACL: str
    VIENNACL: str
    SEQCUDA: str
    MPICUDA: str
    CUDA: str
    SEQHIP: str
    MPIHIP: str
    HIP: str
    NEST: str
    SEQKOKKOS: str
    MPIKOKKOS: str
    KOKKOS: str

class VecOption:
    """Vector assembly option."""

    IGNORE_OFF_PROC_ENTRIES: int
    IGNORE_NEGATIVE_INDICES: int

class Vec(Object):
    """A vector object.

    Vec is the basic PETSc vector object used to store field values
    and right-hand-sides of linear systems.
    """

    Type = VecType
    Option = VecOption

    # Unary operations
    def __pos__(self) -> Vec: ...
    def __neg__(self) -> Vec: ...
    def __abs__(self) -> Vec: ...

    # In-place binary operations
    def __iadd__(self, other: Vec | Scalar) -> Vec: ...
    def __isub__(self, other: Vec | Scalar) -> Vec: ...
    def __imul__(self, other: Vec | Scalar) -> Vec: ...
    def __idiv__(self, other: Vec | Scalar) -> Vec: ...
    def __itruediv__(self, other: Vec | Scalar) -> Vec: ...

    # Binary operations
    def __add__(self, other: Vec | Scalar) -> Vec: ...
    def __radd__(self, other: Vec | Scalar) -> Vec: ...
    def __sub__(self, other: Vec | Scalar) -> Vec: ...
    def __rsub__(self, other: Vec | Scalar) -> Vec: ...
    def __mul__(self, other: Vec | Scalar) -> Vec: ...
    def __rmul__(self, other: Vec | Scalar) -> Vec: ...
    def __div__(self, other: Vec | Scalar) -> Vec: ...
    def __rdiv__(self, other: Vec | Scalar) -> Vec: ...
    def __truediv__(self, other: Vec | Scalar) -> Vec: ...
    def __rtruediv__(self, other: Vec | Scalar) -> Vec: ...
    def __matmul__(self, other: Vec) -> Scalar: ...

    # Indexing
    def __getitem__(self, i: int | slice) -> Scalar | ArrayScalar: ...
    def __setitem__(self, i: int | slice, v: Scalar | Sequence[Scalar]) -> None: ...

    # Buffer protocol
    def __enter__(self) -> ArrayScalar: ...
    def __exit__(self, *exc: Any) -> None: ...
    def view(self, viewer: Viewer | None = None) -> None:
        """Display the vector.

        Parameters
        ----------
        viewer
            A Viewer instance or None for the default viewer.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the vector."""
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a vector object.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setType(self, vec_type: VecType | str) -> None:
        """Set the vector type.

        Parameters
        ----------
        vec_type
            The vector type.
        """
        ...

    def setSizes(self, size: LayoutSizeSpec, bsize: int | None = None) -> None:
        """Set the local and global sizes of the vector.

        Parameters
        ----------
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        """
        ...

    def createSeq(
        self, size: LayoutSizeSpec, bsize: int | None = None, comm: Comm | None = None
    ) -> Self:
        """Create a sequential Type.SEQ vector.

        Parameters
        ----------
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to COMM_SELF.
        """
        ...

    def createMPI(
        self, size: LayoutSizeSpec, bsize: int | None = None, comm: Comm | None = None
    ) -> Self:
        """Create a parallel Type.MPI vector.

        Parameters
        ----------
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createWithArray(
        self,
        array: Sequence[Scalar],
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a vector using a provided array.

        Parameters
        ----------
        array
            Array to store the vector values.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createCUDAWithArrays(
        self,
        cpuarray: Sequence[Scalar] | None = None,
        cudahandle: Any | None = None,
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a Type.CUDA vector with optional arrays.

        Parameters
        ----------
        cpuarray
            Host array. Will be lazily allocated if not provided.
        cudahandle
            Address of the array on the GPU.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createHIPWithArrays(
        self,
        cpuarray: Sequence[Scalar] | None = None,
        hiphandle: Any | None = None,
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a Type.HIP vector with optional arrays.

        Parameters
        ----------
        cpuarray
            Host array. Will be lazily allocated if not provided.
        hiphandle
            Address of the array on the GPU.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createViennaCLWithArrays(
        self,
        cpuarray: Sequence[Scalar] | None = None,
        viennaclvechandle: Any | None = None,
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a Type.VIENNACL vector with optional arrays.

        Parameters
        ----------
        cpuarray
            Host array. Will be lazily allocated if not provided.
        viennaclvechandle
            Address of the array on the GPU.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createWithDLPack(
        self,
        dltensor: Any,
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a vector wrapping a DLPack object, sharing the same memory.

        Parameters
        ----------
        dltensor
            Either an object with a __dlpack__ method or a DLPack tensor object.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def attachDLPackInfo(
        self, vec: Vec | None = None, dltensor: Any | None = None
    ) -> Self:
        """Attach tensor information from another vector or DLPack tensor.

        Parameters
        ----------
        vec
            Vector with attached tensor information.
        dltensor
            DLPack tensor. Only used if vec is None.
        """
        ...

    def clearDLPackInfo(self) -> Self:
        """Clear tensor information."""
        ...

    def __dlpack__(self, stream: int = -1) -> Any:
        """Return a DLPack PyCapsule wrapping the vector data."""
        ...

    def __dlpack_device__(self) -> tuple[int, int]:
        """Return the device type and ID for DLPack."""
        ...

    def toDLPack(self, mode: AccessModeSpec = "rw") -> Any:
        """Return a DLPack PyCapsule wrapping the vector data.

        Parameters
        ----------
        mode
            Access mode for the vector.
        """
        ...

    def createGhost(
        self,
        ghosts: Sequence[int],
        size: LayoutSizeSpec,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a parallel vector with ghost padding on each processor.

        Parameters
        ----------
        ghosts
            Global indices of ghost points.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createGhostWithArray(
        self,
        ghosts: Sequence[int],
        array: Sequence[Scalar],
        size: LayoutSizeSpec | None = None,
        bsize: int | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a parallel vector with ghost padding and provided arrays.

        Parameters
        ----------
        ghosts
            Global indices of ghost points.
        array
            Array to store the vector values.
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createShared(
        self, size: LayoutSizeSpec, bsize: int | None = None, comm: Comm | None = None
    ) -> Self:
        """Create a Type.SHARED vector that uses shared memory.

        Parameters
        ----------
        size
            Vector size.
        bsize
            Vector block size. If None, bsize = 1.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def createNest(
        self,
        vecs: Sequence[Vec],
        isets: Sequence[IS] | None = None,
        comm: Comm | None = None,
    ) -> Self:
        """Create a Type.NEST vector containing multiple nested subvectors.

        Parameters
        ----------
        vecs
            Iterable of subvectors.
        isets
            Iterable of index sets for each nested subvector.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for searching for options in the database."""
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database."""
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for searching for options in the database."""
        ...

    def setFromOptions(self) -> None:
        """Configure the vector from the options database."""
        ...

    def setUp(self) -> Self:
        """Set up the internal data structures for using the vector."""
        ...

    def setOption(self, option: VecOption | int, flag: bool) -> None:
        """Set option."""
        ...

    def getType(self) -> str:
        """Return the type of the vector."""
        ...

    def getSize(self) -> int:
        """Return the global size of the vector."""
        ...

    def getLocalSize(self) -> int:
        """Return the local size of the vector."""
        ...

    def getSizes(self) -> tuple[int, int]:
        """Return the vector sizes (local, global)."""
        ...

    def setBlockSize(self, bsize: int) -> None:
        """Set the block size of the vector."""
        ...

    def getBlockSize(self) -> int:
        """Return the block size of the vector."""
        ...

    def getOwnershipRange(self) -> tuple[int, int]:
        """Return the locally owned range of indices (start, end)."""
        ...

    def getOwnershipRanges(self) -> ArrayInt:
        """Return the range of indices owned by each process."""
        ...

    def createLocalVector(self) -> Vec:
        """Create a local vector."""
        ...

    def getLocalVector(self, lvec: Vec, readonly: bool = False) -> None:
        """Maps the local portion of the vector into a local vector.

        Parameters
        ----------
        lvec
            The local vector obtained from createLocalVector.
        readonly
            Request read-only access.
        """
        ...

    def restoreLocalVector(self, lvec: Vec, readonly: bool = False) -> None:
        """Unmap a local access obtained with getLocalVector.

        Parameters
        ----------
        lvec
            The local vector.
        readonly
            Request read-only access.
        """
        ...

    def getBuffer(self, readonly: bool = False) -> Any:
        """Return a buffered view of the local portion of the vector.

        Parameters
        ----------
        readonly
            Request read-only access.
        """
        ...

    def getArray(self, readonly: bool = False) -> ArrayScalar:
        """Return local portion of the vector as an ndarray.

        Parameters
        ----------
        readonly
            Request read-only access.
        """
        ...

    def setArray(self, array: Sequence[Scalar]) -> None:
        """Set values for the local portion of the vector."""
        ...

    def placeArray(self, array: Sequence[Scalar]) -> None:
        """Set the local portion of the vector to a provided array."""
        ...

    def resetArray(self, force: bool = False) -> ArrayScalar | None:
        """Reset the vector to use its default array.

        Parameters
        ----------
        force
            Force the calling even if no user array has been placed.
        """
        ...

    def bindToCPU(self, flg: bool) -> None:
        """Bind vector operations execution on the CPU."""
        ...

    def boundToCPU(self) -> bool:
        """Return whether the vector has been bound to the CPU."""
        ...

    def getCUDAHandle(self, mode: AccessModeSpec = "rw") -> Any:
        """Return a pointer to the CUDA device buffer."""
        ...

    def restoreCUDAHandle(self, handle: Any, mode: AccessModeSpec = "rw") -> None:
        """Restore a pointer to the device buffer obtained with getCUDAHandle."""
        ...

    def getHIPHandle(self, mode: AccessModeSpec = "rw") -> Any:
        """Return a pointer to the HIP device buffer."""
        ...

    def restoreHIPHandle(self, handle: Any, mode: AccessModeSpec = "rw") -> None:
        """Restore a pointer to the device buffer obtained with getHIPHandle."""
        ...

    def getOffloadMask(self) -> int:
        """Return the offloading status of the vector."""
        ...

    def getCLContextHandle(self) -> int:
        """Return the OpenCL context associated with the vector."""
        ...

    def getCLQueueHandle(self) -> int:
        """Return the OpenCL command queue associated with the vector."""
        ...

    def getCLMemHandle(self, mode: AccessModeSpec = "rw") -> int:
        """Return the OpenCL buffer associated with the vector."""
        ...

    def restoreCLMemHandle(self) -> None:
        """Restore a pointer to the OpenCL buffer obtained with getCLMemHandle."""
        ...

    def duplicate(self, array: Sequence[Scalar] | None = None) -> Vec:
        """Create a new vector with the same type, optionally with data.

        Parameters
        ----------
        array
            Optional values to store in the new vector.
        """
        ...

    def copy(self, result: Vec | None = None) -> Vec:
        """Return a copy of the vector.

        Parameters
        ----------
        result
            Target vector for the copy. If None then a new vector is created.
        """
        ...

    def chop(self, tol: float) -> None:
        """Set all vector entries less than some absolute tolerance to zero.

        Parameters
        ----------
        tol
            The absolute tolerance below which entries are set to zero.
        """
        ...

    def load(self, viewer: Viewer) -> Self:
        """Load a vector."""
        ...

    def equal(self, vec: Vec) -> bool:
        """Return whether the vector is equal to another.

        Parameters
        ----------
        vec
            Vector to compare with.
        """
        ...

    def dot(self, vec: Vec) -> Scalar:
        """Return the dot product with vec.

        For complex numbers this computes yᴴ·x with self as x, vec as y.

        Parameters
        ----------
        vec
            Vector to compute the dot product with.
        """
        ...

    def dotBegin(self, vec: Vec) -> None:
        """Begin computing the dot product.

        Parameters
        ----------
        vec
            Vector to compute the dot product with.
        """
        ...

    def dotEnd(self, vec: Vec) -> Scalar:
        """Finish computing the dot product initiated with dotBegin."""
        ...

    def tDot(self, vec: Vec) -> Scalar:
        """Return the indefinite dot product with vec.

        This computes yᵀ·x with self as x, vec as y.

        Parameters
        ----------
        vec
            Vector to compute the indefinite dot product with.
        """
        ...

    def tDotBegin(self, vec: Vec) -> None:
        """Begin computing the indefinite dot product.

        Parameters
        ----------
        vec
            Vector to compute the indefinite dot product with.
        """
        ...

    def tDotEnd(self, vec: Vec) -> Scalar:
        """Finish computing the indefinite dot product initiated with tDotBegin."""
        ...

    def mDot(self, vecs: Sequence[Vec], out: ArrayScalar | None = None) -> ArrayScalar:
        """Compute Xᴴ·y with X an array of vectors.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Optional placeholder for the result.
        """
        ...

    def mDotBegin(self, vecs: Sequence[Vec], out: ArrayScalar) -> None:
        """Start a split phase multiple dot product computation.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Placeholder for the result.
        """
        ...

    def mDotEnd(self, vecs: Sequence[Vec], out: ArrayScalar) -> ArrayScalar:
        """End a split phase multiple dot product computation.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Placeholder for the result.
        """
        ...

    def mtDot(self, vecs: Sequence[Vec], out: ArrayScalar | None = None) -> ArrayScalar:
        """Compute Xᵀ·y with X an array of vectors.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Optional placeholder for the result.
        """
        ...

    def mtDotBegin(self, vecs: Sequence[Vec], out: ArrayScalar) -> None:
        """Start a split phase transpose multiple dot product computation.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Placeholder for the result.
        """
        ...

    def mtDotEnd(self, vecs: Sequence[Vec], out: ArrayScalar) -> ArrayScalar:
        """End a split phase transpose multiple dot product computation.

        Parameters
        ----------
        vecs
            Array of vectors.
        out
            Placeholder for the result.
        """
        ...

    def norm(self, norm_type: NormTypeSpec = None) -> float | tuple[float, float]:
        """Compute the vector norm.

        A 2-tuple is returned if NormType.NORM_1_AND_2 is specified.

        Parameters
        ----------
        norm_type
            The norm type.
        """
        ...

    def normBegin(self, norm_type: NormTypeSpec = None) -> None:
        """Begin computing the vector norm.

        Parameters
        ----------
        norm_type
            The norm type.
        """
        ...

    def normEnd(self, norm_type: NormTypeSpec = None) -> float | tuple[float, float]:
        """Finish computations initiated with normBegin.

        Parameters
        ----------
        norm_type
            The norm type.
        """
        ...

    def dotNorm2(self, vec: Vec) -> tuple[Scalar, float]:
        """Return the dot product with vec and its squared norm.

        Parameters
        ----------
        vec
            Vector to compute with.
        """
        ...

    def sum(self) -> Scalar:
        """Return the sum of all the entries of the vector."""
        ...

    def mean(self) -> Scalar:
        """Return the arithmetic mean of all the entries of the vector."""
        ...

    def min(self) -> tuple[int, float]:
        """Return the vector entry with minimum real part and its location.

        Returns
        -------
        p : int
            Location of the minimum value.
        val : float
            Minimum value.
        """
        ...

    def max(self) -> tuple[int, float]:
        """Return the vector entry with maximum real part and its location.

        Returns
        -------
        p : int
            Location of the maximum value.
        val : float
            Maximum value.
        """
        ...

    def normalize(self) -> float:
        """Normalize the vector by its 2-norm.

        Returns
        -------
        float
            The vector norm before normalization.
        """
        ...

    def reciprocal(self) -> None:
        """Replace each entry in the vector by its reciprocal."""
        ...

    def exp(self) -> None:
        """Replace each entry (xₙ) in the vector by exp(xₙ)."""
        ...

    def log(self) -> None:
        """Replace each entry in the vector by its natural logarithm."""
        ...

    def sqrtabs(self) -> None:
        """Replace each entry (xₙ) in the vector by √|xₙ|."""
        ...

    def abs(self) -> None:
        """Replace each entry (xₙ) in the vector by abs|xₙ|."""
        ...

    def conjugate(self) -> None:
        """Conjugate the vector."""
        ...

    def setRandom(self, random: Random | None = None) -> None:
        """Set all components of the vector to random numbers.

        Parameters
        ----------
        random
            Random number generator. If None then one will be created internally.
        """
        ...

    def permute(self, order: IS, invert: bool = False) -> None:
        """Permute the vector in-place with a provided ordering.

        Parameters
        ----------
        order
            Ordering for the permutation.
        invert
            Whether to invert the permutation.
        """
        ...

    def zeroEntries(self) -> None:
        """Set all entries in the vector to zero."""
        ...

    def set(self, alpha: Scalar) -> None:
        """Set all components of the vector to the same value.

        Parameters
        ----------
        alpha
            Value to set.
        """
        ...

    def isset(self, idx: IS, alpha: Scalar) -> None:
        """Set specific elements of the vector to the same value.

        Parameters
        ----------
        idx
            Index set specifying the vector entries to set.
        alpha
            Value to set the selected entries to.
        """
        ...

    def scale(self, alpha: Scalar) -> None:
        """Scale all entries of the vector.

        Parameters
        ----------
        alpha
            The scaling factor.
        """
        ...

    def shift(self, alpha: Scalar) -> None:
        """Shift all entries in the vector.

        Parameters
        ----------
        alpha
            The shift to apply to the vector values.
        """
        ...

    def swap(self, vec: Vec) -> None:
        """Swap the content of two vectors.

        Parameters
        ----------
        vec
            The vector to swap data with.
        """
        ...

    def axpy(self, alpha: Scalar, x: Vec) -> None:
        """Compute and store y = ɑ·x + y.

        Parameters
        ----------
        alpha
            Scale factor.
        x
            Input vector.
        """
        ...

    def isaxpy(self, idx: IS, alpha: Scalar, x: Vec) -> None:
        """Add a scaled reduced-space vector to a subset of the vector.

        Equivalent to y[idx[i]] += alpha*x[i].

        Parameters
        ----------
        idx
            Index set for the reduced space.
        alpha
            Scale factor.
        x
            Reduced-space vector.
        """
        ...

    def aypx(self, alpha: Scalar, x: Vec) -> None:
        """Compute and store y = x + ɑ·y.

        Parameters
        ----------
        alpha
            Scale factor.
        x
            Input vector.
        """
        ...

    def axpby(self, alpha: Scalar, beta: Scalar, x: Vec) -> None:
        """Compute and store y = ɑ·x + β·y.

        Parameters
        ----------
        alpha
            First scale factor.
        beta
            Second scale factor.
        x
            Input vector.
        """
        ...

    def waxpy(self, alpha: Scalar, x: Vec, y: Vec) -> None:
        """Compute and store w = ɑ·x + y.

        Parameters
        ----------
        alpha
            Scale factor.
        x
            First input vector.
        y
            Second input vector.
        """
        ...

    def maxpy(self, alphas: Sequence[Scalar], vecs: Sequence[Vec]) -> None:
        """Compute and store y = Σₙ(ɑₙ·Xₙ) + y with X an array of vectors.

        Parameters
        ----------
        alphas
            Array of scale factors.
        vecs
            Array of vectors.
        """
        ...

    def pointwiseMult(self, x: Vec, y: Vec) -> None:
        """Compute and store the component-wise multiplication of two vectors.

        Equivalent to w[i] = x[i] * y[i].

        Parameters
        ----------
        x, y
            Input vectors to multiply component-wise.
        """
        ...

    def pointwiseDivide(self, x: Vec, y: Vec) -> None:
        """Compute and store the component-wise division of two vectors.

        Equivalent to w[i] = x[i] / y[i].

        Parameters
        ----------
        x
            Numerator vector.
        y
            Denominator vector.
        """
        ...

    def pointwiseMin(self, x: Vec, y: Vec) -> None:
        """Compute and store the component-wise minimum of two vectors.

        Equivalent to w[i] = min(x[i], y[i]).

        Parameters
        ----------
        x, y
            Input vectors.
        """
        ...

    def pointwiseMax(self, x: Vec, y: Vec) -> None:
        """Compute and store the component-wise maximum of two vectors.

        Equivalent to w[i] = max(x[i], y[i]).

        Parameters
        ----------
        x, y
            Input vectors.
        """
        ...

    def pointwiseMaxAbs(self, x: Vec, y: Vec) -> None:
        """Compute and store the component-wise maximum absolute values.

        Equivalent to w[i] = max(abs(x[i]), abs(y[i])).

        Parameters
        ----------
        x, y
            Input vectors.
        """
        ...

    def maxPointwiseDivide(self, vec: Vec) -> float:
        """Return the maximum of the component-wise absolute value division.

        Equivalent to result = max_i abs(x[i] / y[i]).

        Parameters
        ----------
        vec
            Denominator vector.
        """
        ...

    def getValue(self, index: int) -> Scalar:
        """Return a single value from the vector.

        Parameters
        ----------
        index
            Location of the value to read.
        """
        ...

    def getValues(
        self, indices: Sequence[int], values: Sequence[Scalar] | None = None
    ) -> ArrayScalar:
        """Return values from certain locations in the vector.

        Parameters
        ----------
        indices
            Locations of the values to read.
        values
            Location to store the collected values.
        """
        ...

    def getValuesStagStencil(self, indices: Any, values: Any = None) -> None:
        """Not implemented."""
        ...

    def setValue(self, index: int, value: Scalar, addv: InsertModeSpec = None) -> None:
        """Insert or add a single value in the vector.

        Parameters
        ----------
        index
            Location to write to.
        value
            Value to insert at index.
        addv
            Insertion mode.
        """
        ...

    def setValues(
        self,
        indices: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None,
    ) -> None:
        """Insert or add multiple values in the vector.

        Parameters
        ----------
        indices
            Locations to write to.
        values
            Values to insert at indices.
        addv
            Insertion mode.
        """
        ...

    def setValuesBlocked(
        self,
        indices: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None,
    ) -> None:
        """Insert or add blocks of values in the vector.

        Parameters
        ----------
        indices
            Block indices to write to.
        values
            Values to insert at indices.
        addv
            Insertion mode.
        """
        ...

    def setValuesStagStencil(self, indices: Any, values: Any, addv: Any = None) -> None:
        """Not implemented."""
        ...

    def setLGMap(self, lgmap: LGMap) -> None:
        """Set the local-to-global mapping."""
        ...

    def getLGMap(self) -> LGMap:
        """Return the local-to-global mapping."""
        ...

    def setValueLocal(
        self, index: int, value: Scalar, addv: InsertModeSpec = None
    ) -> None:
        """Insert or add a single value in the vector using a local numbering.

        Parameters
        ----------
        index
            Location to write to.
        value
            Value to insert at index.
        addv
            Insertion mode.
        """
        ...

    def setValuesLocal(
        self,
        indices: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None,
    ) -> None:
        """Insert or add multiple values in the vector with a local numbering.

        Parameters
        ----------
        indices
            Locations to write to.
        values
            Values to insert at indices.
        addv
            Insertion mode.
        """
        ...

    def setValuesBlockedLocal(
        self,
        indices: Sequence[int],
        values: Sequence[Scalar],
        addv: InsertModeSpec = None,
    ) -> None:
        """Insert or add blocks of values in the vector with a local numbering.

        Parameters
        ----------
        indices
            Local block indices to write to.
        values
            Values to insert at indices.
        addv
            Insertion mode.
        """
        ...

    def assemblyBegin(self) -> None:
        """Begin an assembling stage of the vector."""
        ...

    def assemblyEnd(self) -> None:
        """Finish the assembling stage initiated with assemblyBegin."""
        ...

    def assemble(self) -> None:
        """Assemble the vector."""
        ...

    # Strided vector methods
    def strideScale(self, field: int, alpha: Scalar) -> None:
        """Scale a component of the vector.

        Parameters
        ----------
        field
            Component index. Must be between 0 and vec.block_size.
        alpha
            Factor to multiple the component entries by.
        """
        ...

    def strideSum(self, field: int) -> Scalar:
        """Sum subvector entries.

        Parameters
        ----------
        field
            Component index. Must be between 0 and vec.block_size.
        """
        ...

    def strideMin(self, field: int) -> tuple[int, float]:
        """Return the minimum of entries in a subvector.

        Parameters
        ----------
        field
            Component index. Must be between 0 and vec.block_size.

        Returns
        -------
        int
            Location of minimum.
        float
            Minimum value.
        """
        ...

    def strideMax(self, field: int) -> tuple[int, float]:
        """Return the maximum of entries in a subvector.

        Parameters
        ----------
        field
            Component index. Must be between 0 and vec.block_size.

        Returns
        -------
        int
            Location of maximum.
        float
            Maximum value.
        """
        ...

    def strideNorm(
        self, field: int, norm_type: NormTypeSpec = None
    ) -> float | tuple[float, float]:
        """Return the norm of entries in a subvector.

        Parameters
        ----------
        field
            Component index. Must be between 0 and vec.block_size.
        norm_type
            The norm type.
        """
        ...

    def strideScatter(self, field: int, vec: Vec, addv: InsertModeSpec = None) -> None:
        """Scatter entries into a component of another vector.

        Parameters
        ----------
        field
            Component index.
        vec
            Multi-component vector to be scattered into.
        addv
            Insertion mode.
        """
        ...

    def strideGather(self, field: int, vec: Vec, addv: InsertModeSpec = None) -> None:
        """Insert component values into a single-component vector.

        Parameters
        ----------
        field
            Component index.
        vec
            Single-component vector to be inserted into.
        addv
            Insertion mode.
        """
        ...

    # Ghost vector methods
    def localForm(self) -> Any:
        """Return a context manager for viewing ghost vectors in local form."""
        ...

    def ghostUpdateBegin(
        self, addv: InsertModeSpec = None, mode: ScatterModeSpec = None
    ) -> None:
        """Begin updating ghosted vector entries."""
        ...

    def ghostUpdateEnd(
        self, addv: InsertModeSpec = None, mode: ScatterModeSpec = None
    ) -> None:
        """Finish updating ghosted vector entries initiated with ghostUpdateBegin."""
        ...

    def ghostUpdate(
        self, addv: InsertModeSpec = None, mode: ScatterModeSpec = None
    ) -> None:
        """Update ghosted vector entries.

        Parameters
        ----------
        addv
            Insertion mode.
        mode
            Scatter mode.
        """
        ...

    def setMPIGhost(self, ghosts: Sequence[int]) -> None:
        """Set the ghost points for a ghosted vector.

        Parameters
        ----------
        ghosts
            Global indices of ghost points.
        """
        ...

    def getGhostIS(self) -> IS:
        """Return ghosting indices of a ghost vector."""
        ...

    def getSubVector(self, iset: IS, subvec: Vec | None = None) -> Vec:
        """Return a subvector from given indices.

        Parameters
        ----------
        iset
            Index set describing which indices to extract.
        subvec
            Subvector to copy entries into.
        """
        ...

    def restoreSubVector(self, iset: IS, subvec: Vec) -> None:
        """Restore a subvector extracted using getSubVector.

        Parameters
        ----------
        iset
            Index set describing the indices represented by the subvector.
        subvec
            Subvector to be restored.
        """
        ...

    def getNestSubVecs(self) -> list[Vec]:
        """Return all the vectors contained in the nested vector."""
        ...

    def setNestSubVecs(
        self, sx: Sequence[Vec], idxm: Sequence[int] | None = None
    ) -> None:
        """Set the component vectors at specified indices in the nested vector.

        Parameters
        ----------
        sx
            Array of component vectors.
        idxm
            Indices of the component vectors.
        """
        ...

    def setDM(self, dm: DM) -> None:
        """Associate a DM to the vector."""
        ...

    def getDM(self) -> DM:
        """Return the DM associated to the vector."""
        ...

    @classmethod
    def concatenate(cls, vecs: Sequence[Vec]) -> tuple[Vec, list[IS]]:
        """Concatenate vectors into a single vector.

        Parameters
        ----------
        vecs
            The vectors to be concatenated.

        Returns
        -------
        vector_out : Vec
            The concatenated vector.
        indices_list : list of IS
            A list of index sets corresponding to the concatenated components.
        """
        ...

    # Properties
    @property
    def sizes(self) -> tuple[int, int]:
        """The local and global vector sizes."""
        ...

    @sizes.setter
    def sizes(self, value: LayoutSizeSpec) -> None: ...
    @property
    def size(self) -> int:
        """The global vector size."""
        ...

    @property
    def local_size(self) -> int:
        """The local vector size."""
        ...

    @property
    def block_size(self) -> int:
        """The block size."""
        ...

    @property
    def owner_range(self) -> tuple[int, int]:
        """The locally owned range of indices in the form [low, high)."""
        ...

    @property
    def owner_ranges(self) -> ArrayInt:
        """The range of indices owned by each process."""
        ...

    @property
    def buffer_w(self) -> Any:
        """Writeable buffered view of the local portion of the vector."""
        ...

    @property
    def buffer_r(self) -> Any:
        """Read-only buffered view of the local portion of the vector."""
        ...

    @property
    def array_w(self) -> ArrayScalar:
        """Writeable ndarray containing the local portion of the vector."""
        ...

    @array_w.setter
    def array_w(self, value: Sequence[Scalar]) -> None: ...
    @property
    def array_r(self) -> ArrayScalar:
        """Read-only ndarray containing the local portion of the vector."""
        ...

    @property
    def buffer(self) -> Any:
        """Alias for buffer_w."""
        ...

    @property
    def array(self) -> ArrayScalar:
        """Alias for array_w."""
        ...

    @array.setter
    def array(self, value: Sequence[Scalar]) -> None: ...
