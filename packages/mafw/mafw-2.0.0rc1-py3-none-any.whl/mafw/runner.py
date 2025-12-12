#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Provides a container to run configurable and modular analytical tasks.
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from mafw import mafw_errors
from mafw.enumerators import ProcessorExitStatus
from mafw.plugin_manager import MAFwPluginManager, get_plugin_manager
from mafw.processor import ProcessorList
from mafw.tools import toml_tools
from mafw.tools.regexp import parse_processor_name
from mafw.ui.abstract_user_interface import UserInterfaceBase

log = logging.getLogger(__name__)


class MAFwApplication:
    """
    The MAFw Application.

    This class takes care of reading a steering file and from the information retrieved construct a
    :class:`~mafw.processor.ProcessorList` from the processor listed there and execute it.

    It is very practical because any combination of processors can be run without having to write dedicated scripts
    but simply modifying a steering file.

    The application will search for processors not only among the ones available in the MAFw library, but also in all
    other packages exposing processors via the :ref:`plugin mechanism <plugins>`.

    All parameters in the constructor are optional.

    An instance can be created also without the `steering_file`, but such an instance cannot be executed. The steering
    file can be provided in a later stage via the :meth:`init` method or directly to the :meth:`run` method.

    The user interface can be either provided directly in the constructor, or it will be taken from the steering
    file. In the worst case, the fallback :class:`~mafw.ui.console_user_interface.ConsoleInterface` will be used.

    The plugin manager, if not provided, the global plugin manager will be retrieved from the
    :func:`~mafw.plugin_manager.get_plugin_manager`.

    A simple example is provided here below:

    .. code-block:: python
        :name: MAFwApplication_run
        :caption: Creation and execution of a MAFwApplication

        import logging
        from pathlib import Path

        from mafw.runner import MAFwApplication

        log = logging.getLogger(__name__)

        # put here your steering file
        steering_file = Path('path_to_my_steering_file.toml')

        try:
            # create the app
            app = MAFwApplication(steering_file)

            # run it!
            app.run()

        except Exception as e:
            log.error('An error occurred!')
            log.exception(e)
    """

    __default_ui__: str = 'rich'

    def __init__(
        self,
        steering_file: Path | str | None = None,
        user_interface: UserInterfaceBase | type[UserInterfaceBase] | str | None = None,
        plugin_manager: MAFwPluginManager | None = None,
    ):
        """
        Constructor parameters:

        :param steering_file: The path to the steering file.
        :type steering_file: Path | str, Optional
        :param user_interface: The user interface to be used by the application.
        :type user_interface: UserInterfaceBase | type[UserInterfaceBase] | str, Optional
        :param plugin_manager: The plugin manager.
        :type plugin_manager: PluginManager, Optional
        """
        #: the name of the application instance
        self.name = self.__class__.__name__
        self._configuration_dict: dict[str, Any] = {}

        #: the plugin manager of the application instance
        self.plugin_manager = plugin_manager or get_plugin_manager()

        #: the exit status of the application
        self.exit_status = ProcessorExitStatus.Successful

        self.user_interface: UserInterfaceBase | None
        if user_interface is not None:
            if isinstance(user_interface, UserInterfaceBase):
                self.user_interface = user_interface
            else:  # if isinstance(user_interface, str):
                if TYPE_CHECKING:
                    assert isinstance(user_interface, str)
                self.user_interface = self.get_user_interface(user_interface)
        else:
            self.user_interface = None

        if steering_file is None:
            self._initialized = False
            self.steering_file = None
        else:
            self.steering_file = steering_file if isinstance(steering_file, Path) else Path(steering_file)
            self.init(self.steering_file)

    def get_user_interface(self, user_interface: str) -> UserInterfaceBase:
        """
        Retrieves the user interface from the plugin managers.

        User interfaces are exposed via the plugin manager.

        If the requested `user_interface` is not available, then the fallback console interface is used.

        :param user_interface: The name of the user interface to be used. Normally rich or console.
        :type user_interface: str
        """
        plugins = self.plugin_manager.load_plugins({'ui'})
        if user_interface in plugins.ui_dict:
            ui_type = plugins.ui_dict[user_interface]
        else:
            log.warning('User interface %s is not available. Using console.' % user_interface)
            ui_type = plugins.ui_dict['console']
        return ui_type()

    def run(self, steering_file: Path | str | None = None) -> ProcessorExitStatus:
        """
        Runs the application.

        This method builds the :class:`~mafw.processor.ProcessorList` with the processors listed in the steering file
        and launches its execution.

        A steering file can be provided at this stage if it was not done before.

        .. versionchanged:: v2.0.0
            Refactor to accept replica names in the processor to run list.

        :param steering_file: The steering file. Defaults to None.
        :type steering_file: Path | str, Optional
        :raises RunnerNotInitialized: if the application has not been initialized. Very likely a steering file was
            never provided.
        :raises UnknownProcessor: if a processor listed in the steering file is not available in the plugin library.
        """
        if steering_file is None and not self._initialized:
            log.error('%s is not initialized. Have you provided a steering file?' % self.name)
            raise mafw_errors.RunnerNotInitialized()

        if steering_file is not None and steering_file != self.steering_file:
            self.init(steering_file)

        plugins = self.plugin_manager.load_plugins({'processors', 'db_modules'})

        description = self._configuration_dict.get('analysis_description', None)
        processors_to_run = self._configuration_dict.get('processors_to_run', [])

        # processor_to_run is a list of replica aware name
        processor_names_and_replicas = [parse_processor_name(replica_name) for replica_name in processors_to_run]
        processor_types = set([t[0] for t in processor_names_and_replicas])

        for processor in processor_types:
            if processor not in plugins.processor_dict:
                log.critical(
                    'Processor %s is not available. Check your plugin configuration or your steering file.' % processor
                )
                raise mafw_errors.UnknownProcessor(processor)

        processor_list = ProcessorList(
            name=self.name,
            description=description,
            user_interface=self.user_interface,
            database_conf=self._configuration_dict.get('DBConfiguration', None),
            create_standard_tables=self._configuration_dict.get('create_standard_tables', True),
        )
        for proc_class, replica in processor_names_and_replicas:
            processor_list.append(
                plugins.processor_dict[proc_class](config=self._configuration_dict, replica_id=replica)
            )

        return processor_list.execute()

    def init(self, steering_file: Path | str) -> None:
        """
        Initializes the application.

        This method is normally automatically invoked by the class constructor.
        It can be called in a later moment to force the parsing of the provided steering file.

        :param steering_file: The path to the steering file.
        :type steering_file: Path | str
        """
        if isinstance(steering_file, str):
            steering_file = Path(steering_file)

        self.steering_file = steering_file
        self._configuration_dict = toml_tools.load_steering_file(steering_file)

        if self.user_interface is None:
            self.user_interface = self.get_user_interface(self._configuration_dict['UserInterface']['interface'])

        self._initialized = True
        self.name = self._configuration_dict.get('analysis_name', 'mafw analysis')
