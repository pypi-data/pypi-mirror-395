#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides default configurations for different database engines.
"""

#: default configuration dictionary used to generate steering files
default_conf = {}

default_conf['sqlite'] = {
    'URL': 'sqlite:///my_database.db',
    'pragmas': {'journal_mode': 'wal', 'cache_size': -64000, 'foreign_keys': 1, 'synchronous': 0},
}
default_conf['postgresql'] = {
    'URL': 'postgresql://postgres:my_password@localhost:5432/my_database',
}

default_conf['mysql'] = {
    'URL': 'mysql://user:passwd@ip:port/my_db',
}

#: default database scheme
db_scheme = {
    'sqlite': 'sqlite:///',
    'postgresql': 'postgresql://',
    'mysql': 'mysql://',
}
