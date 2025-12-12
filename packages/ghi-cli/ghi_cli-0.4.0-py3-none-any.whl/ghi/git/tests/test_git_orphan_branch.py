import pytest
from unittest.mock import patch, call
from ghi.git.orphan_branch import handle_command


def test_branch_already_exists_exits():
    args = type('obj', (), {'name': 'test-branch'})()

    with patch('subprocess.run') as mock_run, pytest.raises(SystemExit) as exc:
        mock_run.return_value.returncode = 0
        handle_command(args)

    assert exc.value.code == 1

def test_create_orphan_branch_success_no_readme():
    args = type('obj', (), {'name': 'new-branch', 'readme': False})()

    with patch('ghi.git.orphan_branch.is_branch_already_created') as mock_exists, \
         patch('ghi.git.orphan_branch.run') as mock_run:

        mock_exists.return_value = False  # Branch does NOT exist

        handle_command(args)

        # run() should be called with these commands in order
        expected_calls = [
            call('git checkout --orphan new-branch'),
            call('git rm --cached -r .'),
            call('rm -rf ./*'),
            # no README creation when readme=False
            call('git add .'),
            call('git commit -m "Add branch new-branch initial commit" --allow-empty'),
        ]

        mock_run.assert_has_calls(expected_calls)
        assert mock_run.call_count == len(expected_calls)


def test_create_orphan_branch_success_with_readme():
    args = type('obj', (), {'name': 'new-branch', 'readme': True})()

    with patch('ghi.git.orphan_branch.is_branch_already_created') as mock_exists, \
         patch('ghi.git.orphan_branch.run') as mock_run:

        mock_exists.return_value = False  # Branch does NOT exist

        handle_command(args)

        expected_calls = [
            call('git checkout --orphan new-branch'),
            call('git rm --cached -r .'),
            call('rm -rf ./*'),
            call('echo "# README" > README.md'),  # README created
            call('git add .'),
            call('git commit -m "Add branch new-branch initial commit" --allow-empty'),
        ]

        mock_run.assert_has_calls(expected_calls)
        assert mock_run.call_count == len(expected_calls)
