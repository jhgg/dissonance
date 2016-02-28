from .api_client import APIClient
from .gateway_socket import GatewaySocket

from ..lib.event_emitter import EventEmitter
from ..stores import Stores, autodiscover

autodiscover()


class Client(object):
    def __init__(self):
        self._gateway_socket = None
        self.config = {}
        self.events = EventEmitter()
        self.api_client = APIClient(self)
        self.stores = Stores(self)

    def login(self, email, password):
        self.api_client.login(email, password)
        return self

    def connect(self):
        gateway = self.api_client.discover_gateway()
        self._gateway_socket = GatewaySocket(gateway, self)
        self._gateway_socket.start()
        return self

    def join(self):
        if self._gateway_socket:
            self._gateway_socket.join()

    def handle_packet(self, packet):
        event = packet['t']
        data = packet['d']

        self.stores.dispatch(event, data)

        handler_name = 'handle_%s' % event.lower()
        handler_fn = getattr(self, handler_name, None)
        if handler_fn:
            handler_fn(data)

    def handle_ready(self, data):
        self.emit('ready', ready_data=data)

    def handle_message_create(self, message):
        message = self.stores.messages.with_id(message['id'])
        self.emit('message-create', message=message)

    def emit(self, event, **kwargs):
        self.events.emit(event, client=self, **kwargs)

    def start_debug_manhole(self, port):
        # TODO: Store this somewhere?
        from dissonance.lib.manhole import Manhole
        Manhole(self).start(9001)

        return self