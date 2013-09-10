# -*- coding: utf-8 -*-

'''
Color definitions for use in printing
'''

class Color():
    def __init__(self, use_color):
        if use_color:
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

        else:
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

