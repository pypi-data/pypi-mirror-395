"""Type stubs for PETSc KSP module."""


from typing import Any, Callable, overload, Self
from numpy import ndarray, dtype

from .Object import Object

from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .DM import DM
from .PC import PC

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    ArrayComplex,
    KSPRHSFunction,
    KSPOperatorsFunction,
    KSPConvergenceTestFunction,
    KSPMonitorFunction,
    KSPPreSolveFunction,
    KSPPostSolveFunction,
)

class KSPType:
    """KSP Type.

    The available types are various Krylov subspace methods.
    """

    RICHARDSON: str
    CHEBYSHEV: str
    CG: str
    GROPPCG: str
    PIPECG: str
    PIPECGRR: str
    PIPELCG: str
    PIPEPRCG: str
    PIPECG2: str
    CGNE: str
    NASH: str
    STCG: str
    GLTR: str
    FCG: str
    PIPEFCG: str
    GMRES: str
    PIPEFGMRES: str
    FGMRES: str
    LGMRES: str
    DGMRES: str
    PGMRES: str
    TCQMR: str
    BCGS: str
    IBCGS: str
    QMRCGS: str
    FBCGS: str
    FBCGSR: str
    BCGSL: str
    PIPEBCGS: str
    CGS: str
    TFQMR: str
    CR: str
    PIPECR: str
    LSQR: str
    PREONLY: str
    NONE: str
    QCG: str
    BICG: str
    MINRES: str
    SYMMLQ: str
    LCD: str
    PYTHON: str
    GCR: str
    PIPEGCR: str
    TSIRM: str
    CGLS: str
    FETIDP: str
    HPDDM: str

class KSPNormType:
    """KSP norm type.

    The available norm types are:
    - NONE: Skips computing the norm
    - PRECONDITIONED: Uses the l₂ norm of the preconditioned residual
    - UNPRECONDITIONED: Uses the l₂ norm of the true residual
    - NATURAL: Supported by CG, CR, CGNE, CGS
    """

    # native
    NORM_DEFAULT: int
    NORM_NONE: int
    NORM_PRECONDITIONED: int
    NORM_UNPRECONDITIONED: int
    NORM_NATURAL: int
    # aliases
    DEFAULT: int
    NONE: int
    NO: int
    PRECONDITIONED: int
    UNPRECONDITIONED: int
    NATURAL: int

class KSPConvergedReason:
    """KSP Converged Reason.

    Indicates whether the solver converged, is still iterating, or diverged.
    """

    # iterating
    CONVERGED_ITERATING: int
    ITERATING: int
    # converged
    CONVERGED_RTOL_NORMAL_EQUATIONS: int
    CONVERGED_ATOL_NORMAL_EQUATIONS: int
    CONVERGED_RTOL: int
    CONVERGED_ATOL: int
    CONVERGED_ITS: int
    CONVERGED_NEG_CURVE: int
    CONVERGED_STEP_LENGTH: int
    CONVERGED_HAPPY_BREAKDOWN: int
    # diverged
    DIVERGED_NULL: int
    DIVERGED_MAX_IT: int
    DIVERGED_DTOL: int
    DIVERGED_BREAKDOWN: int
    DIVERGED_BREAKDOWN_BICG: int
    DIVERGED_NONSYMMETRIC: int
    DIVERGED_INDEFINITE_PC: int
    DIVERGED_NANORINF: int
    DIVERGED_INDEFINITE_MAT: int
    DIVERGED_PCSETUP_FAILED: int

class KSPHPDDMType:
    """The HPDDM Krylov solver type."""

    GMRES: int
    BGMRES: int
    CG: int
    BCG: int
    GCRODR: int
    BGCRODR: int
    BFBCG: int
    PREONLY: int

