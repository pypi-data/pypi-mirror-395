import argparse
import json
import os
import sys

import argcomplete

from . import __doc__ as package_doc
from . import api


os.system("")  # nosec

verbose = False


def main() -> None:
    parser = argparse.ArgumentParser(description="NPM Stat")
    # root
    parser.add_argument("package", nargs="?", type=str, help="Package name")
    parser.add_argument("-i", "--indent", default=2, type=int, metavar="N", help="indent level of json, default: 2")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose command output")
    parser.add_argument("-C", "--clear-cache", action="store_true", help="clear the request cache and exit")
    parser.add_argument("-V", "--version", action="store_true", help="show the package version and exit")
    subparsers = parser.add_subparsers(dest="command")
    # info
    info_parser = subparsers.add_parser("info", help="get detailed package info")
    info_parser.add_argument("pkg_version", metavar="version", nargs="?", type=str, help="Package version")
    # stats
    push_parser = subparsers.add_parser("stats", help="get package download stats")
    push_parser.add_argument("period", default="last-day", nargs="?", type=str, help="Package name")
    push_parser.add_argument("-r", "--range", action="store_true", help="show a range vs cumulative")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    if args.version:
        from importlib.metadata import version

        print(package_doc, file=sys.stderr)
        print(version("npmstat"))
        return

    if args.clear_cache:
        from .api import session

        session.cache.clear()
        print("Cache Cleared")
        return

    verb_print("package", args.package)
    if not args.package:
        exit_error("No package provided.", parser)

    if args.command == "info":
        verb_print("version", args.pkg_version)
        r = api.get_package(args.package, args.pkg_version)
        verb_print("url", r.url)
        verb_print("from_cache", r.from_cache)
        stats = r.json()
        if "readme" in stats:
            del stats["readme"]
        print(json.dumps(stats, indent=args.indent or None))
        return

    if args.command == "stats":
        verb_print("period", args.period)
        verb_print("range", args.range)
        r = api.get_downloads(args.package, args.period, args.range)
        verb_print("url", r.url)
        verb_print("from_cache", r.from_cache)
        downloads = r.json()
        print(json.dumps(downloads, indent=args.indent or None))
        return

    exit_error("No command provided.", parser)


def verb_print(name, value):
    if verbose:
        print(f"\033[35;1m{name}: \033[36;1m{value}\033[0m", file=sys.stderr)


def exit_error(message: str, arg_parser: argparse.ArgumentParser):
    print(f"\033[31;1merror: \033[33;1m{message}\033[0m", file=sys.stderr, end="\n\n")
    arg_parser.print_help(sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
