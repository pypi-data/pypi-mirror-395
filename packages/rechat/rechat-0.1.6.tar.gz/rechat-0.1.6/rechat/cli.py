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

import argparse, os, sys
from typing import List
from mitmproxy.tools.main import mitmdump



DEFAULT_LISTEN_HOST = "localhost"
DEFAULT_LISTEN_PORT = 8910
DEFAULT_UPSTREAM = "https://api.openai.com/v1"



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
        "-m",
        "--mode",
        help="Mitmproxy mode to use, e.g. '--mode local'."
        ),


    parser.add_argument(
        "-p",
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
        "--diff",
        action="store_true",
        help=(
            "Enable diff mode: only serve requests that have a matching "
            "recorded flow; other requests will be blocked, and differences "
            "will be logged."
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



def build_mitmdump_args(args: argparse.Namespace) -> List[str]:
    """Construct the argv list for mitmdump.

    We rely on mitmproxy's CLI for most behavior and just inject our addon.
    """

    mitmdump_args: List[str] = ["mitmdump"]

    if args.mode:
        mitmdump_args += ["--mode", args.mode]
    else:
        # Basic listening config
        mitmdump_args += [
            "--listen-host",
            args.listen_host,
            "--listen-port",
            str(args.listen_port),
        ]

    # Mitmproxy verbosity flags roughly mirroring README expectations.
    if args.quiet:
        mitmdump_args.append("--quiet")
    if args.verbose:
        # mitmdump uses multiple -v for more verbosity; a single -v is enough.
        mitmdump_args.append("-v")

    # Load our package's replayer as a script/addon, using a direct file path.
    here = os.path.dirname(__file__)
    script_path = os.path.join(here, "replayer.py")
    mitmdump_args += ["-s", script_path]
        
    return mitmdump_args



def cli_entry(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)
    mitm_args = build_mitmdump_args(args)


    # mitmdump(sys.argv[1:]) style interface; we already prepended
    # a placeholder program name so we pass the full list.
    # mitmdump() will call sys.exit() internally, so we catch SystemExit
    # to translate it to an int return code when called as a function.
    try:
        # Output where rechat is listening, with the export var command, for user convenience, stderr.
        export_cmd = f"export OPENAI_BASE_URL=http://{args.listen_host}:{args.listen_port}/v1"
        print(f"Using upstream endpoint: {args.upstream}", file=sys.stderr)
        print(f"Serving Web UI at http://{args.listen_host}:{args.listen_port}. Set your OpenAI client's base URL with:\n\n  {export_cmd}\n", file=sys.stderr)

        # Pass command-line args to the replayer via an env var
        os.environ["RECHAT_ARGS"] = " ".join(argv)

        mitmdump(mitm_args[1:])  # drop the placeholder program name
    except SystemExit as exc:  # pragma: no cover - depends on mitmdump internals
        code = int(exc.code) if isinstance(exc.code, int) else 1
        return code

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(cli_entry())
