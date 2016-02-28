import logging
import re
import gevent
import time
from gevent.event import Event
from .utils.periodic import Periodic
from .storage import get_store_by_name
from .web import Web
from .module import Modules
from .utils.env import EnvFallbackDict
from . import version
from .client import Client

logger = logging.getLogger('dissonance.dissonance')


class Dissonance(object):
    _name = None
    _web = None

    def __init__(self, config):
        opts_for = lambda name: EnvFallbackDict(name, getattr(config, '%s_opts' % name, {}))

        self._opts = EnvFallbackDict(None, getattr(config, 'dissonance_opts', {}))
        storage_class = get_store_by_name(self._opts.get('storage', getattr(config, 'storage', 'shelve')))

        self.config = config
        self.client = Client()

        self._storage = storage_class(self, opts_for('storage'))
        self.modules = Modules(self)
        self._storage_sync_periodic = Periodic(int(self._opts.get('storage_sync_interval', 600)),
                                               self.modules._save_loaded_module_data)
        self._stop_event = Event()
        self._stop_event.set()

        self.client.events.on('message-create', self._handle_message)

    def _handle_message(self, message, **kwargs):
        # Schedule the handling of the message to occur during the next iteration of the event loop.
        gevent.spawn_raw(self.__handle_message, message)

    def __handle_message(self, message):
        logger.debug("Incoming message %r", message)
        start = time.time()

        message._dissonance = self
        message.targeting_client = message.content.startswith('doot, ')
        self.modules._handle_message(message)
        end = time.time()

        logger.debug("Took %.5f seconds to handle message %r", end - start, message)

    def _get_module_data(self, module):
        logger.debug("Getting module data for module %s", module.name)
        return self._storage.get_data_for_module_name(module.name)

    @property
    def name(self):
        return self.client.me.username

    @property
    def running(self):
        return not self._stop_event.is_set()

    @property
    def stopped(self):
        return not self.running

    @property
    def version(self):
        return version

    def run(self, auto_join=False):
        """
            Runs Dissonance, loading all the modules, starting the web service, and starting the adapter.

            If auto_join=True, this function will not return, and will run until dissonance stops if starting dissonance from
            outside of a greenlet.

        """
        if self.running:
            raise RuntimeError("Dissonance is already running!")

        logger.info("Starting Dissonance v%s", self.version)

        logger.info("Starting storage %s", self._storage)
        self._storage.start()

        logger.info("Loading modules")
        self.modules.load_all()

        if getattr(self.config, 'web', False) or str(self._opts.get('web', False)).upper() == 'TRUE':
            self._web = Web(self, EnvFallbackDict('web', getattr(self.config, 'web_opts', {})))
            self._web.start()

        logger.info("Attempting to log in as %s" % self._opts['email'])
        self.client.login(self._opts['email'], self._opts['password'])
        logger.info("Starting connection to Discord")
        self.client.start()
        self._storage_sync_periodic.start(right_away=False)
        self._stop_event.clear()

        # If we are the main greenlet, chances are we probably want to never return,
        # so the main greenlet won't exit, and tear down everything with it.
        if auto_join and gevent.get_hub().parent == gevent.getcurrent():
            self.join()

    def join(self, timeout=None):
        """
            Blocks until Dissonance is stopped.
        """
        if self.stopped:
            raise RuntimeError("Dissonance is not running!")

        self._stop_event.wait(timeout)

    def stop(self):
        """
            Stops dissonance, turning off the web listener, unloading modules, and stopping the adapter.
        """
        if self.stopped:
            raise RuntimeError("Dissonance is not running!")

        logger.info('Stopping Dissonance')
        try:
            self.modules.unload_all()

            if self._web:
                self._web.stop()
                self._web = None

            self.client.stop()
            self._storage_sync_periodic.stop()
            self._storage.stop()

        finally:
            self._stop_event.set()

    def on_module_error(self, module, e):
        print(module, e)
