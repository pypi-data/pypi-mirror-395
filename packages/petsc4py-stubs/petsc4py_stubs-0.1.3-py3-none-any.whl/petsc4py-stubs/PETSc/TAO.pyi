"""Type stubs for PETSc TAO module."""


from typing import (
    Any,
    Callable,
    Self,
)

from .Object import Object

from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .KSP import KSP
from .IS import IS

# Import types from typing module
from petsc4py.typing import (
    TAOObjectiveFunction,
    TAOResidualFunction,
    TAOJacobianResidualFunction,
    TAOGradientFunction,
    TAOObjectiveGradientFunction,
    TAOVariableBoundsFunction,
    TAOConstraintsFunction,
    TAOHessianFunction,
    TAOJacobianFunction,
    TAOConstraintsJacobianFunction,
    TAOUpdateFunction,
    TAOConvergedFunction,
    TAOMonitorFunction,
    TAOLSObjectiveFunction,
    TAOLSGradientFunction,
    TAOLSObjectiveGradientFunction,
)

class TAOType:
    """TAO solver type.

    See Also
    --------
    petsc.TaoType
    """

    LMVM: str
    NLS: str
    NTR: str
    NTL: str
    CG: str
    TRON: str
    OWLQN: str
    BMRM: str
    BLMVM: str
    BQNLS: str
    BNCG: str
    BNLS: str
    BNTR: str
    BNTL: str
    BQNKLS: str
    BQNKTR: str
    BQNKTL: str
    BQPIP: str
    GPCG: str
    NM: str
    POUNDERS: str
    BRGN: str
    LCL: str
    SSILS: str
    SSFLS: str
    ASILS: str
    ASFLS: str
    IPM: str
    PDIPM: str
    SHELL: str
    ADMM: str
    ALMM: str
    PYTHON: str

class TAOConvergedReason:
    """TAO solver termination reason.

    See Also
    --------
    petsc.TaoConvergedReason
    """

    # iterating
    CONTINUE_ITERATING: int
    CONVERGED_ITERATING: int
    ITERATING: int
    # converged
    CONVERGED_GATOL: int
    CONVERGED_GRTOL: int
    CONVERGED_GTTOL: int
    CONVERGED_STEPTOL: int
    CONVERGED_MINF: int
    CONVERGED_USER: int
    # diverged
    DIVERGED_MAXITS: int
    DIVERGED_NAN: int
    DIVERGED_MAXFCN: int
    DIVERGED_LS_FAILURE: int
    DIVERGED_TR_REDUCTION: int
    DIVERGED_USER: int

class TAOBNCGType:
    """TAO Bound Constrained Conjugate Gradient (BNCG) Update Type."""

    GD: int
    PCGD: int
    HS: int
    FR: int
    PRP: int
    PRP_PLUS: int
    DY: int
    HZ: int
    DK: int
    KD: int
    SSML_BFGS: int
    SSML_DFP: int
    SSML_BRDN: int

class TAOALMMType:
    """TAO Augmented Lagrangian Multiplier method (ALMM) Type."""

    CLASSIC: int
    PHR: int

