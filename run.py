import argparse
import logging

from app.main import Runner


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "config_file", type=str, help="Path to config file",
    )
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    Runner(args.config_file).run()


if __name__ == "__main__":
    _main(_parse())
