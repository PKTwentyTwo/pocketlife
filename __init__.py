'''A Python package for manipulation of patterns in cellular automata. '''
import os
#Check for .so and .pyd files:
localfiles = os.listdir(os.getcwd())
localfiles = [x for x in localfiles if x.endswith('.pyd') or x.endswith('.so')]
if 'pylifetree.so' in localfiles or 'pylifetree.pyd' in localfiles:
    try:
        from pylifetree import Lifetree
        lifetree = Lifetree
    except ImportError:
        raise Warning('''Failed to import from compiled package!
Try running cython_compile() or remove_cython_compilation()''')
        from .lifetree import Lifetree as lifetree
else:
    from .lifetree import Lifetree as lifetree
#Import the compiler regardless:
from .cython_setup import cython_compile, remove_cython_compilation
__all__ = ['lifetree', 'cython_compile', 'remove_cython_compilation']
