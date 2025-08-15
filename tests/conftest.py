# Ensure src/ is importable for tests when running from repo root
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def wait_for_port(host, port, timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Server {host}:{port} not available after {timeout} seconds")


@pytest.fixture(scope="module")
def uvicorn_server_factory():
    procs = []

    def _start(app_module, host="127.0.0.1", port=8000):
        proc = subprocess.Popen(
            [
                "uvicorn",
                f"{app_module}:app",
                "--host",
                host,
                "--port",
                str(port),
            ],
            env={**os.environ, "PYTHONPATH": "src"},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        procs.append(proc)
        wait_for_port(host, port, timeout=10)
        return proc

    yield _start

    # Teardown: terminate all started servers
    for proc in procs:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.fixture(scope="module")
def app_client_factory():
    def _app_client(app_instance):
        with TestClient(app_instance) as c:
            return c

    return _app_client
