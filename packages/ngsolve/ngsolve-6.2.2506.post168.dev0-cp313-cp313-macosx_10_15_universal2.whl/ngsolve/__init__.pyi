"""

NGSolve
=======

A high order finite element library

Modules:
ngsolve.bla .... simple vectors and matrices
ngsolve.fem .... finite elements and integrators
ngsolve.comp ... function spaces, forms
"""
from __future__ import annotations
import atexit as atexit
from builtins import sum as builtin_sum
import netgen as netgen
from netgen import Redraw
from netgen import TimeFunction
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import InnerProduct
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Matrix
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Vector
from ngsolve.comp import APhiHCurlAMG
from ngsolve.comp import BilinearForm
from ngsolve.comp import COUPLING_TYPE
from ngsolve.comp import Compress
from ngsolve.comp import ContactBoundary
from ngsolve.comp import Discontinuous
from ngsolve.comp import ElementId
from ngsolve.comp import FESpace
from ngsolve.comp import FacetFESpace
from ngsolve.comp import FacetSurface
from ngsolve.comp import GridFunction
from ngsolve.comp import H1
from ngsolve.comp import H1LumpingFESpace
from ngsolve.comp import HCurl
from ngsolve.comp import HCurlAMG
from ngsolve.comp import HCurlCurl
from ngsolve.comp import HCurlDiv
from ngsolve.comp import HDiv
from ngsolve.comp import HDivDiv
from ngsolve.comp import HDivDivSurface
from ngsolve.comp import HDivSurface
from ngsolve.comp import Hidden
from ngsolve.comp import Hidden as PrivateSpace
from ngsolve.comp import L2
from ngsolve.comp import LinearForm
from ngsolve.comp import MatrixValued
from ngsolve.comp import Mesh
from ngsolve.comp import MultiGridPreconditioner
from ngsolve.comp import NodalFESpace
from ngsolve.comp import NodeId
from ngsolve.comp import NormalFacetFESpace
from ngsolve.comp import NormalFacetSurface
from ngsolve.comp import NumberSpace
from ngsolve.comp import ORDER_POLICY
from ngsolve.comp import Periodic
from ngsolve.comp import PlateauFESpace
from ngsolve.comp import Preconditioner
from ngsolve.comp import ProductSpace
from ngsolve.comp import Region
from ngsolve.comp import SurfaceL2
from ngsolve.comp import TangentialFacetFESpace
from ngsolve.comp import TangentialSurfaceL2
from ngsolve.comp import VTKOutput
from ngsolve.comp import Variation
from ngsolve.comp import VectorFacetFESpace
from ngsolve.comp import VectorFacetSurface
from ngsolve.comp import VectorH1
from ngsolve.comp import VectorL2
from ngsolve.comp import VectorNodalFESpace
from ngsolve.comp import VectorSurfaceL2
from ngsolve.comp import VectorValued
from ngsolve.comp import pml
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import BoundaryFromVolumeCF
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompressCompound
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import ConvertOperator
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Integrate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Interpolate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import PatchwiseSolve
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetHeapSize
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetTestoutFile
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicBFI
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicEnergy
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicLFI
from ngsolve.fem import BFI
from ngsolve.fem import BSpline
from ngsolve.fem import CoefficientFunction as CF
from ngsolve.fem import CoefficientFunction
from ngsolve.fem import ET
from ngsolve.fem import IntegrationRule
from ngsolve.fem import LFI
from ngsolve.fem import Parameter
from ngsolve.fem import ParameterC
from ngsolve.fem import PlaceholderCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CacheCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cof
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Conj
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cross
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Det
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Id
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import IfPos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Inv
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Skew
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Sym
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Trace
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import VoxelCoefficient
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Zero as ZeroCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import acos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import asin
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import atan
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import atan2
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import ceil
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import cos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import cosh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import erf
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import exp
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import floor
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import log
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import pow
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sin
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sinh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sqrt
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import tan
from ngsolve.la import BaseMatrix
from ngsolve.la import BaseVector
from ngsolve.la import BlockMatrix
from ngsolve.la import BlockVector
from ngsolve.la import ConstEBEMatrix
from ngsolve.la import DiagonalMatrix
from ngsolve.la import Embedding
from ngsolve.la import IdentityMatrix
from ngsolve.la import MultiVector
from ngsolve.la import PARALLEL_STATUS
from ngsolve.la import ParallelMatrix
from ngsolve.la import PermutationMatrix
from ngsolve.la import Projector
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import ArnoldiSolver
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import CGSolver
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import CreateVVector
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import GMRESSolver
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import QMRSolver
from ngsolve.ngstd import IntRange
from ngsolve.solve.pybind11_detail_function_record_v1_system_libcpp_abi1 import Draw
from ngsolve.solve.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetVisualization
from ngsolve.solve_implementation.Application import Solve
from ngsolve.timing import Timing
from ngsolve.utils import Deviator
from ngsolve.utils import Grad
from ngsolve.utils import Normalize
from ngsolve.utils import OuterProduct
from ngsolve.utils import PyCof
from ngsolve.utils import PyCross
from ngsolve.utils import PyDet
from ngsolve.utils import PyId
from ngsolve.utils import PyInv
from ngsolve.utils import PySkew
from ngsolve.utils import PySym
from ngsolve.utils import PyTrace
from ngsolve.utils import curl
from ngsolve.utils import div
from ngsolve.utils import grad
from ngsolve.utils import printonce
import os as os
from pyngcore.pyngcore import BitArray
from pyngcore.pyngcore import PajeTrace
from pyngcore.pyngcore import TaskManager
from pyngcore.pyngcore import Timer
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetNumThreads
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import Timers
import sys as sys
from . import bla
from . import bvp
from . import comp
from . import config
from . import directsolvers
from . import eigenvalues
from . import fem
from . import krylovspace
from . import la
from . import ngstd
from . import nonlinearsolvers
from . import preconditioners
from . import solve
from . import solve_implementation
from . import solvers
from . import timestepping
from . import timing
from . import utils
__all__ = ['APhiHCurlAMG', 'ArnoldiSolver', 'BBBND', 'BBND', 'BFI', 'BND', 'BSpline', 'BaseMatrix', 'BaseVector', 'BilinearForm', 'BitArray', 'BlockBFI', 'BlockLFI', 'BlockMatrix', 'BlockVector', 'BoundaryFromVolumeCF', 'CELL', 'CF', 'CGSolver', 'COUPLING_TYPE', 'CacheCF', 'CoefficientFunction', 'Cof', 'CompoundBFI', 'CompoundLFI', 'Compress', 'CompressCompound', 'Conj', 'ConstEBEMatrix', 'ContactBoundary', 'ConvertOperator', 'CreateVVector', 'Cross', 'Det', 'Deviator', 'DiagonalMatrix', 'Discontinuous', 'Draw', 'EDGE', 'ELEMENT', 'ET', 'ElementId', 'Embedding', 'FACE', 'FACET', 'FESpace', 'FacetFESpace', 'FacetSurface', 'GMRESSolver', 'Grad', 'GridFunction', 'H1', 'H1LumpingFESpace', 'HCurl', 'HCurlAMG', 'HCurlCurl', 'HCurlDiv', 'HDiv', 'HDivDiv', 'HDivDivSurface', 'HDivSurface', 'HEX', 'Hidden', 'Id', 'IdentityMatrix', 'IfPos', 'InnerProduct', 'IntRange', 'Integrate', 'IntegrationRule', 'Interpolate', 'Inv', 'L2', 'LFI', 'LinearForm', 'Matrix', 'MatrixValued', 'Mesh', 'MultiGridPreconditioner', 'MultiVector', 'NodalFESpace', 'NodeId', 'Norm', 'NormalFacetFESpace', 'NormalFacetSurface', 'Normalize', 'NumberSpace', 'ORDER_POLICY', 'OuterProduct', 'PARALLEL_STATUS', 'POINT', 'PRISM', 'PYRAMID', 'PajeTrace', 'ParallelMatrix', 'Parameter', 'ParameterC', 'PatchwiseSolve', 'Periodic', 'PermutationMatrix', 'PlaceholderCF', 'PlateauFESpace', 'Preconditioner', 'PrivateSpace', 'ProductSpace', 'Projector', 'PyCof', 'PyCross', 'PyDet', 'PyId', 'PyInv', 'PySkew', 'PySym', 'PyTrace', 'QMRSolver', 'QUAD', 'Redraw', 'Region', 'SEGM', 'SetHeapSize', 'SetNumThreads', 'SetTestoutFile', 'SetVisualization', 'Skew', 'Solve', 'SurfaceL2', 'Sym', 'SymbolicBFI', 'SymbolicEnergy', 'SymbolicLFI', 'TET', 'TRIG', 'TangentialFacetFESpace', 'TangentialSurfaceL2', 'TaskManager', 'TimeFunction', 'Timer', 'Timers', 'Timing', 'Trace', 'VERTEX', 'VOL', 'VTKOutput', 'Variation', 'Vector', 'VectorFacetFESpace', 'VectorFacetSurface', 'VectorH1', 'VectorL2', 'VectorNodalFESpace', 'VectorSurfaceL2', 'VectorValued', 'VoxelCoefficient', 'ZeroCF', 'acos', 'asin', 'atan', 'atan2', 'atexit', 'bla', 'builtin_sum', 'bvp', 'ceil', 'comp', 'config', 'cos', 'cosh', 'curl', 'directsolvers', 'div', 'ds', 'dx', 'eigenvalues', 'erf', 'exp', 'fem', 'floor', 'grad', 'krylovspace', 'la', 'log', 'netgen', 'ngsglobals', 'ngslib', 'ngstd', 'nonlinearsolvers', 'os', 'pi', 'pml', 'pow', 'preconditioners', 'printonce', 'sin', 'sinh', 'solve', 'solve_implementation', 'solvers', 'specialcf', 'sqrt', 'sum', 'sys', 'tan', 'timestepping', 'timing', 'unit_cube', 'unit_square', 'utils', 'x', 'y', 'z']
def _add_flags_doc(module):
    ...
