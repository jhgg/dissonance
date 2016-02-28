from .dispatcher import Dispatcher


def wait_for(*store_names):
    def wrapper(wrapped):
        wrapped._dependencies = getattr(wrapper, '_dependencies', set()) | set(store_names)
        return wrapped

    return wrapper


def handler(*events):
    def wrapper(wrapped):
        wrapped._events = getattr(wrapper, '_events', set()) | set(events)
        return wrapped

    return wrapper


class BaseStore(object):
    dispatch_token = None

    def __init__(self, stores):
        self._stores = stores
        self._dispatcher = stores.dispatcher

    def discover_handlers(self):
        for name in dir(self):
            handler_fn = getattr(self, name)
            events = getattr(handler_fn, '_events', None)
            if events and callable(handler_fn):
                for event in events:
                    self.add_handler(event, handler_fn)

    def add_handler(self, event, handler):
        self._dispatcher.on(self.dispatch_token, event, handler)

    def initialize(self):
        pass


class BaseStores(object):
    _known_stores = {}

    @classmethod
    def register(cls, name):
        def registry(store_cls):
            cls._known_stores[name] = store_cls

        return registry

    def __init__(self, *args, **kwargs):
        self.dispatcher = Dispatcher()
        self.dispatch = self.dispatcher.dispatch
        self.stores = []

        for name, store_class in self._known_stores.items():
            store = store_class(self, *args, **kwargs)
            store.dispatch_token = name
            setattr(self, name, store)
            self.stores.append(store)

        for store in self.stores:
            store.discover_handlers()
            store.initialize()
