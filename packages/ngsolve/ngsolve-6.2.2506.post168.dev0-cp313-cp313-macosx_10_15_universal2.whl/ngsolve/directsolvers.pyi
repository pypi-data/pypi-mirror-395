from __future__ import annotations
import ngsolve as ngsolve
from ngsolve.comp import BilinearForm
from ngsolve.la import BaseMatrix
from ngsolve.la import BaseVector
from pyngcore.pyngcore import BitArray
import typing
__all__ = ['BaseMatrix', 'BaseVector', 'BilinearForm', 'BitArray', 'SuperLU', 'ngsolve']
class SuperLU(ngsolve.la.SparseFactorizationInterface):
    __firstlineno__: typing.ClassVar[int] = 4
    __static_attributes__: typing.ClassVar[tuple] = ('inv_mat')
    def Factor(self):
        ...
    def Solve(self, rhs, sol):
        ...
