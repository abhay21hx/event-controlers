import time
from urllib.error import URLError
from urllib.request import urlopen


deadline = time.monotonic() + 30
while time.monotonic() < deadline:
    try:
        with urlopen("http://127.0.0.1:8000/health", timeout=1) as response:
            if response.status == 200:
                raise SystemExit(0)
    except (OSError, URLError):
        time.sleep(1)

raise SystemExit("Backend did not respond at http://127.0.0.1:8000/health")
