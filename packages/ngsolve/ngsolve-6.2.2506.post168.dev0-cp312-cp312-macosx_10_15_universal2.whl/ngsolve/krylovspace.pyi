from __future__ import annotations
import logging as logging
from math import log
from netgen import TimeFunction
from netgen.libngpy._meshing.pybind11_detail_function_record_v1_system_libcpp_abi1 import _GetStatus
from netgen.libngpy._meshing.pybind11_detail_function_record_v1_system_libcpp_abi1 import _PushStatus
from netgen.libngpy._meshing.pybind11_detail_function_record_v1_system_libcpp_abi1 import _SetThreadPercentage
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import InnerProduct
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Matrix
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Vector
import ngsolve.comp
from ngsolve.comp import Preconditioner
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sqrt
import ngsolve.la
from ngsolve.la import BaseMatrix
from ngsolve.la import BaseVector
from ngsolve.la import BlockVector
from ngsolve.la import Projector
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import EigenValues_Preconditioner
import os as os
from pyngcore.pyngcore import BitArray
import typing
__all__ = ['BaseMatrix', 'BaseVector', 'BitArray', 'BlockVector', 'BramblePasciakCG', 'CG', 'CGSolver', 'EigenValues_Preconditioner', 'GMRes', 'GMResSolver', 'InnerProduct', 'LinearSolver', 'Matrix', 'MinRes', 'MinResSolver', 'Norm', 'PreconditionedRichardson', 'Preconditioner', 'Projector', 'QMR', 'QMRSolver', 'RichardsonSolver', 'TimeFunction', 'Vector', 'linear_solver_param_doc', 'log', 'logging', 'os', 'sqrt', 'update_plot']
class CGSolver(LinearSolver):
    name: typing.ClassVar[str] = 'CG'
    def _SolveImpl(self, rhs: ngsolve.la.BaseVector, sol: ngsolve.la.BaseVector):
        ...
    def __init__(self, *args, conjugate: bool = False, abstol: float = None, maxsteps: int = None, printing: bool = False, **kwargs):
        ...
    @property
    def errors(self):
        ...
class GMResSolver(LinearSolver):
    name: typing.ClassVar[str] = 'GMRes'
    def _SolveImpl(self, rhs: ngsolve.la.BaseVector, sol: ngsolve.la.BaseVector):
        ...
    def __init__(self, *args, innerproduct: typing.Optional[typing.Callable[[ngsolve.la.BaseVector, ngsolve.la.BaseVector], typing.Union[float, complex]]] = None, restart: typing.Optional[int] = None, **kwargs):
        ...
class LinearSolver(ngsolve.la.BaseMatrix):
    name: typing.ClassVar[str] = 'LinearSolver'
    @staticmethod
    def Solve(*args, **kwargs):
        ...
    def CheckResidual(self, residual):
        ...
    def CreateVector(self, col):
        ...
    def Height(self) -> int:
        ...
    def IsComplex(self) -> bool:
        ...
    def Mult(self, x: ngsolve.la.BaseVector, y: ngsolve.la.BaseVector) -> None:
        ...
    def Update(self):
        ...
    def Width(self) -> int:
        ...
    def __init__(self, mat: ngsolve.la.BaseMatrix, pre: typing.Optional[ngsolve.comp.Preconditioner] = None, freedofs: typing.Optional[pyngcore.pyngcore.BitArray] = None, tol: float = None, maxiter: int = 100, atol: float = None, callback: typing.Optional[typing.Callable[[int, float], NoneType]] = None, callback_sol: typing.Optional[typing.Callable[[ngsolve.la.BaseVector], NoneType]] = None, printrates: bool = False, plotrates: bool = False):
        ...
class MinResSolver(LinearSolver):
    def _SolveImpl(self, rhs: ngsolve.la.BaseVector, sol: ngsolve.la.BaseVector):
        ...
    def __init__(self, *args, **kwargs):
        ...
