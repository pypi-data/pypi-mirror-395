"""
pybind fem
"""
from __future__ import annotations
import collections.abc
import ngsolve.bla
import ngsolve.ngstd
import numpy
import numpy.typing
import pyngcore.pyngcore
import typing
__all__ = ['BFI', 'BSpline', 'BSpline2D', 'BaseMappedIntegrationPoint', 'BlockBFI', 'BlockLFI', 'CELL', 'CacheCF', 'CoefficientFunction', 'Cof', 'CompilePythonModule', 'CompoundBFI', 'CompoundLFI', 'Conj', 'CoordCF', 'CoordinateTrafo', 'Cross', 'Det', 'DifferentialOperator', 'EDGE', 'ELEMENT', 'ET', 'Einsum', 'ElementTopology', 'ElementTransformation', 'FACE', 'FACET', 'FiniteElement', 'GenerateL2ElementCode', 'H1FE', 'HCurlFE', 'HDivDivFE', 'HDivFE', 'HEX', 'Id', 'IfPos', 'IntegrationPoint', 'IntegrationRule', 'Inv', 'L2FE', 'LFI', 'LeviCivitaSymbol', 'LoggingCF', 'MeshPoint', 'MinimizationCF', 'MixedFE', 'NODE_TYPE', 'NewtonCF', 'POINT', 'PRISM', 'PYRAMID', 'Parameter', 'ParameterC', 'PlaceholderCF', 'PointEvaluationFunctional', 'QUAD', 'SEGM', 'ScalarFE', 'SetPMLParameters', 'Skew', 'SpecialCFCreator', 'Sym', 'TET', 'TRIG', 'Trace', 'VERTEX', 'VoxelCoefficient', 'Zero', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'erf', 'exp', 'floor', 'log', 'pow', 'sin', 'sinh', 'specialcf', 'sqrt', 'tan']
class BFI:
    """
    
    Bilinear Form Integrator
    
    Parameters:
    
    name : string
      Name of the bilinear form integrator.
    
    py_coef : object
      CoefficientFunction of the bilinear form.
    
    dim : int
      dimension of the bilinear form integrator
    
    imag : bool
      Multiplies BFI with 1J
    
    filename : string
      filename 
    
    kwargs : kwargs
      For a description of the possible kwargs have a look a bit further down.
    
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    @staticmethod
    def __special_treated_flags__() -> dict:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def ApplyElementMatrix(self, fel: FiniteElement, vec: ngsolve.bla.FlatVectorD, trafo: ElementTransformation, heapsize: typing.SupportsInt = 10000) -> typing.Any:
        """
        Apply element matrix of a specific element.
        
        Parameters:
        
        fel : ngsolve.fem.FiniteElement
          input finite element
        
        vec : Vector
          evaluation argument
        
        trafo : ngsolve.fem.ElementTransformation
          input element transformation
        
        heapsize : int
          input heapsize
        """
    def CalcElementMatrix(self, fel: FiniteElement, trafo: ElementTransformation, heapsize: typing.SupportsInt = 10000, complex: bool = False) -> typing.Any:
        """
        Calculate element matrix of a specific element.
        
        Parameters:
        
        fel : ngsolve.fem.FiniteElement
          input finite element
        
        trafo : ngsolve.fem.ElementTransformation
          input element transformation
        
        heapsize : int
          input heapsize
        
        complex : bool
          input complex
        """
    def CalcLinearizedElementMatrix(self, fel: FiniteElement, vec: ngsolve.bla.FlatVectorD, trafo: ElementTransformation, heapsize: typing.SupportsInt = 10000) -> typing.Any:
        """
        Calculate (linearized) element matrix of a specific element.
        
        Parameters:
        
        fel : ngsolve.fem.FiniteElement
          input finite element
        
        vec : Vector
          linearization argument
        
        trafo : ngsolve.fem.ElementTransformation
          input element transformation
        
        heapsize : int
          input heapsize
        """
    def Evaluator(self, name: str) -> DifferentialOperator:
        """
        Returns requested evaluator
        
        Parameters:
        
        name : string
          input name of requested evaluator
        """
    def GetDefinedOn(self) -> pyngcore.pyngcore.BitArray:
        """
        Returns a BitArray where the bilinear form is defined on
        """
    def SetDefinedOnElements(self, bitarray: pyngcore.pyngcore.BitArray) -> None:
        """
        Set the elements on which the bilinear form is defined on.
        
        Parameters:
        
        bitarray : ngsolve.ngstd.BitArray
          input bitarray
        """
    def SetIntegrationRule(self, et: ET, intrule: IntegrationRule) -> BFI:
        """
        Set integration rule of the bilinear form.
        
        Parameters:
        
        et : ngsolve.fem.Element_Type
          input element type
        
        intrule : ngsolve.fem.Integrationrule
          input integration rule
        """
    def __init__(self, name: str = '', coef: typing.Any, dim: typing.SupportsInt = -1, imag: bool = False, filename: str = '', **kwargs) -> None:
        ...
    def __initialize__(self, **kwargs) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def simd_evaluate(self) -> bool:
        """
        SIMD evaluate ?
        """
    @simd_evaluate.setter
    def simd_evaluate(self, arg1: bool) -> None:
        ...
class BSpline:
    """
    
    BSpline of arbitrary order
    
    Parameters:
    
    order : int
      order of the BSpline
    
    knots : list
      list of float
    
    vals : list
      list of float
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Differentiate(self) -> BSpline:
        """
        Differentiate the BSpline
        """
    def Integrate(self) -> BSpline:
        """
        Integrate the BSpline
        """
    @typing.overload
    def __call__(self, pt: typing.SupportsFloat) -> float:
        ...
    @typing.overload
    def __call__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    def __init__(self, order: typing.SupportsInt, knots: list, vals: list) -> None:
        """
        B-Spline of a certain order, provide knot and value vectors
        """
    def __str__(self) -> str:
        ...
