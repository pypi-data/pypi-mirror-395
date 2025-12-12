from __future__ import annotations
import os as os
import pickle as pickle
from pyngcore.pyngcore import TaskManager
import typing
__all__: list = ['Timing']
class Timing:
    """
    
    Class for timing analysis of performance critical functions. Some 
    classes export a C++ function as __timing__, which returns a map 
    of performance critical parts with their timings. The class can save 
    these maps, load them and compare them. It can be saved as a benchmark 
    to be compared against.
    
    2 overloaded __init__ functions:
    
    1. __init__(name,obj,parallel=True,serial=True)
    2. __init__(filename)
    
    Parameters
    ----------
    
    name (str): Name for the timed class (for output formatting and 
        saving/loading of results)
    obj (NGSolve object): Some NGSolve class which has the __timing__ 
        functionality implemented. Currently supported classes:
            FESpace
    filename (str): Filename to load a previously saved Timing
    parallel (bool=True): Time in parallel (using TaskManager)
    serial (bool=True): Time not in parallel (not using TaskManager)
    
    """
    __firstlineno__: typing.ClassVar[int] = 5
    __static_attributes__: typing.ClassVar[tuple] = ('timings_par', 'name', 'timings')
    def CompareTo(self, folder):
        """
        
        Compares the timing with the one saved in folder 'folder' with filename 
        'name.dat'.
        """
    def CompareToBenchmark(self):
        """
        Compares the timing with the one stored as benchmark
        """
    def Save(self, folder):
        """
        Saves the pickled results in folder 'folder' 
        """
    def SaveBenchmark(self):
        """
        Makes the timing the new benchmark for that object. 
        """
    def __init__(self, name = None, obj = None, filename = None, parallel = True, serial = True):
        ...
    def __str__(self):
        ...
