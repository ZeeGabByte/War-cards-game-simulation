# -*-coding:utf8;-*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("Cython_War", [r"C:\Users\admin\PycharmProjects\Bataille\War\CythonModule.pyx"])],
    include_dirs=[numpy.get_include()]
)
