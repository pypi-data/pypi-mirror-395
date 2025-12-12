"""
module for perfectly matched layers
"""
from __future__ import annotations
import ngsolve.bla
import ngsolve.fem
import typing
__all__ = ['BrickRadial', 'Cartesian', 'Compound', 'Custom', 'HalfSpace', 'PML', 'Radial']
class PML:
    """
    Base PML object
    
    can only be created by generator functions. Use PML(x, [y, z]) to evaluate the scaling.
    """
    @staticmethod
    def __call__(*args) -> ngsolve.bla.VectorC:
        """
        map a point
        """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def call_jacobian(*args) -> ngsolve.bla.MatrixC:
        """
        evaluate PML jacobian at point x, [y, z]
        """
    def __add__(self, pml: PML) -> PML:
        ...
    def __str__(self) -> str:
        ...
    @property
    def Det_CF(self) -> ngsolve.fem.CoefficientFunction:
        """
        the determinant of the jacobian as coefficient function
        """
    @property
    def JacInv_CF(self) -> ngsolve.fem.CoefficientFunction:
        """
        the inverse of the jacobian as coefficient function
        """
    @property
    def Jac_CF(self) -> ngsolve.fem.CoefficientFunction:
        """
        the jacobian of the PML as coefficient function
        """
    @property
    def PML_CF(self) -> ngsolve.fem.CoefficientFunction:
        """
        the scaling as coefficient function
        """
    @property
    def dim(self) -> int:
        """
        dimension
        """
def BrickRadial(mins: typing.Any, maxs: typing.Any, origin: typing.Any = (0.0, 0.0, 0.0), alpha: complex = 1j) -> PML:
    """
    radial pml on a brick
    
    mins, maxs and origin are given as tuples/lists
    """
def Cartesian(mins: typing.Any, maxs: typing.Any, alpha: complex = 1j) -> PML:
    """
    cartesian pml transformation
    
    mins and maxs are tuples/lists determining the dimension
    """
def Compound(pml1: PML, pml2: PML, dims1: typing.Any = None, dims2: typing.Any = None) -> PML:
    """
    tensor product of two pml transformations
    
            dimensions are optional, given as tuples/lists and start with 1
    """
def Custom(trafo: ngsolve.fem.CoefficientFunction, jac: ngsolve.fem.CoefficientFunction) -> PML:
    """
    custom pml transformation
    
    trafo and jac are coefficient functions of the scaling and the jacobian
    """
def HalfSpace(point: typing.Any, normal: typing.Any, alpha: complex = 1j) -> PML:
    """
    half space pml
    
    scales orthogonal to specified plane in direction of normal point and normal are given as tuples/lists determining the dimension
    """
def Radial(origin: typing.Any, rad: typing.SupportsFloat = 1, alpha: complex = 1j) -> PML:
    """
    radial pml transformation
    
    origin is a list/tuple with as many entries as dimenson
    """
