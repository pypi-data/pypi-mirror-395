import subprocess
import sys


def new_orphan_branch(subparsers):
    new_cmd = subparsers.add_parser('new-orphan-branch',
        aliases=['n',],
        help='Create a new orphan branch.'
    )
    new_cmd.add_argument(
        'name',
        help='Name of the new orphan branch to create.',
    )
    new_cmd.add_argument(
        '--readme',
        '-r',
        action='store_true',
        help='Add a README.md file to the new orphan branch created.',
    )
    new_cmd.set_defaults(func=handle_command)


def is_branch_already_created(name):
    result = subprocess.run(
        f"git rev-parse --verify {name}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def handle_command(args):

    if is_branch_already_created(args.name):
        print(f"Error: branch '{args.name}' already exists.")
        sys.exit(1)

    try:
        run(f'git checkout --orphan {args.name}')
        run(f'git rm --cached -r .')
        run('rm -rf ./*')
        run('echo "# README" > README.md') if args.readme else None
        run('git add .')
        run(f'git commit -m "Add branch {args.name} initial commit" --allow-empty')
    except subprocess.CalledProcessError as e:
        print(f'Command failed: {e}')
        sys.exit(1)

def run(command):
    subprocess.run(command, shell=True, check=True)
