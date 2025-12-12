#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides a simplified script to perform MAFw changelog update using ``auto-changelog``.
It can be used as pre-commit entry point and also in CI.

The basic idea is that this command is invoking the auto-changelog tool to generate a temporary changelog. The
checksum of the temporary changelog is compared with the existing one. If the two checksums differs, the current
changelog is replaced with the newly created version.

When committing the changelog update please use mute as commit type, to avoid having a new changelog generated
containing the changelog update commit.

"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click
from rich import print

from mafw.__about__ import __version__ as mafw_version
from mafw.tools.file_tools import file_checksum


def get_last_commit_message() -> str:
    """
    Get the message of the last commit.

    :return: The last commit message
    :rtype: str
    """
    result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def get_latest_tag() -> str:
    """
    Get the latest git tag.

    :return: The last git tag.
    :rtype: str
    """
    result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def commit_changelog_changes() -> None:
    """Commit the changes to CHANGELOG.md."""

    subprocess.run(['git', 'add', 'CHANGELOG.md'], check=True)
    subprocess.run(['git', 'commit', '-m', 'mute: update changelog'], check=True)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-i',
    '--input-file',
    default=Path.cwd() / Path('CHANGELOG.md'),
    type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, allow_dash=False),
    help='The path to the input changelog file. Default CHANGELOG.md',
)
@click.option('-f', '--force-recreate', is_flag=True, default=False, help='Force recreation of CHANGELOG.md')
@click.option('-r', '--remote', default='code.europa.eu', help='The name of the remote to be used for link generation')
@click.option(
    '--release/--no-release',
    is_flag=True,
    default=False,
    help='A boolean flag to identify if the Changelog should consider the latest changes as unreleased '
    '(--no-release, default) or belonging to the latest release (--release)',
)
@click.option(
    '--guess-release/--no-guess-release',
    is_flag=True,
    default=False,
    help='Guess if this is a release CHANGELOG, based on the label [pre-release] in the last commit message',
)
@click.option(
    '--silent/--no-silent',
    is_flag=True,
    default=False,
    help='A boolean flag to control the output of the script. By default, the script will print comments on the std '
    'output, but when executed pre-commit, it is better to put it silent.',
)
@click.option(
    '--auto-commit/--no-autocommit',
    is_flag=True,
    default=False,
    help='A boolean flag to control if the changes to the CHANGELOG.md should be automatically committed. Default False',
)
def update(
    input_file: click.Path | Path | str,
    force_recreate: bool,
    remote: str,
    release: bool,
    guess_release: bool,
    silent: bool,
    auto_commit: bool,
) -> int:
    """Execute the auto-changelog program with default configuration for MAFw.

    \f

    :return: 0: if no updates were required.
        1: if the changelog was modified.
        -1: if an error occurred during the process.
    """
    exe = 'auto-changelog'
    if shutil.which(exe) is None:
        if not silent:
            print(
                f'[red]{exe} is not available in this environment. Are you sure, you have installed MAFw with optional dev?'
            )
        return -1

    description = 'MAFw: Modular Analysis Framework'
    latest_version = f'v{mafw_version}'
    # tag_prefix = 'v'
    tag_pattern = '[vV](\\d+)\\.(\\d+)\\.(\\d+)(?:-*(alpha|beta|rc)(\\d+))*'
    release_label = '[release]'

    if guess_release:
        # we need to get the last commit message
        try:
            last_msg = get_last_commit_message()
            if release_label in last_msg:
                release = True
        except subprocess.CalledProcessError:
            print('Error: Failed to get last commit message.')
            return -1

    if release:
        # check if the latest tag is corresponding to the current mafw version.
        # if so then there is an error.
        try:
            latest_tag = get_latest_tag()
        except subprocess.CalledProcessError:
            print('Unable to retrieve the latest tag')
            return -1

        if latest_tag == latest_version:
            print('The latest tag and the current version are the same')
            print('Advance the current version with hatch version to fix the issue')
            return -1

    if isinstance(input_file, (click.Path, str)):
        input_file = Path(str(input_file))

    if not input_file.exists():
        if not silent:
            print(f'[orange3]No input file {input_file.name} found. Creating a new one.')
        input_file.touch()

    if force_recreate:
        if not silent:
            print(f'[orange3]{input_file.name} will be recreated.')
        input_file.unlink()
        input_file.touch()

    original_changelog_cs = file_checksum(input_file)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        file = Path(tmp_dir_name) / Path(input_file.name)
        args = [
            exe,
            '-o',
            str(file),
            '-d',
            f'"{description}"',
            '--gitlab',
            '--tag-pattern',
            tag_pattern,
            '-r',
            remote,
        ]
        if release:
            args.extend(
                [
                    '-v',
                    latest_version,
                ]
            )
        else:
            args.append('-u')

        subprocess.run(args)
        new_changelog_cs = file_checksum(file)

        if new_changelog_cs != original_changelog_cs:
            shutil.copy(file, input_file)
            if not silent:
                print(f'[green]{input_file.name} successfully updated')

            if auto_commit:
                try:
                    commit_changelog_changes()
                    return 0
                except subprocess.CalledProcessError as e:
                    print(f'Error committing CHANGELOG.md changes: {e}')
                    return -1
            else:
                return 1
        else:
            if not silent:
                print(f'[cyan]{input_file.name} was already up to date')
            return 0


def main() -> None:
    """Script entry point"""
    ret_val = update(standalone_mode=False)
    sys.exit(ret_val)


if __name__ == '__main__':
    main()
