"""Type stubs for PETSc DMUtils module."""


from typing import Self

# Import types from other modules
from .DM import DM
from .Comm import Comm
from .Vec import Vec

class DMInterpolation:
    """Interpolation on a mesh.

    Used for interpolating field values at arbitrary points within a mesh.
    """

    def create(self, comm: Comm | None = None) -> Self:
        """Create a DMInterpolation context.

        Collective.

        Parameters
        ----------
        comm
            MPI communicator, defaults to COMM_SELF.
        """
        ...

    def destroy(self) -> Self:
        """Destroy the DMInterpolation context.

        Collective.
        """
        ...

    def evaluate(self, dm: DM, x: Vec, v: Vec | None = None) -> Vec:
        """Calculate interpolated field values at the interpolation points.

        Collective.

        Parameters
        ----------
        dm
            The DM.
        x
            The local vector containing the field to be interpolated.
        v
            A vector capable of holding the interpolated field values.

        Returns
        -------
        Vec
            The vector containing the interpolated field values.
        """
        ...

    def getCoordinates(self) -> Vec:
        """Return the coordinates of each interpolation point.

        Collective.

        The local vector entries correspond to interpolation points lying on
        this process, according to the associated DM.
        """
        ...

    def getDim(self) -> int:
        """Return the spatial dimension of the interpolation context.

        Not collective.
        """
        ...

    def getDof(self) -> int:
        """Return the number of fields interpolated at a point.

        Not collective.
        """
        ...

    def setDim(self, dim: int) -> None:
        """Set the spatial dimension for the interpolation context.

        Not collective.

        Parameters
        ----------
        dim
            The spatial dimension.
        """
        ...

    def setDof(self, dof: int) -> None:
        """Set the number of fields interpolated at a point.

        Not collective.

        Parameters
        ----------
        dof
            The number of fields.
        """
        ...

    def setUp(
        self, dm: DM, redundantPoints: bool = False, ignoreOutsideDomain: bool = False
    ) -> None:
        """Compute spatial indices for point location during interpolation.

        Collective.

        Parameters
        ----------
        dm
            The DM for the function space used for interpolation.
        redundantPoints
            If True, all processes are passing in the same array of points.
            Otherwise, points need to be communicated among processes.
        ignoreOutsideDomain
            Ignore points outside of the domain if True; otherwise, return an
            error.
        """
        ...

    def getVector(self) -> Vec:
        """Return a Vec which can hold all the interpolated field values.

        Collective.

        This vector should be returned using restoreVector.
        """
        ...

    def restoreVector(self, vec: Vec) -> None:
        """Restore a Vec which can hold all the interpolated field values.

        Collective.

        Parameters
        ----------
        vec
            A vector capable of holding the interpolated field values.
        """
        ...
