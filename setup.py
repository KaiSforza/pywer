#!/usr/bin/env python3

from setuptools import setup
import libaur

setup(name='pywer',
      version=libaur.__version__,
      description='A simple python-based AUR helper',
      url='http://git.kaictl.net/wgiokas/pywer.git',
      author=libaur.__author__,
      author_email=libaur.__authoremail__,
      license=libaur.__license__,
      packages=[libaur.__title__],
      scripts=['pywer'],
      # Config scripts are placed in $PREFIX/share/doc/pywer
      data_files=[('share/doc/pywer', ['pywer.ini']),
                  ('share/licenses/pywer', ['LICENSE'])],
      install_requires=['requests',
                        'pyxdg'],
      provides=['pywer', libaur.__title__],
      test_suite='test',
      )
