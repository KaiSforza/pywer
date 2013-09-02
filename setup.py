#!/usr/bin/env python3

from setuptools import setup
import sys
import libaur

setup(name='pywer',
      version=libaur.__version__,
      description='A simple python-based AUR helper',
      url='http://git.kaictl.net/wgiokas/pywer.git',
      author='William Giokas',
      author_email='1007380@gmail.com',
      license='MIT',
      py_modules=['libaur'],
      scripts=['pywer'],
      # Config scripts are placed in $PREFIX/share/doc/pywer
      data_files=[('share/doc/pywer', ['pywer.ini'])],
      install_requires=["requests",
                        "pyxdg"]
      )
