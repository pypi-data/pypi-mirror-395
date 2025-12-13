#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import json
import os
import sys

import argcomplete

from . import __doc__ as package_doc
from . import api
from ._version import __version__


_verbose = False


def run():
    if os.name == "nt":
        os.system("")  # nosec

    parser = argparse.ArgumentParser(
        prog="npmstat",
        description="example: npmstat stats @cssnr/vitepress-swiper",
        epilog="Docs: https://cssnr.github.io/npmstat/",
    )
    # root
    parser.add_argument("-C", "--clear-cache", action="store_true", help="clear the request cache and exit")
    parser.add_argument("-V", "--version", action="store_true", help="show the package version and exit")

    # global
    common = argparse.ArgumentParser(add_help=False)
    c_group = common.add_argument_group("global options")
    c_group.add_argument("-i", "--indent", default=2, type=int, metavar="N", help="indent level of json, default: 2")
    c_group.add_argument("-p", "--purge", action="store_true", help="purge cache for this request")
    c_group.add_argument("-f", "--force-purge", action="store_true", help="force purge for this request")
    c_group.add_argument("-v", "--verbose", action="store_true", help="enable verbose command output")

    subparsers = parser.add_subparsers(dest="command", metavar="[command]")

    # info
    info_parser = subparsers.add_parser("info", parents=[common], help="get package info")
    info_parser.add_argument("package", type=str, help="Package name")
    info_parser.add_argument("pkg_version", metavar="version", nargs="?", type=str, help="Package version")

    # stats
    stats_parser = subparsers.add_parser("stats", parents=[common], help="get download stats")
    stats_parser.add_argument("package", type=str, help="Package name")
    stats_parser.add_argument("period", default="last-day", nargs="?", type=str, help="Stats period")
    stats_parser.add_argument("-r", "--range", action="store_true", help="show a range vs cumulative")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    global _verbose
    _verbose = args.verbose if hasattr(args, "verbose") else False

    if args.version:
        print(package_doc, file=sys.stderr)
        print(__version__)
        return

    if args.clear_cache:
        api.session.cache.clear()
        print("Cache Cleared")
        return

    verb_print("package", getattr(args, "package", None))
    kwargs = {"refresh": getattr(args, "purge", False), "force_refresh": getattr(args, "force_purge", False)}
    verb_print("kwargs", kwargs)

    if args.command == "info":
        verb_print("version", args.pkg_version)
        r = api.get_package(args.package, args.pkg_version, **kwargs)
        verb_print("url", r.url)
        verb_print("from_cache", r.from_cache)
        stats = r.json()
        print(json.dumps(stats, indent=args.indent or None))
        return

    if args.command == "stats":
        verb_print("period", args.period)
        verb_print("range", args.range)
        r = api.get_downloads(args.package, args.period, args.range, **kwargs)
        verb_print("url", r.url)
        verb_print("from_cache", r.from_cache)
        downloads = r.json()
        print(json.dumps(downloads, indent=args.indent or None))
        return

    print("\033[31;1merror: \033[33;1mNo command provided.\033[0m", file=sys.stderr, end="\n\n")
    parser.print_help(sys.stderr)
    sys.exit(1)


def verb_print(name, value):
    if _verbose:
        print(f"\033[35;1m{name}: \033[36;1m{value}\033[0m", file=sys.stderr)


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as error:
        print("\nError: {}".format(str(error)))
        sys.exit(1)


if __name__ == "__main__":
    main()
