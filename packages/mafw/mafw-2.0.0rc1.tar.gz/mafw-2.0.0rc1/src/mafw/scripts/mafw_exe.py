#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The execution framework.

This module provides the run functionality to the whole library.

It is heavily relying on ``click`` for the generation of commands, options, and arguments.

.. click:: mafw.scripts.mafw_exe:cli
    :prog: mafw
    :nested: full

"""

import datetime
import logging
import pathlib
import shutil
import sys
import warnings
from enum import IntEnum
from typing import TYPE_CHECKING, Any

import click
from click import ClickException
from pwiz import DATABASE_MAP, make_introspector  # type: ignore[import-untyped]
from rich import print as rprint
from rich import traceback
from rich.align import Align
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table

from mafw.__about__ import __version__
from mafw.db.db_configurations import db_scheme, default_conf
from mafw.db.db_wizard import dump_models
from mafw.enumerators import ProcessorExitStatus
from mafw.lazy_import import LazyImportProcessor
from mafw.mafw_errors import AbortProcessorException
from mafw.plugin_manager import get_plugin_manager
from mafw.runner import MAFwApplication
from mafw.tools.toml_tools import generate_steering_file

suppress = [click]
traceback.install(show_locals=True, suppress=suppress)

LEVELS = {'debug': 10, 'info': 20, 'warning': 30, 'error': 40, 'critical': 50}
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def custom_formatwarning(
    message: Warning | str, category: type[Warning], filename: str, lineno: int, line: str | None = None
) -> str:
    """Return the pure message of the warning."""
    return str(message)


warnings.formatwarning = custom_formatwarning
logging.captureWarnings(True)

log = logging.getLogger()


class ReturnValue(IntEnum):
    """Enumerator to handle the script return value."""

    OK = 0
    """No error"""

    Error = 1
    """Generic error"""


def logger_setup(level: str, ui: str, tracebacks: bool) -> None:
    """Set up the logger.

    This function is actually configuring the root logger level from the command line options and it attaches either
    a RichHandler or a StreamHandler depending on the user interface type.

    The `tracebacks` flag is used only by the RichHandler. Printing the tracebacks is rather useful when debugging
    the code, but it could be detrimental for final users. In normal circumstances, tracebacks is set to False,
    and is turned on when the debug flag is activated.

    :param level: Logging level as a string.
    :type level: str
    :param ui: User interface as a string ('rich' or 'console').
    :type ui: str
    :param tracebacks: Enable/disable the logging of exception tracebacks.
    """
    level = level.lower()
    ui = ui.lower()

    log.setLevel(LEVELS[level])
    handler: logging.Handler

    if ui == 'rich':
        fs = '%(message)s'
        handler = RichHandler(
            rich_tracebacks=tracebacks, markup=True, show_path=False, log_time_format='%Y%m%d-%H:%M:%S'
        )
    else:
        fs = '%(asctime)s - %(levelname)s - %(message)s'
        handler = logging.StreamHandler()

    formatter = logging.Formatter(fs)
    handler.setFormatter(formatter)
    log.addHandler(handler)


def display_exception(exception: Exception, show_traceback: bool = False) -> None:
    """
    Display exception information with optional debug details.

    This function logs exception information at the critical level. When show_traceback is enabled,
    it logs the full exception including traceback information. Otherwise, it logs a simplified
    message directing users to enable debug mode for more details.

    :param exception: The exception to be displayed and logged.
    :type exception: Exception
    :param show_traceback: Flag indicating whether to show detailed traceback information. Defaults to False
    :type show_traceback: bool
    """

    if show_traceback:
        log.critical('A critical error occurred')
        log.exception(exception)
    else:
        log.critical('A critical error occurred. Set option -D to get traceback output')
        log.exception(
            '%s: %s' % (exception.__class__.__name__, exception), exc_info=False, stack_info=False, stacklevel=1
        )


class MAFwGroup(click.Group):
    """Custom Click Group for MAFw runner.

    It implements two main features:

        1. Support commands abbreviation. Instead of providing the whole command,
           the user can use whatever abbreviation instead as long as it is unique.
           So for example, instead of `mafw list`, the use can provide `mafw l` and the result
           will be the same.
        2. Implements the cascading of return values among different command levels.
    """

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        """
        Return a command.

        Given a context and a command name as passed from the CLI, the click.Command is returned.
        This method overloads the basic one allowing to use command abbreviations.

        If more than one match is found, then an error is raised.

        If no matches are found, then click will handle this case as in the standard situation.

        :param ctx: The click context
        :param cmd_name: The command name as provided from the CLI
        :return: The corresponding command or None if no command is found.
        """
        rv = super().get_command(ctx, cmd_name)

        if rv is not None:
            return rv

        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]

        if not matches:
            return None

        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])

        ctx.fail(f'Too many matches: {", ".join(sorted(matches))}')

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        if TYPE_CHECKING:
            assert isinstance(cmd, click.Command)
        return cmd.name, cmd, args

    def invoke(self, ctx: click.Context) -> Any:
        """Invoke the command.

        This override method is just wrapping the base invoke call in a try / except block.

        In the case of a ClickException, then this is shown and its exit code is used passed to the sys.exit call. In
        case of a SystemExit or click.exceptions.Exit, then this is simply re-raised, so that Click can handle it as
        in normal circumstances In all other cases, the exception is caught and the sys.exit is called with the
        :attr:`.ReturnValue.Error`.

        :param ctx: The click context
        :return: The return value of the invoked command
        """
        try:
            return super().invoke(ctx)

        except ClickException as e:
            e.show()
            sys.exit(e.exit_code)
        except (SystemExit, click.exceptions.Exit):
            # Re-raise SystemExit to maintain Click's normal behavior
            raise
        except Exception:
            # For any other exception, exit with error code
            sys.exit(ReturnValue.Error)

    def main(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        """Override main to handle return values properly."""
        try:
            # Get the result from the command
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore[call-overload]

            # If the command returned a ReturnValue or an integer, use it as exit code
            if isinstance(rv, (ReturnValue, int)):
                sys.exit(rv)
            else:
                # Default to success if no return value or unknown return value
                sys.exit(ReturnValue.OK)

        except ClickException as e:
            e.show()
            sys.exit(e.exit_code)
        except SystemExit:
            # Re-raise SystemExit (this includes calls to sys.exit())
            raise
        except Exception:
            # For any unhandled exception, exit with error code
            sys.exit(ReturnValue.Error)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS, name='mafw', cls=MAFwGroup)
@click.pass_context
@click.option(
    '--log-level',
    type=click.Choice(['debug', 'info', 'warning', 'error', 'critical'], case_sensitive=False),
    show_default=True,
    default='info',
    help='Log level',
)
@click.option(
    '--ui',
    type=click.Choice(['console', 'rich'], case_sensitive=False),
    default='rich',
    help='The user interface',
    show_default=True,
)
@click.option('-D', '--debug', is_flag=True, default=False, help='Show debug information about errors')
@click.version_option(__version__, '-v', '--version')
def cli(ctx: click.core.Context, log_level: str, ui: str, debug: bool) -> None:
    """
    The Modular Analysis Framework execution.

    This is the command line interface where you can configure and launch your analysis tasks.

    More information on our documentation page.
    \f

    :param ctx: The click context.
    :type ctx: click.core.Context
    :param log_level: The logging level as a string. Choice from debug, info, warning, error and critical.
    :type log_level: str
    :param ui: The user interface as a string. Choice from console and rich.
    :type ui: str
    :param debug: Flag to show debug information about exception.
    :type debug: bool
    """
    ctx.ensure_object(dict)
    ctx.obj = {'log_level': log_level, 'ui': ui, 'debug': debug}
    logger_setup(log_level, ui, debug)

    if ctx.invoked_subcommand is None:
        rprint('Use --help to get a quick help on the mafw command.')


@cli.command(name='list')
@click.pass_obj
def list_processors(obj: dict[str, Any]) -> ReturnValue:
    """Display the list of available processors.

    This command will retrieve all available processors via the plugin manager. Both internal and external processors
    will be listed if the ext-plugins option is passed.
    \f

    """
    try:
        plugin_manager = get_plugin_manager()
        plugins = plugin_manager.load_plugins({'processors'})
        available_processors = plugins.processor_list
        print('\n')
        table = Table(
            title='Available processors',
            header_style='orange3',
            expand=True,
            title_style='italic red',
        )
        table.add_column('Processor Name', justify='left', style='cyan')
        table.add_column('Package Name', justify='left', style='cyan')
        table.add_column('Module', justify='left', style='cyan')
        mafw_processors = 0
        other_processors = 0
        for processor in available_processors:
            if isinstance(processor, LazyImportProcessor):
                package, module = processor.plugin_qualname.split('.', 1)
                name = processor.plugin_name
            else:
                package, module = processor.__module__.split('.', 1)
                name = processor.__name__
            table.add_row(name, package, module)
            if package == 'mafw':
                mafw_processors += 1
            else:
                other_processors += 1
        table.caption = f'Total processors = {len(available_processors)}, internal = {mafw_processors}, external = {other_processors}'
        table.caption_style = 'italic green'
        console = Console()
        console.print(Align.center(table))
        return ReturnValue.OK
    except Exception as e:
        display_exception(e, show_traceback=obj['debug'])
        return ReturnValue.Error


@cli.command(name='steering')
@click.pass_obj
@click.option('--show/--no-show', default=False, help='Display the generated steering file on console')
@click.option('--ext-plugins/--no-ext-plugin', default=True, help='Load external plugins')
@click.option('--open-editor/--no-open-editor', default=False, help='Open the file in your editor.')
@click.option(
    '--db-engine',
    type=click.Choice(['sqlite', 'mysql', 'postgresql'], case_sensitive=False),
    help='Select a DB engine',
    default='sqlite',
)
@click.option('--db-url', type=str, default=':memory:', help='URL to the DB')
@click.argument('steering-file', type=click.Path())
def generate_steering(
    obj: dict[str, Any],
    show: bool,
    ext_plugins: bool,
    open_editor: bool,
    steering_file: pathlib.Path,
    db_engine: str,
    db_url: str,
) -> ReturnValue:
    """Generates a steering file with the default parameters of all available processors.

    STEERING_FILE   A path to the steering file to execute.

    The user must modify the generated steering file to ensure it can be executed using the run command.
    \f

    :param obj: The context object being passed from the main command.
    :type obj: dict
    :param show: Display the steering file in the console after the generation. Defaults to False.
    :type show: bool
    :param ext_plugins: Extend the search for processor to external libraries.
    :type ext_plugins: bool
    :param open_editor: Open a text editor after the generation to allow direct editing.
    :type open_editor: bool
    :param steering_file: The steering file path.
    :type steering_file: Path
    :param db_engine: The name of the db engine.
    :type db_engine: str
    :param db_url: The URL of the database.
    :type db_url: str
    """
    try:
        plugin_manager = get_plugin_manager()
        plugins = plugin_manager.load_plugins({'processors'})
        available_processors = plugins.processor_list
        # db_engine is already sure to be in the default conf because the Choice is assuring it.
        database_conf = default_conf[db_engine]
        database_conf['URL'] = db_scheme[db_engine] + db_url
        generate_steering_file(steering_file, available_processors, database_conf)

        if show:
            console = Console()
            with open(steering_file) as fp:
                text = fp.read()
            with console.pager():
                console.print(text, highlight=True)
            console.print(Rule())

        if open_editor:
            click.edit(filename=str(steering_file))
        else:
            rprint(f'A generic steering file has been saved in [blue underline]{steering_file}[/blue underline].')
            rprint('Open it in your favourite text editor, change the processors_to_run list and save it.')
            rprint('')
            rprint(f'To execute it launch: [blue]mafw run {steering_file}[/blue].')

        return ReturnValue.OK

    except Exception as e:
        display_exception(e, show_traceback=obj['debug'])
        return ReturnValue.Error


@cli.command()
@click.pass_obj
@click.argument('steering-file', type=click.Path())
def run(obj: dict[str, Any], steering_file: click.Path) -> ReturnValue:
    """Runs a steering file.

    STEERING_FILE   A path to the steering file to execute.

    \f

    :param obj: The context object being passed from the main command.
    :type obj: dict
    :param steering_file: The path to the output steering file.
    :type steering_file: Path
    """
    try:
        app = MAFwApplication(steering_file)  # type: ignore
        pes = app.run()
        if pes == ProcessorExitStatus.Successful:
            rv = ReturnValue.OK
        else:
            rv = ReturnValue.Error
        return rv

    except AbortProcessorException:
        return ReturnValue.Error
    except Exception as e:
        display_exception(e, show_traceback=obj['debug'])
        return ReturnValue.Error


@cli.group
@click.pass_context
def db(ctx: click.core.Context) -> None:
    """
    Advanced database commands.

    The db group of commands offers a set of useful database operations. Invoke the help option of each command for
    more details.
    \f

    :param ctx: The click context.
    :type ctx: click.core.Context
    """


@db.command(name='wizard')
@click.pass_context
@click.option(
    '-o',
    '--output-file',
    type=click.Path(),
    default=pathlib.Path.cwd() / pathlib.Path('my_model.py'),
    help='The name of the output file with the reflected model.',
)
@click.option('-s', '--schema', type=str, help='The name of the DB schema')
@click.option(
    '-t', '--tables', type=str, multiple=True, help='Generate model for selected tables. Multiple option possible.'
)
@click.option('--overwrite/--no-overwrite', default=True, help='Overwrite output file if already exists.')
@click.option('--preserve-order/--no-preserve-order', default=True, help='Preserve column order.')
@click.option('--with-views/--without-views', default=False, help='Include also database views.')
@click.option('--ignore-unknown/--no-ignore-unknown', default=False, help='Ignore unknown fields.')
@click.option('--snake-case/--no-snake-case', default=True, help='Use snake case for table and field names.')
@click.option('--host', type=str, help='Hostname for the DB server.')
@click.option('-p', '--port', type=int, help='Port number for the DB server.')
@click.option('-u', '--user', '--username', type=str, help='Username for the connection to the DB server.')
@click.option('--password', prompt=True, prompt_required=False, hide_input=True, help='Insert password when prompted')
@click.option('-e', '--engine', type=click.Choice(sorted(DATABASE_MAP)), help='The DB engine')
@click.argument('database', type=str)
def wizard(
    ctx: click.core.Context,
    overwrite: bool,
    tables: tuple[str, ...] | None,
    preserve_order: bool,
    with_views: bool,
    ignore_unknown: bool,
    snake_case: bool,
    output_file: click.Path | pathlib.Path | str,
    host: str,
    port: int,
    user: str,
    password: str,
    engine: str,
    schema: str,
    database: str,
) -> ReturnValue:
    """
    Reflect an existing DB into a python module.

    mafw db wizard [Options] Database

    Database Name of the Database to be reflected.

    About connection options (user / host / port):

    That information will be used only in case you are trying to access a network database (MySQL or PostgreSQL). In
    case of Sqlite, the parameters will be discarded.

    About passwords:

    If you need to specify a password to connect to the DB server, just add --password in the command line without
    typing your password as clear text. You will be prompted to insert the password with hidden characters at the start
    of the processor.

    About engines:

    The full list of supported engines is provided in the option below. If you do not specify any
    engine and the database is actually an existing filename, then engine is set to Sqlite, otherwise to postgresql.

    \f

    :param database: The name of the database.
    :type database: str
    :param schema: The database schema to be reflected.
    :type schema: str
    :param engine: The database engine. A selection of possible values is provided in the script help.
    :type engine: str
    :param password: The password for the DB connection. Not used in case of Sqlite.
    :type password: str
    :param user: The username for the DB connection. Not used in case of Sqlite.
    :type user: str
    :param port: The port number of the database server. Not used in case of Sqlite.
    :type port: int
    :param host: The database hostname. Not used in case of Sqlite.
    :type host: str
    :param output_file: The filename for the output python module.
    :type output_file: click.Path | pathlib.Path | str
    :param snake_case: Flag to select snake_case convention for table and field names, or all small letter formatting.
    :type snake_case: bool
    :param ignore_unknown: Flag to ignore unknown fields. If False, an unknown field will be labelled with UnknownField.
    :type ignore_unknown: bool
    :param with_views: Flag to include views in the reflected elements.
    :type with_views: bool
    :param preserve_order: Flag to select if table fields should be reflected in the original order (True) or in
        alphabetical order (False)
    :type preserve_order: bool
    :param tables: A tuple containing a selection of table names to be reflected.
    :type tables: tuple[str, ...]
    :param overwrite: Flag to overwrite the output file if exists. If False and the output file already exists, the
        user can decide what to do.
    :type overwrite: bool
    :param ctx: The click context, that includes the original object with global options.
    :type ctx: click.core.Context
    :return: The script return value
    """
    obj = ctx.obj

    if isinstance(output_file, (str, click.Path)):
        output_file = pathlib.Path(str(output_file))

    # if not overwrite, check if the file exists
    if not overwrite and output_file.exists():
        answer = Prompt.ask(
            f'A module ({output_file.name}) already exists. Do you want to overwrite, cancel or backup?',
            case_sensitive=False,
            choices=['o', 'c', 'b'],
            show_choices=True,
            show_default=True,
            default='b',
        )
        if answer == 'c':
            return ReturnValue.OK
        elif answer == 'b':
            bck_filename = output_file.parent / pathlib.Path(
                output_file.stem + f'_{datetime.datetime.now():%Y%m%dT%H%M%S}' + output_file.suffix
            )

            shutil.copy(output_file, bck_filename)

    if tables == ():
        tables = None

    if engine is None:
        engine = 'sqlite' if pathlib.Path(database).exists() else 'postgresql'

    # prepare the connection options
    if engine in ['sqlite', 'sqlite3']:
        # for sqlite the connection
        keys: list[str] = ['schema']
        values: list[str | int] = [schema]
    else:
        keys = ['host', 'port', 'user', 'schema', 'password']
        values = [host, port, user, schema, password]

    connection_options: dict[str, Any] = {}
    for k, v in zip(keys, values):
        if v:
            connection_options[k] = v

    try:
        introspector = make_introspector(engine, database, **connection_options)
    except Exception as e:
        msg = f'[red]Problem generating an introspector instance of {database}.'
        display_exception(e, show_traceback=obj['debug'])
        return ReturnValue.Error

    try:
        with open(output_file, 'tw') as out_file:
            dump_models(
                out_file,
                introspector,
                tables,
                preserve_order=preserve_order,
                include_views=with_views,
                ignore_unknown=ignore_unknown,
                snake_case=snake_case,
            )
    except Exception as e:
        display_exception(e, obj['debug'])
        return ReturnValue.Error

    msg = f'[green]Database {database} successfully reflected in {output_file.name}'
    log.info(msg)
    return ReturnValue.OK


if __name__ == '__main__':
    # Use the custom main method that handles exit codes
    cli.main()
