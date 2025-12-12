#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides a simplified script to perform an update of the version number hard coded in the NOTICE.txt file.
It is meant to be used as a pre-commit hook.

Maybe one day it will be detached from MAFw to become a real hook on its own.
"""

import re
from pathlib import Path

import mafw


def update_notice_version() -> None:
    """Perform the update of the version number in the NOTICE.txt file

    :raises RuntimeError: if the target NOTICE.txt file is not found
    """
    this_dir = Path(__file__).parent
    notice_filename = 'NOTICE.txt'
    notice_path = this_dir.parent.parent.parent / notice_filename
    if not notice_path.exists():
        raise RuntimeError(f'Unable to find {notice_path}')

    # this is the current version
    actual_version = mafw.__version__

    # read the content of the notice file
    with open(notice_path, 'r') as f:
        notice_content = f.read()

    matching_string = r"""MAFw - Modular Analysis Framework

version:\s*V[0-9]+\.[0-9]+\.[0-9]+(?:[-a-zA-Z0-9\.\-\_]+)?"""

    replacing_string = rf"""MAFw - Modular Analysis Framework

version: V{actual_version}"""

    new_notice_content = re.sub(matching_string, replacing_string, notice_content, re.MULTILINE)

    with open(notice_path, 'w') as f:
        f.write(new_notice_content)


def main() -> None:
    """Script entry point"""
    update_notice_version()


if __name__ == '__main__':
    main()
