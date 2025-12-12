# CryoLock
*The advisory file lock mechanism for the paranoid; designed to work under restrictive environments.*

CryoLock is a library for file-based locking of critical sections. It's primarily developed for applications that make changes to critical files as it ensures that two instances of the same application won't interfere with one another or corrupt said critical files. A CryoLock is essentially Python's `threading.Lock` and `multiprocessing.Lock` but for threads and processes that can't interact with each other and therefore can't be provided with a shared lock instance.

- Completely systemwide. Can be used to enforce mutual exclusion even if the processes trying to acquire the lock are completely independent from one another.
- Cross-platform. Works in any environment where the required functions are available in the Python standard library (namely `os.urandom` and `os.utime`).
- Logically atomic. There are no race conditions that could allow multiple parallel threads to acquire the same lock; even if the underlying OS doesn't offer any atomic FS operations.
- Portable. Written in pure Python and without any external dependencies.
- Anywhere. Supports Python 2.7 as well as Python 3.
## Usage
Executing `help(__import__('cryolock'))` in a Python console should provide some documentation; but here are some templates:
```python
"""Simple example."""

import os
from cryolock import Lock

# Do normal stuff here...

with Lock(os.path.join(os.getcwd(), 'my-simple-lock.cryolock')):
    # Do critical stuff here...

# Continue doing normal stuff here...
```
```python
"""Example with a reentrant lock."""

import os
from cryolock import Lock, RLock

def foo(lock = None):
    if lock is None:
        lock = Lock(os.path.join(os.getcwd(), 'my-simple-lock.cryolock'))

    # Do normal stuff here...

    with lock:
        # Do critical stuff here...

    # Continue doing normal stuff here...

def bar(recursive_lock = None):
    if recursive_lock is None:
        recursive_lock = RLock(os.path.join(os.getcwd(), 'my-simple-lock.cryolock'))

    # Do normal stuff here...

    with recursive_lock:
        # Do critical stuff here...

        foo(recursive_lock)

        # Do more critical stuff here...

    # Continue doing normal stuff here...

foo()
bar()


def this_would_have_raised_a_runtime_error():
    # Do normal stuff here...

    lock = Lock(os.path.join(os.getcwd(), 'my-simple-lock.cryolock'))

    with lock:
        # Do critical stuff here...

        foo(lock)

        # Do more critical stuff here...

    # Continue doing normal stuff here...

def this_would_have_caused_a_deadlock():
    # Do normal stuff here...

    with RLock(os.path.join(os.getcwd(), 'my-simple-lock.cryolock')):
        # Do critical stuff here...

        foo()

        # Do more critical stuff here...

    # Continue doing normal stuff here...
```
```python
"""Example with a `cryolock.Lock` instance being shared between multiple threads."""

import os
from cryolock import Lock as FSLock
from threading import Lock as ThreadLock, Thread

def thread_function(thread_lock, fs_lock):
    # Do normal stuff here...

    # An acquired `cryolock.Lock` instance EXCLUSIVELY stops OTHER `cryolock.Lock` instances from accessing a
    # critical region; so utilizing a `threading.Lock` is required if you're gonna be sharing a `cryolock.Lock`
    # instance between multiple threads.
    with thread_lock:
        with fs_lock:
            # Do critical stuff here...

    # Continue doing normal stuff here...

tl = ThreadLock()
fsl = FSLock(os.path.join(os.getcwd(), 'my-shared-lock.cryolock'))
for _ in range(5):
    Thread(target=thread_function, args=(tl, fsl))
```

## Cloning and Contributing
This repository can be cloned and accepts issues and pull requests:
- Using [Radicle](https://radicle.xyz): `rad clone rad:zydhRDohqad4wUDqCGuD2zynYqVp`
- From Codeberg: https://codeberg.org/3ra/cryolock
