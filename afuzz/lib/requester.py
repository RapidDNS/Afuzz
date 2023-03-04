import httpx
from afuzz.utils.common import CaseInsensitiveDict
from afuzz.settings import DEFAULT_HEADERS


class Requester:
    def __init__(self):
        self._url = None
        self._proxy_cred = None
        self._rate = 0
        self.headers = CaseInsensitiveDict(DEFAULT_HEADERS)
        self.agents = []
        self.limits = httpx.Limits(max_connections=100, max_keepalive_connections=10)
        self.session = httpx.AsyncClient(headers=self.headers, verify=False, limits=self.limits)

    def get(self):
        pass