class BSpline2D:
    """
    
    Bilinear intepolation of data given on a regular grid
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __call__(self, x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
        ...
    @typing.overload
    def __call__(self, cx: CoefficientFunction, cy: CoefficientFunction) -> CoefficientFunction:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, x: list, y: list, vals: list, order: typing.SupportsInt = 1, extrapolate: bool = True) -> None:
        """
        x : list, y: list
          sorted list of grid coordinates
        
        vals : list
          list of values at (x0,y0), (x0,y1), ...
        
        order: int
          interpolation order (only order=1 is supported)
        
        extrapolate: bool = True
          extrapolate values if outside given x/y coordinates (instead of throwing an exception)
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
class BaseMappedIntegrationPoint:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: MeshPoint) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def elementid(self) -> ...:
        """
        Element ID of the mapped integration point
        """
    @property
    def jacobi(self) -> ngsolve.bla.FlatMatrixD:
        """
        jacobian of the mapped integration point
        """
    @property
    def measure(self) -> float:
        """
        Measure of the mapped integration point 
        """
    @property
    def point(self) -> ngsolve.bla.FlatVectorD:
        """
        Point of the mapped integration point
        """
    @property
    def trafo(self) -> ...:
        """
        Transformation of the mapped integration point
        """
class CoefficientFunction:
    """
    A CoefficientFunction (CF) is some function defined on a mesh.
    Examples are coordinates x, y, z, domain-wise constants, solution-fields, ...
    CFs can be combined by mathematical operations (+,-,sin(), ...) to form new CFs
    Parameters:
    
    val : can be one of the following:
    
      scalar (float or complex):
        Creates a constant CoefficientFunction with value val
    
      tuple of scalars or CoefficientFunctions:
        Creates a vector or matrix valued CoefficientFunction, use dims=(h,w)
        for matrix valued CF
      list of scalars or CoefficientFunctions:
        Creates a domain-wise CF, use with generator expressions and mesh.GetMaterials()
        and mesh.GetBoundaries()
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Compile(self, realcompile: bool = False, maxderiv: typing.SupportsInt = 2, wait: bool = False, keep_files: bool = False) -> CoefficientFunction:
        """
        Compile list of individual steps, experimental improvement for deep trees
        
        Parameters:
        
        realcompile : bool
          True -> Compile to C++ code
        
        maxderiv : int
          input maximal derivative
        
        wait : bool
          True -> Waits until the previous Compile call is finished before start compiling
        
        keep_files : bool
          True -> Keep temporary files
        """
    def Derive(self, variable: CoefficientFunction, direction: CoefficientFunction = 1.0) -> CoefficientFunction:
        """
        depricated: use 'Diff' instead
        """
    def Diff(self, variable: CoefficientFunction, direction: CoefficientFunction = None) -> CoefficientFunction:
        """
        Compute directional derivative with respect to variable
        """
    def DiffShape(self, direction: CoefficientFunction = 1.0, Eulerian: collections.abc.Sequence[CoefficientFunction] = []) -> CoefficientFunction:
        """
        Compute shape derivative in direction
        """
    def Eig(self) -> CoefficientFunction:
        """
        Returns eigenvectors and eigenvalues of matrix-valued CF
        """
    def ExtendDimension(self, dims: tuple, pos: tuple | None = None, stride: tuple | None = None) -> CoefficientFunction:
        """
        Extend shape by 0-padding
        """
    def Freeze(self) -> CoefficientFunction:
        """
        don't differentiate this expression
        """
    def InnerProduct(self, cf: CoefficientFunction) -> CoefficientFunction:
        """
        Returns InnerProduct with another CoefficientFunction.
        
        Parameters:
        
        cf : ngsolve.CoefficientFunction
          input CoefficientFunction
        """
    def MakeVariable(self) -> CoefficientFunction:
        """
        make node a variable, by which we can differentiate
        """
    def Norm(self) -> CoefficientFunction:
        """
        Returns Norm of the CF
        """
    def Operator(self, arg0: str) -> CoefficientFunction:
        ...
    def Other(self) -> CoefficientFunction:
        """
        Evaluate on other element, as needed for DG jumps
        """
    def Replace(self, arg0: collections.abc.Mapping[CoefficientFunction, CoefficientFunction]) -> CoefficientFunction:
        ...
    def Reshape(self, arg0: tuple) -> CoefficientFunction:
        """
        reshape CF:  (dim) for vector, (h,w) for matrix
        """
    def TensorTranspose(self, arg0: tuple) -> CoefficientFunction:
        ...
    def _BuildFieldLines(self, mesh: ..., start_points: collections.abc.Sequence[tuple[typing.SupportsFloat, typing.SupportsFloat, typing.SupportsFloat]], num_fieldlines: typing.SupportsInt = 100, length: typing.SupportsFloat = 0.5, max_points: typing.SupportsFloat = 500, thickness: typing.SupportsFloat = 0.0015, tolerance: typing.SupportsFloat = 0.0005, direction: typing.SupportsInt = 0, randomized: bool = True, critical_value: typing.SupportsFloat = -1) -> dict:
        ...
    @typing.overload
    def __add__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    @typing.overload
    def __add__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __add__(self, value: complex) -> CoefficientFunction:
        ...
    @typing.overload
    def __call__(self, mip: BaseMappedIntegrationPoint) -> typing.Any:
        """
        evaluate CF at a mapped integrationpoint mip. mip can be generated by calling mesh(x,y,z)
        """
    @typing.overload
    def __call__(self, x: typing.SupportsFloat, y: typing.SupportsFloat | None = None, z: typing.SupportsFloat | None = None) -> ...:
        ...
    @typing.overload
    def __call__(self, arg0: CoordinateTrafo) -> CoefficientFunction:
        ...
    @typing.overload
    def __call__(self, arg0: MeshPoint) -> typing.Any:
        ...
    @typing.overload
    def __call__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, MeshPoint]) -> numpy.ndarray:
        ...
    @typing.overload
    def __getitem__(self, comp: typing.SupportsInt) -> CoefficientFunction:
        """
        returns component comp of vectorial CF
        """
    @typing.overload
    def __getitem__(self, components: slice) -> CoefficientFunction:
        ...
    @typing.overload
    def __getitem__(self, arg0: tuple) -> CoefficientFunction:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, arg0: dict) -> None:
        ...
    @typing.overload
    def __init__(self, coef: typing.Any, dims: tuple | None = None) -> None:
        """
        Construct a CoefficientFunction from either one of
          a scalar (float or complex)
          a tuple of scalars and or CFs to define a vector-valued CF
             use dims=(h,w) to define matrix-valued CF
          a list of scalars and or CFs to define a domain-wise CF
        """
    @typing.overload
    def __mul__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    @typing.overload
    def __mul__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __mul__(self, value: complex) -> CoefficientFunction:
        ...
    @typing.overload
    def __mul__(self, arg0: ...) -> ...:
        ...
    def __neg__(self) -> CoefficientFunction:
        ...
    @typing.overload
    def __or__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    @typing.overload
    def __or__(self, cf: ...) -> typing.Any:
        ...
    @typing.overload
    def __pow__(self, exponent: typing.SupportsInt) -> CoefficientFunction:
        ...
    @typing.overload
    def __pow__(self, arg0: typing.SupportsFloat) -> typing.Any:
        ...
    @typing.overload
    def __pow__(self, arg0: CoefficientFunction) -> typing.Any:
        ...
    @typing.overload
    def __radd__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __radd__(self, value: complex) -> CoefficientFunction:
        ...
    @typing.overload
    def __rmul__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __rmul__(self, value: complex) -> CoefficientFunction:
        ...
    def __rpow__(self, arg0: typing.SupportsFloat) -> typing.Any:
        ...
    def __rsub__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __rtruediv__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __rtruediv__(self, value: complex) -> CoefficientFunction:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    @typing.overload
    def __sub__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __truediv__(self, cf: CoefficientFunction) -> CoefficientFunction:
        ...
    @typing.overload
    def __truediv__(self, value: typing.SupportsFloat) -> CoefficientFunction:
        ...
    @typing.overload
    def __truediv__(self, value: complex) -> CoefficientFunction:
        ...
    @property
    def data(self) -> dict:
        ...
    @property
    def dim(self) -> int:
        """
        number of components of CF
        """
    @property
    def dims(self) -> pyngcore.pyngcore.Array_I_S:
        """
        shape of CF:  (dim) for vector, (h,w) for matrix
        """
    @dims.setter
    def dims(self, arg1: tuple) -> None:
        ...
    @property
    def imag(self) -> CoefficientFunction:
        """
        imaginary part of CF
        """
    @property
    def is_complex(self) -> bool:
        """
        is CoefficientFunction complex-valued ?
        """
    @property
    def real(self) -> CoefficientFunction:
        """
        real part of CF
        """
    @property
    def shape(self) -> typing.Any:
        """
        shape of CF
        """
    @property
    def spacedim(self) -> int:
        ...
    @spacedim.setter
    def spacedim(self, arg1: typing.SupportsInt) -> None:
        ...
    @property
    def trans(self) -> CoefficientFunction:
        """
        transpose of matrix-valued CF
        """
class CoordinateTrafo:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: ..., arg1: ...) -> None:
        ...
class DifferentialOperator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __call__(self, arg0: FiniteElement, arg1: MeshPoint) -> ngsolve.bla.MatrixD:
        ...
    def __timing__(self, arg0: FiniteElement, arg1: ElementTransformation, arg2: IntegrationRule) -> list[tuple[str, float]]:
        ...
class ET:
    """
    Enumeration of all supported element types.
    
    Members:
    
      POINT
    
      SEGM
    
      TRIG
    
      QUAD
    
      TET
    
      PRISM
    
      PYRAMID
    
      HEX
    """
    HEX: typing.ClassVar[ET]  # value = <ET.HEX: 24>
    POINT: typing.ClassVar[ET]  # value = <ET.POINT: 0>
    PRISM: typing.ClassVar[ET]  # value = <ET.PRISM: 22>
    PYRAMID: typing.ClassVar[ET]  # value = <ET.PYRAMID: 21>
    QUAD: typing.ClassVar[ET]  # value = <ET.QUAD: 11>
    SEGM: typing.ClassVar[ET]  # value = <ET.SEGM: 1>
    TET: typing.ClassVar[ET]  # value = <ET.TET: 20>
    TRIG: typing.ClassVar[ET]  # value = <ET.TRIG: 10>
    __members__: typing.ClassVar[dict[str, ET]]  # value = {'POINT': <ET.POINT: 0>, 'SEGM': <ET.SEGM: 1>, 'TRIG': <ET.TRIG: 10>, 'QUAD': <ET.QUAD: 11>, 'TET': <ET.TET: 20>, 'PRISM': <ET.PRISM: 22>, 'PYRAMID': <ET.PYRAMID: 21>, 'HEX': <ET.HEX: 24>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ElementTopology:
    """
    
    Element Topology
    
    Parameters:
    
    et : ngsolve.fem.ET
      input element type
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, et: ET) -> None:
        ...
    @property
    def name(self) -> str:
        """
        Name of the element topology
        """
    @property
    def vertices(self) -> list:
        """
        Vertices of the element topology
        """
