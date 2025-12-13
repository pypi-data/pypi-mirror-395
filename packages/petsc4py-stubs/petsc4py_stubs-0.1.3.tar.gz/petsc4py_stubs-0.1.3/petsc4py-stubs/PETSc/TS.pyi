"""Type stubs for PETSc TS (Time Stepper) module."""


from typing import (
    Any,
    Callable,
    Sequence,
    Self,
)
from numpy import ndarray, dtype

from .Object import Object

from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .DM import DM
from .KSP import KSP
from .SNES import SNES
from .IS import IS

# Import types from typing module
from petsc4py.typing import (
    Scalar,
    ArrayInt,
    ArrayReal,
    ArrayScalar,
    TSRHSFunction,
    TSRHSJacobian,
    TSRHSJacobianP,
    TSIFunction,
    TSIJacobian,
    TSIJacobianP,
    TSI2Function,
    TSI2Jacobian,
    TSI2JacobianP,
    TSMonitorFunction,
    TSPreStepFunction,
    TSPostStepFunction,
    TSIndicatorFunction,
    TSPostEventFunction,
)


class TSType:
    """The time stepping method."""

    # native
    EULER: str
    BEULER: str
    BASICSYMPLECTIC: str
    PSEUDO: str
    CN: str
    SUNDIALS: str
    RK: str
    PYTHON: str
    THETA: str
    ALPHA: str
    ALPHA2: str
    GLLE: str
    GLEE: str
    SSP: str
    ARKIMEX: str
    DIRK: str
    ROSW: str
    EIMEX: str
    MIMEX: str
    BDF: str
    RADAU5: str
    MPRK: str
    DISCGRAD: str
    # aliases
    FE: str
    BE: str
    TH: str
    CRANK_NICOLSON: str
    RUNGE_KUTTA: str


class TSRKType:
    """The Runge-Kutta subtype."""

    RK1FE: str
    RK2A: str
    RK2B: str
    RK4: str
    RK3BS: str
    RK3: str
    RK5F: str
    RK5DP: str
    RK5BS: str
    RK6VR: str
    RK7VR: str
    RK8VR: str


class TSARKIMEXType:
    """The ARKIMEX subtype."""

    ARKIMEX1BEE: str
    ARKIMEXA2: str
    ARKIMEXL2: str
    ARKIMEXARS122: str
    ARKIMEX2C: str
    ARKIMEX2D: str
    ARKIMEX2E: str
    ARKIMEXPRSSP2: str
    ARKIMEX3: str
    ARKIMEXBPR3: str
    ARKIMEXARS443: str
    ARKIMEX4: str
    ARKIMEX5: str


class TSDIRKType:
    """The DIRK subtype."""

    DIRKS212: str
    DIRKES122SAL: str
    DIRKES213SAL: str
    DIRKES324SAL: str
    DIRKES325SAL: str
    DIRK657A: str
    DIRKES648SA: str
    DIRK658A: str
    DIRKS659A: str
    DIRK7510SAL: str
    DIRKES7510SA: str
    DIRK759A: str
    DIRKS7511SAL: str
    DIRK8614A: str
    DIRK8616SAL: str
    DIRKES8516SAL: str


class TSProblemType:
    """Distinguishes linear and nonlinear problems."""

    LINEAR: int
    NONLINEAR: int


class TSEquationType:
    """Distinguishes among types of explicit and implicit equations."""

    UNSPECIFIED: int
    EXPLICIT: int
    ODE_EXPLICIT: int
    DAE_SEMI_EXPLICIT_INDEX1: int
    DAE_SEMI_EXPLICIT_INDEX2: int
    DAE_SEMI_EXPLICIT_INDEX3: int
    DAE_SEMI_EXPLICIT_INDEXHI: int
    IMPLICIT: int
    ODE_IMPLICIT: int
    DAE_IMPLICIT_INDEX1: int
    DAE_IMPLICIT_INDEX2: int
    DAE_IMPLICIT_INDEX3: int
    DAE_IMPLICIT_INDEXHI: int


class TSExactFinalTime:
    """The method for ending time stepping."""

    UNSPECIFIED: int
    STEPOVER: int
    INTERPOLATE: int
    MATCHSTEP: int


class TSConvergedReason:
    """The reason the time step is converging."""

    # iterating
    CONVERGED_ITERATING: int
    ITERATING: int
    # converged
    CONVERGED_TIME: int
    CONVERGED_ITS: int
    CONVERGED_USER: int
    CONVERGED_EVENT: int
    # diverged
    DIVERGED_NONLINEAR_SOLVE: int
    DIVERGED_STEP_REJECTED: int


