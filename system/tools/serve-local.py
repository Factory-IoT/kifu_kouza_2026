"""Serve the lecture on this PC using only the Python standard library."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8310)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    public = root / "public"  # Portable package layout.
    if not public.is_dir():
        public = root.parent / "web" / "public"  # Repository layout.
    if not (public / "slides.js").is_file():
        raise SystemExit("Lecture files not found. Extract the entire ZIP first.")
    try:
        server = ThreadingHTTPServer(
            ("127.0.0.1", args.port), partial(Handler, directory=str(public))
        )
    except OSError as error:
        raise SystemExit(f"Cannot start server on port {args.port}: {error}")
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Lecture: {url}\nFiles: {public}\nStop: Ctrl+C", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
