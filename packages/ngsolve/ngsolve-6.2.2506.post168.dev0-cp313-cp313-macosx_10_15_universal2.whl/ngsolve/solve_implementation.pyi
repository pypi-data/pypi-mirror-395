from __future__ import annotations
import functools as functools
import ngsolve.comp
from ngsolve.comp import BilinearForm
from ngsolve.comp import GridFunction
from ngsolve.comp import Preconditioner
from ngsolve.comp import Region
from ngsolve.fem import CoefficientFunction
from ngsolve.krylovspace import GMResSolver
from ngsolve.krylovspace import LinearSolver
from ngsolve.nonlinearsolvers import NewtonSolver
import typing
__all__ = ['Application', 'BND', 'BilinearForm', 'CoefficientFunction', 'Dirichlet', 'Equation', 'GMResSolver', 'GridFunction', 'LinearApplication', 'LinearSolver', 'NewtonSolver', 'NonLinearApplication', 'Preconditioner', 'Region', 'Solve', 'functools']
class Application:
    __firstlineno__: typing.ClassVar[int] = 21
    __hash__: typing.ClassVar[None] = None
    __static_attributes__: typing.ClassVar[tuple] = ('gf', 'a')
    def Solve(self, rhs, *args, dirichlet = None, pre = None, printrates: bool = False, **kwargs):
        ...
    def __eq__(self, other):
        ...
    def __init__(self, a: ngsolve.comp.BilinearForm, gf: ngsolve.comp.GridFunction):
        ...
class Dirichlet:
    __firstlineno__: typing.ClassVar[int] = 15
    __static_attributes__: typing.ClassVar[tuple] = ('region', 'cf')
    def __init__(self, cf, region):
        ...
class Equation:
    __firstlineno__: typing.ClassVar[int] = 147
    __static_attributes__: typing.ClassVar[tuple] = ('lhs', 'rhs')
    def Solve(self, *args, **kwargs):
        ...
    def __init__(self, lhs, rhs):
        ...
class LinearApplication(Application):
    __firstlineno__: typing.ClassVar[int] = 78
    __static_attributes__: typing.ClassVar[tuple] = ('vec')
    def Assemble(self):
        ...
    def Solve(self, rhs, *args, dirichlet = None, pre = None, lin_solver = None, lin_solver_args = None, printrates: bool = False):
        ...
class NonLinearApplication(Application):
    __firstlineno__: typing.ClassVar[int] = 41
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    def Solve(self, rhs = None, dirichlet = None, printing: bool = False, **kwargs):
        ...
def Solve(eq, *args, **kwargs):
    ...
def _create_lin_appl(self, gfu: ngsolve.comp.GridFunction) -> LinearApplication:
    ...
BND: ngsolve.comp.VorB  # value = <VorB.BND: 1>
