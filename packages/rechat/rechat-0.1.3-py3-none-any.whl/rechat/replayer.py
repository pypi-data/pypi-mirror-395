# proxy_replay.py
from mitmproxy import http, io, ctx
import sys
from time import time
from glob import glob
from tqdm import tqdm
from marker import flow_to_markdown, markdown_blockquote
from rich.console import Console
from rich.markdown import Markdown
from debug import get_debug_html


DUMP_PATH = f"flows_{int(time())}.dump"
DUMPS_PATH = "flows*.dump"
TARGET_PATH = "/v1/chat/completions"
TARGET_SCHEME = "https"
TARGET_HOST = "api.openai.com"
TARGET_PORT = 443

# Simple in-memory buffer for the current session's markdown log that can be
# served by the debug endpoint. This keeps implementation tiny and avoids
# extra files. For long sessions this may grow, but it's sufficient for
# interactive debugging.
SESSION_MARKDOWN: list[str] = []


class Replayer:
    def __init__(self, dumps_path: str = DUMPS_PATH, dump_path: str = DUMP_PATH):
        self.dumps_path = dumps_path
        self.dump_path = dump_path
        # key: (method, path, body_bytes) -> recorded HTTPFlow
        self.cache = {}
        self._writer = None
        self._file = None
        self._console = Console()
        self._blockquote = True  # fallback: print to stdout with blockquotes


    def _cache(self, req, flow):
        # Only index chat completions on the expected path
        if req.path == TARGET_PATH and req.method.upper() == "POST":
            body = req.raw_content or b""
            key = (req.method, req.path, body)
            # Last one wins if duplicates exist
            self.cache[key] = flow

    def _handle_debug(self, flow: http.HTTPFlow) -> None:
        """Serve a tiny in-process debug UI on the same port.

        - GET /debug returns a static HTML page which loads /debug.md
        - GET /debug.md returns the accumulated session markdown.

        This intentionally stays minimal and self-contained so it doesn't
        interfere with normal proxying behavior.
        """

        # Text/markdown of the current session
        if flow.request.path.rstrip("/") == "/debug.md":
                body = "".join(SESSION_MARKDOWN) or "```python\nprint('Hello World!')\n```\n"
                flow.response = http.Response.make(
                        200,
                        body,
                        {"Content-Type": "text/markdown; charset=utf-8"},
                )
                return

        # Simple HTML shell that fetches markdown and renders it using
        # a CDN-hosted markdown renderer. This keeps the Python side tiny.
        if flow.request.path.rstrip("/") in ["/index.html", "/debug", ""]:
            html = get_debug_html()
            flow.response = http.Response.make(
                    200,
                    html,
                    {"Content-Type": "text/html; charset=utf-8"},
            )
            return

    def load(self, loader):
        # Load and index flows once at startup
        flows = []
        ctx.log.info(f"Loading dumps from {self.dumps_path}")
        for dump_file in tqdm(glob(self.dumps_path), desc="Loading dumps"):
            with open(dump_file, "rb") as f:
                reader = io.FlowReader(f)
                for flow in reader.stream():
                    if isinstance(flow, http.HTTPFlow):
                        flows.append(flow)

        ctx.log.info(f"Indexing {len(flows)} flows for cache")
        for flow in tqdm(flows, desc="Indexing flows"):
            self._cache(flow.request, flow)

        ctx.log.info(f"Built cache with {len(self.cache)} entries")

    def request(self, flow: http.HTTPFlow):
        # Handle built-in debug UI endpoints first, on the same port.
        if flow.request.path in ["/debug", "/debug.md", "/index.html", "/"]:
            self._handle_debug(flow)
            return

        # Only try to serve /v1/chat/completions from cache
        if flow.request.path != TARGET_PATH or flow.request.method.upper() != "POST":
            return  # fall back to normal proxy behavior if configured

        body = flow.request.raw_content or b""
        key = (flow.request.method, flow.request.path, body)

        cached = self.cache.get(key)
        if cached is not None and cached.response is not None:
            # Serve a copy of the recorded response
            flow.response = cached.response.copy()
            ctx.log.info(f"Cache hit for {flow.request.method} {flow.request.path}")
            md = flow_to_markdown(flow)  # for side-effect logging
            qmd = markdown_blockquote(md) if self._blockquote else md

            if self._console is not None:
                renderable_markup = Markdown(qmd)
                self._console.print(renderable_markup)
            else:
                print(qmd)


            # Also append the raw markdown to the in-memory debug buffer so
            # /debug.md (and thus /debug) can display the whole conversation.
            SESSION_MARKDOWN.append(md + "\n")

        else:
            ctx.log.warn(f"Cache miss for {flow.request.method} {flow.request.path}")
            flow.request.scheme = TARGET_SCHEME
            flow.request.host = TARGET_HOST
            flow.request.port = TARGET_PORT
    
    def response(self, flow: http.HTTPFlow) -> None:
        # record every new flow, add to cache
        if self._writer is None:
            # Create writer to save any new flows during this session
            ctx.log.info(f"Creating new dump file at {self.dump_path}")
            self._file = open(self.dump_path, "wb")
            self._writer = io.FlowWriter(self._file)


        if self._writer is not None:
            self._writer.add(flow)
            self._cache(flow.request, flow)

            #md = flow_to_markdown(flow)  # for side-effect logging
            #rendered = convert(markdown_blockquote(md))
            #print(rendered, file=sys.stderr)



    def done(self):
        # close dump cleanly
        if self._file is not None:
            self._file.close()



addons = [Replayer()]