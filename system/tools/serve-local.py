"""Serve the lecture on this PC using only the Python standard library."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import webbrowser


class Handler(SimpleHTTPRequestHandler):
    """Static file handler with byte ranges for seeking bundled videos."""

    _range = None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def send_head(self):
        self._range = None
        range_header = self.headers.get("Range")
        path = Path(self.translate_path(self.path))
        if not range_header or not path.is_file():
            return super().send_head()

        match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
        size = path.stat().st_size
        if not match or not size:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        first, last = match.groups()
        if not first:
            length = int(last or 0)
            start = max(0, size - length)
            end = size - 1
        else:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        file = path.open("rb")
        self._range = (start, end)
        self.send_response(206)
        self.send_header("Content-type", self.guess_type(str(path)))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Last-Modified", self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        return file

    def copyfile(self, source, outputfile):
        if self._range is None:
            return super().copyfile(source, outputfile)
        start, end = self._range
        source.seek(start)
        remaining = end - start + 1
        while remaining:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)


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
