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
"""The actual lock functionality."""

import os
import time
import errno
import random
from threading import Thread

if hasattr(__import__('inspect'), 'getfullargspec'):
    from inspect import getfullargspec
else:
    from inspect import getargspec as getfullargspec

if 'exist_ok' in getfullargspec(os.makedirs).args:
    from os import makedirs
else:
    from cryolock._counterfeit import makedirs

if hasattr(os, 'scandir'):
    from os import scandir
else:
    from cryolock._counterfeit import scandir

if hasattr(__import__('threading'), 'get_native_id'):
    from threading import get_native_id
else:
    from cryolock._counterfeit import get_native_id

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Optional


class Lock(object):
    def __init__(self, path, capacity = 10):  # type: (str, Optional[float]) -> None
        """A non-recursive lock object. Once a lock has been acquired at a specific path by a `cryolock.Lock` instance,
        all other attempts across the entire system to acquire the same path **via OTHER instances** will block until
        the locked instance's `cryolock.Lock.release` is called. `cryolock.Lock`s are guaranteed to be atomic.

        Instances of `cryolock.Lock` are NOT thread-safe and only provide file-based lock mechanisms; see
        `cryolock.Lock.acquire` and `cryolock.Lock.release` for details. It is best practice to use `cryolock.Lock`
        instances in conjunction with `threading.Lock` if thread-safety or traditional lock functionality is required.

        - `path` must be a valid path formatted as a string which ends with ".cryolock". It is crucial for the path to
          either not lead to a file, to lead to a directory that contains no non-lock files, or to lead to nothing.
        - `capacity` can be a `float` that specifies after how many seconds of inactivity the lock can be considered
          dead by other `cryolock.Lock` instances across the system. This is useful for avoiding deadlocks in the case
          of system failure. Acquired instances attempt to constantly keep their lock active; trying to never take more
          than `capacity / 2` seconds between attempts. Theoretically it is possible for a `cryolock.Lock` to fail if
          the capacity is set low enough and the hardware is weak enough, so the option to completely prevent a lock
          from ever being considered dead is given and can be used by setting `capacity` to `None`.

        `cryolock.Lock` supports the context manager protocol and thus may be used in `with` statements.
        """
        if not path.endswith('.cryolock'):
            raise ValueError('`path` must end with ".cryolock".')
        self._capacity = capacity
        self._dir_path = path
        self._spec_name = str(get_native_id()) + '-' + str(id(self))
        self._spec_path = os.path.join(path, self._spec_name)
        self._holding = False
        self._keeper = None
        self._worst_time = 0

    def __enter__(self):  # type: () -> None
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: (...) -> None
        self.release()

    def _keep_lock(self):  # type: () -> None
        while self._holding:
            st = time.time()
            os.utime(self._spec_path, None)
            self._worst_time = (
                max(self._worst_time, time.time() - st)
                if self._capacity is None
                else min(self._capacity / 2, max(self._worst_time, time.time() - st))
            )
            time.sleep(self._worst_time)

    def _ripe(self):  # type: () -> None
        while True:
            st = time.time()
            ripe = True

            makedirs(self._dir_path, exist_ok=True)
            try:
                for fil in scandir(self._dir_path):
                    if fil.is_file():
                        try:
                            last_held = os.path.getmtime(fil.path)
                            try:
                                with open(fil.path) as f:
                                    capacity = float(f.read())
                                if last_held + capacity > time.time():
                                    ripe = False
                                    break
                                os.remove(fil.path)
                            except ValueError:
                                ripe = False
                                break
                        except (IOError, OSError) as e:
                            if e.errno != errno.ENOENT:
                                ripe = False
                                break
            except (IOError, OSError) as e:
                if e.errno != errno.ENOENT:
                    ripe = False
                    break
            if not ripe:
                self._worst_time = (
                    max(self._worst_time, time.time() - st)
                    if self._capacity is None
                    else min(self._capacity / 2, max(self._worst_time, time.time() - st))
                )
                time.sleep(self._worst_time)
                continue

            makedirs(self._dir_path, exist_ok=True)
            with open(self._spec_path, 'w') as f:
                f.write(str(self._capacity))
            for fil in scandir(self._dir_path):
                if fil.name != self._spec_name and fil.is_file():
                    self._safe_remove_spec_path()
                    ripe = False
                    break
            if ripe:
                break

            # If we have gotten to this point in the cycle, it means that there is at least one other thread attempting
            # to lock the same .cryolock directory as us; a thread that we are almost perfectly in sync with. Remaining
            # in sync with said thread will cause both us and it to halt indefinitely until one is terminated; therefore
            # we should do something to prevent this dance to the death. Our method is to introduce asymmetry to the
            # algorithms behind the conflicting locks by making them wait two different amounts of time before retrying;
            # hopefully enough time for the two threads to desync.

            # Using our spec_name here ensures that our seed will be different from the conflicting thread's; but there
            # is a slight chance for our seeds to generate the same number; causing the threads to still remain in sync
            # indefinitely. Appending four cryptographically random bytes to the seed will ensure that the seed will
            # change in every iteration while still remaining unique. os.urandom is not used for the entire seed due to
            # (to the best of my knowledge) being no guarantee that the underlying randomness API will be atomic on all
            # platforms.
            urbs = os.urandom(4)
            if isinstance(urbs, str):
                random.seed(self._spec_name + urbs)
            else:
                random.seed(bytes(self._spec_name, 'utf-8') + urbs)
            time.sleep(random.random())

    def _safe_remove_spec_path(self):  # type: () -> None
        while True:
            st = time.time()
            try:
                os.remove(self._spec_path)
                break
            except (IOError, OSError):
                self._worst_time = (
                    max(self._worst_time, time.time() - st)
                    if self._capacity is None
                    else min(self._capacity / 2, max(self._worst_time, time.time() - st))
                )
                time.sleep(self._worst_time)

    def acquire(self):  # type: () -> None
        """Attempt to hold the lock at the `path` the `cryolock.Lock` instance was initialized with.

        - If the path isn't being held by any `cryolock.Lock`, attempt to hold it and return once done.
        - If the path is being held by another `cryolock.Lock` instance across the system, halt until the holding
          instance stops holding the path; after which attempt to hold it and return once done.
        - If this instance is already holding the path, raise a `RuntimeError`.

        Note that returns are never immediate and the time it takes for a "lock attempt" to succeed is variable but
        statistically short; this is to ensure that each path is only ever held by either 1 or 0 locks systemwide.
        """
        if self._holding:
            raise RuntimeError(
                'Attempted to acquire a locked (or locking) instance. Make sure to call `release` on CryoLock '
                'instances before acquiring them again or create a new instance if necessary.',
            )
        self._holding = True
        self._ripe()
        self._keeper = Thread(target=self._keep_lock)
        self._keeper.start()

    def release(self):  # type: () -> None
        """Attempt to stop holding the lock at the `path` the `cryolock.Lock` instance was initialized with.

        - If this instance is already holding the path, attempt to stop holding it and return once done.
        - If this instance isn't holding the path, raise a `RuntimeError`.
        """
        if not self._holding:
            raise RuntimeError(
                'Attempted to release an unlocked (or unlocking) instance. Make sure to call acquire on CryoLock '
                'instances before trying to release them.',
            )
        self._holding = False
        if self._keeper and self._keeper.is_alive():
            self._keeper.join()
        self._safe_remove_spec_path()
        self._worst_time = 0


