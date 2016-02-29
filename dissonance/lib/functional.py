import functools
from gevent.lock import RLock


def once(wrapped):
    """
    Decorates a function that takes no arguments, ensuring it's only called once & that the result
    is memoized. This function is greenlet safe.
    """
    wrapped._once_called = False
    wrapped._once_retval = None
    lock = RLock()

    @functools.wraps(wrapped)
    def wrapper():
        if wrapped._once_called:
            return wrapped._once_retval

        with lock:
            if wrapped._once_called:
                return wrapped._once_retval

            wrapped._once_retval = wrapped()
            wrapped._once_called = True

            return wrapped._once_retval

    return wrapper