def _jupyter_nbextension_paths():
    ...
def sum(iterable, start = None):
    """
    NGSolve sum function that uses the first element of an iterable as
    start argument if no start argument is provided.
    """
BBBND: comp.VorB  # value = <VorB.BBBND: 3>
BBND: comp.VorB  # value = <VorB.BBND: 2>
BND: comp.VorB  # value = <VorB.BND: 1>
CELL: fem.NODE_TYPE  # value = <NODE_TYPE.CELL: 3>
EDGE: fem.NODE_TYPE  # value = <NODE_TYPE.EDGE: 1>
ELEMENT: fem.NODE_TYPE  # value = <NODE_TYPE.ELEMENT: 4>
FACE: fem.NODE_TYPE  # value = <NODE_TYPE.FACE: 2>
FACET: fem.NODE_TYPE  # value = <NODE_TYPE.FACET: 5>
HEX: fem.ET  # value = <ET.HEX: 24>
POINT: fem.ET  # value = <ET.POINT: 0>
PRISM: fem.ET  # value = <ET.PRISM: 22>
PYRAMID: fem.ET  # value = <ET.PYRAMID: 21>
QUAD: fem.ET  # value = <ET.QUAD: 11>
SEGM: fem.ET  # value = <ET.SEGM: 1>
TET: fem.ET  # value = <ET.TET: 20>
TRIG: fem.ET  # value = <ET.TRIG: 10>
VERTEX: fem.NODE_TYPE  # value = <NODE_TYPE.VERTEX: 0>
VOL: comp.VorB  # value = <VorB.VOL: 0>
__version__: str = '6.2.2506-168-g9f2571191'
ds: comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
dx: comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
ngsglobals: comp.GlobalVariables  # value = <ngsolve.comp.GlobalVariables object>
pi: float = 3.141592653589793
specialcf: fem.SpecialCFCreator  # value = <ngsolve.fem.SpecialCFCreator object>
unit_cube: netgen.libngpy._NgOCC.OCCGeometry  # value = <netgen.libngpy._NgOCC.OCCGeometry object>
unit_square: netgen.libngpy._NgOCC.OCCGeometry  # value = <netgen.libngpy._NgOCC.OCCGeometry object>
x: fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
y: fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
z: fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
ngslib = 
