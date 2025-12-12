from __future__ import annotations
from math import sqrt
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Matrix
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Vector
from ngsolve.la import IdentityMatrix
from ngsolve.la import MultiVector
from ngsolve.la import Projector
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import InnerProduct
__all__ = ['Arnoldi', 'IdentityMatrix', 'InnerProduct', 'LOBPCG', 'Matrix', 'MultiVector', 'Norm', 'Orthogonalize', 'PINVIT', 'PINVIT1', 'Projector', 'SOAR', 'TOAR', 'Vector', 'sqrt']
def Arnoldi(mat, tol = 1e-10, maxiter = 200):
    ...
def LOBPCG(mata, matm, pre, num = 1, maxit = 20, initial = None, printrates = True, largest = False):
    """
    Knyazev's cg-like extension of PINVIT
    """
def Orthogonalize(vecs, mat):
    ...
def PINVIT(mata, matm, pre, num = 1, maxit = 20, printrates = True, GramSchmidt = True):
    """
    preconditioned inverse iteration
    """
def PINVIT1(mata, matm, pre, num = 1, maxit = 20, printrates = True, GramSchmidt = False):
    """
    preconditioned inverse iteration
    """
def SOAR(A, B, maxiter = 200):
    ...
def TOAR(A, B, maxiter = 200):
    ...