class ElementTransformation:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __call__(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0, z: typing.SupportsFloat = 0) -> BaseMappedIntegrationPoint:
        ...
    @typing.overload
    def __call__(self, ip: IntegrationPoint) -> BaseMappedIntegrationPoint:
        ...
    @typing.overload
    def __call__(self, arg0: IntegrationRule) -> numpy.typing.NDArray[MeshPoint]:
        ...
    def __init__(self, et: ET = ..., vertices: list) -> None:
        ...
    @property
    def VB(self) -> ...:
        """
        VorB (VOL, BND, BBND, BBBND)
        """
    @property
    def curved(self) -> bool:
        """
        Is mapping non-affine ?
        """
    @property
    def elementid(self) -> ...:
        """
        Element ID of the element transformation
        """
    @property
    def spacedim(self) -> int:
        """
        Space dimension of the element transformation
        """
class FiniteElement:
    """
    any finite element
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __str__(self) -> str:
        ...
    def __timing__(self) -> list[tuple[str, float]]:
        ...
    @property
    def classname(self) -> str:
        """
        name of element family
        """
    @property
    def dim(self) -> int:
        """
        spatial dimension of element
        """
    @property
    def ndof(self) -> int:
        """
        number of degrees of freedom of element
        """
    @property
    def order(self) -> int:
        """
        maximal polynomial order of element
        """
    @property
    def type(self) -> ET:
        """
        geometric type of element
        """
class HCurlFE(FiniteElement):
    """
    an H(curl) finite element
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def CalcCurlShape(self, mip: ...) -> ngsolve.bla.MatrixD:
        ...
    @typing.overload
    def CalcShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.MatrixD:
        ...
    @typing.overload
    def CalcShape(self, mip: ...) -> ngsolve.bla.MatrixD:
        ...
