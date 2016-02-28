import socket
import code

import gevent
import sys
from io import StringIO


class ManholeConsole(code.InteractiveConsole):
    def __init__(self, sock, **kwargs):
        self.sock = sock
        self.file = sock.makefile()
        super(ManholeConsole, self).__init__(**kwargs)

    def raw_input(self, prompt=""):
        if prompt:
            self.sock.send(bytes(prompt, 'utf-8'))
        return self.file.readline()

    def write(self, data):
        if not isinstance(data, bytes):
            data = bytes(data, 'utf-8')

        self.sock.send(data)

    def runcode(self, code):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        io = StringIO()
        sys.stdout = io
        sys.stderr = io

        try:
            super(ManholeConsole, self).runcode(code)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            self.write(io.getvalue())


class ManholeClient(object):
    def __init__(self, manhole, sock, addr):
        self.manhole = manhole
        self.sock = sock
        self.addr = addr
        self.console = ManholeConsole(sock, locals={
            'client': manhole.client,
            'quit': self.kill
        })
        self._greenlet = None

    def start(self):
        self._greenlet = gevent.spawn(self.console.interact)
        self._greenlet.link(self._dead)

    def kill(self):
        if self._greenlet:
            self._greenlet.kill()
            self._greenlet = None

    def _dead(self, *args):
        print('dead pls?')
        self._greenlet = None
        self.manhole.remove_client(self)
        self.console.file.close()
        self.sock.close()


class Manhole(object):
    def __init__(self, client):
        self.client = client
        self._socket = None
        self._acceptor = None

    def start(self, port):
        self._socket = socket.socket()
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('127.0.0.1', port))
        self._socket.listen()

        self._acceptor = gevent.spawn(self._accept_loop)
        self._clients = set()
        return self

    def _accept_loop(self):
        try:
            while True:
                sock, addr = self._socket.accept()
                client = ManholeClient(self, sock, addr).start()
                self._clients.add(client)

        finally:
            self._acceptor = None

    def stop(self):
        for g in list(self._clients):
            g.kill()
        self._clients.clear()

        if self._acceptor:
            self._acceptor.kill()
            self._acceptor = None

    def remove_client(self, client):
        print('removing client', client)
        self._clients.discard(client)

    def join(self):
        if self._acceptor:
            self._acceptor.join()
