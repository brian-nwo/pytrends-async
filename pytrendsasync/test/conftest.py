import proxy as proxy_py
import pytest
import time
import threading

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