class HDivDivFE(FiniteElement):
    """
    an H(div div) finite element
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def CalcDivShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.MatrixD:
        ...
    def CalcShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.MatrixD:
        ...
class HDivFE(FiniteElement):
    """
    an H(div) finite element
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def CalcDivShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.VectorD:
        ...
    def CalcShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.MatrixD:
        ...
class IntegrationPoint:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def point(self) -> tuple:
        """
        Integration point coordinates as tuple, has always x,y and z component, which do not have meaning in lesser dimensions
        """
    @property
    def weight(self) -> float:
        """
        Weight of the integration point
        """
class IntegrationRule:
    """
    
    Integration rule
    
    2 __init__ overloads
    
    
    1)
    
    Parameters:
    
    element type : ngsolve.fem.ET
      input element type
    
    order : int
      input order of integration rule
    
    
    2)
    
    Parameters:
    
    points : list
      input list of integration points
    
    weights : list
      input list of integration weights
    
    """
    @staticmethod
    @typing.overload
    def __init__(*args, **kwargs) -> None:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Integrate(self, func: typing.Any) -> typing.Any:
        """
        Integrates a given function
        """
    def __getitem__(self, nr: typing.SupportsInt) -> IntegrationPoint:
        """
        Return integration point at given position
        """
    @typing.overload
    def __init__(self, points: list, weights: list = []) -> None:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    @property
    def points(self) -> list:
        """
        Points of IntegrationRule as tuple
        """
    @property
    def weights(self) -> list:
        """
        Weights of IntegrationRule
        """