class QMRSolver(LinearSolver):
    name: typing.ClassVar[str] = 'QMR'
    def _SolveImpl(self, rhs: ngsolve.la.BaseVector, sol: ngsolve.la.BaseVector):
        ...
    def __init__(self, *args, pre2: ngsolve.comp.Preconditioner = None, ep: float = 1.0, **kwargs):
        ...
class RichardsonSolver(LinearSolver):
    name: typing.ClassVar[str] = 'Richardson'
    def _SolveImpl(self, rhs: ngsolve.la.BaseVector, sol: ngsolve.la.BaseVector):
        ...
    def __init__(self, *args, dampfactor = 1.0, **kwargs):
        ...
def BramblePasciakCG(A, B, C, f, g, preA, preS, maxit = 1000, tol = 1e-08, printrates = False):
    ...
def CG(mat, rhs, pre = None, sol = None, tol = 1e-12, maxsteps = 100, printrates = True, plotrates = False, initialize = True, conjugate = False, callback = None, **kwargs):
    """
    preconditioned conjugate gradient method
    
    
        Parameters
        ----------
    
        mat : Matrix
          The left hand side of the equation to solve. The matrix has to be spd o hermitsch.
    
        rhs : Vector
          The right hand side of the equation.
    
        pre : Preconditioner
          If provided the preconditioner is used.
    
        sol : Vector
          Start vector for CG method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.
    
        tol : double
          Tolerance of the residuum. CG stops if tolerance is reached.
    
        maxsteps : int
          Number of maximal steps for CG. If the maximal number is reached before the tolerance is reached CG stops.
    
        printrates : bool
          If set to True then the error of the iterations is displayed.
    
        plotrates : bool
          If set to True then the error of the iterations is plotted.
    
        initialize : bool
          If set to True then the initial guess for the CG method is set to zero. Otherwise the values of the vector sol, if provided, is used.
    
        conjugate : bool
          If set to True, then the complex inner product is used.
    
    
        Returns
        -------
        (vector)
          Solution vector of the CG method.
    
        
    """
def GMRes(A, b, pre = None, freedofs = None, x = None, maxsteps = 100, tol = None, innerproduct = None, callback = None, restart = None, startiteration = 0, printrates = True, reltol = None):
    """
    Restarting preconditioned gmres solver for A*x=b. Minimizes the preconditioned residuum pre*(b-A*x).
    
    Parameters
    ----------
    
    A : BaseMatrix
      The left hand side of the linear system.
    
    b : BaseVector
      The right hand side of the linear system.
    
    pre : BaseMatrix = None
      The preconditioner for the system. If no preconditioner is given, the freedofs
      of the system must be given.
    
    freedofs : BitArray = None
      Freedofs to solve on, only necessary if no preconditioner is given.
    
    x : BaseVector = None
      Startvector, if given it will be modified in the routine and returned. Will be created
      if not given.
    
    maxsteps : int = 100
      Maximum iteration steps.
    
    tol : float = 1e-7
    
    innerproduct : function = None
      Innerproduct to be used in iteration, all orthogonalizations/norms are computed with
      respect to that inner product.
    
    callback : function = None
      If given, this function is called with the solution vector x in each step. Only for debugging
    
    restart : int = None
      If given, gmres is restarted with the current solution x every 'restart' steps.
    
    startiteration : int = 0
      Internal value to count total number of iterations in restarted setup, no user input required
      here.
    
    printrates : bool = True
      Print norm of preconditioned residual in each step.
    """
def MinRes(mat, rhs, pre = None, sol = None, maxsteps = 100, printrates = True, initialize = True, tol = 1e-07):
    """
    Minimal Residuum method
    
    
        Parameters
        ----------
    
        mat : Matrix
          The left hand side of the equation to solve
    
        rhs : Vector
          The right hand side of the equation.
    
        pre : Preconditioner
          If provided the preconditioner is used.
    
        sol : Vector
          Start vector for MinRes method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.
    
        maxsteps : int
          Number of maximal steps for MinRes. If the maximal number is reached before the tolerance is reached MinRes stops.
    
        printrates : bool
          If set to True then the error of the iterations is displayed.
    
        initialize : bool
          If set to True then the initial guess for the MinRes method is set to zero. Otherwise the values of the vector sol, if prevented, is used.
    
        tol : double
          Tolerance of the residuum. MinRes stops if tolerance is reached.
    
    
        Returns
        -------
        (vector)
          Solution vector of the MinRes method.
    
        
    """
