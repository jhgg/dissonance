import requests


class APIClient(object):
    def __init__(self, client):
        self._client = client
        self._api_base = client.config.get('API_CLIENT_BASE', 'https://discordapp.com/api/{}')
        self._token = None

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
        payload = {
            'content': str(content)
        }
        if tts:
            payload['tts'] = True

        return self._post('channels/%s/messages' % channel_id, payload)
