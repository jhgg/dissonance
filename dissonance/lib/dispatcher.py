import collections
import traceback


class DispatcherContext(object):
    def __init__(self):
        self._callbacks = collections.defaultdict(list)
        self._handled = set()
        self._pending = set()
        self._current_args = None
        self._current_kwargs = None

    def add(self, store, handler):
        self._callbacks[store].append(handler)

    def dispatch(self, *args, **kwargs):
        self._handled.clear()
        self._pending.clear()
        self._current_args = args
        self._current_kwargs = kwargs

        try:
            for store in self._callbacks:
                if store in self._pending:
                    continue

                self.invoke_callbacks(store)

        finally:
            self._handled.clear()
            self._pending.clear()
            self._current_args = None
            self._current_kwargs = None

    def invoke_callbacks(self, store):
        if store not in self._callbacks:
            return

        callbacks = self._callbacks[store]
        self._pending.add(store)
        for callback in callbacks:
            dependencies = getattr(callback, '_dependencies', None)
            if dependencies:
                self.wait_for(dependencies)

            # noinspection PyBroadException
            try:
                # noinspection PyArgumentList
                callback(*self._current_args, **self._current_kwargs)

            except:
                traceback.print_exc()

        self._handled.add(store)

    def wait_for(self, dependencies):
        for dep in dependencies:
            if dep in self._pending:
                if dep not in self._handled:
                    raise RuntimeError("Circular dependency while waiting for %s" % dep)

                continue

            self.invoke_callbacks(dep)


class Dispatcher(object):
    def __init__(self):
        self._contexts = collections.defaultdict(DispatcherContext)
        self._dispatching = False

    def dispatch(self, action, *args, **kwargs):
        if self._dispatching:
            raise ValueError("Cannot dispatch while dispatching")

        if action not in self._contexts:
            return

        self._dispatching = True
        context = self._contexts[action]
        try:
            context.dispatch(*args, **kwargs)
        finally:
            self._dispatching = False

    def on(self, store, event, handler):
        self._contexts[event].add(store, handler)
        return self
