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
import time
import errno
import random
from threading import RLock as RThreadLock, Thread
from multiprocessing import Process, Queue

try:
    from queue import Empty
except ImportError:
    from Queue import Empty

from cryolock import RLock as RFSLock

SHARED_LOCK_COUNT = 1
PROPER_THREAD_COUNT = 5
BAD_THREAD_COUNT = 5
PROCESS_COUNT = 5
ACQUIRE_PER_THREAD = 5


class RaceConditionError(Exception):
    pass


try:
    TimeoutError
except NameError:
    class TimeoutError(OSError):
        def __init__(self, *args):
            super(TimeoutError, self).__init__(*args)
            self.errno = errno.ETIME


def work(p, i, t, q, rtl, rfsl):
    time.sleep(t - time.time())
    r = ACQUIRE_PER_THREAD
    counter = 0
    while r:
        if counter > 1 and random.random() < 0.25:
            counter -= 1
            print(p + 'Releasing the lock.')
            q.put(i)
            rfsl.release()
            rtl.release()
            print(p + 'Released the lock.')
        else:
            r -= 1
            counter += 1
            print(p + 'Acquiring the lock.')
            rtl.acquire()
            rfsl.acquire()
            q.put(i)
            print(p + 'Acquired the lock.')
            time.sleep(random.random())
    for _ in range(counter):
        print(p + 'Releasing the lock.')
        q.put(i)
        rfsl.release()
        rtl.release()
        print(p + 'Released the lock.')


def simple_work(p, i, t, q, c):
    time.sleep(t - time.time())
    rfsl = RFSLock('test.cryolock', c)
    r = ACQUIRE_PER_THREAD
    counter = 0
    while r:
        if counter > 1 and random.random() < 0.25:
            counter -= 1
            print(p + 'Releasing the lock.')
            q.put(i)
            rfsl.release()
            print(p + 'Released the lock.')
        else:
            r -= 1
            counter += 1
            print(p + 'Acquiring the lock.')
            rfsl.acquire()
            q.put(i)
            print(p + 'Acquired the lock.')
            time.sleep(random.random())
    for _ in range(counter):
        print(p + 'Releasing the lock.')
        q.put(i)
        rfsl.release()
        print(p + 'Released the lock.')


if __name__ == '__main__':
    print('Starting test.')
    st = time.time() + 10.0
    results = Queue()
    tlock = RThreadLock()
    locks = [RFSLock('test.cryolock') for _ in range(SHARED_LOCK_COUNT)]
    threads = []
    k = 0
    for j in range(PROPER_THREAD_COUNT):
        threads.append(
            Thread(
                target=work,
                args=('(ProperThread-' + str(j) + ') ', k, st, results, tlock, locks[k % SHARED_LOCK_COUNT]),
            ),
        )
        threads[-1].start()
        k += 1
    for j in range(BAD_THREAD_COUNT):
        threads.append(
            Thread(
                target=simple_work,
                args=('(BadThread-' + str(j) + ') ', k, st, results, None if j == 0 else j % BAD_THREAD_COUNT),
            ),
        )
        threads[-1].start()
        k += 1
    for j in range(PROCESS_COUNT):
        threads.append(
            Process(
                target=simple_work,
                args=('(Process-' + str(j) + ') ', k, st, results, None if j == 0 else j % PROCESS_COUNT),
            ),
        )
        threads[-1].start()
        k += 1
    print('Synchronized threads. should begin in 10 seconds...')
    time.sleep(9)
    print('Dynamically analyzing results...')
    for _ in range(k):
        try:
            v = results.get(timeout=10)
            for _ in range(1, 2 * ACQUIRE_PER_THREAD):
                if results.get(timeout=10) != v:
                    raise RaceConditionError('Two or more threads simultaneously held the same lock.')
        except Empty:
            raise TimeoutError('Results queue empty for 10 seconds. Something is wrong')
    for thread in threads:
        thread.join()
    print('Test passing.')
