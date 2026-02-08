'''Used to compile a .so or .pyd to improve speed.'''
from setuptools import setup, Extension
from Cython.Build import cythonize
import platform
import os
import sys
#Create a .pyx file:
with open('lifetree.py', 'r', encoding='utf-8') as f:
    code = f.read()
with open('pylifetree.pyx', 'w', encoding='utf-8') as f:
    f.write(code)
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