def PreconditionedRichardson(a, rhs, pre = None, freedofs = None, maxit = 100, tol = 1e-08, dampfactor = 1.0, printing = True):
    """
     Preconditioned Richardson Iteration
    
        Parameters
        ----------
        a : BilinearForm
          The left hand side of the equation to solve
    
        rhs : Vector
          The right hand side of the equation.
    
        pre : Preconditioner
          If provided the preconditioner is used.
        
        freedofs : BitArray
          The FreeDofs on which the Richardson iteration acts. If argument is 'None' then the FreeDofs of the underlying FESpace is used.
    
        maxit : int
          Number of maximal iteration for Richardson iteration. If the maximal number is reached before the tolerance is reached a warning is displayed.
    
        tol : double
          Tolerance of the residuum. Richardson iteration stops if residuum < tolerance*initial_residuum is reached.
    
        dampfactor : float
          Set the damping factor for the Richardson iteration. If it is 1 then no damping is done. Values greater than 1 are allowed.
    
        printing : bool
          Set if Richardson iteration should print informations about the actual iteration like the residuum. 
    
        Returns
        -------
        (vector)
          Solution vector of the Preconditioned Richardson iteration.
    
        
    """
def QMR(mat, rhs, fdofs, pre1 = None, pre2 = None, sol = None, maxsteps = 100, printrates = True, initialize = True, ep = 1.0, tol = 1e-07):
    """
    Quasi Minimal Residuum method
    
    
        Parameters
        ----------
    
        mat : Matrix
          The left hand side of the equation to solve
    
        rhs : Vector
          The right hand side of the equation.
    
        fdofs : BitArray
          BitArray of free degrees of freedoms.
    
        pre1 : Preconditioner
          First preconditioner if provided
    
        pre2 : Preconditioner
          Second preconditioner if provided
    
        sol : Vector
          Start vector for QMR method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.
    
        maxsteps : int
          Number of maximal steps for QMR. If the maximal number is reached before the tolerance is reached QMR stops.
    
        printrates : bool
          If set to True then the error of the iterations is displayed.
    
        initialize : bool
          If set to True then the initial guess for the QMR method is set to zero. Otherwise the values of the vector sol, if provided, is used.
    
        ep : double
          Start epsilon.
    
        tol : double
          Tolerance of the residuum. QMR stops if tolerance is reached.
    
    
        Returns
        -------
        (vector)
          Solution vector of the QMR method.
    
        
    """
def update_plot(plt, ax, its, ress):
    ...
_clear_line_command: str = '\x1b[2K'
linear_solver_param_doc: str = '\nmat : BaseMatrix\n  The left hand side of the equation to solve.\n\npre : Preconditioner, BaseMatrix = None\n  If provided, the preconditioner for the system.\n\nfreedofs : BitArray = None\n  If no preconditioner is provided, the BitArray of the FESpace freedofs must be given.\n\ntol : double = 1e-12\n  Relative tolerance for the residuum reduction.\n\nmaxiter : int = 100\n  Maximum number of iterations, if reached solver will emit a warning.\n\ncallback : Callable[[int, float], None] = None\n  Callback function that is called with iteration number and residual in each iteration step.\n\ncallback_sol : Callable[[BaseVector], None] = None\n  Callback function that is called with solution x_k in each iteration step.\n\nprintrates : bool = False\n  Print iterations to stdout. One can give a string to be passed as an `end`\n  argument to the print function, for example:\n  >>> printrates="\r"\n  will call\n  >>> print("iteration = 1, residual = 1e-3", end="\r")\n  if "\r" is passed, a final output will also be printed.\n\nplotrates : bool = False\n  matplotlib plot of errors (residuals)\n'
