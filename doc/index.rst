.. pywer documentation master file, created by
   sphinx-quickstart on Fri Sep  6 13:38:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. license:
  MIT/X Consortium License
  © 2013-13 William Giokas <1007380@gmail.com>
  Permission is hereby granted, free of charge, to any person obtaining a
  copy of this software and associated documentation files (the "Software"),
  to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  DEALINGS IN THE SOFTWARE.

pywer and :mod:`libaur` documentation
=====================================

pywer is a python interface to the `Arch Linux AUR`_. While the defaults
make it work with ``https://aur.archlinux.org/``, it can also be used with any
website using the AUR software. It requires `requests`_, `pyxdg`_, and
`pyalpm`_ [1]_.

While you can use the ``pywer`` script to easily search, introspect or
update from a terminal, there is also an interface provided in :mod:`libaur`
for use in your own python programs. It uses python3, though I will accept
patches for compatability with python2.7+.

This software is licensed by William Giokas under the MIT/X Consortium
License (See source). A copy of the license must be included when
distributing this software or any major chunk of this software.

.. _Arch Linux AUR: https://aur.archlinux.org/
.. _requests: http://python-requests.org
.. _pyxdg: http://freedesktop.org/Software/pyxdg
.. _pyalpm: http://projects.archlinux.org/users/remy/pyalpm.git/
.. toctree::
   :maxdepth: 2

   pywer
   libaur
   libaur.aur
   libaur.printer
   libaur.PKGBUILD
   libaur.repo
   libaur.error
   libaur.color

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. [1] We only require pyalpm for the use of vercmp. If you have some other
       way of comparing versions that is the same as that of pacman but
       written in python, or a way to use just pyalpm, please send in a
       patch. There is a ``libaur.vercmp`` branch to this repository that
       contains tests for a vercmp system.
