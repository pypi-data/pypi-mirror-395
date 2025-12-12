from __future__ import annotations
__all__ = ['BVP']
def BVP(bf, lf, gf, pre = None, pre_flags = {}, solver = None, solver_flags = {}, maxsteps = 200, tol = 1e-08, print = True, inverse = 'umfpack', needsassembling = True):
    """
    
        Solve a linear boundary value problem A(u,v) = f(v)
    
    Parameters
    ----------
    
    bf : BilinearForm
      provides the matrix. 
    
    lf : LinearForm
      provides the right hand side.
    
    gf : GridFunction
      provides the solution vector
    
    pre : Basematrix or class or string = None
      used if an iterative solver is used
      can be one of 
        * a preconditioner object
        * a preconditioner class
        * a preconditioner class name
    
    pre_flags : dictionary = { }
      flags used to create preconditioner
    
    
        
    """
