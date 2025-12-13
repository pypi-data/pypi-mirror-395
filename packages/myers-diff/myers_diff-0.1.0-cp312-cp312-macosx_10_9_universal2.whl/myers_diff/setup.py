from setuptools import setup, Extension
from Cython.Build import cythonize
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
extensions = [
    Extension(
        "myers_wrapper",
        sources=["myers_wrapper.pyx", "myers.c"],
        include_dirs=["."],
        extra_compile_args=["-O3", "-fomit-frame-pointer", "-funroll-loops"],
    )
]
setup(
    ext_modules=cythonize(extensions, language_level="3"),
)
