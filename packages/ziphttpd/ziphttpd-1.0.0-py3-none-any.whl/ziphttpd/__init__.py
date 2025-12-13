from argparse import ArgumentParser
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import logging as lg
import mimetypes
from pathlib import Path
import shutil
import sys
from typing import Self
from urllib.parse import urlsplit
import webbrowser
from zipfile import ZipFile


LOG = lg.getLogger(__name__)


@dataclass
class Settings:
    address: str
    port: int
    does_run_browser: bool
    path_zip: Path
    level_log: int

    @classmethod
    def from_args(cls, args: list[str] | None = None) -> Self:
        parser = ArgumentParser(
            description="""
                Serves the contents of a Zip file over HTTP.
            """,
        )
        parser.add_argument(
            "-b",
            "--address",
            help="IP interface (address) to bind to (default: localhost)",
            default="localhost",
        )
        parser.add_argument(
            "-p",
            "--port",
            help="""
                Port to bind to (default: random ephemeral port;
                look up the URL echoed on standard output once the server
                is started)
            """,
            type=int,
            default=0,
        )
        parser.add_argument(
            "-B",
            "--no-browser",
            dest="browser",
            default=True,
            action="store_false",
            help=(
                """
                Default behaviour is to open a window or tab of this machine's web
                browser to the server that just got started, at path /. When using
                this argument, only the web server is run, and no browsing is attempted.
                """
            )
        )
        parser.add_argument(
            "-v",
            "--verbose",
            dest="verbosity",
            action="count",
            help="""
                Logs goings-on more verbosely. Use twice for debug tracing.
            """,
        )
        parser.add_argument(
            "zipfile",
            help="Path to Zip file whose contents to serve.",
            type=Path,
        )
        ns = parser.parse_args(args)
        level_log = {
            1: lg.INFO,
            2: lg.DEBUG,
        }.get(ns.verbosity, lg.WARN)
        return cls(
            address=ns.address,
            port=int(ns.port),
            does_run_browser=bool(ns.browser),
            path_zip=Path(ns.zipfile),
            level_log=level_log,
        )


class ZipFileHandler(BaseHTTPRequestHandler):

    def __init__(self, path_zip: Path, *args, **kwargs) -> None:
        self._path_zip = path_zip
        super().__init__(*args, **kwargs)

    @classmethod
    def with_zip(cls, path_zip: Path) -> Callable[..., HTTPServer]:
        def make_handler(*args, **kwargs):
            return cls(path_zip, *args, **kwargs)

        return make_handler

    @contextmanager
    def zip_file(self) -> Iterator[ZipFile]:
        with ZipFile(self._path_zip, "r") as zf:
            yield zf

    def do_HEAD(self):
        with self.zip_file() as zf:
            self.respond_metadata(zf)

    def do_GET(self):
        with self.zip_file() as zf:
            path = self.respond_metadata(zf)
            with zf.open(path, "r") as source:
                shutil.copyfileobj(source, self.wfile)

    def respond_metadata(self, zf: ZipFile) -> str:
        _, _, path, *_ = urlsplit(self.path)
        if path.endswith("/"):
            path = f"{path}index.html"
        while path.startswith("/"):
            path = path[1:]
        try:
            zi = zf.getinfo(path)
            self.send_response(HTTPStatus.OK)
            mime_type, _ = mimetypes.guess_type(path)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.send_header("Content-Length", str(zi.file_size))
            self.end_headers()
            return path
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return ""


def make_server(interface: str, port: int, path_zip: Path) -> tuple[HTTPServer, str]:
    server = ThreadingHTTPServer(
        (interface, port),
        ZipFileHandler.with_zip(path_zip)  # type: ignore
    )
    return server, f"http://{':'.join(str(c) for c in server.server_address)}/"


def main() -> None:
    lg.basicConfig(
        level=lg.WARNING,
        format="%(localtime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    settings = Settings.from_args()
    server, url = make_server(settings.address, settings.port, settings.path_zip)
    print(f"Server set up at {url}")
    if settings.does_run_browser:
        if not webbrowser.open(url, new=2):
            LOG.error(
                "Was not able to open a browser tab or window to the server URL"
            )
    try:
        print("Service started. Type CTRL+C to exit.")
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("Server shutdown requested interactively")
    sys.exit(0)
