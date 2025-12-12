from .orphan_branch import new_orphan_branch


def create_git_subcommands(subparsers):

    parser = subparsers.add_parser("git", help="Simplified some git operations.")

    subparsers = parser.add_subparsers(
        title="git commands",
        dest="git_command",
        required=True,
    )

    new_orphan_branch(subparsers)

    return subparsers
