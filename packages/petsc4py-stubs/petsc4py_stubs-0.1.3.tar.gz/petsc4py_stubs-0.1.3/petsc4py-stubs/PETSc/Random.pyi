"""Type stubs for PETSc Random module."""


from typing import Self

from .Object import Object

from .Comm import Comm
from .Viewer import Viewer

# Import types from typing module
from petsc4py.typing import Scalar

class RandomType:
    """The random number generator type."""

    RAND: str
    RAND48: str
    SPRNG: str
    RANDER48: str
    RANDOM123: str

class Random(Object):
    """The random number generator object.

    See Also
    --------
    petsc.PetscRandom
    """

    Type = RandomType

    def __init__(self) -> None: ...
    def __call__(self) -> Scalar:
        """Generate a scalar random number.

        Not collective.

        See Also
        --------
        petsc.PetscRandomGetValue
        """
        ...

    def view(self, viewer: Viewer | None = None) -> None:
        """View a random number generator object.

        Collective.

        Parameters
        ----------
        viewer
            A `Viewer` instance or `None` for the default viewer.

        See Also
        --------
        petsc.PetscRandomView
        """
        ...

    def destroy(self) -> Self:
        """Destroy the random number generator object.

        Collective.

        See Also
        --------
        petsc.PetscRandomDestroy
        """
        ...

    def create(self, comm: Comm | None = None) -> Self:
        """Create a random number generator object.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to `Sys.getDefaultComm`.

        See Also
        --------
        Sys.getDefaultComm, petsc.PetscRandomCreate
        """
        ...

    def setType(self, rnd_type: RandomType | str) -> None:
        """Set the type of the random number generator object.

        Collective.

        Parameters
        ----------
        rnd_type
            The type of the generator.

        See Also
        --------
        getType, petsc.PetscRandomSetType
        """
        ...

    def getType(self) -> str:
        """Return the type of the random number generator object.

        Not collective.

        See Also
        --------
        setType, petsc.PetscRandomGetType
        """
        ...

    def setFromOptions(self) -> None:
        """Configure the random number generator from the options database.

        Collective.

        See Also
        --------
        petsc_options, petsc.PetscRandomSetFromOptions
        """
        ...

    def getValue(self) -> Scalar:
        """Generate a scalar random number.

        Not collective.

        See Also
        --------
        petsc.PetscRandomGetValue
        """
        ...

    def getValueReal(self) -> float:
        """Generate a real random number.

        Not collective.

        See Also
        --------
        petsc.PetscRandomGetValueReal
        """
        ...

    def getSeed(self) -> int:
        """Return the random number generator seed.

        Not collective.

        See Also
        --------
        setSeed, petsc.PetscRandomGetSeed
        """
        ...

    def setSeed(self, seed: int | None = None) -> None:
        """Set the seed of random number generator.

        Not collective.

        Parameters
        ----------
        seed
            The value for the seed. If `None`, it only seeds the generator.

        See Also
        --------
        getSeed, petsc.PetscRandomSetSeed, petsc.PetscRandomSeed
        """
        ...

    def getInterval(self) -> tuple[Scalar, Scalar]:
        """Return the interval containing the random numbers generated.

        Not collective.

        See Also
        --------
        setInterval, petsc.PetscRandomGetInterval
        """
        ...

    def setInterval(self, interval: tuple[Scalar, Scalar]) -> None:
        """Set the interval of the random number generator.

        Not collective.

        See Also
        --------
        getInterval, petsc.PetscRandomSetInterval
        """
        ...

    @property
    def seed(self) -> int:
        """The seed of the random number generator."""
        ...

    @seed.setter
    def seed(self, value: int | None) -> None: ...
    @property
    def interval(self) -> tuple[Scalar, Scalar]:
        """The interval of the generated random numbers."""
        ...

    @interval.setter
    def interval(self, value: tuple[Scalar, Scalar]) -> None: ...
