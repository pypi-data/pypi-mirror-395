import argparse
import logging


def build_parser():
    """Build and configure an ArgumentParser with subcommands"""
    parser = argparse.ArgumentParser(
        prog="ex_cd.tools",
        description="ex-cd tools for gallery management"
    )

    # Common options
    parser.add_argument(
        "-c", "--config",
        dest="config", type=str,
        help="Path to config json file or a json string",
        default=None,
    )
    parser.add_argument(
        "-q", "--quiet",
        dest="loglevel", default=logging.INFO,
        action="store_const", const=logging.ERROR,
        help="Activate quiet mode",
    )
    parser.add_argument(
        "-v", "--verbose",
        dest="loglevel",
        action="store_const", const=logging.DEBUG,
        help="Print various debugging information",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # delete subcommand
    delete_parser = subparsers.add_parser("delete", help="Delete all history of a gallery")
    delete_parser.add_argument("url", type=str, help="URL of the gallery to delete")

    # latest-meta subcommand
    meta_parser = subparsers.add_parser("latest-meta", help="Get metadata of the latest version of a gallery")
    meta_parser.add_argument("url", type=str, help="URL of the gallery")
    meta_parser.add_argument(
        "-o", "--output",
        dest="output", type=str, default=None,
        help="Output file path for metadata JSON (default: print to stdout)"
    )

    return parser