class LFI:
    """
    
    Linear Form Integrator
    
    Parameters:
    
    name : string
      Name of the linear form integrator.
    
    dim : int
      dimension of the linear form integrator
    
    coef : object
      CoefficientFunction of the bilinear form.
    
    definedon : object
      input region where the linear form is defined on
    
    imag : bool
      Multiplies LFI with 1J
    
    flags : ngsolve.ngstd.Flags
      input flags
    
    definedonelem : object
      input definedonelem
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def CalcElementVector(self, fel: FiniteElement, trafo: ElementTransformation, vec: ngsolve.bla.FlatVectorD, lh: ngsolve.ngstd.LocalHeap) -> None:
        ...
    @typing.overload
    def CalcElementVector(self, fel: FiniteElement, trafo: ElementTransformation, heapsize: typing.SupportsInt = 10000, complex: bool = False) -> typing.Any:
        ...
    def GetDefinedOn(self) -> pyngcore.pyngcore.BitArray:
        """
        Reterns regions where the lienar form integrator is defined on.
        """
    def SetDefinedOnElements(self, ba: pyngcore.pyngcore.BitArray) -> None:
        """
        Set the elements on which the linear form integrator is defined on
        
        Parameters:
        
        ba : ngsolve.ngstd.BitArray
          input bit array ( 1-> defined on, 0 -> not defoned on)
        """
    def SetIntegrationRule(self, et: ET, ir: IntegrationRule) -> LFI:
        """
        Set a different integration rule for elements of type et
        
        Parameters:
        
        et : ngsolve.fem.ET
          input element type
        
        ir : ngsolve.fem.IntegrationRule
          input integration rule
        """
    def __init__(self, name: str = 'lfi', dim: typing.SupportsInt = -1, coef: typing.Any, definedon: ... | list | None = None, imag: bool = False, flags: pyngcore.pyngcore.Flags = {}, definedonelements: pyngcore.pyngcore.BitArray = None) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def simd_evaluate(self) -> bool:
        """
        SIMD evaluate ?
        """
    @simd_evaluate.setter
    def simd_evaluate(self, arg1: bool) -> None:
        ...
class MeshPoint:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def mesh(self) -> ...:
        ...
    @property
    def nr(self) -> int:
        ...
    @property
    def pnt(self) -> tuple:
        """
        Gives coordinates of point on reference triangle. One can create a MappedIntegrationPoint using the ngsolve.fem.BaseMappedIntegrationPoint constructor. For physical coordinates the coordinate CoefficientFunctions x,y,z can be evaluated in the MeshPoint
        """
    @property
    def vb(self) -> ...:
        ...
class MixedFE(FiniteElement):
    """
    pair of finite elements for trial and test-functions
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: FiniteElement, arg1: FiniteElement) -> None:
        ...
class NODE_TYPE:
    """
    Enumeration of all supported node types.
    
    Members:
    
      VERTEX
    
      EDGE
    
      FACE
    
      CELL
    
      ELEMENT
    
      FACET
    """
    CELL: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.CELL: 3>
    EDGE: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.EDGE: 1>
    ELEMENT: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.ELEMENT: 4>
    FACE: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.FACE: 2>
    FACET: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.FACET: 5>
    VERTEX: typing.ClassVar[NODE_TYPE]  # value = <NODE_TYPE.VERTEX: 0>
    __members__: typing.ClassVar[dict[str, NODE_TYPE]]  # value = {'VERTEX': <NODE_TYPE.VERTEX: 0>, 'EDGE': <NODE_TYPE.EDGE: 1>, 'FACE': <NODE_TYPE.FACE: 2>, 'CELL': <NODE_TYPE.CELL: 3>, 'ELEMENT': <NODE_TYPE.ELEMENT: 4>, 'FACET': <NODE_TYPE.FACET: 5>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Parameter(CoefficientFunction):
    """
    
    CoefficientFunction with a modifiable value
    
    Parameters:
    
    value : float
      Parameter value
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Get(self) -> float:
        """
        return parameter value
        """
    def Set(self, value: typing.SupportsFloat) -> None:
        """
        Modify parameter value.
        
        Parameters:
        
        value : double
          input scalar  
        """
    def __ge__(self, arg0: typing.SupportsFloat) -> bool:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __gt__(self, arg0: typing.SupportsFloat) -> bool:
        ...
    def __iadd__(self, arg0: typing.SupportsFloat) -> Parameter:
        ...
    def __imul__(self, arg0: typing.SupportsFloat) -> Parameter:
        ...
    def __init__(self, value: typing.SupportsFloat) -> None:
        """
        Construct a ParameterCF from a scalar
        """
    def __isub__(self, arg0: typing.SupportsFloat) -> Parameter:
        ...
    def __itruediv__(self, arg0: typing.SupportsFloat) -> Parameter:
        ...
    def __le__(self, arg0: typing.SupportsFloat) -> bool:
        ...
    def __lt__(self, arg0: typing.SupportsFloat) -> bool:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class ParameterC(CoefficientFunction):
    """
    
    CoefficientFunction with a modifiable complex value
    
    Parameters:
    
    value : complex
      Parameter value
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Get(self) -> complex:
        """
        return parameter value
        """
    def Set(self, value: complex) -> None:
        """
        Modify parameter value.
        
        Parameters:
        
        value : complex
          input scalar
        """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, value: complex) -> None:
        """
        Construct a ParameterCF from a scalar
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class PlaceholderCF(CoefficientFunction):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Set(self, arg0: CoefficientFunction) -> None:
        ...
    def __init__(self, arg0: CoefficientFunction) -> None:
        ...
class PointEvaluationFunctional:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Assemble(self) -> ngsolve.bla.SparseVector:
        ...
class ScalarFE(FiniteElement):
    """
    a scalar-valued finite element
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def CalcDShape(self, mip: ...) -> ngsolve.bla.MatrixD:
        """
        Computes derivative of the shape in an integration point.
        
        Parameters:
        
        mip : ngsolve.BaseMappedIntegrationPoint
          input mapped integration point
        """
    @typing.overload
    def CalcDShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.MatrixD:
        """
        Computes derivative of the shape in an integration point.
        
        Parameters:
        
        x : double
          input x value
        
        y : double
          input y value
        
        z : double
          input z value
        """
    @typing.overload
    def CalcShape(self, x: typing.SupportsFloat, y: typing.SupportsFloat = 0.0, z: typing.SupportsFloat = 0.0) -> ngsolve.bla.VectorD:
        """
        Parameters:
        
        x : double
          input x value
        
        y : double
          input y value
        
        z : double
          input z value
        """
    @typing.overload
    def CalcShape(self, mip: ...) -> ngsolve.bla.VectorD:
        """
        Parameters:
        
        mip : ngsolve.BaseMappedIntegrationPoint
          input mapped integration point
        """
