``pywer``
=========
Synopsis
--------
| **pywer** [options] <operation> [target [target...]]

Description
-----------

Written in python, this project was created to provide a python
interface to the AUR, and also to emulate cower_ in its options and output.
I'm still working on the latter, but it's getting there.

It also includes a library, `libaur`, that can be imported for use in your
scripts.

Operations
----------

-d, --download
    Download package(s) specified as arguments. Requires at least one
    target.

-s, --search
    Search for the specified term. Only takes one target.

-m, --msearch
    Search for the specified maintainer. Only takes one target.

-i, --info
    Get some basic information on the package(s) specified. Takes one or
    more targets. Specify twice to get more information on a package.

-u, --update
    Check for updates on all installed packages or the specified package.
    Takes zero or more targets. With no targets, it will search for updates
    on all of the installed packages that are not in official repos. See
    **--ignorerepo**.

Options
-------

-q, --quiet
    Be quieter

-v, --verbose
    Be verbose

-f, --force
    Allow overwriting of download directory

--config file
    Use `file` as a configuration file instead of
    $XDG_CONFIG_HOME/pywer/pywer.ini

-V, --version
    Print version information

-o, --ignore-ood
    Do not display, download, or check for updates on packages marked out of
    date on the AUR.

--no-ignore-ood
    The opposite of --ignore-ood

-c, --color
    Use color

--no-color
    Don't use color

--ignorerepo repos
    Ignore the repo or list of repos. Space separated.

-t dir, --target dir
    Download to `dir` instead of the one specified in the pywer config.

--baseurl URL
    Specify the location of an alternate AUR.

--dbpath path
    For ``-u``, you can specify a dbpath on the commandline to override the
    one in your config file.

Configuration
-------------

A configuration file is installed to `$PREFIX/share/doc/pywer` by default
that is the same version as your installation of **pywer**. If you get an
error that the current configuration is not compatible with the version you
are using, use a diff application to set things right.

.. _cower: https://github.com/falconindy/cower

