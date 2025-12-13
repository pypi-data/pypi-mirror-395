"""Type stubs for PETSc SNES module."""


from typing import (
    Any,
    Callable,
    Literal,
    Sequence,
    Self,
)
from numpy import ndarray, dtype

from .Object import Object

from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .DM import DM, Section
from .KSP import KSP
from .PC import PC
from .IS import IS

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    SNESGuessFunction,
    SNESFunction,
    SNESUpdateFunction,
    SNESJacobianFunction,
    SNESObjFunction,
    SNESNGSFunction,
    SNESConvergedFunction,
    SNESMonitorFunction,
    SNESLSPreFunction,
)

class SNESType:
    """SNES solver type.

    The available types are various nonlinear solvers.
    """

    NEWTONLS: str
    NEWTONTR: str
    NEWTONAL: str
    PYTHON: str
    NRICHARDSON: str
    KSPONLY: str
    KSPTRANSPOSEONLY: str
    VINEWTONRSLS: str
    VINEWTONSSLS: str
    NGMRES: str
    QN: str
    SHELL: str
    NGS: str
    NCG: str
    FAS: str
    MS: str
    NASM: str
    ANDERSON: str
    ASPIN: str
    COMPOSITE: str
    PATCH: str

class SNESNormSchedule:
    """SNES norm schedule.

    Determines how the residual norm is computed.
    """

    # native
    NORM_DEFAULT: int
    NORM_NONE: int
    NORM_ALWAYS: int
    NORM_INITIAL_ONLY: int
    NORM_FINAL_ONLY: int
    NORM_INITIAL_FINAL_ONLY: int
    # aliases
    DEFAULT: int
    NONE: int
    ALWAYS: int
    INITIAL_ONLY: int
    FINAL_ONLY: int
    INITIAL_FINAL_ONLY: int

class SNESConvergedReason:
    """SNES solver termination reason.

    Indicates whether the solver converged, is still iterating, or diverged.
    """

    # iterating
    CONVERGED_ITERATING: int
    ITERATING: int
    # converged
    CONVERGED_FNORM_ABS: int
    CONVERGED_FNORM_RELATIVE: int
    CONVERGED_SNORM_RELATIVE: int
    CONVERGED_ITS: int
    # diverged
    DIVERGED_FUNCTION_DOMAIN: int
    DIVERGED_FUNCTION_COUNT: int
    DIVERGED_LINEAR_SOLVE: int
    DIVERGED_FNORM_NAN: int
    DIVERGED_MAX_IT: int
    DIVERGED_LINE_SEARCH: int
    DIVERGED_INNER: int
    DIVERGED_LOCAL_MIN: int
    DIVERGED_DTOL: int
    DIVERGED_JACOBIAN_DOMAIN: int
    DIVERGED_TR_DELTA: int

class SNESNewtonALCorrectionType:
    """SNESNEWTONAL correction type."""

    EXACT: int
    NORMAL: int

class SNESLineSearchType:
    """SNES linesearch type."""

    BT: str
    NLEQERR: str
    BASIC: str
    NONE: str
    SECANT: str
    CP: str
    SHELL: str
    NCGLINEAR: str
    BISECTION: str