class SpecialCFCreator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def EdgeCurvature(self, dim: typing.SupportsInt) -> ...:
        """
        EdgeCurvature 
        space-dimension must be provided
        """
    def EdgeFaceTangentialVectors(self, dim: typing.SupportsInt) -> ...:
        """
        EdgeFaceTangentialVectors 
        space-dimension must be provided
        """
    @typing.overload
    def JacobianMatrix(self, dim: typing.SupportsInt) -> ...:
        """
        Jacobian matrix of transformation to physical element
        space-dimension must be provided
        """
    @typing.overload
    def JacobianMatrix(self, dimr: typing.SupportsInt, dims: typing.SupportsInt) -> ...:
        """
        Jacobian matrix of transformation to physical element
        space-dimensions dimr >= dims must be provided
        """
    def VertexTangentialVectors(self, dim: typing.SupportsInt) -> ...:
        """
        VertexTangentialVectors 
        space-dimension must be provided
        """
    def Weingarten(self, dim: typing.SupportsInt) -> ...:
        """
        Weingarten tensor 
        space-dimension must be provided
        """
    @typing.overload
    def normal(self, arg0: typing.SupportsInt) -> ...:
        """
        depending on contents: normal-vector to geometry or element
        space-dimension must be provided.
        """
    @typing.overload
    def normal(self, arg0: ...) -> ...:
        """
        If region is provided, normal is pointing outwards of region (only supported on 2d/3d surface elements)
        """
    def num_els_on_facet(self) -> ...:
        """
        number of elements on facet, available for element-bnd integrals, and surface integrals
        """
    def tangential(self, dim: typing.SupportsInt, consistent: bool = False) -> ...:
        """
        depending on contents: tangential-vector to element
        space-dimension must be provided
        """
    def xref(self, dim: typing.SupportsInt) -> ...:
        """
        element reference-coordinates
        """
    @property
    def mesh_size(self) -> ...:
        """
        local mesh-size (approximate element diameter) as CF
        """
def BlockBFI(bfi: BFI = 0, dim: typing.SupportsInt = 2, comp: typing.SupportsInt = 0) -> ...:
    """
    Block Bilinear Form Integrator
    
    Parameters:
    
    bfi : ngsolve.fem.BFI
      input bilinear form integrator
    
    dim : int
      input dimension of block bilinear form integrator
    
    comp : int
      input comp
    """
def BlockLFI(lfi: LFI = 0, dim: typing.SupportsInt = 2, comp: typing.SupportsInt = 0) -> LFI:
    """
    Block Linear Form Integrator
    
    Parameters:
    
    lfi : ngsolve.fem.LFI
      input bilinear form integrator
    
    dim : int
      input dimension of block linear form integrator
    
    comp : int
      input comp
    """
def CacheCF(cf: CoefficientFunction) -> CoefficientFunction:
    ...
