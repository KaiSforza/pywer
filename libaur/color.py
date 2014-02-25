# -*- coding: utf-8 -*-

'''
Color definitions for use in printing

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

import sys


class Color():
    def color_on(self):
        self.black = "\x1b[30m"
        self.red = "\x1b[31m"
        self.green = "\x1b[32m"
        self.yellow = "\x1b[33m"
        self.blue = "\x1b[34m"
        self.magenta = "\x1b[35m"
        self.cyan = "\x1b[36m"
        self.white = "\x1b[37m"

        self.bold = "\x1b[1m"
        self.bold_black = "\x1b[1;30m"
        self.bold_red = "\x1b[1;31m"
        self.bold_green = "\x1b[1;32m"
        self.bold_yellow = "\x1b[1;33m"
        self.bold_blue = "\x1b[1;34m"
        self.bold_magenta = "\x1b[1;35m"
        self.bold_cyan = "\x1b[1;36m"
        self.bold_white = "\x1b[1;37m"
        self.reset = "\x1b[0m"

    def color_off(self):
        self.black = ""
        self.red = ""
        self.green = ""
        self.yellow = ""
        self.blue = ""
        self.magenta = ""
        self.cyan = ""
        self.white = ""

        self.bold = ""
        self.bold_black = ""
        self.bold_red = ""
        self.bold_green = ""
        self.bold_yellow = ""
        self.bold_blue = ""
        self.bold_magenta = ""
        self.bold_cyan = ""
        self.bold_white = ""
        self.reset = ""

    def __init__(self, use_color):

        if use_color == 0:
            self.color_off()
        elif use_color == 1:
            if sys.stdout.isatty():
                self.color_on()
            else:
                self.color_off()
        elif use_color == 2:
            self.color_on()
