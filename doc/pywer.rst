``pywer``
=========
Synopsis
--------
| **pywer** [options] <operation>
| **pywer** -d pkg [pkg ...]
| **pywer** -i pkg [pkg ...]
| **pywer** -u [pkg [pkg ...]]
| **pywer** -s searchterm
| **pywer** -m maintainer

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
    Download package(s) specified as arguments

-s, --search
    Search for the specified term

-m, --msearch
    Search for the specified maintainer

-i, --info
    Get some basic information on the package(s) specified

-u, --update
    Check for updates on all installed packages or the specified package

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

--ignorerepo repo[,repo2,...repoN]
    Ignore the repos. Requires a comman separated list or single repo name.

-t dir, --target dir
    Download to `dir` instead of the one specified in the pywer config.

--baseurl URL
    Specify the location of an alternate AUR.

Configuration
-------------

A configuration file is installed to `$PREFIX/share/doc/pywer` by default
that is the same version as your installation of **pywer**. If you get an
error that the current configuration is not compatible with the version you
are using, use a diff application to set things right.

.. _cower: https://github.com/falconindy/cower