class SNESLineSearch(Object):
    """Linesearch object used by SNES solvers."""

    Type = SNESLineSearchType

    def create(self, comm: Comm | None = None) -> Self:
        """Create a new linesearch object.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the linesearch from the options database."""
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View the linesearch object.

        Parameters
        ----------
        viewer
            A Viewer instance or None for the default viewer.
        """
        ...

    def getType(self) -> str:
        """Return the type of the linesearch."""
        ...

    def setType(self, ls_type: Type | str) -> None:
        """Set the type of the linesearch.

        Parameters
        ----------
        ls_type
            The linesearch type.
        """
        ...

    def getTolerances(self) -> tuple[float, float, float, float, float, int]:
        """Return the tolerance parameters used in the linesearch.

        Returns
        -------
        minstep : float
            Minimum step length.
        maxstep : float
            Maximum step length.
        rtol : float
            Relative tolerance.
        atol : float
            Absolute tolerance.
        ltol : float
            Lambda tolerance.
        max_its : int
            Maximum number of iterations for the linesearch.
        """
        ...

    def setTolerances(
        self,
        minstep: float | None = None,
        maxstep: float | None = None,
        rtol: float | None = None,
        atol: float | None = None,
        ltol: float | None = None,
        max_its: int | None = None,
    ) -> None:
        """Set the tolerance parameters used in the linesearch.

        Parameters
        ----------
        minstep
            Minimum step length.
        maxstep
            Maximum step length.
        rtol
            Relative tolerance.
        atol
            Absolute tolerance.
        ltol
            Lambda tolerance.
        max_its
            Maximum number of iterations for the linesearch.
        """
        ...

    def getOrder(self) -> int:
        """Return the order of the linesearch."""
        ...

    def setOrder(self, order: int) -> None:
        """Set the order of the linesearch.

        Parameters
        ----------
        order
            The linesearch order.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the linesearch object."""
        ...

class SNES(Object):
    """Nonlinear equations solver.

    SNES is described in the PETSc manual.
    """

    Type = SNESType
    NormSchedule = SNESNormSchedule
    ConvergedReason = SNESConvergedReason
    NewtonALCorrectionType = SNESNewtonALCorrectionType

    # --- View and lifecycle ---

    def view(self, viewer: Viewer | None = None) -> None:
        """View the solver.

        Parameters
        ----------
        viewer
            A Viewer instance or None for the default viewer.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the solver."""
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a SNES solver.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    # --- Type and options ---

    def setType(self, snes_type: Type | str) -> None:
        """Set the type of the solver.

        Parameters
        ----------
        snes_type
            The type of the solver.
        """
        ...

    def getType(self) -> str:
        """Return the type of the solver."""
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for searching for options in the database.

        Parameters
        ----------
        prefix
            The prefix to prepend to all option names.
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database."""
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for searching for options in the database.

        Parameters
        ----------
        prefix
            The prefix to append.
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the solver from the options database."""
        ...

    # --- Application context ---

    def setApplicationContext(self, appctx: Any) -> None:
        """Set the application context.

        Parameters
        ----------
        appctx
            The application context.
        """
        ...

    def getApplicationContext(self) -> Any:
        """Return the application context."""
        ...

    # Backward compatibility
    setAppCtx = setApplicationContext
    getAppCtx = getApplicationContext

    # --- DM ---

    def getDM(self) -> DM:
        """Return the DM associated with the solver."""
        ...

    def setDM(self, dm: DM) -> None:
        """Associate a DM with the solver.

        Parameters
        ----------
        dm
            The DM object.
        """
        ...

    # --- Trust Region (TR) ---

    def setTRTolerances(
        self,
        delta_min: float | None = None,
        delta_max: float | None = None,
        delta_0: float | None = None,
    ) -> None:
        """Set the tolerance parameters used for the trust region.

        Parameters
        ----------
        delta_min
            The minimum allowed trust region size.
        delta_max
            The maximum allowed trust region size.
        delta_0
            The initial trust region size.
        """
        ...

    def getTRTolerances(self) -> tuple[float, float, float]:
        """Return the tolerance parameters used for the trust region.

        Returns
        -------
        delta_min : float
            The minimum allowed trust region size.
        delta_max : float
            The maximum allowed trust region size.
        delta_0 : float
            The initial trust region size.
        """
        ...

    def setTRUpdateParameters(
        self,
        eta1: float | None = None,
        eta2: float | None = None,
        eta3: float | None = None,
        t1: float | None = None,
        t2: float | None = None,
    ) -> None:
        """Set the update parameters used for the trust region.

        Parameters
        ----------
        eta1
            The step acceptance tolerance.
        eta2
            The shrinking tolerance.
        eta3
            The enlarging tolerance.
        t1
            The shrinking factor.
        t2
            The enlarging factor.
        """
        ...

    def getTRUpdateParameters(self) -> tuple[float, float, float, float, float]:
        """Return the update parameters used for the trust region.

        Returns
        -------
        eta1 : float
            The step acceptance tolerance.
        eta2 : float
            The shrinking tolerance.
        eta3 : float
            The enlarging tolerance.
        t1 : float
            The shrinking factor.
        t2 : float
            The enlarging factor.
        """
        ...

    # --- FAS (Full Approximation Scheme) ---

    def setFASInterpolation(self, level: int, mat: Mat) -> None:
        """Set the Mat to be used to apply the interpolation from level-1 to level.

        Parameters
        ----------
        level
            The level.
        mat
            The interpolation matrix.
        """
        ...

    def getFASInterpolation(self, level: int) -> Mat:
        """Return the Mat used to apply the interpolation from level-1 to level.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def setFASRestriction(self, level: int, mat: Mat) -> None:
        """Set the Mat to be used to apply the restriction from level-1 to level.

        Parameters
        ----------
        level
            The level.
        mat
            The restriction matrix.
        """
        ...

    def getFASRestriction(self, level: int) -> Mat:
        """Return the Mat used to apply the restriction from level-1 to level.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def setFASInjection(self, level: int, mat: Mat) -> None:
        """Set the Mat to be used to apply the injection from level-1 to level.

        Parameters
        ----------
        level
            The level.
        mat
            The injection matrix.
        """
        ...

    def getFASInjection(self, level: int) -> Mat:
        """Return the Mat used to apply the injection from level-1 to level.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def setFASRScale(self, level: int, vec: Vec) -> None:
        """Set the scaling factor of the restriction operator from level to level-1.

        Parameters
        ----------
        level
            The level.
        vec
            The scaling vector.
        """
        ...

    def setFASLevels(self, levels: int, comms: Sequence[Comm] | None = None) -> None:
        """Set the number of levels to use with FAS.

        Parameters
        ----------
        levels
            The number of levels.
        comms
            An optional sequence of communicators of length levels.
        """
        ...

    def getFASLevels(self) -> int:
        """Return the number of levels used."""
        ...

    def getFASCycleSNES(self, level: int) -> SNES:
        """Return the SNES corresponding to a particular level of the FAS hierarchy.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def getFASCoarseSolve(self) -> SNES:
        """Return the SNES used at the coarsest level of the FAS hierarchy."""
        ...

    def getFASSmoother(self, level: int) -> SNES:
        """Return the smoother used at a given level of the FAS hierarchy.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def getFASSmootherDown(self, level: int) -> SNES:
        """Return the downsmoother used at a given level of the FAS hierarchy.

        Parameters
        ----------
        level
            The level.
        """
        ...

    def getFASSmootherUp(self, level: int) -> SNES:
        """Return the upsmoother used at a given level of the FAS hierarchy.

        Parameters
        ----------
        level
            The level.
        """
        ...

    # --- Nonlinear preconditioner ---

    def getNPC(self) -> SNES:
        """Return the nonlinear preconditioner associated with the solver."""
        ...

    def hasNPC(self) -> bool:
        """Return a boolean indicating whether the solver has a nonlinear preconditioner."""
        ...

    def setNPC(self, snes: SNES) -> None:
        """Set the nonlinear preconditioner.

        Parameters
        ----------
        snes
            The nonlinear preconditioner.
        """
        ...

    def setNPCSide(self, side: PC.Side) -> None:
        """Set the nonlinear preconditioning side.

        Parameters
        ----------
        side
            The preconditioning side.
        """
        ...

    def getNPCSide(self) -> PC.Side:
        """Return the nonlinear preconditioning side."""
        ...

    # --- Callback functions ---

    def setLineSearchPreCheck(
        self,
        precheck: SNESLSPreFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback that will be called before applying the linesearch.

        Parameters
        ----------
        precheck
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def setInitialGuess(
        self,
        initialguess: SNESGuessFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the initial guess.

        Parameters
        ----------
        initialguess
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getInitialGuess(self) -> SNESGuessFunction:
        """Return the callback to compute the initial guess."""
        ...

    def setFunction(
        self,
        function: SNESFunction | None,
        f: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the nonlinear function.

        Parameters
        ----------
        function
            The callback.
        f
            An optional vector to store the result.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getFunction(self) -> tuple[Vec, SNESFunction | None]:
        """Return the callback to compute the nonlinear function.

        Returns
        -------
        f : Vec
            The function vector.
        function : SNESFunction | None
            The callback tuple or None.
        """
        ...

    def setUpdate(
        self,
        update: SNESUpdateFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute update at the beginning of each step.

        Parameters
        ----------
        update
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getUpdate(self) -> SNESUpdateFunction:
        """Return the callback to compute the update at the beginning of each step."""
        ...

    def setJacobian(
        self,
        jacobian: SNESJacobianFunction | None,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the Jacobian.

        Parameters
        ----------
        jacobian
            The Jacobian callback.
        J
            The matrix to store the Jacobian.
        P
            The matrix to construct the preconditioner.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getJacobian(self) -> tuple[Mat, Mat, SNESJacobianFunction]:
        """Return the matrices used to compute the Jacobian and the callback tuple.

        Returns
        -------
        J : Mat
            The matrix to store the Jacobian.
        P : Mat
            The matrix to construct the preconditioner.
        callback : SNESJacobianFunction
            Callback, positional and keyword arguments.
        """
        ...

    def setObjective(
        self,
        objective: SNESObjFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the objective function.

        Parameters
        ----------
        objective
            The objective callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getObjective(self) -> SNESObjFunction:
        """Return the objective callback tuple."""
        ...

    def computeFunction(self, x: Vec, f: Vec) -> None:
        """Compute the function.

        Parameters
        ----------
        x
            The input state vector.
        f
            The output vector.
        """
        ...

    def computeJacobian(self, x: Vec, J: Mat, P: Mat | None = None) -> None:
        """Compute the Jacobian.

        Parameters
        ----------
        x
            The input state vector.
        J
            The output Jacobian matrix.
        P
            The output Jacobian matrix used to construct the preconditioner.
        """
        ...

    def computeObjective(self, x: Vec) -> float:
        """Compute the value of the objective function.

        Parameters
        ----------
        x
            The input state vector.
        """
        ...

    def setNGS(
        self,
        ngs: SNESNGSFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute nonlinear Gauss-Seidel.

        Parameters
        ----------
        ngs
            The nonlinear Gauss-Seidel callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getNGS(self) -> SNESNGSFunction:
        """Return the nonlinear Gauss-Seidel callback tuple."""
        ...

    def computeNGS(self, x: Vec, b: Vec | None = None) -> None:
        """Compute a nonlinear Gauss-Seidel step.

        Parameters
        ----------
        x
            The input/output state vector.
        b
            The input right-hand side vector.
        """
        ...

    # --- Tolerances and convergence ---

    def setTolerances(
        self,
        rtol: float | None = None,
        atol: float | None = None,
        stol: float | None = None,
        max_it: int | None = None,
    ) -> None:
        """Set the tolerance parameters used in the solver convergence tests.

        Parameters
        ----------
        rtol
            The relative norm of the residual.
        atol
            The absolute norm of the residual.
        stol
            The absolute norm of the step.
        max_it
            The maximum allowed number of iterations.
        """
        ...

    def getTolerances(self) -> tuple[float, float, float, int]:
        """Return the tolerance parameters used in the solver convergence tests.

        Returns
        -------
        rtol : float
            The relative norm of the residual.
        atol : float
            The absolute norm of the residual.
        stol : float
            The absolute norm of the step.
        max_it : int
            The maximum allowed number of iterations.
        """
        ...

    def setDivergenceTolerance(self, dtol: float) -> None:
        """Set the divergence tolerance parameter used in the convergence tests.

        Parameters
        ----------
        dtol
            The divergence tolerance.
        """
        ...

    def getDivergenceTolerance(self) -> float:
        """Get the divergence tolerance parameter used in the convergence tests."""
        ...

    def setNormSchedule(self, normsched: NormSchedule) -> None:
        """Set the norm schedule.

        Parameters
        ----------
        normsched
            The norm schedule.
        """
        ...

    def getNormSchedule(self) -> NormSchedule:
        """Return the norm schedule."""
        ...

    def setConvergenceTest(
        self,
        converged: SNESConvergedFunction | Literal["skip", "default"],
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to use as convergence test.

        Parameters
        ----------
        converged
            The convergence testing callback or "skip"/"default".
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getConvergenceTest(self) -> SNESConvergedFunction:
        """Return the callback to used as convergence test."""
        ...

    def callConvergenceTest(
        self, its: int, xnorm: float, ynorm: float, fnorm: float
    ) -> ConvergedReason:
        """Compute the convergence test.

        Parameters
        ----------
        its
            Iteration number.
        xnorm
            Solution norm.
        ynorm
            Update norm.
        fnorm
            Function norm.
        """
        ...

    def converged(self, its: int, xnorm: float, ynorm: float, fnorm: float) -> None:
        """Compute the convergence test and update the solver converged reason.

        Parameters
        ----------
        its
            Iteration number.
        xnorm
            Solution norm.
        ynorm
            Update norm.
        fnorm
            Function norm.
        """
        ...

    def setConvergenceHistory(
        self, length: int | bool | None = None, reset: bool = False
    ) -> None:
        """Set the convergence history.

        Parameters
        ----------
        length
            The length of the history array.
        reset
            Whether to reset the history on each solve.
        """
        ...

    def getConvergenceHistory(self) -> tuple[ArrayReal, ArrayInt]:
        """Return the convergence history."""
        ...

    def logConvergenceHistory(self, norm: float, linear_its: int = 0) -> None:
        """Log residual norm and linear iterations.

        Parameters
        ----------
        norm
            The residual norm.
        linear_its
            The number of linear iterations.
        """
        ...

    def setResetCounters(self, reset: bool = True) -> None:
        """Set the flag to reset the counters.

        Parameters
        ----------
        reset
            Whether to reset counters.
        """
        ...

    # --- Monitoring ---

    def setMonitor(
        self,
        monitor: SNESMonitorFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback used to monitor solver convergence.

        Parameters
        ----------
        monitor
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getMonitor(
        self,
    ) -> list[tuple[SNESMonitorFunction, tuple[Any, ...], dict[str, Any]]]:
        """Return the callback used to monitor solver convergence."""
        ...

    def monitorCancel(self) -> None:
        """Cancel all the monitors of the solver."""
        ...

    cancelMonitor = monitorCancel

    def monitor(self, its: int, rnorm: float) -> None:
        """Monitor the solver.

        Parameters
        ----------
        its
            Current number of iterations.
        rnorm
            Current value of the residual norm.
        """
        ...

    # --- Function evaluations and failures ---

    def setMaxFunctionEvaluations(self, max_funcs: int) -> None:
        """Set the maximum allowed number of function evaluations.

        Parameters
        ----------
        max_funcs
            Maximum number of function evaluations.
        """
        ...

    def getMaxFunctionEvaluations(self) -> int:
        """Return the maximum allowed number of function evaluations."""
        ...

    def getFunctionEvaluations(self) -> int:
        """Return the current number of function evaluations."""
        ...

    def setMaxStepFailures(self, max_fails: int) -> None:
        """Set the maximum allowed number of step failures.

        Parameters
        ----------
        max_fails
            Maximum number of step failures.
        """
        ...

    def getMaxStepFailures(self) -> int:
        """Return the maximum allowed number of step failures."""
        ...

    def getStepFailures(self) -> int:
        """Return the current number of step failures."""
        ...

    def setMaxKSPFailures(self, max_fails: int) -> None:
        """Set the maximum allowed number of linear solve failures.

        Parameters
        ----------
        max_fails
            Maximum number of linear solve failures.
        """
        ...

    def getMaxKSPFailures(self) -> int:
        """Return the maximum allowed number of linear solve failures."""
        ...

    def getKSPFailures(self) -> int:
        """Return the current number of linear solve failures."""
        ...

    # Backward compatibility aliases
    setMaxNonlinearStepFailures = setMaxStepFailures
    getMaxNonlinearStepFailures = getMaxStepFailures
    getNonlinearStepFailures = getStepFailures
    setMaxLinearSolveFailures = setMaxKSPFailures
    getMaxLinearSolveFailures = getMaxKSPFailures
    getLinearSolveFailures = getKSPFailures

    # --- Solving ---

    def setUp(self) -> None:
        """Set up the internal data structures for using the solver."""
        ...

    def setUpMatrices(self) -> None:
        """Ensures that matrices are available for Newton-like methods."""
        ...

    def reset(self) -> None:
        """Reset the solver."""
        ...

    def solve(self, b: Vec | None = None, x: Vec | None = None) -> None:
        """Solve the nonlinear equations.

        Parameters
        ----------
        b
            The affine right-hand side or None to use zero.
        x
            The starting vector or None to use the vector stored internally.
        """
        ...

    def setConvergedReason(self, reason: ConvergedReason) -> None:
        """Set the termination flag.

        Parameters
        ----------
        reason
            The convergence reason.
        """
        ...

    def getConvergedReason(self) -> ConvergedReason:
        """Return the termination flag."""
        ...

    def setErrorIfNotConverged(self, flag: bool) -> None:
        """Immediately generate an error if the solver has not converged.

        Parameters
        ----------
        flag
            Whether to error on divergence.
        """
        ...

    def getErrorIfNotConverged(self) -> bool:
        """Return the flag indicating error on divergence."""
        ...

    def setIterationNumber(self, its: int) -> None:
        """Set the current iteration number.

        Parameters
        ----------
        its
            The iteration number.
        """
        ...

    def getIterationNumber(self) -> int:
        """Return the current iteration number."""
        ...

    def setForceIteration(self, force: bool) -> None:
        """Force solve to take at least one iteration.

        Parameters
        ----------
        force
            Whether to force at least one iteration.
        """
        ...

    def setFunctionNorm(self, norm: float) -> None:
        """Set the function norm value.

        Parameters
        ----------
        norm
            The function norm.
        """
        ...

    def getFunctionNorm(self) -> float:
        """Return the function norm."""
        ...

    def getLinearSolveIterations(self) -> int:
        """Return the total number of linear iterations."""
        ...

    def getRhs(self) -> Vec:
        """Return the vector holding the right-hand side."""
        ...

    def getSolution(self) -> Vec:
        """Return the vector holding the solution."""
        ...

    def setSolution(self, vec: Vec) -> None:
        """Set the vector used to store the solution.

        Parameters
        ----------
        vec
            The solution vector.
        """
        ...

    def getSolutionUpdate(self) -> Vec:
        """Return the vector holding the solution update."""
        ...

    # --- Linear solver ---

    def setKSP(self, ksp: KSP) -> None:
        """Set the linear solver that will be used by the nonlinear solver.

        Parameters
        ----------
        ksp
            The linear solver.
        """
        ...

    def getKSP(self) -> KSP:
        """Return the linear solver used by the nonlinear solver."""
        ...

    def setUseEW(self, flag: bool = True, *targs: Any, **kargs: Any) -> None:
        """Tell the solver to use the Eisenstat-Walker trick.

        Parameters
        ----------
        flag
            Whether or not to use the Eisenstat-Walker trick.
        *targs
            Positional arguments for setParamsEW.
        **kargs
            Keyword arguments for setParamsEW.
        """
        ...

    def getUseEW(self) -> bool:
        """Return the flag indicating if the solver uses the Eisenstat-Walker trick."""
        ...

    def setParamsEW(
        self,
        version: int | None = None,
        rtol_0: float | None = None,
        rtol_max: float | None = None,
        gamma: float | None = None,
        alpha: float | None = None,
        alpha2: float | None = None,
        threshold: float | None = None,
    ) -> None:
        """Set the parameters for the Eisenstat and Walker trick.

        Parameters
        ----------
        version
            The version of the algorithm.
        rtol_0
            The initial relative residual norm.
        rtol_max
            The maximum relative residual norm.
        gamma
            Parameter.
        alpha
            Parameter.
        alpha2
            Parameter.
        threshold
            Parameter.
        """
        ...

    def getParamsEW(self) -> dict[str, int | float]:
        """Get the parameters of the Eisenstat and Walker trick."""
        ...

    def setUseKSP(self, flag: bool = True) -> None:
        """Set the boolean flag indicating to use a linear solver.

        Parameters
        ----------
        flag
            Whether to use a linear solver.
        """
        ...

    def getUseKSP(self) -> bool:
        """Return the flag indicating if the solver uses a linear solver."""
        ...

    # --- Matrix-free / finite differences ---

    def setUseMF(self, flag: bool = True) -> None:
        """Set the boolean flag indicating to use matrix-free finite-differencing.

        Parameters
        ----------
        flag
            Whether to use matrix-free finite-differencing.
        """
        ...

    def getUseMF(self) -> bool:
        """Return the flag indicating if the solver uses matrix-free finite-differencing."""
        ...

    def setUseFD(self, flag: bool = True) -> None:
        """Set the boolean flag to use coloring finite-differencing for Jacobian assembly.

        Parameters
        ----------
        flag
            Whether to use coloring finite-differencing.
        """
        ...

    def getUseFD(self) -> bool:
        """Return true if the solver uses color finite-differencing for the Jacobian."""
        ...

    # --- Variational Inequality (VI) ---

    def setVariableBounds(self, xl: Vec, xu: Vec) -> None:
        """Set the vector for the variable bounds.

        Parameters
        ----------
        xl
            Lower bound vector.
        xu
            Upper bound vector.
        """
        ...

    def getVariableBounds(self) -> tuple[Vec, Vec]:
        """Get the vectors for the variable bounds."""
        ...

    def getVIInactiveSet(self) -> IS:
        """Return the index set for the inactive set."""
        ...

    # --- Python ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create a nonlinear solver of Python type.

        Parameters
        ----------
        context
            An instance of the Python class implementing the required methods.
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def setPythonContext(self, context: Any) -> None:
        """Set the instance of the class implementing the required Python methods.

        Parameters
        ----------
        context
            The Python context object.
        """
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing the required Python methods."""
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used.

        Parameters
        ----------
        py_type
            The fully qualified Python name.
        """
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the solver."""
        ...

    # --- Composite ---

    def getCompositeSNES(self, n: int) -> SNES:
        """Return the n-th solver in the composite.

        Parameters
        ----------
        n
            The index of the solver.
        """
        ...

    def getCompositeNumber(self) -> int:
        """Return the number of solvers in the composite."""
        ...

    # --- NASM ---

    def getNASMSNES(self, n: int) -> SNES:
        """Return the n-th solver in NASM.

        Parameters
        ----------
        n
            The index of the solver.
        """
        ...

    def getNASMNumber(self) -> int:
        """Return the number of solvers in NASM."""
        ...

    # --- Patch ---

    def setPatchCellNumbering(self, sec: Section) -> None:
        """Set cell patch numbering.

        Parameters
        ----------
        sec
            The section.
        """
        ...

    def setPatchDiscretisationInfo(
        self,
        dms: Sequence[DM],
        bs: Sequence[int],
        cellNodeMaps: Sequence[Any],
        subspaceOffsets: Sequence[int],
        ghostBcNodes: Sequence[int],
        globalBcNodes: Sequence[int],
    ) -> None:
        """Set patch discretisation information.

        Parameters
        ----------
        dms
            The DM objects.
        bs
            Block sizes.
        cellNodeMaps
            Cell node maps.
        subspaceOffsets
            Subspace offsets.
        ghostBcNodes
            Ghost boundary condition nodes.
        globalBcNodes
            Global boundary condition nodes.
        """
        ...

    def setPatchComputeOperator(
        self,
        operator: Any,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set patch compute operator.

        Parameters
        ----------
        operator
            The operator callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def setPatchComputeFunction(
        self,
        function: Any,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set patch compute function.

        Parameters
        ----------
        function
            The function callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def setPatchConstructType(
        self,
        typ: PC.PatchConstructType,
        operator: Any | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set patch construct type.

        Parameters
        ----------
        typ
            The patch construction type.
        operator
            The operator callback (required for USER or PYTHON type).
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    # --- LineSearch ---

    def getLineSearch(self) -> SNESLineSearch:
        """Return the linesearch object associated with this SNES."""
        ...

    def setLineSearch(self, linesearch: SNESLineSearch) -> None:
        """Set the linesearch object to be used by this SNES.

        Parameters
        ----------
        linesearch
            The linesearch object.
        """
        ...

    # --- NewtonAL methods ---

    def setNewtonALFunction(
        self,
        function: SNESFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the tangent load vector for SNESNEWTONAL.

        Parameters
        ----------
        function
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.
        """
        ...

    def getNewtonALLoadParameter(self) -> float:
        """Return the load parameter for SNESNEWTONAL."""
        ...

    def setNewtonALCorrectionType(self, corrtype: NewtonALCorrectionType) -> None:
        """Set the correction type for SNESNEWTONAL.

        Parameters
        ----------
        corrtype
            The correction type.
        """
        ...

    # --- Properties ---

    @property
    def appctx(self) -> Any:
        """Application context."""
        ...

    @appctx.setter
    def appctx(self, value: Any) -> None: ...
    @property
    def dm(self) -> DM:
        """DM."""
        ...

    @dm.setter
    def dm(self, value: DM) -> None: ...
    @property
    def npc(self) -> SNES:
        """Nonlinear preconditioner."""
        ...

    @npc.setter
    def npc(self, value: SNES) -> None: ...
    @property
    def vec_sol(self) -> Vec:
        """Solution vector."""
        ...

    @property
    def vec_upd(self) -> Vec:
        """Update vector."""
        ...

    @property
    def vec_rhs(self) -> Vec:
        """Right-hand side vector."""
        ...

    @property
    def ksp(self) -> KSP:
        """Linear solver."""
        ...

    @ksp.setter
    def ksp(self, value: KSP) -> None: ...
    @property
    def use_ksp(self) -> bool:
        """Boolean indicating if the solver uses a linear solver."""
        ...

    @use_ksp.setter
    def use_ksp(self, value: bool) -> None: ...
    @property
    def use_ew(self) -> bool:
        """Use the Eisenstat-Walker trick."""
        ...

    @use_ew.setter
    def use_ew(self, value: bool) -> None: ...
    @property
    def rtol(self) -> float:
        """Relative residual tolerance."""
        ...

    @rtol.setter
    def rtol(self, value: float) -> None: ...
    @property
    def atol(self) -> float:
        """Absolute residual tolerance."""
        ...

    @atol.setter
    def atol(self, value: float) -> None: ...
    @property
    def stol(self) -> float:
        """Solution update tolerance."""
        ...

    @stol.setter
    def stol(self, value: float) -> None: ...
    @property
    def max_it(self) -> int:
        """Maximum number of iterations."""
        ...

    @max_it.setter
    def max_it(self, value: int) -> None: ...
    @property
    def max_funcs(self) -> int:
        """Maximum number of function evaluations."""
        ...

    @max_funcs.setter
    def max_funcs(self, value: int) -> None: ...
    @property
    def its(self) -> int:
        """Number of iterations."""
        ...

    @its.setter
    def its(self, value: int) -> None: ...
    @property
    def norm(self) -> float:
        """Function norm."""
        ...

    @norm.setter
    def norm(self, value: float) -> None: ...
    @property
    def history(self) -> tuple[ArrayReal, ArrayInt]:
        """Convergence history."""
        ...

    @property
    def reason(self) -> ConvergedReason:
        """Converged reason."""
        ...

    @reason.setter
    def reason(self, value: ConvergedReason) -> None: ...
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

    @property
    def use_mf(self) -> bool:
        """Boolean indicating if the solver uses matrix-free finite-differencing."""
        ...

    @use_mf.setter
    def use_mf(self, value: bool) -> None: ...
    @property
    def use_fd(self) -> bool:
        """Boolean indicating if the solver uses coloring finite-differencing."""
        ...

    @use_fd.setter
    def use_fd(self, value: bool) -> None: ...
    @property
    def linesearch(self) -> SNESLineSearch:
        """The linesearch object associated with this SNES."""
        ...

    @linesearch.setter
    def linesearch(self, value: SNESLineSearch) -> None: ...