class KSP(Object):
    """Abstract PETSc object that manages all Krylov methods.

    This is the object that manages the linear solves in PETSc (even
    those such as direct solvers that do no use Krylov accelerators).

    Notes
    -----
    When a direct solver is used, but no Krylov solver is used, the KSP
    object is still used but with a Type.PREONLY, meaning that
    only application of the preconditioner is used as the linear
    solver.
    """

    Type = KSPType
    NormType = KSPNormType
    ConvergedReason = KSPConvergedReason
    HPDDMType = KSPHPDDMType

    def __call__(self, b: Vec, x: Vec | None = None) -> Vec:
        """Solve linear system.

        Parameters
        ----------
        b
            Right hand side vector.
        x
            Solution vector.

        Returns
        -------
        Vec
            The solution vector.
        """
        ...

    # --- View and lifecycle ---

    def view(self, viewer: Viewer | None = None) -> None:
        """Print the KSP data structure.

        Parameters
        ----------
        viewer
            Viewer used to display the KSP.
        """
        ...

    def destroy(self) -> Self:
        """Destroy KSP context."""
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create the KSP context.

        Parameters
        ----------
        comm
            MPI communicator.
        """
        ...

    # --- Type and options ---

    def setType(self, ksp_type: KSPType | str) -> None:
        """Build the KSP data structure for a particular Type.

        Parameters
        ----------
        ksp_type
            KSP Type object.
        """
        ...

    def getType(self) -> str:
        """Return the KSP type as a string from the KSP object."""
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for all KSP options in the database.

        Parameters
        ----------
        prefix
            The options prefix.
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for all KSP options in the database."""
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to prefix used for all KSP options in the database.

        Parameters
        ----------
        prefix
            The options prefix to append.
        """
        ...

    def setFromOptions(self) -> None:
        """Set KSP options from the options database."""
        ...

    # --- Application context ---

    def setAppCtx(self, appctx: Any) -> None:
        """Set the optional user-defined context for the linear solver.

        Parameters
        ----------
        appctx
            The user defined context.
        """
        ...

    def getAppCtx(self) -> Any:
        """Return the user-defined context for the linear solver."""
        ...

    # --- DM ---

    def getDM(self) -> DM:
        """Return the DM that may be used by some preconditioners."""
        ...

    def setDM(self, dm: DM) -> None:
        """Set the DM that may be used by some preconditioners.

        Parameters
        ----------
        dm
            The DM object, cannot be None.
        """
        ...

    def setDMActive(self, flag: bool) -> None:
        """DM should be used to generate system matrix & RHS vector.

        Parameters
        ----------
        flag
            Whether to use the DM.
        """
        ...

    # --- Operators and preconditioner ---

    def setComputeRHS(
        self,
        rhs: KSPRHSFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set routine to compute the right-hand side of the linear system.

        Parameters
        ----------
        rhs
            Function which computes the right-hand side.
        args
            Positional arguments for callback function.
        kargs
            Keyword arguments for callback function.
        """
        ...

    def setComputeOperators(
        self,
        operators: KSPOperatorsFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set routine to compute the linear operators.

        Parameters
        ----------
        operators
            Function which computes the operators.
        args
            Positional arguments for callback function.
        kargs
            Keyword arguments for callback function.
        """
        ...

    def setOperators(self, A: Mat | None = None, P: Mat | None = None) -> None:
        """Set matrix associated with the linear system.

        Parameters
        ----------
        A
            Matrix that defines the linear system.
        P
            Matrix to be used in constructing the preconditioner,
            usually the same as A.
        """
        ...

    def getOperators(self) -> tuple[Mat, Mat]:
        """Return the matrix associated with the linear system.

        Returns
        -------
        A : Mat
            Matrix that defines the linear system.
        P : Mat
            Matrix to be used in constructing the preconditioner.
        """
        ...

    def setPC(self, pc: PC) -> None:
        """Set the preconditioner.

        Parameters
        ----------
        pc
            The preconditioner object.
        """
        ...

    def getPC(self) -> PC:
        """Return the preconditioner."""
        ...

    # --- Tolerances and convergence ---

    def setTolerances(
        self,
        rtol: float | None = None,
        atol: float | None = None,
        divtol: float | None = None,
        max_it: int | None = None,
    ) -> None:
        """Set various tolerances used by the KSP convergence testers.

        Parameters
        ----------
        rtol
            The relative convergence tolerance.
        atol
            The absolute convergence tolerance.
        divtol
            The divergence tolerance.
        max_it
            Maximum number of iterations to use.
        """
        ...

    def getTolerances(self) -> tuple[float, float, float, int]:
        """Return various tolerances used by the KSP convergence tests.

        Returns
        -------
        rtol : float
            The relative convergence tolerance.
        atol : float
            The absolute convergence tolerance.
        dtol : float
            The divergence tolerance.
        maxits : int
            Maximum number of iterations.
        """
        ...

    def setConvergenceTest(
        self,
        converged: KSPConvergenceTestFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function to be used to determine convergence.

        Parameters
        ----------
        converged
            Callback which computes the convergence.
        args
            Positional arguments for callback function.
        kargs
            Keyword arguments for callback function.
        """
        ...

    def addConvergenceTest(
        self,
        converged: KSPConvergenceTestFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
        prepend: bool = False,
    ) -> None:
        """Add the function to be used to determine convergence.

        Parameters
        ----------
        converged
            Callback which computes the convergence.
        args
            Positional arguments for callback function.
        kargs
            Keyword arguments for callback function.
        prepend
            Whether to prepend this call before the default convergence test.
        """
        ...

    def getConvergenceTest(self) -> KSPConvergenceTestFunction | None:
        """Return the function to be used to determine convergence."""
        ...

    def callConvergenceTest(self, its: int, rnorm: float) -> KSPConvergedReason:
        """Call the convergence test callback.

        Parameters
        ----------
        its
            Number of iterations.
        rnorm
            The residual norm.

        Returns
        -------
        KSPConvergedReason
            The converged reason.
        """
        ...

    def setConvergenceHistory(
        self, length: int | None = None, reset: bool = False
    ) -> None:
        """Set the array used to hold the residual history.

        Parameters
        ----------
        length
            Length of array to store history in.
        reset
            True indicates the history counter is reset to zero for each new solve.
        """
        ...

    def getConvergenceHistory(self) -> ArrayReal:
        """Return array containing the residual history."""
        ...

    def logConvergenceHistory(self, rnorm: float) -> None:
        """Add residual to convergence history.

        Parameters
        ----------
        rnorm
            Residual norm to be added to convergence history.
        """
        ...

    # --- Monitoring ---

    def setMonitor(
        self,
        monitor: KSPMonitorFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set additional function to monitor the residual.

        Parameters
        ----------
        monitor
            Callback which monitors the convergence.
        args
            Positional arguments for callback function.
        kargs
            Keyword arguments for callback function.
        """
        ...

    def getMonitor(
        self,
    ) -> list[tuple[KSPMonitorFunction, tuple[Any, ...], dict[str, Any]]] | None:
        """Return function used to monitor the residual."""
        ...

    def monitorCancel(self) -> None:
        """Clear all monitors for a KSP object."""
        ...

    cancelMonitor = monitorCancel

    def monitor(self, its: int, rnorm: float) -> None:
        """Run the user provided monitor routines, if they exist.

        Parameters
        ----------
        its
            The iteration number.
        rnorm
            The residual norm.
        """
        ...

    # --- Customization ---

    def setPCSide(self, side: PC.Side) -> None:
        """Set the preconditioning side.

        Parameters
        ----------
        side
            The preconditioning side.
        """
        ...

    def getPCSide(self) -> PC.Side:
        """Return the preconditioning side."""
        ...

    def setNormType(self, normtype: KSPNormType | int) -> None:
        """Set the norm that is used for convergence testing.

        Parameters
        ----------
        normtype
            The norm type to use.
        """
        ...

    def getNormType(self) -> KSPNormType:
        """Return the norm that is used for convergence testing."""
        ...

    def setComputeEigenvalues(self, flag: bool) -> None:
        """Set a flag to compute eigenvalues.

        Parameters
        ----------
        flag
            Boolean whether to compute eigenvalues (or not).
        """
        ...

    def getComputeEigenvalues(self) -> bool:
        """Return flag indicating whether eigenvalues will be calculated."""
        ...

    def setComputeSingularValues(self, flag: bool) -> None:
        """Set flag to calculate singular values.

        Parameters
        ----------
        flag
            Boolean whether to compute singular values (or not).
        """
        ...

    def getComputeSingularValues(self) -> bool:
        """Return flag indicating whether singular values will be calculated."""
        ...

    # --- Initial guess ---

    def setInitialGuessNonzero(self, flag: bool) -> None:
        """Tell the iterative solver that the initial guess is nonzero.

        Parameters
        ----------
        flag
            True indicates the guess is non-zero.
        """
        ...

    def getInitialGuessNonzero(self) -> bool:
        """Determine whether the KSP solver uses a zero initial guess."""
        ...

    def setInitialGuessKnoll(self, flag: bool) -> None:
        """Tell solver to use PC.apply to compute the initial guess.

        Parameters
        ----------
        flag
            True uses Knoll trick.
        """
        ...

    def getInitialGuessKnoll(self) -> bool:
        """Determine whether the KSP solver is using the Knoll trick."""
        ...

    def setUseFischerGuess(self, model: int, size: int) -> None:
        """Use the Paul Fischer algorithm to compute initial guesses.

        Parameters
        ----------
        model
            Use model 1, model 2, model 3, any other number to turn it off.
        size
            Size of subspace used to generate initial guess.
        """
        ...

    # --- Solving ---

    def setUp(self) -> None:
        """Set up internal data structures for an iterative solver."""
        ...

    def reset(self) -> None:
        """Resets a KSP context.

        Resets a KSP context to the kspsetupcalled = 0 state and
        removes any allocated Vecs and Mats.
        """
        ...

    def setUpOnBlocks(self) -> None:
        """Set up the preconditioner for each block in a block method.

        Methods include: block Jacobi, block Gauss-Seidel, and
        overlapping Schwarz methods.
        """
        ...

    def setPreSolve(
        self,
        presolve: KSPPreSolveFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function that is called at the beginning of each KSP.solve.

        Parameters
        ----------
        presolve
            The callback function.
        args
            Positional arguments for the callback function.
        kargs
            Keyword arguments for the callback function.
        """
        ...

    def setPostSolve(
        self,
        postsolve: KSPPostSolveFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function that is called at the end of each KSP.solve.

        Parameters
        ----------
        postsolve
            The callback function.
        args
            Positional arguments for the callback function.
        kargs
            Keyword arguments for the callback function.
        """
        ...

    def solve(self, b: Vec, x: Vec) -> None:
        """Solve the linear system.

        Parameters
        ----------
        b
            Right hand side vector.
        x
            Solution vector.
        """
        ...

    def solveTranspose(self, b: Vec, x: Vec) -> None:
        """Solve the transpose of a linear system.

        Parameters
        ----------
        b
            Right hand side vector.
        x
            Solution vector.
        """
        ...

    def matSolve(self, B: Mat, X: Mat) -> None:
        """Solve a linear system with multiple right-hand sides.

        Parameters
        ----------
        B
            Block of right-hand sides.
        X
            Block of solutions.
        """
        ...

    def matSolveTranspose(self, B: Mat, X: Mat) -> None:
        """Solve the transpose of a linear system with multiple RHS.

        Parameters
        ----------
        B
            Block of right-hand sides.
        X
            Block of solutions.
        """
        ...

    def setIterationNumber(self, its: int) -> None:
        """Set the iteration number (use `its` property)."""
        ...

    def getIterationNumber(self) -> int:
        """Return the iteration number (use `its` property)."""
        ...

    def setResidualNorm(self, rnorm: float) -> None:
        """Set the residual norm (use `norm` property)."""
        ...

    def getResidualNorm(self) -> float:
        """Return the residual norm (use `norm` property)."""
        ...

    def setConvergedReason(self, reason: KSPConvergedReason | int) -> None:
        """Set the converged reason (use `reason` property)."""
        ...

    def getConvergedReason(self) -> KSPConvergedReason:
        """Return the converged reason (use `reason` property)."""
        ...

    def getCGObjectiveValue(self) -> float:
        """Return the CG objective function value."""
        ...

    def setHPDDMType(self, hpddm_type: KSPHPDDMType | int) -> None:
        """Set the HPDDM Krylov solver type.

        Parameters
        ----------
        hpddm_type
            The type of Krylov solver to use.
        """
        ...

    def getHPDDMType(self) -> KSPHPDDMType:
        """Return the HPDDM Krylov solver type."""
        ...

    def setErrorIfNotConverged(self, flag: bool) -> None:
        """Cause solve to generate an error if not converged.

        Parameters
        ----------
        flag
            True enables this behavior.
        """
        ...

    def getErrorIfNotConverged(self) -> bool:
        """Return the flag indicating the solver will error if divergent."""
        ...

    def getRhs(self) -> Vec:
        """Return the right-hand side vector for the linear system."""
        ...

    def getSolution(self) -> Vec:
        """Return the solution for the linear system to be solved."""
        ...

    @overload
    def getWorkVecs(self, right: int, left: None = None) -> list[Vec]: ...
    @overload
    def getWorkVecs(self, right: None, left: int) -> list[Vec]: ...
    @overload
    def getWorkVecs(self, right: int, left: int) -> tuple[list[Vec], list[Vec]]: ...
    @overload
    def getWorkVecs(self, right: None = None, left: None = None) -> None: ...
    def buildSolution(self, x: Vec | None = None) -> Vec:
        """Return the solution vector.

        Parameters
        ----------
        x
            Optional vector to store the solution.
        """
        ...

    def buildResidual(self, r: Vec | None = None) -> Vec:
        """Return the residual of the linear system.

        Parameters
        ----------
        r
            Optional vector to use for the result.
        """
        ...

    def computeEigenvalues(self) -> ArrayComplex:
        """Compute the extreme eigenvalues for the preconditioned operator."""
        ...

    def computeExtremeSingularValues(self) -> tuple[float, float]:
        """Compute the extreme singular values for the preconditioned operator.

        Returns
        -------
        smax : float
            The maximum singular value.
        smin : float
            The minimum singular value.
        """
        ...

    # --- GMRES ---

    def setGMRESRestart(self, restart: int) -> None:
        """Set number of iterations at which KSP restarts.

        Parameters
        ----------
        restart
            Integer restart value.
        """
        ...

    # --- Python ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create a linear solver of Python type.

        Parameters
        ----------
        context
            An instance of the Python class implementing the required methods.
        comm
            MPI communicator.
        """
        ...

    def setPythonContext(self, context: Any | None = None) -> None:
        """Set the instance of the class implementing Python methods."""
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing Python methods."""
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used."""
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the solver."""
        ...

    # --- Properties ---

    @property
    def appctx(self) -> Any:
        """The solver application context."""
        ...

    @appctx.setter
    def appctx(self, value: Any) -> None: ...
    @property
    def dm(self) -> DM:
        """The solver DM."""
        ...

    @dm.setter
    def dm(self, value: DM) -> None: ...
    @property
    def vec_sol(self) -> Vec:
        """The solution vector."""
        ...

    @property
    def vec_rhs(self) -> Vec:
        """The right-hand side vector."""
        ...

    @property
    def mat_op(self) -> Mat:
        """The system matrix operator."""
        ...

    @property
    def mat_pc(self) -> Mat:
        """The preconditioner operator."""
        ...

    @property
    def guess_nonzero(self) -> bool:
        """Whether guess is non-zero."""
        ...

    @guess_nonzero.setter
    def guess_nonzero(self, value: bool) -> None: ...
    @property
    def guess_knoll(self) -> bool:
        """Whether solver uses Knoll trick."""
        ...

    @guess_knoll.setter
    def guess_knoll(self, value: bool) -> None: ...
    @property
    def pc(self) -> PC:
        """The PC of the solver."""
        ...

    @property
    def pc_side(self) -> PC.Side:
        """The side on which preconditioning is performed."""
        ...

    @pc_side.setter
    def pc_side(self, value: PC.Side) -> None: ...
    @property
    def norm_type(self) -> KSPNormType:
        """The norm used by the solver."""
        ...

    @norm_type.setter
    def norm_type(self, value: KSPNormType | int) -> None: ...
    @property
    def rtol(self) -> float:
        """The relative tolerance of the solver."""
        ...

    @rtol.setter
    def rtol(self, value: float) -> None: ...
    @property
    def atol(self) -> float:
        """The absolute tolerance of the solver."""
        ...

    @atol.setter
    def atol(self, value: float) -> None: ...
    @property
    def divtol(self) -> float:
        """The divergence tolerance of the solver."""
        ...

    @divtol.setter
    def divtol(self, value: float) -> None: ...
    @property
    def max_it(self) -> int:
        """The maximum number of iteration the solver may take."""
        ...

    @max_it.setter
    def max_it(self, value: int) -> None: ...
    @property
    def its(self) -> int:
        """The current number of iterations the solver has taken."""
        ...

    @its.setter
    def its(self, value: int) -> None: ...
    @property
    def norm(self) -> float:
        """The norm of the residual at the current iteration."""
        ...

    @norm.setter
    def norm(self, value: float) -> None: ...
    @property
    def history(self) -> ArrayReal:
        """The convergence history of the solver."""
        ...

    @property
    def reason(self) -> KSPConvergedReason:
        """The converged reason."""
        ...

    @reason.setter
    def reason(self, value: KSPConvergedReason | int) -> None: ...
    @property
    def is_iterating(self) -> bool:
        """Boolean indicating if the solver has not converged yet."""
        ...

    @property
    def is_converged(self) -> bool:
        """Boolean indicating if the solver has converged."""
        ...

    @property
    def is_diverged(self) -> bool:
        """Boolean indicating if the solver has failed."""
        ...
