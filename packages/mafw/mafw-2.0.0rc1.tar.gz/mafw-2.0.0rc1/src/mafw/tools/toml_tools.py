#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides tools to read / write / modify specific TOML files.
"""

import datetime
import logging
from pathlib import Path, PosixPath, WindowsPath
from typing import Any, cast

import tomlkit
from tomlkit import TOMLDocument, boolean, comment, document, item, nl, table
from tomlkit.exceptions import ConvertError
from tomlkit.items import Item, String, StringType
from tomlkit.toml_file import TOMLFile

import mafw.mafw_errors
from mafw.__about__ import __version__ as version
from mafw.db.db_configurations import default_conf
from mafw.lazy_import import LazyImportProcessor, ProcessorClassProtocol
from mafw.mafw_errors import InvalidSteeringFile
from mafw.processor import PassiveParameter, Processor
from mafw.tools.regexp import parse_processor_name

log = logging.getLogger(__name__)


class PathItem(String):
    """TOML item representing a Path"""

    def unwrap(self) -> Path:  # type: ignore[override] # do not know how to do it
        return Path(super().unwrap())


def path_encoder(obj: Any) -> Item:
    """Encoder for PathItem."""
    if isinstance(obj, PosixPath):
        return PathItem.from_raw(str(obj), type_=StringType.SLB, escape=False)
    elif isinstance(obj, WindowsPath):
        return PathItem.from_raw(str(obj), type_=StringType.SLL, escape=False)
    else:
        raise ConvertError


tomlkit.register_encoder(path_encoder)


def generate_steering_file(
    output_file: Path | str,
    processors: list[ProcessorClassProtocol] | ProcessorClassProtocol,
    database_conf: dict[str, Any] | None = None,
    db_engine: str = 'sqlite',
) -> None:
    """
    Generates a steering file.

    :param output_file: The output filename where the steering file will be save.
    :type output_file: Path | str
    :param processors: The processors list for which the steering file will be generated.
    :type processors: list[type[Processor] | Processor], type[Processor], Processor
    :param database_conf: The database configuration dictionary
    :type database_conf: dict, Optional
    :param db_engine: A string representing the DB engine to be used. Possible values are: *sqlite*, *postgresql*
        and *mysql*.
    :type: str
    """
    if isinstance(output_file, str):
        output_file = Path(output_file)

    doc = _new_toml_doc()
    doc = _add_db_configuration(database_conf, db_engine=db_engine, doc=doc)
    doc = _add_processor_parameters_to_toml_doc(processors, doc)
    doc = _add_user_interface_configuration(doc)

    with open(output_file, 'w') as fp:
        tomlkit.dump(doc, fp)


def _new_toml_doc() -> TOMLDocument:
    doc = document()
    doc.add(comment(f'MAFw steering file generated on {datetime.datetime.now()}'))
    doc.add(nl())
    doc.add(
        comment('uncomment the line below and insert the processors you want to run from the available processor list')
    )
    doc.add(comment('processors_to_run = []'))
    doc.add(nl())
    doc.add(comment('customise the name of the analysis'))
    doc.add('analysis_name', String.from_raw('mafw analysis', StringType.SLB))
    doc.add('analysis_description', String.from_raw('Summing up numbers', StringType.MLB))
    doc.add('new_only', boolean('true'))
    doc.add('mafw_version', String.from_raw(version, StringType.SLB))
    doc.add('create_standard_tables', boolean('true'))
    return doc


def _add_db_configuration(
    database_conf: dict[str, Any] | None = None, db_engine: str = 'sqlite', doc: TOMLDocument | None = None
) -> TOMLDocument:
    """Add the DB configuration to the TOML document

    The expected structure of the database_conf dictionary is one of these two:

    .. code-block:: python

        option1 = {
            'DBConfiguration': {
                'URL': 'sqlite:///:memory:',
                'pragmas': {
                    'journal_mode': 'wal',
                    'cache_size': -64000,
                    'foreign_keys': 1,
                    'synchronous': 0,
                },
            }
        }

        option2 = {
            'URL': 'sqlite:///:memory:',
            'pragmas': {
                'journal_mode': 'wal',
                'cache_size': -64000,
                'foreign_keys': 1,
                'synchronous': 0,
            },
        }

    We will always convert the option1 in option2.

    :param database_conf: A dictionary with the database configuration. See comments above. If None, then the default
        is used.
    :type database_conf: dict
    :param db_engine: The database engine. It is used only in case the provided database configuration is invalid to
        retrieve the default configuration. Defaults to sqlite.
    :type db_engine: str, Optional
    :param doc: The TOML document to add the DB configuration. If None, one will be created.
    :type doc: TOMLDocument, Optional
    :return: The modified document.
    :rtype: TOMLDocument
    :raises UnknownDBEngine: if the `database_conf` is invalid and the db_engine is not yet implemented.
    """
    if doc is None:
        doc = _new_toml_doc()

    if database_conf is None:
        if db_engine in default_conf:
            database_conf = default_conf[db_engine]
        else:
            log.critical('The provided db_engine (%s) is not yet implemented', db_engine)
            raise mafw.mafw_errors.UnknownDBEngine(f'DB engine ({db_engine} not implemented')

    is_conf_valid = True
    if 'DBConfiguration' in database_conf:
        # it should be option 1. let's check if there is the URL that is required.
        if 'URL' not in database_conf['DBConfiguration']:
            # no URL
            is_conf_valid = False
        else:
            database_conf = cast(dict[str, Any], database_conf['DBConfiguration'])
    else:
        # option 2
        if 'URL' not in database_conf:
            # no URL
            is_conf_valid = False

    if not is_conf_valid:
        log.error('The provided database configuration is invalid. Adding default configuration')
        if db_engine not in default_conf:
            log.critical('The provided db_engine (%s) is not yet implemented', db_engine)
            raise mafw.mafw_errors.UnknownDBEngine(f'DB engine ({db_engine} not implemented')
        database_conf = default_conf[db_engine]

    db_table = table()
    for key, value in database_conf.items():
        db_table[key] = value
        if key == 'URL':
            db_table[key].comment(
                'Change the protocol depending on the DB type. Update this file to the path of your DB.'
            )
        if key == 'pragmas':
            db_table[key].comment('Leave these default values, unless you know what you are doing!')

    doc.add('DBConfiguration', db_table)
    doc.add(nl())

    return doc


def _add_processor_parameters_to_toml_doc(
    processors: list[ProcessorClassProtocol] | ProcessorClassProtocol, doc: TOMLDocument | None = None
) -> TOMLDocument:
    if not isinstance(processors, list):
        processors = [processors]

    if not processor_validator(processors):
        raise TypeError('Only processor instances and classes can be accepted')

    if doc is None:
        doc = _new_toml_doc()

    # add an array with all available processors
    proc_names = []
    for processor in processors:
        if isinstance(processor, LazyImportProcessor):
            proc_names.append(processor.plugin_name)
        elif isinstance(processor, Processor):
            proc_names.append(processor.name)
        else:
            proc_names.append(processor.__name__)
    doc.add('available_processors', item(proc_names))
    doc.add(nl())

    # loop over processors
    for p_item in processors:
        if not isinstance(p_item, Processor):
            # p is a class not an instance. so let's create an instance of p
            p = p_item()
        else:
            p = p_item

        # create a table for the current processor
        p_table = table()

        # add the first line of the class documentation
        if p.__doc__:
            lines = p.__doc__.splitlines()
            for line in lines:
                line = line.strip()
                if line:
                    p_table.comment(line)
                    break
        # add all parameters to the table, including the help_doc as a comment
        param: PassiveParameter[Any]
        for name, param in p.get_parameters().items():
            p_table[name] = param.value
            if param.doc:
                p_table.value.item(name).comment(param.doc)

        # add the table to the doc and a new line before going to the next item.
        doc.add(p.name, p_table)
        doc.add(nl())

    return doc


def processor_validator(processors: list[ProcessorClassProtocol]) -> bool:
    """
    Validates that all items in the list are valid processor instances or classes.

    :param processors: The list of items to be validated.
    :type processors: list[type[Processor] | Processor]
    :return: True if all items are valid.
    :rtype: bool
    """
    return all([isinstance(p, (Processor, type(Processor), LazyImportProcessor)) for p in processors])


def dump_processor_parameters_to_toml(
    processors: list[ProcessorClassProtocol] | ProcessorClassProtocol, output_file: Path | str
) -> None:
    """
    Dumps a toml file with processor parameters.

    This helper function can be used when the parameters of one or many processors have to be dumped to a TOML file.
    For each Processor in the `processors` a table in the TOML file will be added with their parameters is the shape of
    parameter name = value.

    It must be noted that `processors` can be:

        - a list of processor classes (list[type[Processor]])
        - a list of processor instances (list[Processor]])
        - one single processor class (type[Processor])
        - one single processor instance (Processor)

    What value of the parameters will be dumped?
    --------------------------------------------

    Good question, have a look at this :ref:`explanation <parameter_dump>`.

    :param processors: One or more processors for which the parameters should be dumped.
    :type processors: list[type[Processor | Processor]] | type[Processor] | Processor
    :param output_file: The name of the output file for the dump.
    :type output_file: Path | str
    :raise KeyAlreadyPresent: if an attempt to add twice, the same processor is made.
    :raise TypeError: if the list contains items different from Processor classes and instances.
    """

    doc = _add_processor_parameters_to_toml_doc(processors)

    with open(output_file, 'w') as fp:
        tomlkit.dump(doc, fp)


def _add_user_interface_configuration(doc: TOMLDocument | None = None) -> TOMLDocument:
    if doc is None:
        doc = _new_toml_doc()

    ui_table = table()
    ui_table.comment('Specify UI options')
    ui_table['interface'] = 'rich'
    ui_table['interface'].comment('Default "rich", backup "console"')
    doc.add('UserInterface', ui_table)

    return doc


def load_steering_file(steering_file: Path | str, validate: bool = True) -> dict[str, Any]:
    """
    Load a steering file for the execution framework.

    .. versionchanged:: v2.0.0
        Introduce support for replica names along with base names in file validation

    :param steering_file: The path to the steering file.
    :type steering_file: Path, str
    :param validate: A flag to validate the content. Defaults to True.
    :type validate: bool, Optional
    :return: The configuration dictionary.
    :rtype: dict
    :raise FileNotFound: if steering_file does not exist.
    """
    doc = TOMLFile(steering_file).read()

    if validate:
        required_fields = ['processors_to_run', 'UserInterface']
        for field in required_fields:
            if field not in doc.value:
                log.error('Missing section %s in %s' % (field, str(steering_file)))
                raise InvalidSteeringFile(f'Missing {field} in {str(steering_file)}')
        for processor in doc['processors_to_run']:  # type: ignore[union-attr]
            # processor to run is a list of replica aware processor name.
            # the steering file must contain one configuration section for either the
            # base processor or the replica.
            replica_name = processor
            base_name, _ = parse_processor_name(processor)
            # Check if neither the replica nor the base processor configuration exists
            if not any([name in doc.value for name in [replica_name, base_name]]):
                log.error('Missing section %s in %s' % (processor, str(steering_file)))
                raise InvalidSteeringFile(f'Missing {processor} in {str(steering_file)}')

    return doc.value
