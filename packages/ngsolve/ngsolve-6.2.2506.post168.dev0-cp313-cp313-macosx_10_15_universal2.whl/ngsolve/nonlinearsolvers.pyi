from __future__ import annotations
from math import sqrt
from netgen import TimeFunction
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
from ngsolve.la import Projector
from ngsolve.la import SparseFactorizationInterface
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import InnerProduct
import typing
__all__ = ['InnerProduct', 'Newton', 'NewtonMinimization', 'NewtonSolver', 'Norm', 'Projector', 'SparseFactorizationInterface', 'TimeFunction', 'sqrt']
class NewtonSolver:
    __firstlineno__: typing.ClassVar[int] = 6
    __static_attributes__: typing.ClassVar[tuple] = ('freedofs', 'r', 'rhs', 'inv', 'w', 'lin_solver_cls', 'inverse', 'a', 'uh', 'u', 'lin_solver_args')
    @staticmethod
    def Solve(*args, **kwargs):
        ...
    def SetDirichlet(self, dirichletvalues):
        ...
    def _UpdateInverse(self):
        ...
    def __init__(self, a, u, rhs = None, freedofs = None, inverse = '', solver = None, lin_solver_cls = None, lin_solver_args = None):
        ...
def Newton(a, u, freedofs = None, maxit = 100, maxerr = 1e-11, inverse = '', dirichletvalues = None, dampfactor = 1, printing = True, callback = None):
    """
    
    Newton's method for solving non-linear problems of the form A(u)=0.
    
    Parameters
    ----------
    a : BilinearForm
      The BilinearForm of the non-linear variational problem. It does not have to be assembled.
    
    u : GridFunction
      The GridFunction where the solution is saved. The values are used as initial guess for Newton's method.
    
    freedofs : BitArray
      The FreeDofs on which the assembled matrix is inverted. If argument is 'None' then the FreeDofs of the underlying FESpace is used.
    
    maxit : int
      Number of maximal iteration for Newton. If the maximal number is reached before the maximal error Newton might no converge and a warning is displayed.
    
    maxerr : float
      The maximal error which Newton should reach before it stops. The error is computed by the square root of the inner product of the residuum and the correction.
    
    inverse : string
      A string of the sparse direct solver which should be solved for inverting the assembled Newton matrix.
    
    dampfactor : float
      Set the damping factor for Newton's method. If dampfactor is 1 then no damping is done. If value is < 1 then the damping is done by the formula 'min(1,dampfactor*numit)' for the correction, where 'numit' denotes the Newton iteration.
    
    printing : bool
      Set if Newton's method should print informations about the actual iteration like the error. 
    
    Returns
    -------
    (int, int)
      List of two integers. The first one is 0 if Newton's method did converge, -1 otherwise. The second one gives the number of Newton iterations needed.
    
    """
def NewtonMinimization(a, u, freedofs = None, maxit = 100, maxerr = 1e-11, inverse = '', dampfactor = 1, linesearch = False, printing = True, callback = None):
    """
    
    Newton's method for solving non-linear problems of the form A(u)=0 involving energy integrators.
    
    
    Parameters
    ----------
    a : BilinearForm
      The BilinearForm of the non-linear variational problem. It does not have to be assembled.
    
    u : GridFunction
      The GridFunction where the solution is saved. The values are used as initial guess for Newton's method.
    
    freedofs : BitArray
      The FreeDofs on which the assembled matrix is inverted. If argument is 'None' then the FreeDofs of the underlying FESpace is used.
    
    maxit : int
      Number of maximal iteration for Newton. If the maximal number is reached before the maximal error Newton might no converge and a warning is displayed.
    
    maxerr : float
      The maximal error which Newton should reach before it stops. The error is computed by the square root of the inner product of the residuum and the correction.
    
    inverse : string
      A string of the sparse direct solver which should be solved for inverting the assembled Newton matrix.
    
    dampfactor : float
      Set the damping factor for Newton's method. If dampfactor is 1 then no damping is done. If value is < 1 then the damping is done by the formula 'min(1,dampfactor*numit)' for the correction, where 'numit' denotes the Newton iteration.
    
    linesearch : bool
      If True then linesearch is used to guarantee that the energy decreases in every Newton iteration.
    
    printing : bool
      Set if Newton's method should print informations about the actual iteration like the error. 
    
    Returns
    -------
    (int, int)
      List of two integers. The first one is 0 if Newton's method did converge, -1 otherwise. The second one gives the number of Newton iterations needed.
    
    """
