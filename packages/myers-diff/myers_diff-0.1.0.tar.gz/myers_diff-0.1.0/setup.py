from setuptools import setup, Extension
from Cython.Build import cythonize
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')

extensions = [
    Extension(
        "myers_diff.myers_wrapper",
        sources=["myers_diff/myers_wrapper.pyx", "myers_diff/myers.c"],
        include_dirs=["myers_diff"],
        extra_compile_args=["-O3", "-fomit-frame-pointer", "-funroll-loops"],
    )
]

setup(
    ext_modules=cythonize(
        extensions, 
        language_level="3",
        include_path=["myers_diff"],
    ),
)