def Cof(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
@typing.overload
def CompilePythonModule(code: str, init_function_name: str = 'init', add_header: bool = True) -> typing.Any:
    """
    Utility function to compile c++ code with python bindings at run-time.
    
    Parameters:
    
    code: c++ code snippet ( add_header=True ) or a complete .cpp file ( add_header=False )
    
    init_function_name (default = "init"): Function, which is called after the compiled code is loaded. The prototype must match:
    extern "C" void init_function_name(pybind11::object & res);
    
    add_header (default = True): wrap the code snippet with the template
    
    #include <comp.hpp>
    #include <python_ngstd.hpp>
    
    using namespace ngcomp;
    
    extern "C" {
    
      NGCORE_API_EXPORT void init(py::object & res)
      {
        static py::module::module_def def;
        py::module m = py::module::create_extension_module("", "", &def);
    
        // BEGIN USER DEFINED CODE
    
    
        // END USER DEFINED CODE
        res = m;
      }
    }
    """
@typing.overload
def CompilePythonModule(file: os.PathLike | str | bytes, init_function_name: str = 'init') -> typing.Any:
    """
    Utility function to compile a c++ file with python bindings at run-time.
    
    Parameters:
    
    file: c++ code file (type: pathlib.Path)
    
    init_function_name (default = "init"): Function, which is called after the compiled code is loaded. The prototype must match:
    extern "C" void init_function_name(pybind11::object & res);
    """
def CompoundBFI(bfi: BFI = 0, comp: typing.SupportsInt = 0) -> ...:
    """
    Compound Bilinear Form Integrator
    
    Parameters:
    
    bfi : ngsolve.fem.BFI
      input bilinear form integrator
    
    comp : int
      input component
    """
def CompoundLFI(lfi: LFI = 0, comp: typing.SupportsInt = 0) -> LFI:
    """
    Compound Linear Form Integrator
    
    Parameters:
    
    lfi : ngsolve.fem.LFI
      input linear form integrator
    
    comp : int
      input component
    """
def Conj(arg0: CoefficientFunction) -> CoefficientFunction:
    """
    complex-conjugate
    """
def CoordCF(direction: typing.SupportsInt) -> ...:
    """
    CoefficientFunction for x, y, z.
    
    Parameters:
    
    direction : int
      input direction
    """
def Cross(arg0: CoefficientFunction, arg1: CoefficientFunction) -> CoefficientFunction:
    ...
def Det(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
def Einsum(einsum_signature: str, *args, **kwargs) -> CoefficientFunction:
    """
    Generic tensor product in the spirit of numpy's \\"einsum\\" feature.
    
    Parameters:
    
    einsum_signature: str
      specification of the tensor product in numpy's "einsum" notation
      
    args: 
      CoefficientFunctions
      
    kwargs:
      "expand_einsum" (true) -- expand nested "einsums" for later optimization
      "optimize_path" (false) -- try to reorder product for greater efficiency
      "optimize_identities" (false) -- try to eliminate identity tensors
      "use_legacy_ops" (false) -- fall back to existing CFs implementing certain blas operations where possible
      "sparse_evaluation" (true) -- exploit sparsity of tensors
    """
def GenerateL2ElementCode(arg0: typing.SupportsInt) -> str:
    ...
def H1FE(et: ET, order: typing.SupportsInt) -> None:
    """
    Creates an H1 finite element of given geometric shape and polynomial order.
    
    Parameters:
    
    et : ngsolve.fem.ET
      input element type
    
    order : int
      input polynomial order
    """
@typing.overload
def Id(dim: typing.SupportsInt) -> CoefficientFunction:
    """
    Identity matrix of given dimension
    """
@typing.overload
def Id(dims: pyngcore.pyngcore.Array_I_S) -> CoefficientFunction:
    """
    Identity tensor for a space with dimensions 'dims', ie. the result is of 'dims + dims'
    """
@typing.overload
def IfPos(c1: ..., then_obj: typing.Any, else_obj: typing.Any) -> ...:
    """
    Returns new CoefficientFunction with values then_obj if c1 is positive and else_obj else.
    
    Parameters:
    
    c1 : ngsolve.CoefficientFunction
      Indicator function
    
    then_obj : object
      Values of new CF if c1 is positive, object must be implicitly convertible to
      ngsolve.CoefficientFunction. See help(CoefficientFunction ) for information.
    
    else_obj : object
      Values of new CF if c1 is not positive, object must be implicitly convertible to
      ngsolve.CoefficientFunction. See help(CoefficientFunction ) for information.
    """
@typing.overload
def IfPos(arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], arg2: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    ...
def Inv(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
def L2FE(et: ET, order: typing.SupportsInt) -> None:
    """
    Creates an L2 finite element of given geometric shape and polynomial order.
    
    Parameters:
    
    et : ngsolve.fem.ET
      input element type
    
    order : int
      input polynomial order
    """
def LeviCivitaSymbol(arg0: typing.SupportsInt) -> CoefficientFunction:
    ...
def LoggingCF(cf: CoefficientFunction, logfile: str = 'stdout') -> CoefficientFunction:
    ...
def MinimizationCF(expression: CoefficientFunction, startingpoint: typing.Any, tol: typing.SupportsFloat | None = 1e-06, rtol: typing.SupportsFloat | None = 0.0, maxiter: typing.SupportsInt | None = 20, allow_fail: bool | None = False) -> CoefficientFunction:
    """
    Creates a CoefficientFunction that returns the solution to a minimization problem.
    Convergence failure is indicated by returning NaNs. Set ngsgloals.message_level
    to 4 for element information in case of failure. Set ngsgloals.message_level to 5
    for details on the residual.
    
    Parameters:
    
    expression : CoefficientFunction
      the objective function to be minimized
    
    startingpoint: CoefficientFunction, list/tuple of CoefficientFunctions
      The initial guess for the iterative solution of the minimization problem. In case of a list or a tuple,
      the order of starting points must match the order of the trial functions in their parent FE space.
    
    tol: double
      absolute tolerance
    
    rtol: double
      relative tolerance
    
    maxiter: int
      maximum iterations
    
    allow_fail : bool
      Returns the result of the final Newton step, even if the tolerance is not reached.
      Otherwise NaNs are returned.
    """
def NewtonCF(expression: CoefficientFunction, startingpoint: typing.Any, tol: typing.SupportsFloat | None = 1e-06, rtol: typing.SupportsFloat | None = 0.0, maxiter: typing.SupportsInt | None = 10, allow_fail: bool | None = False) -> CoefficientFunction:
    """
    Creates a CoefficientFunction that returns the solution to a nonlinear problem.
    By default, convergence failure is indicated by returning NaNs. Set ngsgloals.message_level
    to 4 for element information in case of failure. Set ngsgloals.message_level to 5 for 
    details on the residual.
    
    Parameters:
    
    expression : CoefficientFunction
      The residual of the nonlinear equation
    
    startingpoint: CoefficientFunction, list/tuple of CoefficientFunctions
      The initial guess for the iterative solution of the nonlinear problem. In case of a list or a tuple,
      the order of starting points must match the order of the trial functions in their parent FE space.
    
    tol: double
      Absolute tolerance
    
    rtol: double
      Relative tolerance
    
    maxiter: int
      Maximum number of iterations
    
    allow_fail : bool
        Returns the result of the final Newton step, even if the tolerance is not reached.
        Otherwise NaNs are returned.
    """
def SetPMLParameters(rad: typing.SupportsFloat = 1, alpha: typing.SupportsFloat = 1) -> None:
    """
    Parameters:
    
    rad : double
      input radius of PML
    
    alpha : double
      input damping factor of PML
    """
def Skew(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
def Sym(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
def Trace(arg0: CoefficientFunction) -> CoefficientFunction:
    ...
def VoxelCoefficient(start: tuple, end: tuple, values: numpy.ndarray, linear: bool = True, trafocf: typing.Any = ...) -> CoefficientFunction:
    """
    CoefficientFunction defined on a grid.
    
    Start and end mark the cartesian boundary of domain. The function will be continued by a constant function outside of this box. Inside a cartesian grid will be created by the dimensions of the numpy input array 'values'. This array must have the dimensions of the mesh and the values stored as:
    x1y1z1, x2y1z1, ..., xNy1z1, x1y2z1, ...
    
    If linear is True the function will be interpolated linearly between the values. Otherwise the nearest voxel value is taken.
    """
def Zero(arg0: pyngcore.pyngcore.Array_I_S) -> CoefficientFunction:
    ...
@typing.overload
def acos(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Inverse cosine in radians
    """
@typing.overload
def acos(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Inverse cosine in radians
    """
@typing.overload
def acos(x: ...) -> ...:
    """
    Inverse cosine in radians
    """
@typing.overload
def asin(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Inverse sine in radians
    """
@typing.overload
def asin(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Inverse sine in radians
    """
@typing.overload
def asin(x: ...) -> ...:
    """
    Inverse sine in radians
    """
@typing.overload
def atan(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Inverse tangent in radians
    """
@typing.overload
def atan(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Inverse tangent in radians
    """
@typing.overload
def atan(x: ...) -> ...:
    """
    Inverse tangent in radians
    """
@typing.overload
def atan2(y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Four quadrant inverse tangent in radians
    """
@typing.overload
def atan2(y: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128], x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Four quadrant inverse tangent in radians
    """
@typing.overload
def atan2(y: ..., x: ...) -> ...:
    """
    Four quadrant inverse tangent in radians
    """
@typing.overload
def ceil(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Round to next greater integer
    """
@typing.overload
def ceil(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Round to next greater integer
    """
@typing.overload
def ceil(x: ...) -> ...:
    """
    Round to next greater integer
    """
@typing.overload
def cos(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Cosine of argument in radians
    """
@typing.overload
def cos(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Cosine of argument in radians
    """
@typing.overload
def cos(x: ...) -> ...:
    """
    Cosine of argument in radians
    """
@typing.overload
def cosh(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Hyperbolic cosine of argument in radians
    """
@typing.overload
def cosh(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Hyperbolic cosine of argument in radians
    """
@typing.overload
def cosh(x: ...) -> ...:
    """
    Hyperbolic cosine of argument in radians
    """
@typing.overload
def erf(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Error function
    """
@typing.overload
def erf(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Error function
    """
@typing.overload
def erf(x: ...) -> ...:
    """
    Error function
    """
@typing.overload
def exp(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Exponential function
    """
@typing.overload
def exp(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Exponential function
    """
@typing.overload
def exp(x: ...) -> ...:
    """
    Exponential function
    """
@typing.overload
def floor(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Round to next lower integer
    """
@typing.overload
def floor(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Round to next lower integer
    """
@typing.overload
def floor(x: ...) -> ...:
    """
    Round to next lower integer
    """
@typing.overload
def log(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Logarithm function
    """
@typing.overload
def log(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Logarithm function
    """
@typing.overload
def log(x: ...) -> ...:
    """
    Logarithm function
    """
@typing.overload
def pow(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Power function
    """
@typing.overload
def pow(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128], y: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Power function
    """
@typing.overload
def pow(x: ..., y: ...) -> ...:
    """
    Power function
    """
@typing.overload
def sin(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Sine of argument in radians
    """
@typing.overload
def sin(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Sine of argument in radians
    """
@typing.overload
def sin(x: ...) -> ...:
    """
    Sine of argument in radians
    """
@typing.overload
def sinh(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Hyperbolic sine of argument in radians
    """
@typing.overload
def sinh(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Hyperbolic sine of argument in radians
    """
@typing.overload
def sinh(x: ...) -> ...:
    """
    Hyperbolic sine of argument in radians
    """
@typing.overload
def sqrt(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Square root function
    """
@typing.overload
def sqrt(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Square root function
    """
@typing.overload
def sqrt(x: ...) -> ...:
    """
    Square root function
    """
@typing.overload
def tan(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> typing.Any:
    """
    Tangent of argument in radians
    """
@typing.overload
def tan(x: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> typing.Any:
    """
    Tangent of argument in radians
    """
@typing.overload
def tan(x: ...) -> ...:
    """
    Tangent of argument in radians
    """
CELL: NODE_TYPE  # value = <NODE_TYPE.CELL: 3>
EDGE: NODE_TYPE  # value = <NODE_TYPE.EDGE: 1>
ELEMENT: NODE_TYPE  # value = <NODE_TYPE.ELEMENT: 4>
FACE: NODE_TYPE  # value = <NODE_TYPE.FACE: 2>
FACET: NODE_TYPE  # value = <NODE_TYPE.FACET: 5>
HEX: ET  # value = <ET.HEX: 24>
POINT: ET  # value = <ET.POINT: 0>
PRISM: ET  # value = <ET.PRISM: 22>
PYRAMID: ET  # value = <ET.PYRAMID: 21>
QUAD: ET  # value = <ET.QUAD: 11>
SEGM: ET  # value = <ET.SEGM: 1>
TET: ET  # value = <ET.TET: 20>
TRIG: ET  # value = <ET.TRIG: 10>
VERTEX: NODE_TYPE  # value = <NODE_TYPE.VERTEX: 0>
specialcf: SpecialCFCreator  # value = <ngsolve.fem.SpecialCFCreator object>
