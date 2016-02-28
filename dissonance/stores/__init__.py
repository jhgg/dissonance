import glob
import os.path
from weakref import WeakValueDictionary
from ..lib.store import BaseStores, BaseStore, wait_for, handler


class Stores(BaseStores):
    _known_stores = {}

    def __init__(self, client, *args, **kwargs):
        self.client = client
        super(Stores, self).__init__(client, *args, **kwargs)


class Store(BaseStore):
    def __init__(self, stores, client):
        super(Store, self).__init__(stores)
        self.client = client


class ObjectHolder(Store):
    object_class = None
    weak = False

    def __init__(self, *args, **kwargs):
        super(ObjectHolder, self).__init__(*args, **kwargs)
        self._objects = {} if not self.weak else WeakValueDictionary()

    def upsert(self, data):
        object_id = int(data['id'])
        obj = self._objects.get(object_id)
        if obj is None:
            obj = self.make_object(data)
            self._objects[obj.id] = obj

        obj.update(data)
        return obj

    def update(self, data):
        object_id = int(data['id'])
        obj = self._objects.get(object_id)
        if obj is not None:
            obj.update(data)

        return obj

    def clear(self):
        self._objects.clear()

    def with_id(self, id, default=None):
        return self._objects.get(int(id), default)

    def find_one(self, predicate, default=None):
        return next((obj for obj in self._objects.values() if predicate(obj)), default)

    def find_all(self, predicate):
        return [obj for obj in self._objects.values() if predicate(obj)]

    def find_iter(self, predicate):
        return (obj for obj in self._objects.values() if predicate(obj))

    def in_bulk(self, ids):
        result = {}
        for obj_id in ids:
            obj_id = int(obj_id)

            obj = self._objects.get(id)
            if obj is not None:
                result[obj_id] = obj

        return result

    def make_object(self, data):
        # noinspection PyCallingNonCallable
        return self.object_class(self._stores, data['id'])

    def __len__(self):
        return len(self._objects)


def autodiscover():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '*.py')
    stores = glob.glob(path)
    for store in stores:
        store_name = os.path.basename(store).split('.')[0]
        if store_name[0] == '_':
            continue

        __import__('dissonance.stores.%s' % store_name)


register = Stores.register

__all__ = ['register', 'Store', 'Stores', 'ObjectHolder', 'wait_for', 'handler']