class TS(Object):
    """ODE integrator.

    TS is described in the PETSc manual.

    See Also
    --------
    petsc.TS
    """

    Type = TSType
    RKType = TSRKType
    ARKIMEXType = TSARKIMEXType
    DIRKType = TSDIRKType
    ProblemType = TSProblemType
    EquationType = TSEquationType
    ExactFinalTime = TSExactFinalTime
    ExactFinalTimeOption = TSExactFinalTime
    ConvergedReason = TSConvergedReason

    def view(self, viewer: Viewer | None = None) -> None:
        """Print the TS object.

        Collective.

        Parameters
        ----------
        viewer
            The visualization context.
        """
        ...

    def load(self, viewer: Viewer) -> None:
        """Load a TS that has been stored in binary with view.

        Collective.

        Parameters
        ----------
        viewer
            The visualization context.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the TS that was created with create.

        Collective.
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create an empty TS.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to Sys.getDefaultComm.
        """
        ...

    def clone(self) -> TS:
        """Return a shallow clone of the TS object.

        Collective.
        """
        ...

    def setType(self, ts_type: Type | str) -> None:
        """Set the method to be used as the TS solver.

        Collective.

        Parameters
        ----------
        ts_type
            The solver type.
        """
        ...

    def setRKType(self, ts_type: RKType | str) -> None:
        """Set the type of the Runge-Kutta scheme.

        Logically collective.

        Parameters
        ----------
        ts_type
            The type of scheme.
        """
        ...

    def setARKIMEXType(self, ts_type: ARKIMEXType | str) -> None:
        """Set the type of ARKIMEX scheme.

        Logically collective.

        Parameters
        ----------
        ts_type
            The type of ARKIMEX scheme.
        """
        ...

    def setARKIMEXFullyImplicit(self, flag: bool) -> None:
        """Solve both parts of the equation implicitly.

        Logically collective.

        Parameters
        ----------
        flag
            Set to True for fully implicit.
        """
        ...

    def setARKIMEXFastSlowSplit(self, flag: bool) -> None:
        """Use ARKIMEX for solving a fast-slow system.

        Logically collective.

        Parameters
        ----------
        flag
            Set to True for fast-slow partitioned systems.
        """
        ...

    def getType(self) -> str:
        """Return the TS type.

        Not collective.
        """
        ...

    def getRKType(self) -> str:
        """Return the RK scheme.

        Not collective.
        """
        ...

    def getARKIMEXType(self) -> str:
        """Return the ARKIMEX scheme.

        Not collective.
        """
        ...

    def setDIRKType(self, ts_type: DIRKType | str) -> None:
        """Set the type of DIRK scheme.

        Logically collective.

        Parameters
        ----------
        ts_type
            The type of DIRK scheme.
        """
        ...

    def getDIRKType(self) -> str:
        """Return the DIRK scheme.

        Not collective.
        """
        ...

    def setProblemType(self, ptype: ProblemType) -> None:
        """Set the type of problem to be solved.

        Logically collective.

        Parameters
        ----------
        ptype
            The type of problem.
        """
        ...

    def getProblemType(self) -> ProblemType:
        """Return the type of problem to be solved.

        Not collective.
        """
        ...

    def setEquationType(self, eqtype: EquationType) -> None:
        """Set the type of the equation that TS is solving.

        Logically collective.

        Parameters
        ----------
        eqtype
            The type of equation.
        """
        ...

    def getEquationType(self) -> EquationType:
        """Get the type of the equation that TS is solving.

        Not collective.
        """
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for all the TS options.

        Logically collective.

        Parameters
        ----------
        prefix
            The prefix to prepend to all option names.
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for all the TS options.

        Not collective.
        """
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for all the TS options.

        Logically collective.

        Parameters
        ----------
        prefix
            The prefix to append to the current prefix.
        """
        ...

    def setFromOptions(self) -> None:
        """Set various TS parameters from user options.

        Collective.
        """
        ...

    # --- application context ---

    def setAppCtx(self, appctx: Any) -> None:
        """Set the application context.

        Not collective.

        Parameters
        ----------
        appctx
            The application context.
        """
        ...

    def getAppCtx(self) -> Any:
        """Return the application context.

        Not collective.
        """
        ...

    # --- user RHS Function/Jacobian routines ---

    def setRHSFunction(
        self,
        function: TSRHSFunction | None,
        f: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the routine for evaluating the function G in U_t = G(t, u).

        Logically collective.

        Parameters
        ----------
        function
            The right-hand side function.
        f
            The vector into which the right-hand side is computed.
        args
            Additional positional arguments for function.
        kargs
            Additional keyword arguments for function.
        """
        ...

    def setRHSJacobian(
        self,
        jacobian: TSRHSJacobian | None,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function to compute the Jacobian of G in U_t = G(U, t).

        Logically collective.

        Parameters
        ----------
        jacobian
            The right-hand side Jacobian function.
        J
            The matrix into which the Jacobian is computed.
        P
            The matrix into which the preconditioner is computed.
        args
            Additional positional arguments for jacobian.
        kargs
            Additional keyword arguments for jacobian.
        """
        ...

    def computeRHSFunction(self, t: float, x: Vec, f: Vec) -> None:
        """Evaluate the right-hand side function.

        Collective.

        Parameters
        ----------
        t
            The time at which to evaluate the RHS.
        x
            The state vector.
        f
            The Vec into which the RHS is computed.
        """
        ...

    def computeRHSFunctionLinear(self, t: float, x: Vec, f: Vec) -> None:
        """Evaluate the right-hand side via the user-provided Jacobian.

        Collective.

        Parameters
        ----------
        t
            The time at which to evaluate the RHS.
        x
            The state vector.
        f
            The Vec into which the RHS is computed.
        """
        ...

    def computeRHSJacobian(
        self, t: float, x: Vec, J: Mat, P: Mat | None = None
    ) -> None:
        """Compute the Jacobian matrix that has been set with setRHSJacobian.

        Collective.

        Parameters
        ----------
        t
            The time at which to evaluate the Jacobian.
        x
            The state vector.
        J
            The matrix into which the Jacobian is computed.
        P
            The optional matrix to use for building a preconditioner.
        """
        ...

    def computeRHSJacobianConstant(
        self, t: float, x: Vec, J: Mat, P: Mat | None = None
    ) -> None:
        """Reuse a Jacobian that is time-independent.

        Collective.

        Parameters
        ----------
        t
            The time at which to evaluate the Jacobian.
        x
            The state vector.
        J
            A pointer to the stored Jacobian.
        P
            An optional pointer to the matrix used to construct the preconditioner.
        """
        ...

    def getRHSFunction(self) -> tuple[Vec, TSRHSFunction | None]:
        """Return the vector where the rhs is stored and the function used to compute it.

        Not collective.
        """
        ...

    def getRHSJacobian(self) -> tuple[Mat, Mat, TSRHSJacobian | None]:
        """Return the Jacobian and the function used to compute them.

        Not collective.
        """
        ...

    # --- user Implicit Function/Jacobian routines ---

    def setIFunction(
        self,
        function: TSIFunction | None,
        f: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function representing the DAE to be solved.

        Logically collective.

        Parameters
        ----------
        function
            The implicit function.
        f
            The vector to store values or None to be created internally.
        args
            Additional positional arguments for function.
        kargs
            Additional keyword arguments for function.
        """
        ...

    def setIJacobian(
        self,
        jacobian: TSIJacobian | None,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function to compute the Jacobian.

        Logically collective.

        Set the function to compute the matrix dF/dU + a*dF/dU_t where
        F(t, U, U_t) is the function provided with setIFunction.

        Parameters
        ----------
        jacobian
            The function which computes the Jacobian.
        J
            The matrix into which the Jacobian is computed.
        P
            The optional matrix to use for building a preconditioner matrix.
        args
            Additional positional arguments for jacobian.
        kargs
            Additional keyword arguments for jacobian.
        """
        ...

    def setIJacobianP(
        self,
        jacobian: TSIJacobianP | None,
        J: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function that computes the Jacobian with respect to parameters.

        Logically collective.

        Parameters
        ----------
        jacobian
            The function which computes the Jacobian.
        J
            The matrix into which the Jacobian is computed.
        args
            Additional positional arguments for jacobian.
        kargs
            Additional keyword arguments for jacobian.
        """
        ...

    def computeIFunction(
        self, t: float, x: Vec, xdot: Vec, f: Vec, imex: bool = False
    ) -> None:
        """Evaluate the DAE residual written in implicit form.

        Collective.

        Parameters
        ----------
        t
            The current time.
        x
            The state vector.
        xdot
            The time derivative of the state vector.
        f
            The vector into which the residual is stored.
        imex
            A flag which indicates if the RHS should be kept separate.
        """
        ...

    def computeIJacobian(
        self,
        t: float,
        x: Vec,
        xdot: Vec,
        a: float,
        J: Mat,
        P: Mat | None = None,
        imex: bool = False,
    ) -> None:
        """Evaluate the Jacobian of the DAE.

        Collective.

        If F(t, U, Udot)=0 is the DAE, the required Jacobian is
        dF/dU + shift*dF/dUdot

        Parameters
        ----------
        t
            The current time.
        x
            The state vector.
        xdot
            The time derivative of the state vector.
        a
            The shift to apply.
        J
            The matrix into which the Jacobian is computed.
        P
            The optional matrix to use for building a preconditioner.
        imex
            A flag which indicates if the RHS should be kept separate.
        """
        ...

    def computeIJacobianP(
        self,
        t: float,
        x: Vec,
        xdot: Vec,
        a: float,
        J: Mat,
        imex: bool = False,
    ) -> None:
        """Evaluate the Jacobian with respect to parameters.

        Collective.

        Parameters
        ----------
        t
            The current time.
        x
            The state vector.
        xdot
            The time derivative of the state vector.
        a
            The shift to apply.
        J
            The matrix into which the Jacobian is computed.
        imex
            A flag which indicates if the RHS should be kept separate.
        """
        ...

    def getIFunction(self) -> tuple[Vec, TSIFunction | None]:
        """Return the vector and function which computes the implicit residual.

        Not collective.
        """
        ...

    def getIJacobian(self) -> tuple[Mat, Mat, TSIJacobian | None]:
        """Return the matrices and function which computes the implicit Jacobian.

        Not collective.
        """
        ...

    # --- user 2nd order Implicit Function/Jacobian routines ---

    def setI2Function(
        self,
        function: TSI2Function | None,
        f: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function to compute the 2nd order DAE.

        Logically collective.

        Parameters
        ----------
        function
            The implicit function.
        f
            The vector to store values or None to be created internally.
        args
            Additional positional arguments for function.
        kargs
            Additional keyword arguments for function.
        """
        ...

    def setI2Jacobian(
        self,
        jacobian: TSI2Jacobian | None,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function to compute the Jacobian of the 2nd order DAE.

        Logically collective.

        Parameters
        ----------
        jacobian
            The function which computes the Jacobian.
        J
            The matrix into which the Jacobian is computed.
        P
            The optional matrix to use for building a preconditioner.
        args
            Additional positional arguments for jacobian.
        kargs
            Additional keyword arguments for jacobian.
        """
        ...

    def computeI2Function(
        self, t: float, x: Vec, xdot: Vec, xdotdot: Vec, f: Vec
    ) -> None:
        """Evaluate the DAE residual in implicit form.

        Collective.

        Parameters
        ----------
        t
            The current time.
        x
            The state vector.
        xdot
            The time derivative of the state vector.
        xdotdot
            The second time derivative of the state vector.
        f
            The vector into which the residual is stored.
        """
        ...

    def computeI2Jacobian(
        self,
        t: float,
        x: Vec,
        xdot: Vec,
        xdotdot: Vec,
        v: float,
        a: float,
        J: Mat,
        P: Mat | None = None,
    ) -> None:
        """Evaluate the Jacobian of the DAE.

        Collective.

        If F(t, U, V, A)=0 is the DAE,
        the required Jacobian is dF/dU + v dF/dV + a dF/dA.

        Parameters
        ----------
        t
            The current time.
        x
            The state vector.
        xdot
            The time derivative of the state vector.
        xdotdot
            The second time derivative of the state vector.
        v
            The shift to apply to the first derivative.
        a
            The shift to apply to the second derivative.
        J
            The matrix into which the Jacobian is computed.
        P
            The optional matrix to use for building a preconditioner.
        """
        ...

    def getI2Function(self) -> tuple[Vec, TSI2Function | None]:
        """Return the vector and function which computes the residual.

        Not collective.
        """
        ...

    def getI2Jacobian(self) -> tuple[Mat, Mat, TSI2Jacobian | None]:
        """Return the matrices and function which computes the Jacobian.

        Not collective.
        """
        ...

    # --- TSRHSSplit routines to support multirate and IMEX solvers ---

    def setRHSSplitIS(self, splitname: str, iss: IS) -> None:
        """Set the index set for the specified split.

        Logically collective.

        Parameters
        ----------
        splitname
            Name of this split, if None the number of the split is used.
        iss
            The index set for part of the solution vector.
        """
        ...

    def setRHSSplitRHSFunction(
        self,
        splitname: str,
        function: TSRHSFunction | None,
        r: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the split right-hand-side functions.

        Logically collective.

        Parameters
        ----------
        splitname
            Name of the split.
        function
            The RHS function evaluation routine.
        r
            Vector to hold the residual.
        args
            Additional positional arguments for function.
        kargs
            Additional keyword arguments for function.
        """
        ...

    def setRHSSplitIFunction(
        self,
        splitname: str,
        function: TSIFunction | None,
        r: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the split implicit functions.

        Logically collective.

        Parameters
        ----------
        splitname
            Name of the split.
        function
            The implicit function evaluation routine.
        r
            Vector to hold the residual.
        args
            Additional positional arguments for function.
        kargs
            Additional keyword arguments for function.
        """
        ...

    def setRHSSplitIJacobian(
        self,
        splitname: str,
        jacobian: TSIJacobian | None,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the Jacobian for the split implicit function.

        Logically collective.

        Parameters
        ----------
        splitname
            Name of the split.
        jacobian
            The Jacobian evaluation routine.
        J
            Matrix to store Jacobian entries computed by jacobian.
        P
            Matrix used to compute preconditioner (usually the same as J).
        args
            Additional positional arguments for jacobian.
        kargs
            Additional keyword arguments for jacobian.
        """
        ...

    # --- solution vector ---

    def setSolution(self, u: Vec) -> None:
        """Set the initial solution vector.

        Logically collective.

        Parameters
        ----------
        u
            The solution vector.
        """
        ...

    def getSolution(self) -> Vec:
        """Return the solution at the present timestep.

        Not collective.
        """
        ...

    def setSolution2(self, u: Vec, v: Vec) -> None:
        """Set the initial solution and its time derivative.

        Logically collective.

        Parameters
        ----------
        u
            The solution vector.
        v
            The time derivative vector.
        """
        ...

    def getSolution2(self) -> tuple[Vec, Vec]:
        """Return the solution and time derivative at the present timestep.

        Not collective.
        """
        ...

    # --- evaluation times ---

    def setEvaluationTimes(self, tspan: Sequence[float]) -> None:
        """Set evaluation points where solution will be computed and stored.

        Collective.

        Parameters
        ----------
        tspan
            The sequence of time points. The first element and the last element
            are the initial time and the final time respectively.
        """
        ...

    def getEvaluationTimes(self) -> ArrayReal:
        """Return the evaluation points.

        Not collective.
        """
        ...

    def getEvaluationSolutions(self) -> tuple[ArrayReal, list[Vec] | None]:
        """Return the solutions and the times they were recorded at.

        Not collective.
        """
        ...

    # --- time span ---

    def setTimeSpan(self, tspan: Sequence[float]) -> None:
        """Set the time span and time points to evaluate solution at.

        Collective.

        Parameters
        ----------
        tspan
            The sequence of time points.
        """
        ...

    def getTimeSpan(self) -> ArrayReal:
        """Return the time span.

        Not collective.
        """
        ...

    def getTimeSpanSolutions(self) -> list[Vec] | None:
        """Return the solutions at the times in the time span.

        Not collective.
        """
        ...

    # --- inner solver ---

    def getSNES(self) -> SNES:
        """Return the SNES associated with the TS.

        Not collective.
        """
        ...

    def getKSP(self) -> KSP:
        """Return the KSP associated with the TS.

        Not collective.
        """
        ...

    # --- discretization space ---

    def getDM(self) -> DM:
        """Return the DM associated with the TS.

        Not collective.
        """
        ...

    def setDM(self, dm: DM) -> None:
        """Set the DM that may be used by some nonlinear solvers or preconditioners.

        Logically collective.

        Parameters
        ----------
        dm
            The DM object.
        """
        ...

    # --- customization ---

    def setTime(self, t: float) -> None:
        """Set the time.

        Logically collective.

        Parameters
        ----------
        t
            The time.
        """
        ...

    def getTime(self) -> float:
        """Return the time of the most recently completed step.

        Not collective.
        """
        ...

    def getPrevTime(self) -> float:
        """Return the starting time of the previously completed step.

        Not collective.
        """
        ...

    def getSolveTime(self) -> float:
        """Return the time after a call to solve.

        Not collective.
        """
        ...

    def setTimeStep(self, time_step: float) -> None:
        """Set the duration of the timestep.

        Logically collective.

        Parameters
        ----------
        time_step
            The duration of the timestep.
        """
        ...

    def getTimeStep(self) -> float:
        """Return the duration of the current timestep.

        Not collective.
        """
        ...

    def setStepNumber(self, step_number: int) -> None:
        """Set the number of steps completed.

        Logically collective.

        Parameters
        ----------
        step_number
            The number of steps completed.
        """
        ...

    def getStepNumber(self) -> int:
        """Return the number of time steps completed.

        Not collective.
        """
        ...

    def setMaxTime(self, max_time: float) -> None:
        """Set the maximum (final) time.

        Logically collective.

        Parameters
        ----------
        max_time
            The final time.
        """
        ...

    def getMaxTime(self) -> float:
        """Return the maximum (final) time.

        Not collective.
        """
        ...

    def setMaxSteps(self, max_steps: int) -> None:
        """Set the maximum number of steps to use.

        Logically collective.

        Parameters
        ----------
        max_steps
            The maximum number of steps to use.
        """
        ...

    def getMaxSteps(self) -> int:
        """Return the maximum number of steps to use.

        Not collective.
        """
        ...

    def getSNESIterations(self) -> int:
        """Return the total number of nonlinear iterations used by the TS.

        Not collective.
        """
        ...

    def getKSPIterations(self) -> int:
        """Return the total number of linear iterations used by the TS.

        Not collective.
        """
        ...

    def setMaxStepRejections(self, n: int) -> None:
        """Set the maximum number of step rejections before a time step fails.

        Not collective.

        Parameters
        ----------
        n
            The maximum number of rejected steps, use -1 for unlimited.
        """
        ...

    def getStepRejections(self) -> int:
        """Return the total number of rejected steps.

        Not collective.
        """
        ...

    def setMaxSNESFailures(self, n: int) -> None:
        """Set the maximum number of SNES solves failures allowed.

        Not collective.

        Parameters
        ----------
        n
            The maximum number of failed nonlinear solver, use -1 for unlimited.
        """
        ...

    def getSNESFailures(self) -> int:
        """Return the total number of failed SNES solves in the TS.

        Not collective.
        """
        ...

    def setErrorIfStepFails(self, flag: bool = True) -> None:
        """Immediately error if no step succeeds.

        Not collective.

        Parameters
        ----------
        flag
            Enable to error if no step succeeds.
        """
        ...

    def setTolerances(
        self,
        rtol: float | Vec | None = None,
        atol: float | Vec | None = None,
    ) -> None:
        """Set tolerances for local truncation error when using an adaptive controller.

        Logically collective.

        Parameters
        ----------
        rtol
            The relative tolerance, or None to leave the current value.
        atol
            The absolute tolerance, or None to leave the current value.
        """
        ...

    def getTolerances(self) -> tuple[float | Vec, float | Vec]:
        """Return the tolerances for local truncation error.

        Logically collective.

        Returns
        -------
        rtol
            The relative tolerance.
        atol
            The absolute tolerance.
        """
        ...

    def setExactFinalTime(self, option: ExactFinalTime) -> None:
        """Set method of computing the final time step.

        Logically collective.

        Parameters
        ----------
        option
            The exact final time option.
        """
        ...

    def setConvergedReason(self, reason: ConvergedReason) -> None:
        """Set the reason for handling the convergence of solve.

        Logically collective.

        Parameters
        ----------
        reason
            The reason for convergence.
        """
        ...

    def getConvergedReason(self) -> ConvergedReason:
        """Return the reason the TS step was stopped.

        Not collective.
        """
        ...

    # --- monitoring ---

    def setMonitor(
        self,
        monitor: TSMonitorFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set an additional monitor to the TS.

        Logically collective.

        Parameters
        ----------
        monitor
            The custom monitor function.
        args
            Additional positional arguments for monitor.
        kargs
            Additional keyword arguments for monitor.
        """
        ...

    def getMonitor(
        self,
    ) -> list[tuple[TSMonitorFunction, tuple[Any, ...], dict[str, Any]]] | None:
        """Return the monitor.

        Not collective.
        """
        ...

    def monitorCancel(self) -> None:
        """Clear all the monitors that have been set.

        Logically collective.
        """
        ...

    cancelMonitor = monitorCancel

    def monitor(self, step: int, time: float, u: Vec | None = None) -> None:
        """Monitor the solve.

        Collective.

        Parameters
        ----------
        step
            The step number that has just completed.
        time
            The model time of the state.
        u
            The state at the current model time.
        """
        ...

    # --- event handling ---

    def setEventHandler(
        self,
        direction: Sequence[int],
        terminate: Sequence[bool],
        indicator: TSIndicatorFunction | None,
        postevent: TSPostEventFunction | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set a function used for detecting events.

        Logically collective.

        Parameters
        ----------
        direction
            Direction of zero crossing to be detected {-1, 0, +1}.
        terminate
            Flags for each event to indicate stepping should be terminated.
        indicator
            Function for defining the indicator-functions marking the events.
        postevent
            Function to execute after the event.
        args
            Additional positional arguments for indicator.
        kargs
            Additional keyword arguments for indicator.
        """
        ...

    def setEventTolerances(
        self,
        tol: float | None = None,
        vtol: Sequence[float] | None = None,
    ) -> None:
        """Set tolerances for event zero crossings when using event handler.

        Logically collective.

        Parameters
        ----------
        tol
            The scalar tolerance or None to leave at the current value.
        vtol
            A sequence of scalar tolerance for each event.
        """
        ...

    def getNumEvents(self) -> int:
        """Return the number of events.

        Logically collective.
        """
        ...

    # --- solving ---

    def setPreStep(
        self,
        prestep: TSPreStepFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set a function to be called at the beginning of each time step.

        Logically collective.

        Parameters
        ----------
        prestep
            The function to be called at the beginning of each step.
        args
            Additional positional arguments for prestep.
        kargs
            Additional keyword arguments for prestep.
        """
        ...

    def getPreStep(
        self,
    ) -> tuple[TSPreStepFunction, tuple[Any, ...] | None, dict[str, Any] | None] | None:
        """Return the prestep function.

        Not collective.
        """
        ...

    def setPostStep(
        self,
        poststep: TSPostStepFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set a function to be called at the end of each time step.

        Logically collective.

        Parameters
        ----------
        poststep
            The function to be called at the end of each step.
        args
            Additional positional arguments for poststep.
        kargs
            Additional keyword arguments for poststep.
        """
        ...

    def getPostStep(
        self,
    ) -> tuple[TSPostStepFunction, tuple[Any, ...] | None, dict[str, Any] | None] | None:
        """Return the poststep function.

        Not collective.
        """
        ...

    def setUp(self) -> None:
        """Set up the internal data structures for the TS.

        Collective.
        """
        ...

    def reset(self) -> None:
        """Reset the TS, removing any allocated vectors and matrices.

        Collective.
        """
        ...

    def step(self) -> None:
        """Take one step.

        Collective.
        """
        ...

    def restartStep(self) -> None:
        """Flag the solver to restart the next step.

        Collective.
        """
        ...

    def rollBack(self) -> None:
        """Roll back one time step.

        Collective.
        """
        ...

    def solve(self, u: Vec | None = None) -> None:
        """Step the requested number of timesteps.

        Collective.

        Parameters
        ----------
        u
            The solution vector. Can be None.
        """
        ...

    def interpolate(self, t: float, u: Vec) -> None:
        """Interpolate the solution to a given time.

        Collective.

        Parameters
        ----------
        t
            The time to interpolate.
        u
            The state vector to interpolate.
        """
        ...

    def setStepLimits(self, hmin: float, hmax: float) -> None:
        """Set the minimum and maximum allowed step sizes.

        Logically collective.

        Parameters
        ----------
        hmin
            The minimum step size.
        hmax
            The maximum step size.
        """
        ...

    def getStepLimits(self) -> tuple[float, float]:
        """Return the minimum and maximum allowed time step sizes.

        Not collective.
        """
        ...

    # --- Adjoint methods ---

    def setSaveTrajectory(self) -> None:
        """Enable to save solutions as an internal TS trajectory.

        Collective.
        """
        ...

    def removeTrajectory(self) -> None:
        """Remove the internal TS trajectory object.

        Collective.
        """
        ...

    def getCostIntegral(self) -> Vec:
        """Return a vector of values of the integral term in the cost functions.

        Not collective.
        """
        ...

    def setCostGradients(
        self,
        vl: Vec | Sequence[Vec] | None,
        vm: Vec | Sequence[Vec] | None = None,
    ) -> None:
        """Set the cost gradients.

        Logically collective.

        Parameters
        ----------
        vl
            Gradients with respect to the initial condition variables.
        vm
            Gradients with respect to the parameters.
        """
        ...

    def getCostGradients(self) -> tuple[list[Vec] | None, list[Vec] | None]:
        """Return the cost gradients.

        Not collective.
        """
        ...

    def setRHSJacobianP(
        self,
        jacobianp: TSRHSJacobianP | None,
        A: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the function that computes the Jacobian with respect to the parameters.

        Logically collective.

        Parameters
        ----------
        jacobianp
            The user-defined function.
        A
            The matrix into which the Jacobian will be computed.
        args
            Additional positional arguments for jacobianp.
        kargs
            Additional keyword arguments for jacobianp.
        """
        ...

    def computeRHSJacobianP(self, t: float, x: Vec, J: Mat) -> None:
        """Run the user-defined JacobianP function.

        Collective.

        Parameters
        ----------
        t
            The time at which to compute the Jacobian.
        x
            The solution at which to compute the Jacobian.
        J
            The output Jacobian matrix.
        """
        ...

    def createQuadratureTS(self, forward: bool = True) -> TS:
        """Create a sub TS that evaluates integrals over time.

        Collective.

        Parameters
        ----------
        forward
            Enable to evaluate forward in time.
        """
        ...

    def getQuadratureTS(self) -> tuple[bool, TS]:
        """Return the sub TS that evaluates integrals over time.

        Not collective.

        Returns
        -------
        forward
            True if evaluating the integral forward in time.
        qts
            The sub TS.
        """
        ...

    def adjointSetSteps(self, adjoint_steps: int) -> None:
        """Set the number of steps the adjoint solver should take backward in time.

        Logically collective.

        Parameters
        ----------
        adjoint_steps
            The number of steps to take.
        """
        ...

    def adjointSetUp(self) -> None:
        """Set up the internal data structures for the later use of an adjoint solver.

        Collective.
        """
        ...

    def adjointSolve(self) -> None:
        """Solve the discrete adjoint problem for an ODE/DAE.

        Collective.
        """
        ...

    def adjointStep(self) -> None:
        """Step one time step backward in the adjoint run.

        Collective.
        """
        ...

    def adjointReset(self) -> None:
        """Reset a TS, removing any allocated vectors and matrices.

        Collective.
        """
        ...

    # --- Python ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create an integrator of Python type.

        Collective.

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

        Not collective.

        Parameters
        ----------
        context
            The Python context.
        """
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing the required Python methods.

        Not collective.
        """
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used.

        Collective.

        Parameters
        ----------
        py_type
            The Python type.
        """
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the solver.

        Not collective.
        """
        ...

    # --- Theta ---

    def setTheta(self, theta: float) -> None:
        """Set the abscissa of the stage in (0, 1] for Type.THETA.

        Logically collective.

        Parameters
        ----------
        theta
            Stage abscissa.
        """
        ...

    def getTheta(self) -> float:
        """Return the abscissa of the stage in (0, 1] for Type.THETA.

        Not collective.
        """
        ...

    def setThetaEndpoint(self, flag: bool = True) -> None:
        """Set to use the endpoint variant of Type.THETA.

        Logically collective.

        Parameters
        ----------
        flag
            Enable to use the endpoint variant.
        """
        ...

    def getThetaEndpoint(self) -> bool:
        """Return whether the endpoint variable of Type.THETA is used.

        Not collective.
        """
        ...

    # --- Alpha ---

    def setAlphaRadius(self, radius: float) -> None:
        """Set the spectral radius for Type.ALPHA.

        Logically collective.

        Parameters
        ----------
        radius
            The spectral radius.
        """
        ...

    def setAlphaParams(
        self,
        alpha_m: float | None = None,
        alpha_f: float | None = None,
        gamma: float | None = None,
    ) -> None:
        """Set the algorithmic parameters for Type.ALPHA.

        Logically collective.

        Parameters
        ----------
        alpha_m
            Parameter, leave None to keep current value.
        alpha_f
            Parameter, leave None to keep current value.
        gamma
            Parameter, leave None to keep current value.
        """
        ...

    def getAlphaParams(self) -> tuple[float, float, float]:
        """Return the algorithmic parameters for Type.ALPHA.

        Not collective.
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
        """The DM."""
        ...

    @dm.setter
    def dm(self, value: DM) -> None: ...

    @property
    def problem_type(self) -> ProblemType:
        """The problem type."""
        ...

    @problem_type.setter
    def problem_type(self, value: ProblemType) -> None: ...

    @property
    def equation_type(self) -> EquationType:
        """The equation type."""
        ...

    @equation_type.setter
    def equation_type(self, value: EquationType) -> None: ...

    @property
    def snes(self) -> SNES:
        """The SNES."""
        ...

    @property
    def ksp(self) -> KSP:
        """The KSP."""
        ...

    @property
    def vec_sol(self) -> Vec:
        """The solution vector."""
        ...

    @property
    def time(self) -> float:
        """The current time."""
        ...

    @time.setter
    def time(self, value: float) -> None: ...

    @property
    def time_step(self) -> float:
        """The current time step size."""
        ...

    @time_step.setter
    def time_step(self, value: float) -> None: ...

    @property
    def step_number(self) -> int:
        """The current step number."""
        ...

    @step_number.setter
    def step_number(self, value: int) -> None: ...

    @property
    def max_time(self) -> float:
        """The maximum time."""
        ...

    @max_time.setter
    def max_time(self, value: float) -> None: ...

    @property
    def max_steps(self) -> int:
        """The maximum number of steps."""
        ...

    @max_steps.setter
    def max_steps(self, value: int) -> None: ...

    @property
    def rtol(self) -> float:
        """The relative tolerance."""
        ...

    @rtol.setter
    def rtol(self, value: float) -> None: ...

    @property
    def atol(self) -> float:
        """The absolute tolerance."""
        ...

    @atol.setter
    def atol(self, value: float) -> None: ...

    @property
    def reason(self) -> ConvergedReason:
        """The converged reason."""
        ...

    @reason.setter
    def reason(self, value: ConvergedReason) -> None: ...

    @property
    def iterating(self) -> bool:
        """Indicates the TS is still iterating."""
        ...

    @property
    def converged(self) -> bool:
        """Indicates the TS has converged."""
        ...

    @property
    def diverged(self) -> bool:
        """Indicates the TS has stopped."""
        ...
