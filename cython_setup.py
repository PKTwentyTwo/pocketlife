from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

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
print('a')
