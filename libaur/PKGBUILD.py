# -*- coding: utf-8 -*-

'''
Simple Arch Linux PKGBUILD parsing to get basic declarations. Also does basic
substitution for official variables (ie, pkgname, pkgver, etc). Does not do
positional replacement.

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
'''

import io
import re
import shlex
from .data import PB_SEARCH as SEARCH

def parse_pkgbuild(path=None, full_str=None):
    '''
    Does EXTREMELY BASIC parsing of a PKGBUILD. Only has very basic
    capabilities, and is mostly for finding variables. Also does simple
    substidution of non-bash-array variables.

    Each value is an array with the values, even for those that can only take a
    single string value.

    Arguments:
    path -- path to a PKGBUILD file
    full_str -- a single string containing the whole PKGBUILD file

    Returns:
    Dictionary
    '''
    # Pre-instantiate some variables
    pkg_dict = {
            'epoch':['0'], # default to using 0 for an epoch
            }

    # If we're given a path...
    if path:
        with open(path, "r", encoding='utf8') as pkg:
            # Create a multi-line string from the pkgbuild
            our_pkgbuild = pkg.read()
    # If we're given just the file
    elif full_str:
        our_pkgbuild = full_str
    # If neither are there then just spit out an empty list
    else:
        return {}

    # Now operate on our_pkgbuild
    # First go through each search in SEARCH
    for j in SEARCH:
        # If we find this search regex
        if SEARCH[j].search(our_pkgbuild):
            # Get the match for the search, then split out the part we want
            a = SEARCH[j].findall(our_pkgbuild)
            match = []
            # Split lines crudely for multiline stuff
            for matches in a:
                match.extend(matches.splitlines())
            # make a fresh list that will be even more cleaned up by the end
            newmatch = []
            # Go through each line in our match, cleaning up along the way
            for lines in match:
                # If anything is started by a '#' but is not part of a VCS
                # fragment, then remove it from the final product.
                no_comments = re.sub(
                        '#(?!revision|branch|tag|commit).*$', '', lines)
                # If the line still has something on it...
                if len(no_comments) > 0:
                    # Split up the words in the middle parens for single-line
                    # bash arrays
                    split_arrays = shlex.split(no_comments)
                    # Tack the new array we got to the end of newmatch
                    newmatch.extend(split_arrays)
            # Assign the newmatch array to the right spot.
            pkg_dict[j] = newmatch

    # Use this to find bash variables that we can parse and replace
    bash_vars = re.compile(
            r'\$\{?(' + '|'.join(pkg_dict.keys()) + r')(?!\[[0-9]*\]){1}\}?')

    # Now that we have gotten a finished product in pkg_dict, we need to do the
    # var substitution,
    for var in pkg_dict:
        for ind in range(len(pkg_dict[var])):
            # Replace the dictionary index at [var][ind] with the matched regex
            # group we got from bash_vars' first group.
            pkg_dict[var][ind] = bash_vars.sub(
                    lambda x: pkg_dict[x.group(1)][0], pkg_dict[var][ind])

    # Finally return the well mangled pkg_dict
    return pkg_dict
