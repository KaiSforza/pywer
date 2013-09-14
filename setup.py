#!/usr/bin/env python3

from setuptools import setup
import sys
from libaur import __title__,__version__,__author__,__license__

setup(name='pywer',
      version=__version__,
      description='A simple python-based AUR helper',
      url='http://git.kaictl.net/wgiokas/pywer.git',
      author=__author__,
      author_email='1007380@gmail.com',
      license=__license__,
      packages=['libaur'],
      scripts=['pywer'],
      # Config scripts are placed in $PREFIX/share/doc/pywer
      data_files=[('share/doc/pywer', ['pywer.ini'])],
      install_requires=['requests',
                        'pyxdg'],
      provides=['pywer', __title__],
      test_suite='test',
      )
