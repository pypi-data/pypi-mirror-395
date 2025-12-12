"""
Setup script for genuity package with Cython extension.
This file is required for building the Cython extension.
"""
from setuptools import setup, Extension
from Cython.Build import cythonize

# Cython extension for license validator
extensions = [
    Extension(
        "genuity.licensing.validator",
        ["genuity/licensing/validator.pyx"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"}
    ),
)
