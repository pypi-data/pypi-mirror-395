"""
pybind solve
"""
from __future__ import annotations
import collections.abc
import ngsolve.comp
import ngsolve.fem
import typing
__all__ = ['Draw', 'SetVisualization', 'Tcl_Eval']
@typing.overload
def Draw(cf: ngsolve.fem.CoefficientFunction, mesh: ngsolve.comp.Mesh | ngsolve.comp.Region, name: str, sd: typing.SupportsInt = 2, autoscale: bool = True, min: typing.SupportsFloat = 0.0, max: typing.SupportsFloat = 1.0, draw_vol: bool = True, draw_surf: bool = True, reset: bool = False, title: str = '', number_format: str = '%.3e', unit: str = '', **kwargs) -> None:
    """
    Parameters:
    
    cf : ngsolve.comp.CoefficientFunction
      input CoefficientFunction to draw
    
    mesh : ngsolve.comp.Mesh
      input mesh
    
    name : string
      input name
    
    sd : int
      input subdivisions
    
    autoscale : bool
      input autscale
    
    min : float
      input minimum value. Need autoscale = false
    
    max : float
      input maximum value. Need autoscale = false
    
    draw_vol : bool
      input draw volume
    
    draw_surf : bool
      input draw surface
    
    title : string
      printed on top of colormap
    
    number_format : string
      printf-style format string for numbers under colormap
    
    unit : string
      string (ASCII only) to print after maximum value of colormap
    """
@typing.overload
def Draw(gf: ngsolve.comp.GridFunction, sd: typing.SupportsInt = 2, autoscale: bool = True, min: typing.SupportsFloat = 0.0, max: typing.SupportsFloat = 1.0, **kwargs) -> None:
    """
    Parameters:
    
    gf : ngsolve.comp.GridFunction
      input GridFunction to draw
    
    sd : int
      input subdivisions
    
    autoscale : bool
      input autscale
    
    min : float
      input minimum value. Need autoscale = false
    
    max : float
      input maximum value. Need autoscale = false
    """
@typing.overload
def Draw(mesh: ngsolve.comp.Mesh, **kwargs) -> None:
    ...
@typing.overload
def Draw(arg0: typing.Any) -> None:
    ...
def SetVisualization(deformation: bool | None = None, min: typing.SupportsFloat | None = None, max: typing.SupportsFloat | None = None, clipnormal: tuple | None = None, clipping: bool | None = None) -> None:
    """
    Set visualization options
    
    Parameters:
    
    deformation : object
      input deformation
    
    min : object
      input min
    
    max : object
      input max
    
    clipnormal : object
      input clipnormal
    
    clipping : object
      input clipping
    """
def Tcl_Eval(arg0: str) -> None:
    ...
def _GetFacetValues(arg0: ngsolve.fem.CoefficientFunction, arg1: ngsolve.comp.Mesh, arg2: collections.abc.Mapping[ngsolve.fem.ET, ngsolve.fem.IntegrationRule]) -> dict:
    ...
def _GetValues(arg0: ngsolve.fem.CoefficientFunction, arg1: ngsolve.comp.Mesh, arg2: ngsolve.comp.VorB, arg3: collections.abc.Mapping[ngsolve.fem.ET, ngsolve.fem.IntegrationRule], arg4: bool) -> dict:
    ...
def _GetVisualizationData(arg0: ngsolve.comp.Mesh, arg1: collections.abc.Mapping[ngsolve.fem.ET, ngsolve.fem.IntegrationRule]) -> dict:
    ...
def _SetLocale() -> None:
    ...
def __Cleanup() -> None:
    ...
