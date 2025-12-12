"""Transforms (Finish: muuntuu) helper tool."""

import argparse
import os
import pathlib

from typing import Union  # py39 does not handle |

__version__ = '2025.9.14'
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = [
    'APP_ALIAS',
    'APP_NAME',
    'DEBUG',
    'ENCODING',
    'ENC_ERRS',
    'JSON',
    'NL',
    'Options',
    'PathLike',
    'Request',
    'VERSION',
    'VERSION_INFO',
    'YML',
]

APP_ALIAS = str(pathlib.Path(__file__).parent.name)
APP_ENV = APP_ALIAS.upper()
APP_NAME = locals()['__doc__']

DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))

ENCODING = 'utf-8'
ENC_ERRS = 'ignore'

NL = '\n'
JSON = 'json'
YML = 'yaml'

Options = dict[str, Union[bool, int, str]]
PathLike = Union[pathlib.Path, str]
Request = argparse.Namespace
VERSION = __version__
VERSION_INFO = __version_info__
