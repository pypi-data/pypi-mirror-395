import argparse

from .git.cli import create_git_subcommands

def build_parser():
    parser = argparse.ArgumentParser(
        prog="ghi",
        description="GHI - Gabriel's Helper Interface"
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )

    create_git_subcommands(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