class RLock(Lock):
    def __init__(self, *args, **kwargs):  # type: (...) -> None
        """A recursive lock object. Once a lock has been acquired at a specific path by a `cryolock.Lock` instance, all
        other attempts across the entire system to acquire the same path **via OTHER instances** will block until
        the locked instance's `cryolock.Lock.release` is called. `cryolock.Lock`s are guaranteed to be atomic.

        Instances of `cryolock.Lock` are NOT thread-safe and only provide file-based lock mechanisms; see
        `cryolock.Lock.acquire` and `cryolock.Lock.release` for details. It is best practice to use `cryolock.Lock`
        instances in conjunction with `threading.Lock` if thread-safety or traditional lock functionality is required.

        `cryolock.RLock` takes the same arguments as `cryolock.Lock`.

        `cryolock.Lock` supports the context manager protocol and thus may be used in `with` statements.
        """
        super(RLock, self).__init__(*args, **kwargs)
        self._counter = 0

    def acquire(self):  # type: () -> None
        """Attempt to hold the lock at the `path` the `cryolock.RLock` instance was initialized with.

        - If the path isn't being held by any `cryolock.Lock`, attempt to hold it and return once done.
        - If the path is being held by another `cryolock.Lock` instance across the system, halt until the holding
          instance stops holding the path; after which attempt to hold it and return once done.
        - If this instance is already holding the path, increase an internal counter.

        Note that returns are never immediate and the time it takes for a "lock attempt" to succeed is variable but
        statistically short; this is to ensure that each path is only ever held by either 1 or 0 locks systemwide.
        """
        if self._counter == 0:
            super(RLock, self).acquire()
        self._counter += 1

    def release(self):  # type: () -> None
        """Attempt to stop holding the lock at the `path` the `cryolock.Lock` instance was initialized with.

        - If this instance is already holding the path, decrease an internal counter. If the counter reaches 0, attempt
          to stop holding the path and return once done.
        - If this instance isn't holding the path, raise a `RuntimeError`.
        """
        if self._counter <= 1:
            super(RLock, self).release()
        self._counter -= 1
