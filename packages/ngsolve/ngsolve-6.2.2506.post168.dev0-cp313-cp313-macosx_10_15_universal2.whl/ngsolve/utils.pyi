from __future__ import annotations
from netgen import TimeFunction
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
import ngsolve.comp
from ngsolve.comp import APhiHCurlAMG
from ngsolve.comp import Array_N6ngcomp13COUPLING_TYPEE_S
from ngsolve.comp import BDDCPreconditioner
from ngsolve.comp import BDDCPreconditioner_complex
from ngsolve.comp import BDDCPreconditioner_double
from ngsolve.comp import BilinearForm
from ngsolve.comp import COUPLING_TYPE
from ngsolve.comp import ComponentGridFunction
from ngsolve.comp import Compress
from ngsolve.comp import ContactBoundary
from ngsolve.comp import DifferentialSymbol
from ngsolve.comp import Discontinuous
from ngsolve.comp import DualProxyFunction
from ngsolve.comp import ElementId
from ngsolve.comp import ElementRange
from ngsolve.comp import FESpace
from ngsolve.comp import FESpaceElement
from ngsolve.comp import FESpaceElementRange
from ngsolve.comp import FacetFESpace
from ngsolve.comp import FacetSurface
from ngsolve.comp import FlatArray_N6ngcomp13COUPLING_TYPEE_S
from ngsolve.comp import GlobalInterfaceSpace
from ngsolve.comp import GlobalSpace
from ngsolve.comp import GlobalVariables
from ngsolve.comp import GridFunction
from ngsolve.comp import GridFunctionC
from ngsolve.comp import GridFunctionCoefficientFunction
from ngsolve.comp import GridFunctionD
from ngsolve.comp import H1
from ngsolve.comp import H1AMG
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
from ngsolve.comp import Integral
from ngsolve.comp import IntegrationRuleSpace
from ngsolve.comp import IntegrationRuleSpaceSurface
from ngsolve.comp import InterpolateProxy
from ngsolve.comp import L2
from ngsolve.comp import LinearForm
from ngsolve.comp import LocalPreconditioner
from ngsolve.comp import MatrixValued
from ngsolve.comp import Mesh
from ngsolve.comp import MeshNode
from ngsolve.comp import MeshNodeRange
from ngsolve.comp import MultiGridPreconditioner
from ngsolve.comp import NGS_Object
from ngsolve.comp import Ngs_Element
from ngsolve.comp import NodalFESpace
from ngsolve.comp import NodeId
from ngsolve.comp import NodeRange
from ngsolve.comp import NormalFacetFESpace
from ngsolve.comp import NormalFacetSurface
from ngsolve.comp import NumberSpace
from ngsolve.comp import ORDER_POLICY
from ngsolve.comp import Periodic
from ngsolve.comp import PlateauFESpace
from ngsolve.comp import Preconditioner
from ngsolve.comp import ProductSpace
from ngsolve.comp import Prolongation
from ngsolve.comp import ProxyFunction
from ngsolve.comp import QuasiPeriodicC
from ngsolve.comp import QuasiPeriodicD
from ngsolve.comp import Region
from ngsolve.comp import Reorder
from ngsolve.comp import SumOfIntegrals
from ngsolve.comp import SurfaceL2
from ngsolve.comp import SymbolTable_D
from ngsolve.comp import SymbolTable_sp_D
from ngsolve.comp import SymbolTable_sp_N5ngfem19CoefficientFunctionE
from ngsolve.comp import SymbolTable_sp_N6ngcomp10LinearFormE
from ngsolve.comp import SymbolTable_sp_N6ngcomp12BilinearFormE
from ngsolve.comp import SymbolTable_sp_N6ngcomp12GridFunctionE
from ngsolve.comp import SymbolTable_sp_N6ngcomp14PreconditionerE
from ngsolve.comp import SymbolTable_sp_N6ngcomp7FESpaceE
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
from ngsolve.comp import VorB
from ngsolve.comp import pml
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import BndElementId
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import BoundaryFromVolumeCF
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompressCompound
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import ConvertOperator
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import FromArchiveCF
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import FromArchiveFESpace
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import FromArchiveMesh
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Integrate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Interpolate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import KSpaceCoeffs
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import MatrixFreeOperator
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import PatchwiseSolve
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Prolongate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import ProlongateCoefficientFunction
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import RegisterPreconditioner
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetHeapSize
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetTestoutFile
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicBFI
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicEnergy
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicLFI
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicTPBFI
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import TensorProductFESpace
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import TensorProductIntegrate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import ToArchive
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Transfer2StdMesh
import ngsolve.fem
from ngsolve.fem import BFI
from ngsolve.fem import BSpline
from ngsolve.fem import BSpline2D
from ngsolve.fem import BaseMappedIntegrationPoint
from ngsolve.fem import CoefficientFunction
from ngsolve.fem import CoordinateTrafo
from ngsolve.fem import DifferentialOperator
from ngsolve.fem import ET
from ngsolve.fem import ElementTopology
from ngsolve.fem import ElementTransformation
from ngsolve.fem import FiniteElement
from ngsolve.fem import HCurlFE
from ngsolve.fem import HDivDivFE
from ngsolve.fem import HDivFE
from ngsolve.fem import IntegrationPoint
from ngsolve.fem import IntegrationRule
from ngsolve.fem import LFI
from ngsolve.fem import MeshPoint
from ngsolve.fem import MixedFE
from ngsolve.fem import NODE_TYPE
from ngsolve.fem import Parameter
from ngsolve.fem import ParameterC
from ngsolve.fem import PlaceholderCF
from ngsolve.fem import PointEvaluationFunctional
from ngsolve.fem import ScalarFE
from ngsolve.fem import SpecialCFCreator
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CacheCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cof
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompilePythonModule
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Conj
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CoordCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cross
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Det
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Einsum
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import GenerateL2ElementCode
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import H1FE
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Id
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import IfPos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Inv
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import L2FE
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import LeviCivitaSymbol
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import LoggingCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import MinimizationCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import NewtonCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetPMLParameters
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Skew
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Sym
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Trace
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import VoxelCoefficient
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Zero
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
from ngsolve.ngstd import IntRange
from pyngcore.pyngcore import Timer
__all__ = ['APhiHCurlAMG', 'Array_N6ngcomp13COUPLING_TYPEE_S', 'BBBND', 'BBND', 'BDDCPreconditioner', 'BDDCPreconditioner_complex', 'BDDCPreconditioner_double', 'BFI', 'BND', 'BSpline', 'BSpline2D', 'BaseMappedIntegrationPoint', 'BilinearForm', 'BlockBFI', 'BlockLFI', 'BndElementId', 'BoundaryFromVolumeCF', 'CELL', 'COUPLING_TYPE', 'CacheCF', 'CoefficientFunction', 'Cof', 'CompilePythonModule', 'ComponentGridFunction', 'CompoundBFI', 'CompoundLFI', 'Compress', 'CompressCompound', 'Conj', 'ConstantCF', 'ContactBoundary', 'ConvertOperator', 'CoordCF', 'CoordinateTrafo', 'Cross', 'Det', 'Deviator', 'DifferentialOperator', 'DifferentialSymbol', 'Discontinuous', 'DomainConstantCF', 'DualProxyFunction', 'EDGE', 'ELEMENT', 'ET', 'Einsum', 'ElementId', 'ElementRange', 'ElementTopology', 'ElementTransformation', 'FACE', 'FACET', 'FESpace', 'FESpaceElement', 'FESpaceElementRange', 'FacetFESpace', 'FacetSurface', 'FiniteElement', 'FlatArray_N6ngcomp13COUPLING_TYPEE_S', 'FromArchiveCF', 'FromArchiveFESpace', 'FromArchiveMesh', 'GenerateL2ElementCode', 'GlobalInterfaceSpace', 'GlobalSpace', 'GlobalVariables', 'Grad', 'GridFunction', 'GridFunctionC', 'GridFunctionCoefficientFunction', 'GridFunctionD', 'H1', 'H1AMG', 'H1FE', 'H1LumpingFESpace', 'HCurl', 'HCurlAMG', 'HCurlCurl', 'HCurlDiv', 'HCurlFE', 'HDiv', 'HDivDiv', 'HDivDivFE', 'HDivDivSurface', 'HDivFE', 'HDivSurface', 'HEX', 'Hidden', 'Id', 'IfPos', 'IntRange', 'Integral', 'Integrate', 'IntegrationPoint', 'IntegrationRule', 'IntegrationRuleSpace', 'IntegrationRuleSpaceSurface', 'Interpolate', 'InterpolateProxy', 'Inv', 'KSpaceCoeffs', 'L2', 'L2FE', 'LFI', 'Laplace', 'LeviCivitaSymbol', 'LinearForm', 'LocalPreconditioner', 'LoggingCF', 'Mass', 'MatrixFreeOperator', 'MatrixValued', 'Mesh', 'MeshNode', 'MeshNodeRange', 'MeshPoint', 'MinimizationCF', 'MixedFE', 'MultiGridPreconditioner', 'NGS_Object', 'NODE_TYPE', 'Neumann', 'NewtonCF', 'Ngs_Element', 'NodalFESpace', 'NodeId', 'NodeRange', 'Norm', 'NormalFacetFESpace', 'NormalFacetSurface', 'Normalize', 'NumberSpace', 'ORDER_POLICY', 'OuterProduct', 'POINT', 'PRISM', 'PYRAMID', 'Parameter', 'ParameterC', 'PatchwiseSolve', 'Periodic', 'PlaceholderCF', 'PlateauFESpace', 'PointEvaluationFunctional', 'Preconditioner', 'PrivateSpace', 'ProductSpace', 'Prolongate', 'ProlongateCoefficientFunction', 'Prolongation', 'ProxyFunction', 'PyCof', 'PyCross', 'PyDet', 'PyId', 'PyInv', 'PySkew', 'PySym', 'PyTrace', 'QUAD', 'QuasiPeriodicC', 'QuasiPeriodicD', 'Region', 'RegisterPreconditioner', 'Reorder', 'SEGM', 'ScalarFE', 'SetHeapSize', 'SetPMLParameters', 'SetTestoutFile', 'Skew', 'Source', 'SpecialCFCreator', 'SumOfIntegrals', 'SurfaceL2', 'Sym', 'SymbolTable_D', 'SymbolTable_sp_D', 'SymbolTable_sp_N5ngfem19CoefficientFunctionE', 'SymbolTable_sp_N6ngcomp10LinearFormE', 'SymbolTable_sp_N6ngcomp12BilinearFormE', 'SymbolTable_sp_N6ngcomp12GridFunctionE', 'SymbolTable_sp_N6ngcomp14PreconditionerE', 'SymbolTable_sp_N6ngcomp7FESpaceE', 'SymbolicBFI', 'SymbolicEnergy', 'SymbolicLFI', 'SymbolicTPBFI', 'TET', 'TRIG', 'TangentialFacetFESpace', 'TangentialSurfaceL2', 'TensorProductFESpace', 'TensorProductIntegrate', 'TimeFunction', 'Timer', 'ToArchive', 'Trace', 'Transfer2StdMesh', 'VERTEX', 'VOL', 'VTKOutput', 'Variation', 'VectorFacet', 'VectorFacetFESpace', 'VectorFacetSurface', 'VectorH1', 'VectorL2', 'VectorNodalFESpace', 'VectorSurfaceL2', 'VectorValued', 'VorB', 'VoxelCoefficient', 'Zero', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'curl', 'div', 'ds', 'dt', 'dx', 'erf', 'exp', 'floor', 'grad', 'log', 'ngsglobals', 'pml', 'pow', 'printonce', 'sin', 'sinh', 'specialcf', 'sqrt', 'tan', 'x', 'y', 'z']
def ConstantCF(val):
    ...
