#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module implements some basic functions involving regular expressions.
"""

import logging
import re

from mafw.mafw_errors import UnknownProcessor

log = logging.getLogger(__name__)


def extract_protocol(url: str) -> str | None:
    """
    Extract the protocol portion from a database connection URL.

    The extract_protocol function takes a database connection URL string as input and extracts the protocol portion
    (the part before "://"). This function is useful for identifying the database type from connection strings.

    :param url: The url from which the protocol will be extracted.
    :type url: str
    :return: The protocol or None, if the extraction failed
    :rtype: str | None
    """
    pattern = r'^([a-z0-9_\-+.]+)://'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None


def normalize_sql_spaces(sql_string: str) -> str:
    """
    Normalize multiple consecutive spaces in SQL string to single spaces.
    Only handles spaces, preserves other whitespace characters.

    :param sql_string: The SQL string for space normalization.
    :type sql_string: str
    :return: The normalized SQL command.
    :rtype: str
    """
    return re.sub(r' +', ' ', sql_string.strip())


def parse_processor_name(processor_string: str) -> tuple[str, str | None]:
    """
    Parse a processor name string into name and replica identifier components.

    Given a string in the form 'MyProcessorName#156a', returns a tuple ('MyProcessorName', '156a').
    If the input string is 'MyProcessorName' only, then it returns ('MyProcessorName', None).
    If it gets 'MyProcessorName#', it returns ('MyProcessorName', None) but emits a warning
    informing of a possible malformed name.

    The processor name must be a valid Python identifier (class name).

    :param processor_string: The processor name string to parse.
    :type processor_string: str
    :return: A tuple of (name, replica_id) where replica_id can be None.
    :rtype: tuple[str, str | None]
    :raise UnknownProcessor: if the name part is empty or not a valid Python identifier
    """
    # Split on '#' character
    parts = processor_string.strip().split('#', 1)

    # Get the name part (always exists)
    name = parts[0]

    if len(name) == 0:
        raise UnknownProcessor('Invalid processor name (empty)')

    # Validate that the name is a valid Python identifier
    if not name.isidentifier():
        raise UnknownProcessor(f'Invalid processor name "{name}" - not a valid Python identifier')

    # Check if there's a replica part
    if len(parts) == 1 or parts[1] == '':
        # No or empty replica id part
        if len(parts) == 2 and parts[1] == '':
            # Warn about malformed input like "Name#"
            log.warning(
                f"Malformed processor name '{processor_string}': empty replica part after '#'",
            )
        return name, None
    else:
        replica_id = parts[1]
        return name, replica_id
