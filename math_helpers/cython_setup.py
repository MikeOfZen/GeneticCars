from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("MathHelperC.pyx", annotate=True, language_level=3) ,include_dirs=[numpy.get_include()]
)