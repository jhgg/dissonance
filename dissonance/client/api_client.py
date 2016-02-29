import gevent
import requests
import time
from gevent.event import AsyncResult
from gevent.queue import Queue


class RateLimiter(object):
    def __init__(self, bucket_size, bucket_duration):
        self.bucket_size = bucket_duration
        self.bucket_duration = bucket_size
        self.last_bucket_time = time.time()
        self.last_bucket_drops = bucket_size

    def wait(self):
        now = time.time()
        if self.last_bucket_time + self.bucket_duration > now:
            self.last_bucket_time = now
            self.last_bucket_drops = self.bucket_size

        if self.last_bucket_drops < 0:
            gevent.sleep(self.bucket_duration - now - self.last_bucket_time)

    def consume(self):
        self.last_bucket_drops -= 1


class MessagePump(object):
    def __init__(self, client):
        self._client = client
        self._queue = Queue(maxsize=15)
        self._greenlet = None
        self._rate_limit = RateLimiter(10, 10)

    def start(self):
        if not self._greenlet:
            self._greenlet = gevent.spawn(self._loop)

    def _loop(self):
        while True:
            next_message, async_result = self._queue.get()
            self._rate_limit.wait()
            try:
                result = self._client._create_message(**next_message)
                self._rate_limit.consume()
                async_result.set(result)
            except Exception as e:
                async_result.set_exception(e)

    def send(self, **kwargs):
        result = AsyncResult()
        self._queue.put((kwargs, result))
        return result.get()


class APIClient(object):
    def __init__(self, client):
        self._client = client
        self._api_base = client.config.get('API_CLIENT_BASE', 'https://discordapp.com/api/{}')
        self._token = None
        self._message_pump = MessagePump(self)
        self._message_pump.start()

    def _dispatch(self, method, endpoint, data=None, send_auth_headers=True):
        kwargs = {}
        if send_auth_headers:
            headers = {}
            if not self._token:
                raise ValueError('not logged in')

            headers['Authorization'] = self._token
            kwargs['headers'] = headers

        if data:
            kwargs['json'] = data

        req = requests.request(method, self._api_base.format(endpoint), **kwargs)
        if req.status_code == 429:
            retry_after = int(req.headers.get('Retry-After', 1000)) / 1000.0
            gevent.sleep(retry_after)
            return self._dispatch(method, endpoint, data=data, send_auth_headers=send_auth_headers)

        elif req.status_code == 502:
            gevent.sleep(0.1)
            return self._dispatch(method, endpoint, data=data, send_auth_headers=send_auth_headers)

        req.raise_for_status()
        return req.json()

    _post = lambda self, *args, **kwargs: self._dispatch('post', *args, **kwargs)
    _get = lambda self, *args, **kwargs: self._dispatch('get', *args, **kwargs)
    _patch = lambda self, *args, **kwargs: self._dispatch('patch', *args, **kwargs)
    _delete = lambda self, *args, **kwargs: self._dispatch('delete', *args, **kwargs)

    @property
    def token(self):
        if not self._token:
            raise AttributeError('token')

        return self._token

    def login(self, email, password):
        response = self._post('auth/login', {
            'email': email,
            'password': password
        }, send_auth_headers=False)
        self._token = response['token']

    def discover_gateway(self):
        return self._get('gateway')['url']

    def create_message(self, channel_id, content, tts=False):
        return self._message_pump.send(channel_id=channel_id, content=content, tts=tts)

    def _create_message(self, channel_id, content, tts=False):
        payload = {
            'content': str(content)
        }
        if tts:
            payload['tts'] = True

        return self._post('channels/%s/messages' % channel_id, payload)