def Deviator(mat):
    ...
def DomainConstantCF(values):
    ...
def Grad(func):
    """
    Jacobi-matrix
    """
def Laplace(coef):
    ...
def Mass(coef):
    ...
def Neumann(coef):
    ...
def Normalize(v):
    ...
def OuterProduct(a, b):
    ...
def PyCof(m):
    ...
def PyCross(a, b):
    ...
def PyDet(mat):
    ...
def PyId(dim):
    ...
def PyInv(m):
    ...
def PySkew(m):
    ...
def PySym(m):
    ...
def PyTrace(mat):
    ...
def Source(coef):
    ...
def VectorFacet(mesh, **args):
    ...
def curl(func):
    ...
def div(func):
    ...
def dt(u):
    ...
def grad(func):
    ...
def printonce(*args):
    ...
BBBND: ngsolve.comp.VorB  # value = <VorB.BBBND: 3>
BBND: ngsolve.comp.VorB  # value = <VorB.BBND: 2>
BND: ngsolve.comp.VorB  # value = <VorB.BND: 1>
CELL: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.CELL: 3>
EDGE: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.EDGE: 1>
ELEMENT: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.ELEMENT: 4>
FACE: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.FACE: 2>
FACET: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.FACET: 5>
HEX: ngsolve.fem.ET  # value = <ET.HEX: 24>
POINT: ngsolve.fem.ET  # value = <ET.POINT: 0>
PRISM: ngsolve.fem.ET  # value = <ET.PRISM: 22>
PYRAMID: ngsolve.fem.ET  # value = <ET.PYRAMID: 21>
QUAD: ngsolve.fem.ET  # value = <ET.QUAD: 11>
SEGM: ngsolve.fem.ET  # value = <ET.SEGM: 1>
TET: ngsolve.fem.ET  # value = <ET.TET: 20>
TRIG: ngsolve.fem.ET  # value = <ET.TRIG: 10>
VERTEX: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.VERTEX: 0>
VOL: ngsolve.comp.VorB  # value = <VorB.VOL: 0>
ds: ngsolve.comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
dx: ngsolve.comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
ngsglobals: ngsolve.comp.GlobalVariables  # value = <ngsolve.comp.GlobalVariables object>
specialcf: ngsolve.fem.SpecialCFCreator  # value = <ngsolve.fem.SpecialCFCreator object>
x: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
y: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
z: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
