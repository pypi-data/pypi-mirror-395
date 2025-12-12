# Copyright (C) 2025  Armin "Era" Ramezani <e@4d2.org>
#
# This file is a part of CryoLock.
#
# CryoLock is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# CryoLock is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along with CryoLock.  If not, see
# <https://www.gnu.org/licenses/>.
#
"""Stuff for compatibility."""

import os
import errno

if hasattr(__import__('threading'), 'get_ident'):
    from threading import get_ident
else:
    try:
        from _thread import get_ident
    except ImportError:
        from thread import get_ident

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List


def get_native_id():  # type: () -> str
    return str(os.getpid()) + '-' + str(get_ident())


def makedirs(path, mode = 0o777, exist_ok=False):  # type: (str, int, bool) -> None
    if exist_ok:
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode)
            except (IOError, OSError) as e:
                if e.errno != errno.EEXIST:
                    raise e
    else:
        os.makedirs(path, mode)


def scandir(path):  # type: (str) -> List[PseudoFile]
    return [PseudoFile(path, file_name) for file_name in os.listdir(path)]


class PseudoFile(object):
    def __init__(self, parent, name):  # type: (str, str) -> None
        self._name = name
        self._path = os.path.join(parent, name)

    @property
    def name(self):  # type: () -> str
        return self._name

    @property
    def path(self):  # type: () -> str
        return self._path

    def is_file(self):  # type: () -> bool
        return os.path.isfile(self._path)
