"""Start an offline demo with Python's standard library only."""

from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, default=8000)
args = p.parse_args()
handler = partial(
    SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parent / "demo")
)
server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
print(f"Open http://127.0.0.1:{args.port} (Ctrl+C to stop)", flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
