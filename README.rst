pywer
=====

.. image:: http://kaictl.net:8090/job/pywer/badge/icon

A simple library based AUR helper

(pronounced like 'pyre')

Based on python, this project was started on a whim to provide a python
interface to the AUR, and also to emulate cower_ in its options and output.
I'm still working on the latter, but it's getting there.

It also includes a library, `libaur`, that can be imported for use in your
scripts.

Currently it requres pyalpm, but I'll be adding a non-pyalpm vercmp
operation soon enough.

ZSH completion is included in the sdist tarball, but is not installed by
setup.py. If you want to install it, you can manually put it where it is
needed.

.. _cower: https://github.com/falconindy/cower