class TAO(Object):
    """Optimization solver.

    TAO is described in the PETSc manual.

    See Also
    --------
    petsc.Tao
    """

    Type = TAOType
    ConvergedReason = TAOConvergedReason
    BNCGType = TAOBNCGType
    ALMMType = TAOALMMType
    Reason = TAOConvergedReason

    # --- View and lifecycle ---

    def view(self, viewer: Viewer | None = None) -> None:
        """View the solver.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.TaoView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the solver.

        Collective.

        See Also
        --------
        petsc.TaoDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a TAO solver.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        Sys.getDefaultComm, petsc.TaoCreate
        """
        ...

    # --- Type and options ---

    def setType(self, tao_type: Type | str) -> None:
        """Set the type of the solver.

        Logically collective.

        Parameters
        ----------
        tao_type
            The type of the solver.

        See Also
        --------
        getType, petsc.TaoSetType
        """
        ...

    def getType(self) -> str:
        """Return the type of the solver.

        Not collective.

        See Also
        --------
        setType, petsc.TaoGetType
        """
        ...

    def setOptionsPrefix(self, prefix: str | None) -> None:
        """Set the prefix used for searching for options in the database.

        Logically collective.

        See Also
        --------
        petsc_options, petsc.TaoSetOptionsPrefix
        """
        ...

    def appendOptionsPrefix(self, prefix: str | None) -> None:
        """Append to the prefix used for searching for options in the database.

        Logically collective.

        See Also
        --------
        petsc_options, setOptionsPrefix, petsc.TaoAppendOptionsPrefix
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database.

        Not collective.

        See Also
        --------
        petsc_options, setOptionsPrefix, petsc.TaoGetOptionsPrefix
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the solver from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.TaoSetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Set up the internal data structures for using the solver.

        Collective.

        See Also
        --------
        petsc.TaoSetUp
        """
        ...

    # --- Trust region ---

    def setInitialTrustRegionRadius(self, radius: float) -> None:
        """Set the initial trust region radius.

        Collective.

        See Also
        --------
        petsc.TaoSetInitialTrustRegionRadius
        """
        ...

    # --- Application context ---

    def setAppCtx(self, appctx: Any) -> None:
        """Set the application context."""
        ...

    def getAppCtx(self) -> Any:
        """Return the application context."""
        ...

    # --- Solution and objective ---

    def setSolution(self, x: Vec) -> None:
        """Set the vector used to store the solution.

        Collective.

        See Also
        --------
        getSolution, petsc.TaoSetSolution
        """
        ...

    def getSolution(self) -> Vec:
        """Return the vector holding the solution.

        Not collective.

        See Also
        --------
        setSolution, petsc.TaoGetSolution
        """
        ...

    def setObjective(
        self,
        objective: TAOObjectiveFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the objective function evaluation callback.

        Logically collective.

        Parameters
        ----------
        objective
            The objective function callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setGradient, setObjectiveGradient, petsc.TaoSetObjective
        """
        ...

    def getObjective(self) -> TAOObjectiveFunction:
        """Return the objective evaluation callback.

        Not collective.

        See Also
        --------
        setObjective, petsc.TaoGetObjective
        """
        ...

    # --- Residual ---

    def setResidual(
        self,
        residual: TAOResidualFunction,
        R: Vec,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the residual evaluation callback for least-squares applications.

        Logically collective.

        Parameters
        ----------
        residual
            The residual callback.
        R
            The vector to store the residual.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setJacobianResidual, petsc.TaoSetResidualRoutine
        """
        ...

    def setJacobianResidual(
        self,
        jacobian: TAOJacobianResidualFunction,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the least-squares residual Jacobian.

        Logically collective.

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

        See Also
        --------
        setResidual, petsc.TaoSetJacobianResidualRoutine
        """
        ...

    # --- Gradient ---

    def setGradient(
        self,
        gradient: TAOGradientFunction,
        g: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the gradient evaluation callback.

        Logically collective.

        Parameters
        ----------
        gradient
            The gradient callback.
        g
            The vector to store the gradient.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setObjective, setObjectiveGradient, setHessian, petsc.TaoSetGradient
        """
        ...

    def getGradient(self) -> tuple[Vec, TAOGradientFunction]:
        """Return the vector used to store the gradient and the evaluation callback.

        Not collective.

        See Also
        --------
        setGradient, setHessian, petsc.TaoGetGradient
        """
        ...

    def setObjectiveGradient(
        self,
        objgrad: TAOObjectiveGradientFunction,
        g: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the objective function and gradient evaluation callback.

        Logically collective.

        Parameters
        ----------
        objgrad
            The objective function and gradient callback.
        g
            The vector to store the gradient.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setObjective, setGradient, setHessian, getObjectiveAndGradient
        petsc.TaoSetObjectiveAndGradient
        """
        ...

    def getObjectiveAndGradient(self) -> tuple[Vec, TAOObjectiveGradientFunction]:
        """Return the vector used to store the gradient and the evaluation callback.

        Not collective.

        See Also
        --------
        setObjectiveGradient, petsc.TaoGetObjectiveAndGradient
        """
        ...

    # --- Variable bounds ---

    def setVariableBounds(
        self,
        varbounds: tuple[Vec, Vec] | TAOVariableBoundsFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the lower and upper bounds for the optimization problem.

        Logically collective.

        Parameters
        ----------
        varbounds
            Either a tuple of `Vec` or a `TAOVariableBoundsFunction` callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        petsc.TaoSetVariableBounds, petsc.TaoSetVariableBoundsRoutine
        """
        ...

    def getVariableBounds(self) -> tuple[Vec, Vec]:
        """Return the lower and upper bounds vectors.

        Not collective.

        See Also
        --------
        setVariableBounds, petsc.TaoGetVariableBounds
        """
        ...

    # --- Constraints ---

    def setConstraints(
        self,
        constraints: TAOConstraintsFunction,
        C: Vec | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute constraints.

        Logically collective.

        Parameters
        ----------
        constraints
            The callback.
        C
            The vector to hold the constraints.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        petsc.TaoSetConstraintsRoutine
        """
        ...

    # --- Hessian ---

    def setHessian(
        self,
        hessian: TAOHessianFunction,
        H: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the Hessian matrix.

        Logically collective.

        Parameters
        ----------
        hessian
            The Hessian callback.
        H
            The matrix to store the Hessian.
        P
            The matrix to construct the preconditioner.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        getHessian, setObjective, setObjectiveGradient, setGradient
        petsc.TaoSetHessian
        """
        ...

    def getHessian(self) -> tuple[Mat, Mat, TAOHessianFunction]:
        """Return the matrices used to store the Hessian and the evaluation callback.

        Not collective.

        See Also
        --------
        setHessian, petsc.TaoGetHessian
        """
        ...

    # --- Jacobian ---

    def setJacobian(
        self,
        jacobian: TAOJacobianFunction,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the Jacobian.

        Logically collective.

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

        See Also
        --------
        petsc.TaoSetJacobianRoutine
        """
        ...

    # --- State/Design ---

    def setStateDesignIS(
        self, state: IS | None = None, design: IS | None = None
    ) -> None:
        """Set the index sets indicating state and design variables.

        Collective.

        See Also
        --------
        petsc.TaoSetStateDesignIS
        """
        ...

    def setJacobianState(
        self,
        jacobian_state: TAOJacobianFunction,
        J: Mat | None = None,
        P: Mat | None = None,
        I: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set Jacobian state callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetJacobianStateRoutine
        """
        ...

    def setJacobianDesign(
        self,
        jacobian_design: TAOJacobianFunction,
        J: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set Jacobian design callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetJacobianDesignRoutine
        """
        ...

    # --- LMVM ---

    def getLMVMMat(self) -> Mat:
        """Get the LMVM matrix.

        Not collective.

        See Also
        --------
        setLMVMMat, petsc.TaoGetLMVMMatrix
        """
        ...

    def setLMVMMat(self, M: Mat) -> None:
        """Set the LMVM matrix.

        Logically collective.

        See Also
        --------
        getLMVMMat, petsc.TaoSetLMVMMatrix
        """
        ...

    # --- Equality constraints ---

    def setEqualityConstraints(
        self,
        equality_constraints: TAOConstraintsFunction,
        c: Vec,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set equality constraints callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetEqualityConstraintsRoutine
        """
        ...

    def getEqualityConstraints(
        self,
    ) -> tuple[
        Vec,
        tuple[TAOConstraintsFunction, tuple[Any, ...] | None, dict[str, Any] | None],
    ]:
        """Return tuple holding vector and callback of equality constraints.

        Not collective.

        See Also
        --------
        setEqualityConstraints, petsc.TaoGetEqualityConstraintsRoutine
        """
        ...

    def setJacobianEquality(
        self,
        jacobian_equality: TAOConstraintsJacobianFunction,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set Jacobian equality constraints callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetJacobianEqualityRoutine
        """
        ...

    def getJacobianEquality(
        self,
    ) -> tuple[
        Mat,
        Mat,
        tuple[
            TAOConstraintsJacobianFunction,
            tuple[Any, ...] | None,
            dict[str, Any] | None,
        ],
    ]:
        """Return matrix, precon matrix and callback of equality constraints Jacobian.

        Not collective.

        See Also
        --------
        setJacobianEquality, petsc.TaoGetJacobianEqualityRoutine
        """
        ...

    # --- Inequality constraints ---

    def setInequalityConstraints(
        self,
        inequality_constraints: TAOConstraintsFunction,
        c: Vec,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set inequality constraints callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetInequalityConstraintsRoutine
        """
        ...

    def getInequalityConstraints(
        self,
    ) -> tuple[
        Vec,
        tuple[TAOConstraintsFunction, tuple[Any, ...] | None, dict[str, Any] | None],
    ]:
        """Return tuple holding vector and callback of inequality constraints.

        Not collective.

        See Also
        --------
        setInequalityConstraints, petsc.TaoGetInequalityConstraintsRoutine
        """
        ...

    def setJacobianInequality(
        self,
        jacobian_inequality: TAOConstraintsJacobianFunction,
        J: Mat | None = None,
        P: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set Jacobian inequality constraints callback.

        Logically collective.

        See Also
        --------
        petsc.TaoSetJacobianInequalityRoutine
        """
        ...

    def getJacobianInequality(
        self,
    ) -> tuple[
        Mat,
        Mat,
        tuple[
            TAOConstraintsJacobianFunction,
            tuple[Any, ...] | None,
            dict[str, Any] | None,
        ],
    ]:
        """Return matrix, precon matrix and callback of ineq. constraints Jacobian.

        Not collective.

        See Also
        --------
        setJacobianInequality, petsc.TaoGetJacobianInequalityRoutine
        """
        ...

    # --- Update ---

    def setUpdate(
        self,
        update: TAOUpdateFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute update at each optimization step.

        Logically collective.

        Parameters
        ----------
        update
            The update callback or `None` to reset it.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        getUpdate, petsc.TaoSetUpdate
        """
        ...

    def getUpdate(self) -> tuple[TAOUpdateFunction, tuple[Any, ...], dict[str, Any]]:
        """Return the callback to compute the update.

        Not collective.

        See Also
        --------
        setUpdate
        """
        ...

    # --- Compute methods ---

    def computeObjective(self, x: Vec) -> float:
        """Compute the value of the objective function.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.

        See Also
        --------
        setObjective, petsc.TaoComputeObjective
        """
        ...

    def computeResidual(self, x: Vec, f: Vec) -> None:
        """Compute the residual.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        f
            The output vector.

        See Also
        --------
        setResidual, petsc.TaoComputeResidual
        """
        ...

    def computeGradient(self, x: Vec, g: Vec) -> None:
        """Compute the gradient of the objective function.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        g
            The output gradient vector.

        See Also
        --------
        setGradient, petsc.TaoComputeGradient
        """
        ...

    def computeObjectiveGradient(self, x: Vec, g: Vec) -> float:
        """Compute the gradient of the objective function and its value.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        g
            The output gradient vector.

        See Also
        --------
        setObjectiveGradient, setGradient, setObjective
        petsc.TaoComputeObjectiveAndGradient
        """
        ...

    def computeDualVariables(self, xl: Vec, xu: Vec) -> None:
        """Compute the dual vectors corresponding to variables' bounds.

        Collective.

        See Also
        --------
        petsc.TaoComputeDualVariables
        """
        ...

    def computeVariableBounds(self, xl: Vec, xu: Vec) -> None:
        """Compute the vectors corresponding to variables' bounds.

        Collective.

        See Also
        --------
        setVariableBounds, petsc.TaoComputeVariableBounds
        """
        ...

    def computeConstraints(self, x: Vec, c: Vec) -> None:
        """Compute the vector corresponding to the constraints.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        c
            The output constraints vector.

        See Also
        --------
        setVariableBounds, petsc.TaoComputeVariableBounds
        """
        ...

    def computeHessian(self, x: Vec, H: Mat, P: Mat | None = None) -> None:
        """Compute the Hessian of the objective function.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        H
            The output Hessian matrix.
        P
            The output Hessian matrix used to construct the preconditioner.

        See Also
        --------
        setHessian, petsc.TaoComputeHessian
        """
        ...

    def computeJacobian(self, x: Vec, J: Mat, P: Mat | None = None) -> None:
        """Compute the Jacobian.

        Collective.

        Parameters
        ----------
        x
            The parameter vector.
        J
            The output Jacobian matrix.
        P
            The output Jacobian matrix used to construct the preconditioner.

        See Also
        --------
        setJacobian, petsc.TaoComputeJacobian
        """
        ...

    # --- Tolerances ---

    def setTolerances(
        self,
        gatol: float | None = None,
        grtol: float | None = None,
        gttol: float | None = None,
    ) -> None:
        """Set the tolerance parameters used in the solver convergence tests.

        Collective.

        Parameters
        ----------
        gatol
            The absolute norm of the gradient, or `DETERMINE`
            to use the value when the object's type was set.
            Defaults to `CURRENT`.
        grtol
            The relative norm of the gradient with respect to the
            initial norm of the objective, or `DETERMINE` to
            use the value when the object's type was set. Defaults
            to `CURRENT`.
        gttol
            The relative norm of the gradient with respect to the
            initial norm of the gradient, or `DETERMINE` to
            use the value when the object's type was set. Defaults
            to `CURRENT`.

        See Also
        --------
        getTolerances, petsc.TaoSetTolerances
        """
        ...

    def getTolerances(self) -> tuple[float, float, float]:
        """Return the tolerance parameters used in the solver convergence tests.

        Not collective.

        Returns
        -------
        gatol : float
            The absolute norm of the gradient.
        grtol : float
            The relative norm of the gradient.
        gttol : float
            The relative norm of the gradient with respect to the
            initial norm of the gradient.

        See Also
        --------
        setTolerances, petsc.TaoGetTolerances
        """
        ...

    def setMaximumIterations(self, mit: int) -> float:
        """Set the maximum number of solver iterations.

        Collective.

        See Also
        --------
        setTolerances, petsc.TaoSetMaximumIterations
        """
        ...

    def getMaximumIterations(self) -> int:
        """Return the maximum number of solver iterations.

        Not collective.

        See Also
        --------
        setMaximumIterations, petsc.TaoGetMaximumIterations
        """
        ...

    def setMaximumFunctionEvaluations(self, mit: int) -> None:
        """Set the maximum number of objective evaluations within the solver.

        Collective.

        See Also
        --------
        setMaximumIterations, petsc.TaoSetMaximumFunctionEvaluations
        """
        ...

    def getMaximumFunctionEvaluations(self) -> int:
        """Return the maximum number of objective evaluations within the solver.

        Not collective.

        See Also
        --------
        setMaximumFunctionEvaluations, petsc.TaoGetMaximumFunctionEvaluations
        """
        ...

    def setConstraintTolerances(
        self, catol: float | None = None, crtol: float | None = None
    ) -> None:
        """Set the constraints tolerance parameters used in the solver convergence tests.

        Collective.

        Parameters
        ----------
        catol
            The absolute norm of the constraints, or `DETERMINE`
            to use the value when the object's type was set. Defaults
            to `CURRENT`.
        crtol
            The relative norm of the constraints, or `DETERMINE`
            to use the value when the object's type was set. Defaults
            to `CURRENT`.

        See Also
        --------
        getConstraintTolerances, petsc.TaoSetConstraintTolerances
        """
        ...

    def getConstraintTolerances(self) -> tuple[float, float]:
        """Return the constraints tolerance parameters used in the convergence tests.

        Not collective.

        Returns
        -------
        catol : float
            The absolute norm of the constraints.
        crtol : float
            The relative norm of the constraints.

        See Also
        --------
        setConstraintTolerances, petsc.TaoGetConstraintTolerances
        """
        ...

    # --- Convergence ---

    def setConvergenceTest(
        self,
        converged: TAOConvergedFunction | None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback used to test for solver convergence.

        Logically collective.

        Parameters
        ----------
        converged
            The callback. If `None`, reset to the default convergence test.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        getConvergenceTest, petsc.TaoSetConvergenceTest
        """
        ...

    def getConvergenceTest(
        self,
    ) -> tuple[TAOConvergedFunction, tuple[Any, ...], dict[str, Any]]:
        """Return the callback used to test for solver convergence.

        Not collective.

        See Also
        --------
        setConvergenceTest
        """
        ...

    def setConvergedReason(self, reason: ConvergedReason) -> None:
        """Set the termination flag.

        Collective.

        See Also
        --------
        getConvergedReason, petsc.TaoSetConvergedReason
        """
        ...

    def getConvergedReason(self) -> ConvergedReason:
        """Return the termination flag.

        Not collective.

        See Also
        --------
        setConvergedReason, petsc.TaoGetConvergedReason
        """
        ...

    def checkConverged(self) -> ConvergedReason:
        """Run convergence test and return converged reason.

        Collective.

        See Also
        --------
        converged
        """
        ...

    # --- Monitor ---

    def setMonitor(
        self,
        monitor: TAOMonitorFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback used to monitor solver convergence.

        Logically collective.

        Parameters
        ----------
        monitor
            The callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        getMonitor, petsc.TaoMonitorSet
        """
        ...

    def getMonitor(
        self,
    ) -> list[tuple[TAOMonitorFunction, tuple[Any, ...], dict[str, Any]]]:
        """Return the callback used to monitor solver convergence.

        Not collective.

        See Also
        --------
        setMonitor
        """
        ...

    def cancelMonitor(self) -> None:
        """Cancel all the monitors of the solver.

        Logically collective.

        See Also
        --------
        setMonitor, petsc.TaoMonitorCancel
        """
        ...

    def monitor(
        self,
        its: int | None = None,
        f: float | None = None,
        res: float | None = None,
        cnorm: float | None = None,
        step: float | None = None,
    ) -> None:
        """Monitor the solver.

        Collective.

        This function should be called without arguments,
        unless users want to modify the values internally stored by the solver.

        Parameters
        ----------
        its
            Current number of iterations
            or `None` to use the value stored internally by the solver.
        f
            Current value of the objective function
            or `None` to use the value stored internally by the solver.
        res
            Current value of the residual norm
            or `None` to use the value stored internally by the solver.
        cnorm
            Current value of the constrains norm
            or `None` to use the value stored internally by the solver.
        step
            Current value of the step
            or `None` to use the value stored internally by the solver.

        See Also
        --------
        setMonitor, petsc.TaoMonitor
        """
        ...

    # --- Solve ---

    def solve(self, x: Vec | None = None) -> None:
        """Solve the optimization problem.

        Collective.

        Parameters
        ----------
        x
            The starting vector or `None` to use the vector stored internally.

        See Also
        --------
        setSolution, getSolution, petsc.TaoSolve
        """
        ...

    # --- Gradient norm ---

    def setGradientNorm(self, mat: Mat) -> None:
        """Set the matrix used to compute inner products.

        Collective.

        See Also
        --------
        getGradientNorm, petsc.TaoSetGradientNorm
        """
        ...

    def getGradientNorm(self) -> Mat:
        """Return the matrix used to compute inner products.

        Not collective.

        See Also
        --------
        setGradientNorm, petsc.TaoGetGradientNorm
        """
        ...

    # --- LMVM H0 ---

    def setLMVMH0(self, mat: Mat) -> None:
        """Set the initial Hessian for the quasi-Newton approximation.

        Collective.

        See Also
        --------
        getLMVMH0, petsc.TaoLMVMSetH0
        """
        ...

    def getLMVMH0(self) -> Mat:
        """Return the initial Hessian for the quasi-Newton approximation.

        Not collective.

        See Also
        --------
        setLMVMH0, petsc.TaoLMVMGetH0
        """
        ...

    def getLMVMH0KSP(self) -> KSP:
        """Return the `KSP` for the inverse of the initial Hessian approximation.

        Not collective.

        See Also
        --------
        setLMVMH0, petsc.TaoLMVMGetH0KSP
        """
        ...

    # --- BNCG ---

    def setBNCGType(self, cg_type: BNCGType) -> None:
        """Set the type of the BNCG solver.

        Collective.

        See Also
        --------
        getBNCGType, petsc.TaoBNCGSetType
        """
        ...

    def getBNCGType(self) -> BNCGType:
        """Return the type of the BNCG solver.

        Not collective.

        See Also
        --------
        setBNCGType, petsc.TaoBNCGGetType
        """
        ...

    # --- Iteration ---

    def setIterationNumber(self, its: int) -> None:
        """Set the current iteration number.

        Collective.

        See Also
        --------
        getIterationNumber, petsc.TaoSetIterationNumber
        """
        ...

    def getIterationNumber(self) -> int:
        """Return the current iteration number.

        Not collective.

        See Also
        --------
        setIterationNumber, petsc.TaoGetIterationNumber
        """
        ...

    def getObjectiveValue(self) -> float:
        """Return the current value of the objective function.

        Not collective.

        See Also
        --------
        setObjective, petsc.TaoGetSolutionStatus
        """
        ...

    def getFunctionValue(self) -> float:
        """Return the current value of the objective function.

        Not collective.

        See Also
        --------
        setObjective, petsc.TaoGetSolutionStatus
        """
        ...

    def getSolutionNorm(self) -> tuple[float, float, float]:
        """Return the objective function value and the norms of gradient and constraints.

        Not collective.

        Returns
        -------
        f : float
            Current value of the objective function.
        res : float
            Current value of the residual norm.
        cnorm : float
            Current value of the constrains norm.

        See Also
        --------
        getSolutionStatus, petsc.TaoGetSolutionStatus
        """
        ...

    def getSolutionStatus(
        self,
    ) -> tuple[int, float, float, float, float, ConvergedReason]:
        """Return the solution status.

        Not collective.

        Returns
        -------
        its : int
            Current number of iterations.
        f : float
            Current value of the objective function.
        res : float
            Current value of the residual norm.
        cnorm : float
            Current value of the constrains norm.
        step : float
            Current value of the step.
        reason : ConvergedReason
            Current value of converged reason.

        See Also
        --------
        petsc.TaoGetSolutionStatus
        """
        ...

    # --- KSP ---

    def getKSP(self) -> KSP:
        """Return the linear solver used by the nonlinear solver.

        Not collective.

        See Also
        --------
        petsc.TaoGetKSP
        """
        ...

    # --- ALMM ---

    def getALMMSubsolver(self) -> TAO:
        """Return the subsolver inside the ALMM solver.

        Not collective.

        See Also
        --------
        setALMMSubsolver, petsc.TaoALMMGetSubsolver
        """
        ...

    def getALMMType(self) -> ALMMType:
        """Return the type of the ALMM solver.

        Not collective.

        See Also
        --------
        setALMMType, petsc.TaoALMMGetType
        """
        ...

    def setALMMSubsolver(self, subsolver: TAO) -> None:
        """Set the subsolver inside the ALMM solver.

        Logically collective.

        See Also
        --------
        getALMMSubsolver, petsc.TaoALMMSetSubsolver
        """
        ...

    def setALMMType(self, tao_almm_type: ALMMType) -> None:
        """Set the ALMM type of the solver.

        Logically collective.

        Parameters
        ----------
        tao_almm_type
            The type of the solver.

        See Also
        --------
        getALMMType, petsc.TaoALMMSetType
        """
        ...

    # --- BRGN ---

    def getBRGNSubsolver(self) -> TAO:
        """Return the subsolver inside the BRGN solver.

        Not collective.

        See Also
        --------
        petsc.TaoBRGNGetSubsolver
        """
        ...

    def setBRGNRegularizerObjectiveGradient(
        self,
        objgrad: TAOObjectiveGradientFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the regularizer objective and gradient.

        Logically collective.

        See Also
        --------
        petsc.TaoBRGNSetRegularizerObjectiveAndGradientRoutine
        """
        ...

    def setBRGNRegularizerHessian(
        self,
        hessian: TAOHessianFunction,
        H: Mat | None = None,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the callback to compute the regularizer Hessian.

        Logically collective.

        See Also
        --------
        petsc.TaoBRGNSetRegularizerHessianRoutine
        """
        ...

    def setBRGNRegularizerWeight(self, weight: float) -> None:
        """Set the regularizer weight.

        Collective.
        """
        ...

    def setBRGNSmoothL1Epsilon(self, epsilon: float) -> None:
        """Set the smooth L1 epsilon.

        Collective.

        See Also
        --------
        petsc.TaoBRGNSetL1SmoothEpsilon
        """
        ...

    def setBRGNDictionaryMatrix(self, D: Mat) -> None:
        """Set the dictionary matrix.

        Collective.

        See Also
        --------
        petsc.TaoBRGNSetDictionaryMatrix
        """
        ...

    def getBRGNDampingVector(self) -> Vec:
        """Return the damping vector.

        Not collective.
        """
        ...

    # --- Python ---

    def createPython(self, context: Any = None, comm: Comm | None = None) -> Self:
        """Create an optimization solver of Python type.

        Collective.

        Parameters
        ----------
        context
            An instance of the Python class implementing the required methods.
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        petsc_python_tao, setType, setPythonContext, Type.PYTHON
        """
        ...

    def setPythonContext(self, context: Any) -> None:
        """Set the instance of the class implementing the required Python methods.

        Not collective.

        See Also
        --------
        petsc_python_tao, getPythonContext
        """
        ...

    def getPythonContext(self) -> Any:
        """Return the instance of the class implementing the required Python methods.

        Not collective.

        See Also
        --------
        petsc_python_tao, setPythonContext
        """
        ...

    def setPythonType(self, py_type: str) -> None:
        """Set the fully qualified Python name of the class to be used.

        Collective.

        See Also
        --------
        petsc_python_tao, setPythonContext, getPythonType
        petsc.TaoPythonSetType
        """
        ...

    def getPythonType(self) -> str:
        """Return the fully qualified Python name of the class used by the solver.

        Not collective.

        See Also
        --------
        petsc_python_tao, setPythonContext, setPythonType
        petsc.TaoPythonGetType
        """
        ...

    # --- Line search ---

    def getLineSearch(self) -> TAOLineSearch:
        """Return the TAO Line Search object.

        Not collective.

        See Also
        -------
        petsc.TaoGetLineSearch
        """
        ...

    # --- Backward compatibility ---

    def setInitial(self, x: Vec) -> None:
        """Set the vector used to store the solution (alias for setSolution).

        Collective.

        See Also
        --------
        setSolution, getSolution, petsc.TaoSetSolution
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
    def ksp(self) -> KSP:
        """Linear solver."""
        ...

    @property
    def ftol(self) -> Any:
        """Function tolerances (broken)."""
        ...

    @ftol.setter
    def ftol(self, value: Any) -> None: ...
    @property
    def gtol(self) -> Any:
        """Gradient tolerances (broken)."""
        ...

    @gtol.setter
    def gtol(self, value: Any) -> None: ...
    @property
    def ctol(self) -> Any:
        """Constraint tolerances (broken)."""
        ...

    @ctol.setter
    def ctol(self, value: Any) -> None: ...
    @property
    def its(self) -> int:
        """Number of iterations."""
        ...

    @property
    def gnorm(self) -> float:
        """Gradient norm."""
        ...

    @property
    def cnorm(self) -> float:
        """Constraints norm."""
        ...

    @property
    def solution(self) -> Vec:
        """Solution vector."""
        ...

    @property
    def objective(self) -> float:
        """Objective value."""
        ...

    @property
    def function(self) -> float:
        """Objective value."""
        ...

    @property
    def gradient(self) -> Vec:
        """Gradient vector."""
        ...

    @property
    def reason(self) -> ConvergedReason:
        """Converged reason."""
        ...

    @property
    def iterating(self) -> bool:
        """Boolean indicating if the solver has not converged yet."""
        ...

    @property
    def converged(self) -> bool:
        """Boolean indicating if the solver has converged."""
        ...

    @property
    def diverged(self) -> bool:
        """Boolean indicating if the solver has failed."""
        ...

# --------------------------------------------------------------------

class TAOLineSearchType:
    """TAO Line Search Types."""

    UNIT: str
    ARMIJO: str
    MORETHUENTE: str
    IPM: str
    OWARMIJO: str
    GPCG: str

class TAOLineSearchConvergedReason:
    """TAO Line Search Termination Reasons."""

    # iterating
    CONTINUE_SEARCH: int
    # failed
    FAILED_INFORNAN: int
    FAILED_BADPARAMETER: int
    FAILED_ASCENT: int
    # succeeded
    SUCCESS: int
    SUCCESS_USER: int
    # halted
    HALTED_OTHER: int
    HALTED_MAXFCN: int
    HALTED_UPPERBOUND: int
    HALTED_LOWERBOUND: int
    HALTED_RTOL: int
    HALTED_USER: int

class TAOLineSearch(Object):
    """TAO Line Search."""

    Type = TAOLineSearchType
    Reason = TAOLineSearchConvergedReason

    def view(self, viewer: Viewer | None = None) -> None:
        """View the linesearch object.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.TaoLineSearchView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the linesearch object.

        Collective.

        See Also
        --------
        petsc.TaoLineSearchDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a TAO linesearch.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        Sys.getDefaultComm, petsc.TaoLineSearchCreate
        """
        ...

    def setType(self, ls_type: Type | str) -> None:
        """Set the type of the linesearch.

        Logically collective.

        Parameters
        ----------
        ls_type
            The type of the solver.

        See Also
        --------
        getType, petsc.TaoLineSearchSetType
        """
        ...

    def getType(self) -> str:
        """Return the type of the linesearch.

        Not collective.

        See Also
        --------
        setType, petsc.TaoLineSearchGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the linesearch from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.TaoLineSearchSetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Set up the internal data structures for using the linesearch.

        Collective.

        See Also
        --------
        petsc.TaoLineSearchSetUp
        """
        ...

    def setOptionsPrefix(self, prefix: str | None = None) -> None:
        """Set the prefix used for searching for options in the database.

        Logically collective.

        See Also
        --------
        petsc_options, petsc.TaoLineSearchSetOptionsPrefix
        """
        ...

    def getOptionsPrefix(self) -> str:
        """Return the prefix used for searching for options in the database.

        Not collective.

        See Also
        --------
        petsc_options, setOptionsPrefix, petsc.TaoLineSearchGetOptionsPrefix
        """
        ...

    def setObjective(
        self,
        objective: TAOLSObjectiveFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the objective function evaluation callback.

        Logically collective.

        Parameters
        ----------
        objective
            The objective function callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setGradient, setObjectiveGradient
        petsc.TaoLineSearchSetObjectiveRoutine
        """
        ...

    def setGradient(
        self,
        gradient: TAOLSGradientFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the gradient evaluation callback.

        Logically collective.

        Parameters
        ----------
        gradient
            The gradient callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setObjective, setObjectiveGradient, setHessian
        petsc.TaoLineSearchSetGradientRoutine
        """
        ...

    def setObjectiveGradient(
        self,
        objgrad: TAOLSObjectiveGradientFunction,
        args: tuple[Any, ...] | None = None,
        kargs: dict[str, Any] | None = None,
    ) -> None:
        """Set the objective function and gradient evaluation callback.

        Logically collective.

        Parameters
        ----------
        objgrad
            The objective function and gradient callback.
        args
            Positional arguments for the callback.
        kargs
            Keyword arguments for the callback.

        See Also
        --------
        setObjective, setGradient, setHessian, getObjectiveAndGradient
        petsc.TaoLineSearchSetObjectiveAndGradientRoutine
        """
        ...

    def useTAORoutine(self, tao: TAO) -> None:
        """Use the objective and gradient evaluation routines from the given Tao object.

        Logically collective.

        See Also
        --------
        petsc.TaoLineSearchUseTaoRoutines
        """
        ...

    def apply(
        self, x: Vec, g: Vec, s: Vec
    ) -> tuple[float, float, TAOLineSearchConvergedReason]:
        """Performs a line-search in a given step direction.

        Collective.

        See Also
        --------
        petsc.TaoLineSearchApply
        """
        ...

    def setInitialStepLength(self, s: float) -> None:
        """Sets the initial step length of a line search.

        Logically collective.

        See Also
        --------
        petsc.TaoLineSearchSetInitialStepLength
        """
        ...
