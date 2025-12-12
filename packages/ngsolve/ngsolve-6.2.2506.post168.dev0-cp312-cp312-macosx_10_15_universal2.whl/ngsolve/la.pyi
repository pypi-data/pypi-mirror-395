"""
pybind la
"""
from __future__ import annotations
import collections.abc
import ngsolve.bla
import ngsolve.ngstd
import numpy
import numpy.typing
import pyngcore.pyngcore
import typing
__all__ = ['ArnoldiSolver', 'BaseMatrix', 'BaseSparseMatrix', 'BaseVector', 'BlockMatrix', 'BlockSmoother', 'BlockVector', 'CGSolver', 'ChebyshevIteration', 'ConstEBEMatrix', 'CreateParallelVector', 'CreateVVector', 'CumulationOperator', 'DiagonalMatrix', 'DoArchive', 'DofRange', 'DynamicVectorExpression', 'EigenValues_Preconditioner', 'Embedding', 'EmbeddingTranspose', 'FETI_Jump', 'GMRESSolver', 'GetAvailableSolvers', 'IdentityMatrix', 'InnerProduct', 'KrylovSpaceSolver', 'LoggingMatrix', 'MultiVector', 'MultiVectorExpr', 'PARALLEL_STATUS', 'ParallelDofs', 'ParallelMatrix', 'PermutationMatrix', 'ProductMatrix', 'Projector', 'QMRSolver', 'QMRSolverC', 'QMRSolverD', 'Real2ComplexMatrix', 'RegisterInverseType', 'S_BaseMatrixC', 'S_BaseMatrixD', 'ScaleMatrix', 'Smoother', 'SparseCholesky_c', 'SparseCholesky_d', 'SparseFactorization', 'SparseFactorizationInterface', 'SparseMatrixDynamic', 'SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE', 'SparseMatrixN5ngbla3MatILi2ELi2EdEE', 'SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE', 'SparseMatrixN5ngbla3MatILi3ELi3EdEE', 'SparseMatrixNSt3__17complexIdEE', 'SparseMatrixSymmetricN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE', 'SparseMatrixSymmetricN5ngbla3MatILi2ELi2EdEE', 'SparseMatrixSymmetricN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE', 'SparseMatrixSymmetricN5ngbla3MatILi3ELi3EdEE', 'SparseMatrixSymmetricNSt3__17complexIdEE', 'SparseMatrixSymmetricd', 'SparseMatrixVariableBlocks', 'SparseMatrixd', 'SumMatrix', 'SymmetricBlockGaussSeidelPreconditioner', 'SymmetricGaussSeidelPreconditioner', 'TransposeMatrix']
class BaseMatrix:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def AsVector(self) -> BaseVector:
        """
        Interprets the matrix values as a vector
        """
    def CreateColVector(self) -> BaseVector:
        ...
    def CreateDeviceMatrix(self) -> BaseMatrix:
        ...
    def CreateMatrix(self) -> BaseMatrix:
        """
        Create matrix of same dimension and same sparsestructure
        """
    def CreateRowVector(self) -> BaseVector:
        ...
    def CreateSparseMatrix(self) -> ...:
        ...
    def CreateVector(self, colvector: bool = False) -> BaseVector:
        ...
    def GetInverseType(self) -> str:
        ...
    def GetOperatorInfo(self) -> str:
        ...
    def Inverse(self, freedofs: pyngcore.pyngcore.BitArray = None, inverse: None | str | object = None, flags: pyngcore.pyngcore.Flags = ...) -> BaseMatrix:
        """
        Calculate inverse of sparse matrix
        Parameters:
        
        freedofs : BitArray
          If set, invert only the rows/columns the matrix defined by the bit array, otherwise invert the whole matrix
        
        inverse : string
          Solver to use, allowed values are:
            sparsecholesky - internal solver of NGSolve for symmetric matrices
            umfpack        - solver by Suitesparse/UMFPACK (if NGSolve was configured with USE_UMFPACK=ON)
            pardiso        - PARDISO, either provided by libpardiso (USE_PARDISO=ON) or Intel MKL (USE_MKL=ON).
                             If neither Pardiso nor Intel MKL was linked at compile-time, NGSolve will look
                             for libmkl_rt in LD_LIBRARY_PATH (Unix) or PATH (Windows) at run-time.
        """
    def Mult(self, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultAdd(self, value: typing.SupportsFloat, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultAdd(self, value: complex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultScale(self, value: typing.SupportsFloat, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultScale(self, value: complex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTrans(self, value: typing.SupportsFloat, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTrans(self, value: complex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTransAdd(self, value: typing.SupportsFloat, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTransAdd(self, value: complex, x: BaseVector, y: BaseVector) -> None:
        ...
    def ToDense(self) -> typing.Any:
        ...
    def Update(self) -> None:
        """
        Update matrix
        """
    def __add__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __iadd__(self, mat: BaseMatrix) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: MultiVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ngsolve.bla.MatrixD) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Any) -> None:
        ...
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    @typing.overload
    def __mul__(self, arg0: BaseVector) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: MultiVector) -> MultiVectorExpr:
        ...
    def __neg__(self) -> BaseMatrix:
        ...
    def __radd__(self, arg0: typing.SupportsInt) -> BaseMatrix:
        ...
    @typing.overload
    def __rmul__(self, value: typing.SupportsFloat) -> BaseMatrix:
        ...
    @typing.overload
    def __rmul__(self, value: complex) -> BaseMatrix:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __timing__(self, runs: typing.SupportsInt = 10) -> float:
        ...
    def matvec(self, arg0: BaseVector) -> BaseVector:
        ...
    @property
    def H(self) -> BaseMatrix:
        """
        Return conjugate transpose of matrix (WIP, only partially supported)
        """
    @property
    def T(self) -> BaseMatrix:
        """
        Return transpose of matrix
        """
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm | None:
        ...
    @property
    def dtype(self) -> numpy.dtype:
        ...
    @property
    def height(self) -> int:
        """
        Height of the matrix
        """
    @property
    def is_complex(self) -> bool:
        """
        is the matrix complex-valued ?
        """
    @property
    def local_mat(self) -> BaseMatrix:
        ...
    @property
    def nze(self) -> int:
        """
        number of non-zero elements
        """
    @property
    def shape(self) -> tuple[int, int]:
        ...
    @property
    def width(self) -> int:
        """
        Width of the matrix
        """
class BaseSparseMatrix(BaseMatrix):
    """
    sparse matrix of any type
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def CreateBlockSmoother(self, blocks: typing.Any, parallel: bool = False, GS: bool = False) -> typing.Any:
        ...
    def CreateSmoother(self, freedofs: pyngcore.pyngcore.BitArray = None, GS: bool = False) -> typing.Any:
        ...
    def DeleteZeroElements(self, arg0: typing.SupportsFloat) -> BaseMatrix:
        ...
class BaseVector:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Add(self, vec: BaseVector, value: typing.Any) -> None:
        ...
    def Assign(self, vec: BaseVector, value: typing.Any) -> None:
        ...
    def Copy(self) -> BaseVector:
        """
        creates a new vector of same type, copy contents
        """
    def CreateDeviceVector(self, unified: bool = True, copy: bool = True) -> BaseVector:
        """
        creates a device-vector of the same type
        """
    def CreateVector(self, copy: bool = False) -> BaseVector:
        """
        creates a new vector of same type, contents is undefined if copy is false
        """
    def CreateVectors(self, num: typing.SupportsInt) -> list[BaseVector]:
        """
        creates a num new vector of same type, contents is undefined
        """
    def Cumulate(self) -> None:
        ...
    def Distribute(self) -> None:
        ...
    def FV(self) -> typing.Any:
        ...
    def GetParallelStatus(self) -> PARALLEL_STATUS:
        ...
    def InnerProduct(self, other: BaseVector, conjugate: bool = True) -> typing.Any:
        """
        Computes (complex) InnerProduct
        """
    def Norm(self) -> float:
        """
        Calculate Norm
        """
    def Range(self, from: typing.SupportsInt, to: typing.SupportsInt) -> BaseVector:
        """
        Return values from given range
        """
    def Reshape(self, width: typing.SupportsInt) -> ngsolve.bla.FlatMatrixD:
        ...
    def SetParallelStatus(self, stat: PARALLEL_STATUS) -> None:
        ...
    def SetRandom(self, seed: typing.SupportsInt | None = None) -> None:
        ...
    def __add__(self, arg0: ...) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, ind: typing.SupportsInt) -> typing.Any:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> BaseVector:
        """
        Return values at given position
        """
    @typing.overload
    def __getitem__(self, arg0: ngsolve.ngstd.IntRange) -> BaseVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: DofRange) -> BaseVector:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __iadd__(self, vec: BaseVector) -> BaseVector:
        ...
    @typing.overload
    def __iadd__(self, arg0: ...) -> BaseVector:
        ...
    @typing.overload
    def __imul__(self, value: typing.SupportsFloat) -> BaseVector:
        ...
    @typing.overload
    def __imul__(self, value: complex) -> BaseVector:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt, complex: bool = False, entrysize: typing.SupportsInt = 1) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ...) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        ...
    @typing.overload
    def __isub__(self, vec: BaseVector) -> BaseVector:
        ...
    @typing.overload
    def __isub__(self, arg0: ...) -> BaseVector:
        ...
    @typing.overload
    def __itruediv__(self, value: typing.SupportsFloat) -> BaseVector:
        ...
    @typing.overload
    def __itruediv__(self, value: complex) -> BaseVector:
        ...
    def __len__(self) -> int:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat) -> ...:
        ...
    @typing.overload
    def __rmul__(self, arg0: complex) -> ...:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt, value: typing.SupportsFloat) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt, value: complex) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: typing.SupportsFloat) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: complex) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, vec: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, inds: slice, vec: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, inds: DofRange, vec: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, value: typing.SupportsFloat) -> None:
        """
        Set value for range of indices
        """
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, value: complex) -> None:
        """
        Set value for range of indices
        """
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, vec: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt, vec: ngsolve.bla.FlatVectorD) -> None:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt, vec: ngsolve.bla.FlatVectorC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: pyngcore.pyngcore.BitArray, arg1: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: pyngcore.pyngcore.BitArray, arg1: typing.SupportsFloat) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: ...) -> ...:
        ...
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm | None:
        ...
    @property
    def data(self) -> BaseVector:
        ...
    @data.setter
    def data(self, arg1: ...) -> None:
        ...
    @property
    def is_complex(self) -> bool:
        ...
    @property
    def local_vec(self) -> BaseVector:
        ...
    @property
    def size(self) -> int:
        ...
class BlockMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, inds: tuple) -> BaseMatrix:
        """
        Return value at given position
        """
    def __init__(self, mats: collections.abc.Sequence[collections.abc.Sequence[BaseMatrix]]) -> None:
        """
        Make BlockMatrix with given array of matrices
        """
    @property
    def col_nblocks(self) -> int:
        ...
    @property
    def row_nblocks(self) -> int:
        ...
class BlockSmoother(BaseMatrix):
    """
    block Jacobi and block Gauss-Seidel smoothing
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Smooth(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt = 1) -> None:
        """
        performs steps block-Gauss-Seidel iterations for the linear system A x = b
        """
    def SmoothBack(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt = 1) -> None:
        """
        performs steps block-Gauss-Seidel iterations for the linear system A x = b in reverse order
        """
class BlockVector(BaseVector):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, ind: typing.SupportsInt) -> BaseVector:
        """
        Return block at given position
        """
    def __init__(self, vecs: collections.abc.Sequence[BaseVector]) -> None:
        """
        Makes BlockVector by given array of vectors
        """
    @property
    def nblocks(self) -> int:
        """
        number of blocks in BlockVector
        """
class ConstEBEMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, h: typing.SupportsInt, w: typing.SupportsInt, matrix: ngsolve.bla.MatrixD, col_ind: list, row_ind: list) -> None:
        ...
    @property
    def col_ind(self) -> ...:
        ...
    @property
    def mat(self) -> ngsolve.bla.FlatMatrixD:
        ...
    @property
    def row_ind(self) -> ...:
        ...
class CumulationOperator(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: ParallelDofs) -> None:
        ...
class DiagonalMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: BaseVector) -> None:
        ...
class DofRange(ngsolve.ngstd.IntRange):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class DynamicVectorExpression:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def CreateVector(self) -> BaseVector:
        """
        create vector
        """
    def Evaluate(self) -> BaseVector:
        """
        create vector and evaluate expression into it
        """
    def InnerProduct(self, arg0: BaseVector) -> float:
        ...
    def Norm(self) -> float:
        ...
    def __add__(self, arg0: DynamicVectorExpression) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> None:
        ...
    def __neg__(self) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __rmul__(self, arg0: complex) -> DynamicVectorExpression:
        ...
    def __sub__(self, arg0: DynamicVectorExpression) -> DynamicVectorExpression:
        ...
class Embedding(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, height: typing.SupportsInt, range: ngsolve.ngstd.IntRange, complex: bool = False) -> None:
        """
        Linear operator embedding a shorter vector into a longer vector
        """
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
class EmbeddingTranspose(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __rmatmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
class FETI_Jump(BaseMatrix):
    """
    B-matrix of the FETI-system
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, pardofs: ParallelDofs) -> None:
        ...
    @typing.overload
    def __init__(self, pardofs: ParallelDofs, u_pardofs: ParallelDofs) -> None:
        ...
    @property
    def col_pardofs(self) -> ParallelDofs:
        ...
    @property
    def row_pardofs(self) -> ParallelDofs:
        ...
class IdentityMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt, complex: bool = False) -> None:
        ...
class KrylovSpaceSolver(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def GetSteps(self) -> int:
        ...
    def SetAbsolutePrecision(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def maxsteps(self) -> int:
        ...
    @maxsteps.setter
    def maxsteps(self, arg1: typing.SupportsInt) -> None:
        ...
    @property
    def tol(self) -> float:
        ...
    @tol.setter
    def tol(self, arg1: typing.SupportsFloat) -> None:
        ...
class LoggingMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, mat: BaseMatrix, label: str, logfile: str = 'stdout', comm: pyngcore.pyngcore.MPI_Comm | None = None) -> None:
        ...
class MultiVector(MultiVectorExpr):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Append(self, arg0: BaseVector) -> None:
        ...
    def AppendOrthogonalize(self, vec: BaseVector, ipmat: ... = None, parallel: bool = True, iterations: typing.SupportsInt = 2) -> typing.Any:
        """
        assumes that existing vectors are orthogonal, and orthogonalize new vector against existing vectors
        """
    def Expand(self, arg0: typing.SupportsInt) -> None:
        """
        deprecated, use Extend instead
        """
    def Extend(self, arg0: typing.SupportsInt) -> None:
        ...
    @typing.overload
    def InnerProduct(self, other: MultiVector, conjugate: bool = True) -> typing.Any:
        ...
    @typing.overload
    def InnerProduct(self, other: BaseVector, conjugate: bool = True) -> typing.Any:
        ...
    @typing.overload
    def InnerProduct(self, other: MultiVectorExpr, conjugate: bool = True) -> typing.Any:
        ...
    def Orthogonalize(self, ipmat: ... = None) -> typing.Any:
        """
        Orthogonalize vectors by modified Gram-Schmidt, returns R-factor of QR decomposition (only ipmat version, for the moment)
        """
    @typing.overload
    def Replace(self, ind: typing.SupportsInt, v2: BaseVector) -> None:
        ...
    @typing.overload
    def Replace(self, inds: collections.abc.Sequence[typing.SupportsInt], mv2: MultiVector) -> None:
        ...
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> BaseVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> MultiVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: pyngcore.pyngcore.Array_I_S) -> MultiVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: tuple[slice, slice]) -> MultiVector:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector, arg1: typing.SupportsInt) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.SupportsInt, arg1: typing.SupportsInt, arg2: bool) -> None:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.VectorD) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.VectorC) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.MatrixD) -> MultiVectorExpr:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.MatrixC) -> MultiVectorExpr:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: typing.SupportsFloat) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: complex) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: MultiVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: MultiVectorExpr) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: collections.abc.Sequence[typing.SupportsInt], arg1: MultiVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: collections.abc.Sequence[typing.SupportsInt], arg1: MultiVectorExpr) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def data(self) -> MultiVector:
        ...
    @data.setter
    def data(self, arg1: MultiVectorExpr) -> None:
        ...
class MultiVectorExpr:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Evaluate(self) -> ...:
        ...
    def InnerProduct(self, arg0: typing.Any) -> typing.Any:
        ...
    @typing.overload
    def Scale(self, arg0: ngsolve.bla.VectorD) -> MultiVectorExpr:
        ...
    @typing.overload
    def Scale(self, arg0: ngsolve.bla.VectorC) -> MultiVectorExpr:
        ...
    def __add__(self, arg0: MultiVectorExpr) -> MultiVectorExpr:
        ...
    def __neg__(self) -> MultiVectorExpr:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat) -> MultiVectorExpr:
        ...
    @typing.overload
    def __rmul__(self, arg0: complex) -> MultiVectorExpr:
        ...
    def __sub__(self, arg0: MultiVectorExpr) -> MultiVectorExpr:
        ...
class PARALLEL_STATUS:
    """
    enum of possible parallel statuses
    
    Members:
    
      DISTRIBUTED
    
      CUMULATED
    
      NOT_PARALLEL
    """
    CUMULATED: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.CUMULATED: 1>
    DISTRIBUTED: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.DISTRIBUTED: 0>
    NOT_PARALLEL: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.NOT_PARALLEL: 2>
    __members__: typing.ClassVar[dict[str, PARALLEL_STATUS]]  # value = {'DISTRIBUTED': <PARALLEL_STATUS.DISTRIBUTED: 0>, 'CUMULATED': <PARALLEL_STATUS.CUMULATED: 1>, 'NOT_PARALLEL': <PARALLEL_STATUS.NOT_PARALLEL: 2>}
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
class ParallelDofs:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Dof2Proc(self, dof: typing.SupportsInt) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    def EnumerateGlobally(self, freedofs: pyngcore.pyngcore.BitArray = None) -> tuple[typing.Any, typing.Any]:
        ...
    def ExchangeProcs(self) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    def MasterDofs(self) -> pyngcore.pyngcore.BitArray:
        ...
    def Proc2Dof(self, proc: typing.SupportsInt) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    def SubSet(self, dofs: pyngcore.pyngcore.BitArray) -> ParallelDofs:
        ...
    def __init__(self, dist_procs: typing.Any, comm: pyngcore.pyngcore.MPI_Comm) -> None:
        ...
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm:
        ...
    @property
    def entrysize(self) -> int:
        ...
    @property
    def ndofglobal(self) -> int:
        """
        number of global degrees of freedom
        """
    @property
    def ndoflocal(self) -> int:
        """
        number of degrees of freedom
        """
class ParallelMatrix(BaseMatrix):
    """
    MPI-distributed matrix
    """
    class PARALLEL_OP:
        """
        enum of possible parallel ops
        
        Members:
        
          C2C
        
          C2D
        
          D2C
        
          D2D
        """
        C2C: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.C2C: 3>
        C2D: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.C2D: 2>
        D2C: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.D2C: 1>
        D2D: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.D2D: 0>
        __members__: typing.ClassVar[dict[str, ParallelMatrix.PARALLEL_OP]]  # value = {'C2C': <PARALLEL_OP.C2C: 3>, 'C2D': <PARALLEL_OP.C2D: 2>, 'D2C': <PARALLEL_OP.D2C: 1>, 'D2D': <PARALLEL_OP.D2D: 0>}
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
    C2C: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.C2C: 3>
    C2D: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.C2D: 2>
    D2C: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.D2C: 1>
    D2D: typing.ClassVar[ParallelMatrix.PARALLEL_OP]  # value = <PARALLEL_OP.D2D: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, mat: BaseMatrix, pardofs: ParallelDofs, op: ParallelMatrix.PARALLEL_OP = ...) -> None:
        ...
    @typing.overload
    def __init__(self, mat: BaseMatrix, row_pardofs: ParallelDofs, col_pardofs: ParallelDofs, op: ParallelMatrix.PARALLEL_OP = ...) -> None:
        ...
    @property
    def col_pardofs(self) -> ParallelDofs:
        ...
    @property
    def local_mat(self) -> BaseMatrix:
        ...
    @property
    def op_type(self) -> ParallelMatrix.PARALLEL_OP:
        ...
    @property
    def row_pardofs(self) -> ParallelDofs:
        ...
class PermutationMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, w: typing.SupportsInt, ind: collections.abc.Sequence[typing.SupportsInt]) -> None:
        ...
class ProductMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def matA(self) -> BaseMatrix:
        ...
    @property
    def matB(self) -> BaseMatrix:
        ...
class Projector(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def Project(self, arg0: BaseVector) -> BaseVector:
        """
        project vector inline
        """
    @typing.overload
    def Project(self, arg0: MultiVector) -> MultiVector:
        """
        project vector inline
        """
    def __init__(self, mask: pyngcore.pyngcore.BitArray, range: bool) -> None:
        """
        Linear operator projecting to true/false bits of BitArray mask, depending on argument range
        """
class QMRSolverC(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class QMRSolverD(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class Real2ComplexMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class S_BaseMatrixC(BaseMatrix):
    """
    base sparse matrix
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class S_BaseMatrixD(BaseMatrix):
    """
    base sparse matrix
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class ScaleMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def mat(self) -> BaseMatrix:
        ...
class Smoother(BaseMatrix):
    """
    Jacobi and Gauss-Seidel smoothing
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Smooth(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt = 1) -> None:
        """
        performs one step Gauss-Seidel iteration for the linear system A x = b
        """
    def SmoothBack(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt = 1) -> None:
        """
        performs one step Gauss-Seidel iteration for the linear system A x = b in reverse order
        """
class SparseCholesky_c(SparseFactorization):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class SparseCholesky_d(SparseFactorization):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class SparseFactorization(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Smooth(self, arg0: BaseVector, arg1: BaseVector) -> None:
        """
        perform smoothing step (needs non-symmetric storage so symmetric sparse matrix)
        """
class SparseFactorizationInterface(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def Analyze(self) -> None:
        ...
    def Factor(self) -> None:
        ...
    def GetInnerMatrix(self) -> BaseSparseMatrix:
        ...
    def Update(self) -> None:
        ...
    def __init__(self, mat: BaseSparseMatrix, freedofs: pyngcore.pyngcore.BitArray = None) -> None:
        ...
class SparseMatrixDynamic(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat2C:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat2C) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi2ELi2EdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat2D:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat2D) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat3C:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat3C) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi3ELi3EdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat3D:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat3D) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixNSt3__17complexIdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> complex:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: complex) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixSymmetricN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE(SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixSymmetricN5ngbla3MatILi2ELi2EdEE(SparseMatrixN5ngbla3MatILi2ELi2EdEE):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixSymmetricN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE(SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixSymmetricN5ngbla3MatILi3ELi3EdEE(SparseMatrixN5ngbla3MatILi3ELi3EdEE):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixSymmetricNSt3__17complexIdEE(SparseMatrixNSt3__17complexIdEE):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixSymmetricd(SparseMatrixd):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SparseMatrixVariableBlocks(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class SparseMatrixd(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(indi: pyngcore.pyngcore.Array_I_S, indj: pyngcore.pyngcore.Array_I_S, values: pyngcore.pyngcore.Array_D_S, h: typing.SupportsInt, w: typing.SupportsInt) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt, w: typing.SupportsInt) -> SparseMatrixd:
        ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> float:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, std: ..., std: ..., mat: ..., std: ..., std: ...) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: typing.SupportsFloat) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SumMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def matA(self) -> BaseMatrix:
        ...
    @property
    def matB(self) -> BaseMatrix:
        ...
class SymmetricBlockGaussSeidelPreconditioner(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class SymmetricGaussSeidelPreconditioner(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class TransposeMatrix(BaseMatrix):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def mat(self) -> BaseMatrix:
        ...
def ArnoldiSolver(mata: BaseMatrix, matm: BaseMatrix, freedofs: pyngcore.pyngcore.BitArray, vecs: list, shift: complex = ..., inverse: str | None = None) -> ngsolve.bla.VectorC:
    """
    Shift-and-invert Arnoldi eigenvalue solver
    
    Solves the generalized linear EVP A*u = M*lam*u using an Arnoldi iteration for the 
    shifted EVP (A-shift*M)^(-1)*M*u = lam*u with a Krylow space of dimension 2*len(vecs)+1.
    len(vecs) eigenpairs with the closest eigenvalues to the shift are returned.
    
    Parameters:
    
    mata : ngsolve.la.BaseMatrix
      matrix A
    
    matm : ngsolve.la.BaseMatrix
      matrix M
    
    freedofs : nsolve.ngstd.BitArray
      correct degrees of freedom
    
    vecs : list
      list of BaseVectors for writing eigenvectors
    
    shift : object
      complex or real shift
    """
def CGSolver(mat: BaseMatrix, pre: BaseMatrix, complex: bool = False, printrates: bool = True, precision: typing.SupportsFloat = 1e-08, maxsteps: typing.SupportsInt = 200, conjugate: bool = False, maxiter: typing.SupportsInt | None = None) -> KrylovSpaceSolver:
    """
    A CG Solver.
    
    Parameters:
    
    mat : ngsolve.la.BaseMatrix
      input matrix 
    
    pre : ngsolve.la.BaseMatrix
      input preconditioner matrix
    
    complex : bool
      input complex, if not set it is deduced from matrix type
    
    printrates : bool
      input printrates
    
    precision : float
      input requested precision. CGSolver stops if precision is reached.
    
    maxsteps : int
      input maximal steps. CGSolver stops after this steps.
    """
def ChebyshevIteration(mat: BaseMatrix = None, pre: BaseMatrix = None, steps: typing.SupportsInt = 3, lam_min: typing.SupportsFloat = 1, lam_max: typing.SupportsFloat = 1) -> BaseMatrix:
    ...
def CreateParallelVector(pardofs: ParallelDofs, status: PARALLEL_STATUS) -> ...:
    ...
def CreateVVector(size: typing.SupportsInt, complex: bool = False, entrysize: typing.SupportsInt = 1) -> ...:
    ...
def DoArchive(arg0: ngsolve.ngstd.Archive, arg1: BaseMatrix) -> ngsolve.ngstd.Archive:
    ...
def EigenValues_Preconditioner(mat: BaseMatrix, pre: BaseMatrix, tol: typing.SupportsFloat = 1e-10) -> ngsolve.bla.VectorD:
    """
    Calculate eigenvalues of pre * mat, where pre and mat are positive definite matrices.
    The typical usecase of this function is to calculate the condition number of a preconditioner.It uses the Lanczos algorithm and bisection for the tridiagonal matrix
    """
def GMRESSolver(mat: BaseMatrix, pre: BaseMatrix, printrates: bool = True, precision: typing.SupportsFloat = 1e-08, maxsteps: typing.SupportsInt = 200) -> KrylovSpaceSolver:
    """
    A General Minimal Residuum (GMRES) Solver.
    
    Parameters:
    
    mat : ngsolve.la.BaseMatrix
      input matrix 
    
    pre : ngsolve.la.BaseMatrix
      input preconditioner matrix
    
    printrates : bool
      input printrates
    
    precision : float
      input requested precision. GMRESSolver stops if precision is reached.
    
    maxsteps : int
      input maximal steps. GMRESSolver stops after this steps.
    """
def GetAvailableSolvers() -> list:
    ...
def InnerProduct(x: typing.Any, y: typing.Any, **kwargs) -> typing.Any:
    """
    Computes InnerProduct of given objects
    """
def QMRSolver(mat: BaseMatrix, pre: BaseMatrix, printrates: bool = True, precision: typing.SupportsFloat = 1e-08, maxsteps: typing.SupportsInt = 200) -> KrylovSpaceSolver:
    """
    A Quasi Minimal Residuum (QMR) Solver.
    
    Parameters:
    
    mat : ngsolve.la.BaseMatrix
      input matrix 
    
    pre : ngsolve.la.BaseMatrix
      input preconditioner matrix
    
    printrates : bool
      input printrates
    
    precision : float
      input requested precision. QMRSolver stops if precision is reached.
    
    maxsteps : int
      input maximal steps. QMRSolver stops after this steps.
    """
def RegisterInverseType(arg0: str, arg1: typing.Any) -> None:
    ...
