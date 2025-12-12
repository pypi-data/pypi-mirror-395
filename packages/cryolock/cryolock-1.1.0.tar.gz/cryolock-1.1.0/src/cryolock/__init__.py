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
"""Systemwide pseudo-atomic lock mechanism for Python"""

from cryolock._locks import Lock, RLock

__version__ = '1.1.0'

__all__ = ['Lock', 'RLock']
