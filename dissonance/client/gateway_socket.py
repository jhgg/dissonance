import enum
import json
import sys
import time

import gevent
from websocket import create_connection


class Status(enum.Enum):
    DISCONNECTED = 1
    CONNECTING = 2
    CONNECTED = 3

    AWAITING_RECONNECT = 4


class GatewayOpcode(object):
    HEARTBEAT = 1
    IDENTIFY = 2


class PacketBuilder(object):
    @staticmethod
    def identify(token):
        return {
            'op': GatewayOpcode.IDENTIFY,
            'd': {
                'token': token,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'jake.py',
                    '$device': 'jake.py',
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'v': 3
            }
        }

    @staticmethod
    def heartbeat():
        return {
            'op': GatewayOpcode.HEARTBEAT,
            'd': int(time.time())
        }


class GatewaySocket(object):
    def __init__(self, gateway_url, client):
        self._gateway_url = gateway_url
        self._client = client
        self._status = Status.DISCONNECTED
        self._ws = None
        self._ws_greenlet = None
        self._heartbeat_greenlet = None
        self._loop = gevent.get_hub().loop
        self._seq = None

        ## Todo: use erlpack
        self._encode = json.dumps
        self._decode = json.loads

    def _ws_loop(self, gateway):
        self._status = Status.CONNECTING
        self._ws = create_connection(gateway)
        self._seq = 0

        self._send(PacketBuilder.identify(self._client.api_client.token))
        initial_packet = self._recv()
        self._on_initial_packet(initial_packet)
        self._on_packet(initial_packet)

        try:
            while True:
                packet = self._recv()
                self._on_packet(packet)

        finally:
            if self._heartbeat_greenlet:
                self._heartbeat_greenlet.kill()

            self._ws_greenlet = None

    def _heartbeat_loop(self, interval):
        try:
            while True:
                if not self._ws:
                    return

                self._send(PacketBuilder.heartbeat())
                gevent.sleep(interval)

        finally:
            self._heartbeat_greenlet = None

    def _send(self, payload):
        if not self._ws:
            raise ValueError('no websocket')

        return self._ws.send(self._encode(payload))

    def _recv(self):
        if not self._ws:
            raise ValueError('no websocket')

        return self._decode(self._ws.recv())

    def start(self):
        self._ws_greenlet = gevent.spawn(self._ws_loop, self._gateway_url)

    def join(self):
        self._ws_greenlet.join()

    def _on_packet(self, packet):
        self._seq = packet['s']
        self._client.handle_packet(packet)

    def _on_initial_packet(self, ready_packet):
        heartbeat_interval = int(ready_packet['d']['heartbeat_interval'] / 1000)
        if self._heartbeat_greenlet:
            self._heartbeat_greenlet.kill()

        self._heartbeat_greenlet = gevent.spawn(self._heartbeat_loop, heartbeat_interval)
