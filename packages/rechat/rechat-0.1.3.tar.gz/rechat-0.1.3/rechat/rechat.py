"""rechat CLI entry point.

For now this is a thin wrapper around mitmdump that loads
the Replayer addon from this package.

Usage examples (see README for more details):

    rechat
    rechat https://api.openai.com/v1

This keeps the implementation compact while delegating the heavy
lifting to mitmproxy.
"""

from __future__ import annotations

import argparse
import os
import shlex
import sys
from typing import List

from mitmproxy.tools.main import mitmdump


DEFAULT_LISTEN_HOST = "localhost"
DEFAULT_LISTEN_PORT = 8910
DEFAULT_UPSTREAM = "https://api.openai.com/v1"


def build_mitmdump_args(
    listen_host: str,
    listen_port: int,
    upstream: str,
    dump_pattern: str | None,
    quiet: bool,
    verbose: bool,
) -> List[str]:
    """Construct the argv list for mitmdump.

    We rely on mitmproxy's CLI for most behavior and just inject our addon.
    """

    args: List[str] = ["mitmdump"]

    # Basic listening config
    args += [
        "--listen-host",
        listen_host,
        "--listen-port",
        str(listen_port),
    ]

    # Pass upstream endpoints via env var so replayer.py can use it later
    # without coupling CLI too tightly to mitmproxy's option parsing.
    os.environ.setdefault("RECHAT_UPSTREAM", upstream)

    if dump_pattern:
        os.environ.setdefault("RECHAT_DUMPS", dump_pattern)

    # Mitmproxy verbosity flags roughly mirroring README expectations.
    if quiet:
        args.append("--quiet")
    if verbose:
        # mitmdump uses multiple -v for more verbosity; a single -v is enough.
        args.append("-v")

    # Load our package's replayer as a script/addon, using a direct file path.
    here = os.path.dirname(__file__)
    script_path = os.path.join(here, "replayer.py")
    args += ["-s", script_path]
        
    return args


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rechat",
        description="Caching and replaying man-in-the-middle proxy for OpenAI APIs.",
    )

    parser.add_argument(
        "upstream",
        nargs="?",
        default=DEFAULT_UPSTREAM,
        help=(
            "Upstream OpenAI-compatible endpoint, e.g. https://api.openai.com/v1. "
            f"Defaults to {DEFAULT_UPSTREAM}."
        ),
    )

    parser.add_argument(
        "-l",
        "--listen-port",
        type=int,
        default=DEFAULT_LISTEN_PORT,
        help=f"Local port to listen on (default: {DEFAULT_LISTEN_PORT}).",
    )

    parser.add_argument(
        "--listen-host",
        default=DEFAULT_LISTEN_HOST,
        help=f"Local host/interface to bind (default: {DEFAULT_LISTEN_HOST}).",
    )

    parser.add_argument(
        "-d",
        "--dump",
        metavar="PATTERN",
        help=(
            "Glob pattern for flow dump files to preload, e.g. 'flows*.dump'. "
            "If omitted, all flows_*.dump in the current directory may be used."
        ),
    )

    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help=(
            "Enable strict mode: only serve requests that have a matching "
            "recorded flow; other requests will be blocked."
        ),
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce verbosity (suppress most mitmdump logs).",
    )
    verbosity.add_argument(
        "--verbose",
        action="store_true",
        help="Increase verbosity (include cache hits, detailed logs).",
    )

    return parser.parse_args(argv)


def cli_entry(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    ns = parse_args(argv)

    mitm_args = build_mitmdump_args(
        listen_host=ns.listen_host,
        listen_port=ns.listen_port,
        upstream=ns.upstream,
        dump_pattern=ns.dump,
        quiet=ns.quiet,
        verbose=ns.verbose,
    )

    # mitmdump(sys.argv[1:]) style interface; we already prepended
    # a placeholder program name so we pass the full list.
    # mitmdump() will call sys.exit() internally, so we catch SystemExit
    # to translate it to an int return code when called as a function.
    try:
        # Output where rechat is listening, with the export var command, for user convenience, stderr.
        export_cmd = f"export OPENAI_BASE_URL=http://{ns.listen_host}:{ns.listen_port}/v1"
        print(f"Serving Web UI at http://{ns.listen_host}:{ns.listen_port}. Set your OpenAI client's base URL with:\n\n  {export_cmd}\n", file=sys.stderr)

        mitmdump(mitm_args[1:])  # drop the placeholder program name
    except SystemExit as exc:  # pragma: no cover - depends on mitmdump internals
        code = int(exc.code) if isinstance(exc.code, int) else 1
        return code

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(cli_entry())
