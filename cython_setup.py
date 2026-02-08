'''Used to compile a .so or .pyd to improve speed.'''
from setuptools import setup, Extension
from Cython.Build import cythonize
import platform
import os
import sys
#Create a .pyx file:
f = open('lifetree.py', 'r', encoding='utf-8')
code = f.read()
f.close()
f = open('pylifetree.pyx', 'w', encoding='utf-8')
f.write(code)
f.close()
extensions = [
    Extension(
        name="pylifetree",
        sources=["pylifetree.pyx"],
        language="c",
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
        }
    ),
)
#Rename the output file:
files = os.listdir(os.getcwd())
files = [x for x in files if x.endswith('.so') or x.endswith('.pyd')]
print(files)
