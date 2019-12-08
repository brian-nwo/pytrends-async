import proxy as proxy_py
import pytest
import time
import threading
from httpx.models import Response

def start_proxy(host_name, port):
    proxy_py.main([
        '--hostname', host_name,
        '--port', str(port),
        '--num-workers', '1'])

@pytest.fixture
def create_proxy():
    def _create_proxy(host_name, port):
        t = threading.Thread(target=start_proxy, args=([host_name, port]), daemon=True)
        t.start()
    yield _create_proxy

@pytest.fixture
def trending_searches_200_response():
    r = Response(status_code=200, headers={'Content-Type':'application/json'})
    r._cookies = dict(NID='234809jhfs09549')
    with open('trendingSearches.json', 'r') as f:
        r._text = f.read()
    return r
