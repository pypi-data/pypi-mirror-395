#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides standard tables that are included in all database created by MAFw processor.

Standard tables are automatically created and initialized by a :class:`~mafw.processor.Processor` or a
:class:`~mafw.processor.ProcessorList` when opening a database connection.

This means that if a processor receives a valid database object, then it will suppose that the connection was already
opened somewhere else (either from a ProcessorList or a third party) and thus it is not creating the standard tables.

If a processor is constructed using a database configuration dictionary, then it will first try to open a connection
to the DB, then creating all standard tables and finally executing their :class:`StandardTable.init` method. The same
apply for the Processor list.

In other words, object responsible to open the database connection is taking care also of creating the standard
tables and of initializing them. If the user opens the connection and passes it to a Processor or ProcessorList,
then the user is responsible to create the standard tables and to initialize them.

All standard tables must derive from the :class:`StandardTable` to have the same interface for the
initialization.
"""

from types import TracebackType
from typing import cast

import peewee
from peewee import AutoField, BooleanField, CharField, TextField

from mafw.db.db_model import MAFwBaseModel
from mafw.db.db_types import PeeweeModelWithMeta
from mafw.db.fields import FileChecksumField, FileNameListField


class StandardTable(MAFwBaseModel):
    """A base class for tables that are generated automatically by the MAFw processor."""

    @classmethod
    def init(cls) -> None:
        """The user must overload this method, if he wants some specific operations to be performed on the model
        everytime the database is connected."""
        pass


class StandardTableDoesNotExist(Exception):
    """An exception raised when trying to access a not existing table."""


class TriggerStatus(StandardTable):
    """A Model for the trigger status"""

    trigger_type_id = AutoField(primary_key=True, help_text='Primary key')
    trigger_type = TextField(
        help_text='You can use it to specify the type (DELETE/INSERT/UPDATE) or the name of a specific trigger'
    )
    status = BooleanField(default=True, help_text='False (0) = disable / True (1) = enable')

    # noinspection PyProtectedMember
    @classmethod
    def init(cls) -> None:
        """Resets all triggers to enable when the database connection is opened."""
        data = [
            dict(trigger_type_id=1, trigger_type='DELETE', status=True),
            dict(trigger_type_id=2, trigger_type='INSERT', status=True),
            dict(trigger_type_id=3, trigger_type='UPDATE', status=True),
            dict(trigger_type_id=4, trigger_type='DELETE_FILES', status=True),
        ]

        # this is used just to make mypy happy
        # cls and meta_cls are exactly the same thing
        meta_cls = cast(PeeweeModelWithMeta, cls)

        db_proxy = meta_cls._meta.database
        if isinstance(db_proxy, peewee.DatabaseProxy):
            db = cast(peewee.Database, db_proxy.obj)
        else:
            db = cast(peewee.Database, db_proxy)

        if isinstance(db, peewee.PostgresqlDatabase):
            cls.insert_many(data).on_conflict(
                'update', conflict_target=[cls.trigger_type_id], update={cls.status: True}
            ).execute()
        else:
            cls.insert_many(data).on_conflict_replace().execute()


class TriggerStatusDoesNotExist(Exception):
    """An exception raised when trying to access a not existing table."""


class TriggerDisabler:
    """
    A helper tool to disable a specific type of triggers.

    Not all SQL dialects allow to temporarily disable trigger execution.

    In order overcome this limitation, MAFw has introduced a practical workaround. All types of triggers are active
    by default but they can be temporarily disabled, by changing their status in the :class:`.TriggerStatus` table.

    In order to disable the trigger execution, the user has to set the status of the corresponding status to 0 and also
    add a when condition to the trigger definition.

    Here is an example code:

    .. code-block:: python

        class MyTable(MAFwBaseModel):
            id_ = AutoField(primary_key=True)
            integer = IntegerField()
            float_num = FloatField()

            @classmethod
            def triggers(cls):
                return [
                    Trigger(
                        'mytable_after_insert',
                        (TriggerWhen.After, TriggerAction.Insert),
                        cls,
                        safe=True,
                    )
                    .add_sql(
                        'INSERT INTO target_table (id__id, half_float_num) VALUES (NEW.id_, NEW.float_num / 2)'
                    )
                    .add_when(
                        '1 == (SELECT status FROM trigger_status WHERE trigger_type_id == 1)'
                    )
                ]

    When you want to perform a database action with the trigger disabled, you can either use this class as context
    manager or call the :meth:`.disable` and :meth:`.enable` methods.

    .. code-block:: python

        # as a context manager
        with TriggerDisabler(trigger_type_id = 1):
            # do something without triggering any trigger of type 1.

        # with the explicit methods
        disabler = TriggerDisabler(1)
        disabler.disable()
        # do something without triggering any trigger of type 1.
        disabler.enable()

    When using the two explicit methods, the responsibility to assure that the triggers are re-enabled in on the user.
    """

    def __init__(self, trigger_type_id: int) -> None:
        """
        Constructor parameters:

        :param trigger_type_id: the id of the trigger to be temporary disabled.
        :type trigger_type_id: int
        """
        self.trigger_type_id = trigger_type_id

    def disable(self) -> None:
        """Disable the trigger"""
        TriggerStatus.update({TriggerStatus.status: 0}).where(
            TriggerStatus.trigger_type_id == self.trigger_type_id
        ).execute()

    def enable(self) -> None:
        """Enable the trigger"""
        TriggerStatus.update({TriggerStatus.status: 1}).where(
            TriggerStatus.trigger_type_id == self.trigger_type_id
        ).execute()

    def __enter__(self) -> 'TriggerDisabler':
        """
        Context enter. Disable the trigger.
        """
        self.disable()
        return self

    def __exit__(
        self, type_: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """
        Context exit

        :param type_: Exception type causing the context manager to exit. Defaults to None.
        :type type_: type[BaseException], Optional
        :param value: Exception that caused the context manager to exit. Defaults to None.
        :type value: BaseException, Optional
        :param traceback: Traceback. Defaults to None.
        :type traceback: TracebackType
        """
        self.enable()


class OrphanFile(StandardTable):
    """
    A Model for the files to be removed from disc

    .. versionchanged:: v2.0.0
        The checksum field is set to allow null values.
        The class is set not to automatically generate triggers for file removal

    """

    file_id = AutoField(primary_key=True, help_text='Primary key')
    filenames = FileNameListField(help_text='The path to the file to be deleted', checksum_field='checksum')
    checksum = FileChecksumField(help_text='The checksum of the files in the list.', null=True)

    class Meta:
        file_trigger_auto_create = False


class OrphanFileDoesNotExist(peewee.DoesNotExist):
    """An exception raised when trying to access a not existing table."""


class PlotterOutput(StandardTable):
    """
    A model for the output of the plotter processors.

    The model has a trigger activated on delete queries to insert filenames and checksum in the OrphanFile model via
    the automatic file delete trigger generation.
    """

    plotter_name = CharField(primary_key=True, help_text='The plotter processor name', max_length=511)
    filename_list = FileNameListField(help_text='The path to the output file', checksum_field='checksum')
    checksum = FileChecksumField(help_text='The checksum of the files in the list.')

    class Meta:
        depends_on = [OrphanFile]
        file_trigger_auto_create = True


class PlotterOutputDoesNotExist(peewee.DoesNotExist):
    """An exception raised when trying to access a not existing table."""
