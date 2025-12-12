from __future__ import annotations
import ngsolve as ngsolve
from ngsolve.comp import BilinearForm
from ngsolve.la import BaseMatrix
from ngsolve.la import BaseVector
from pyngcore.pyngcore import BitArray
__all__ = ['BaseMatrix', 'BaseVector', 'BilinearForm', 'BitArray', 'SuperLU', 'ngsolve']
class SuperLU(ngsolve.la.SparseFactorizationInterface):
    def Factor(self):
        ...
    def Solve(self, rhs, sol):
        ...
