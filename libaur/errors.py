# -*- coding: utf-8 -*-


class FileExists(OSError):
    pass


class ConfigMissing(OSError):
    pass


class ConfigWrongVersion(OSError):
    pass


class ArgError(Exception):
    pass
