:mod:`libaur`
=============

.. |synopsis| replace:: A python interface to an Arch User Repository.
.. module:: libaur
   :synopsis: |synopsis|

|synopsis|

The library behind pywer_.

.. _pywer: pywer.html

Description
-----------

This module is a simple python interface to the AUR_ or any other location
using that software's `RPC interface`_. The two main submodules are
:mod:`libaur.printer` and :mod:`libaur.aur`. The former is used for printing
nicely formatted output from the data pulled in by :mod:`libaur.aur`.

.. _AUR: https://aur.archlinux.org/
.. _RPC interface: https://aur.archlinux.org/rpc.php

Submodules
----------

| :mod:`libaur.aur`
| :mod:`libaur.printer`
| :mod:`libaur.PKGBUILD`
| :mod:`libaur.repo`
| :mod:`libaur.error`
| :mod:`libaur.color`
