'''Used to compile a .so or .pyd to improve speed.'''
from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import sys
import platform
def cython_compile():
    '''Compiles a Cython library to improve speed.
Requires that Cython is installed as a Python package.'''
    executable = sys.executable
    cmd = executable + ' ' + __file__ + ' build_ext --inplace'
    print('Attempting to compile using following command:')
    print(cmd)
    os.system(cmd)
def remove_cython_compilation():
    '''Deletes any compiled Cython libraries.'''
    dirloc = os.path.dirname(__file__)
    files = os.listdir(dirloc)
    files = [x for x in files if x.endswith('.so') or x.endswith('.pyd')]
    total = 0
    for n in files:
        total += 1
        os.remove(dirloc + '/' + n)
    print('Successfully removed '+str(total)+' files.')
if __name__ == '__main__':
    #Create a .pyx file:
    oldcwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    with open('lifetree.py', 'r', encoding='utf-8') as f:
        code = f.read()
    with open('pylifetree.pyx', 'w', encoding='utf-8') as f:
        f.write(code)
    compilerargs = ["-O3", "-march=native", "-ffast-math"]
    if platform.uname()[0] == 'Windows':
        compilerargs = ['/O2']
    extensions = [
        Extension(
            name="pylifetree",
            sources=["pylifetree.pyx"],
            language="c",
            extra_compile_args=compilerargs,
        )
    ]

    setup(
        name="pylifetree",
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                "language_level": "3",
                "boundscheck": False,
                "wraparound": False,
                "cdivision": True
            }
        ),
    )
    #Rename the output file:
    files = os.listdir(os.getcwd())
    files = [x for x in files if x.endswith('.so') or x.endswith('.pyd')]
    if len(files) == 0:
        raise FileNotFoundError('Could not locate compiled .so or .pyd!')
    file = files[0]
    if file.endswith('.so'):
        extension = '.so'
    else:
        extension = '.pyd'
    with open(file, 'rb') as f:
        code = f.read()
    os.remove(file)
    with open('pylifetree' + extension, 'wb') as f:
        f.write(code)
    os.chdir(oldcwd)

