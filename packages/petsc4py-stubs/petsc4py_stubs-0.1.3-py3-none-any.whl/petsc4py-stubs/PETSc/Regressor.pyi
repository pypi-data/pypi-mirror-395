"""Type stubs for PETSc Regressor module."""


from typing import Self

from .Object import Object

from .Comm import Comm
from .Vec import Vec
from .Mat import Mat
from .Viewer import Viewer
from .TAO import TAO
from .KSP import KSP

# Import types from typing module
from petsc4py.typing import Scalar


class RegressorType:
    """REGRESSOR solver type.

    See Also
    --------
    petsc.PetscRegressorType
    """

    LINEAR: str


class RegressorLinearType:
    """Linear regressor type.

    See Also
    --------
    petsc.PetscRegressorLinearType
    """

    OLS: int
    LASSO: int
    RIDGE: int


class Regressor(Object):
    """Regression solver.

    REGRESSOR is described in the PETSc manual.

    See Also
    --------
    petsc.PetscRegressor
    """

    Type = RegressorType
    LinearType = RegressorLinearType

    def view(self, viewer: Viewer | None = None) -> None:
        """View the solver.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.PetscRegressorView
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a REGRESSOR solver.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        Sys.getDefaultComm, petsc.PetscRegressorCreate
        """
        ...

    def setRegularizerWeight(self, weight: float) -> None:
        """Set the weight to be used for the regularizer.

        Logically collective.

        See Also
        --------
        setType, petsc.PetscRegressorSetRegularizerWeight
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the solver from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.PetscRegressorSetFromOptions
        """
        ...

    def setUp(self) -> None:
        """Set up the internal data structures for using the solver.

        Collective.

        See Also
        --------
        petsc.PetscRegressorSetUp
        """
        ...

    def fit(self, X: Mat, y: Vec) -> None:
        """Fit the regression problem.

        Collective.

        Parameters
        ----------
        X
            The matrix of training data
        y
            The vector of target values from the training dataset

        See Also
        --------
        petsc.PetscRegressorPredict
        """
        ...

    def predict(self, X: Mat, y: Vec) -> None:
        """Predict the regression problem.

        Collective.

        Parameters
        ----------
        X
            The matrix of unlabeled observations
        y
            The vector of predicted labels

        See Also
        --------
        petsc.PetscRegressorFit
        """
        ...

    def getTAO(self) -> TAO:
        """Return the underlying `TAO` object.

        Not collective.

        See Also
        --------
        getLinearKSP, petsc.PetscRegressorGetTao
        """
        ...

    def reset(self) -> None:
        """Destroy internal data structures of the solver.

        Collective.

        See Also
        --------
        petsc.PetscRegressorDestroy
        """
        ...

    def destroy(self) -> Self:
        """Destroy the solver.

        Collective.

        See Also
        --------
        petsc.PetscRegressorDestroy
        """
        ...

    def setType(self, regressor_type: RegressorType | str) -> None:
        """Set the type of the solver.

        Logically collective.

        Parameters
        ----------
        regressor_type
            The type of the solver.

        See Also
        --------
        getType, petsc.PetscRegressorSetType
        """
        ...

    def getType(self) -> str:
        """Return the type of the solver.

        Not collective.

        See Also
        --------
        setType, petsc.PetscRegressorGetType
        """
        ...

    # --- Linear ---

    def setLinearFitIntercept(self, flag: bool) -> None:
        """Set a flag to indicate that the intercept should be calculated.

        Logically collective.

        See Also
        --------
        petsc.PetscRegressorLinearSetFitIntercept
        """
        ...

    def setLinearUseKSP(self, flag: bool) -> None:
        """Set a flag to indicate that `KSP` instead of `TAO` solvers should be used.

        Logically collective.

        See Also
        --------
        petsc.PetscRegressorLinearSetUseKSP
        """
        ...

    def getLinearKSP(self) -> KSP:
        """Returns the `KSP` context used by the linear regressor.

        Not collective.

        See Also
        --------
        petsc.PetscRegressorLinearGetKSP
        """
        ...

    def getLinearCoefficients(self) -> Vec:
        """Get a vector of the fitted coefficients from a linear regression model.

        Not collective.

        See Also
        --------
        getLinearIntercept, petsc.PetscRegressorLinearGetCoefficients
        """
        ...

    def getLinearIntercept(self) -> Scalar:
        """Get the intercept from a linear regression model.

        Not collective.

        See Also
        --------
        setLinearFitIntercept, petsc.PetscRegressorLinearGetIntercept
        """
        ...

    def setLinearType(self, lineartype: RegressorLinearType) -> None:
        """Set the type of linear regression to be performed.

        Logically collective.

        See Also
        --------
        getLinearType, petsc.PetscRegressorLinearSetType
        """
        ...

    def getLinearType(self) -> RegressorLinearType:
        """Return the type of the linear regressor.

        Not collective.

        See Also
        --------
        setLinearType, petsc.PetscRegressorLinearGetType
        """
        ...
