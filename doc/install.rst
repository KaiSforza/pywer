Installation
############

Being a python application, installation is as simple as running ``setup.py
install`` with the correct permissions. However, I would not recommend this.
If you have pip_ installed, please run::

    $ pip install http://git.kaictl.net/wgiokas/pywer.git/snapshot/pywer-0.9.tar.gz

or, for a development version::

    $ pip install git+git://git.kaictl.net/pub/wgiokas/pywer.git#egg=pywer

The dpendencies required are included in the ``setup.py`` script and will be
installed by pip if they are not already. You can also use virtualenv_ to
install to a user-defined directory.

.. _pip: https://pypi.python.org/pypi/pip
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
