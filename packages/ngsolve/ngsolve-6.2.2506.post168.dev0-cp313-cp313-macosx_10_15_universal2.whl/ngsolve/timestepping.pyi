from __future__ import annotations
import ngsolve as ngs
import ngsolve.comp
import ngsolve.fem
import ngsolve.krylovspace
import typing
__all__ = ['CrankNicolson', 'ImplicitEuler', 'Newmark', 'ngs']
class CrankNicolson:
    __firstlineno__: typing.ClassVar[int] = 129
    __static_attributes__: typing.ClassVar[tuple] = ('bfmstar', '_lin_solver_args', 'dt', 'time', '_lin_solver_cls', 'gfu_old', 'c')
    def Integrate(self, u_start: ngsolve.comp.GridFunction, end_time: float, start_time: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None, callback: typing.Optional[typing.Callable] = None):
        ...
    def Step(self, u: ngsolve.comp.GridFunction, dt: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None):
        ...
    def __init__(self, equation: ngsolve.comp.SumOfIntegrals, dt: typing.Union[float, ngsolve.fem.Parameter], time: ngsolve.fem.Parameter = ..., pc_cls: typing.Type = ngsolve.comp.MultiGridPreconditioner, pc_args: typing.Optional[dict] = None, lin_solver_cls: typing.Type = ngsolve.krylovspace.CGSolver, lin_solver_args: typing.Optional[dict] = None):
        ...
class ImplicitEuler:
    __firstlineno__: typing.ClassVar[int] = 5
    __static_attributes__: typing.ClassVar[tuple] = ('bfmstar', '_lin_solver_args', 'time', 'dt', '_lin_solver_cls', 'gfu_old', 'c')
    def Integrate(self, u_start: ngsolve.comp.GridFunction, end_time: float, start_time: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None, callback: typing.Optional[typing.Callable] = None):
        ...
    def Step(self, u: ngsolve.comp.GridFunction, dt: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None):
        ...
    def __init__(self, equation: ngsolve.comp.SumOfIntegrals, dt: typing.Union[float, ngsolve.fem.Parameter], time: ngsolve.fem.Parameter = ..., pc_cls: typing.Type = ngsolve.comp.MultiGridPreconditioner, pc_args: typing.Optional[dict] = None, lin_solver_cls: typing.Type = ngsolve.krylovspace.CGSolver, lin_solver_args: typing.Optional[dict] = None):
        ...
class Newmark:
    __firstlineno__: typing.ClassVar[int] = 58
    __static_attributes__: typing.ClassVar[tuple] = ('gfa_old', 'bfmstar', '_lin_solver_args', 'dt', 'time', '_lin_solver_cls', 'gfv_old', 'gfu_old', 'c')
    def Integrate(self, u: ngsolve.comp.GridFunction, end_time: float, v: typing.Optional[ngsolve.comp.GridFunction] = None, a: typing.Optional[ngsolve.comp.GridFunction] = None, start_time: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None, callback: typing.Optional[typing.Callable] = None):
        ...
    def Step(self, u: ngsolve.comp.GridFunction, v: ngsolve.comp.GridFunction, a: ngsolve.comp.GridFunction, dt: typing.Optional[float] = None, newton_args: typing.Optional[dict] = None):
        ...
    def __init__(self, equation: ngsolve.comp.SumOfIntegrals, dt: typing.Union[float, ngsolve.fem.Parameter], time: ngsolve.fem.Parameter = ..., pc_cls: typing.Type = ngsolve.comp.MultiGridPreconditioner, pc_args: typing.Optional[dict] = None, lin_solver_cls: typing.Type = ngsolve.krylovspace.CGSolver, lin_solver_args: typing.Optional[dict] = None):
        ...
