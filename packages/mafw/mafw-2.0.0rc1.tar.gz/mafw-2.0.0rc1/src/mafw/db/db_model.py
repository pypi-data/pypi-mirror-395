#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides functionality to MAFw to interface to a DB.
"""

import warnings
from typing import TYPE_CHECKING, Any, Iterable, cast

# peewee type annotations are missing.
from peewee import (  # type: ignore[attr-defined]
    SQL,
    DatabaseProxy,
    Field,
    ModelBase,
    ModelInsert,
    Value,
    make_snake_case,
)
from playhouse.shortcuts import dict_to_model, model_to_dict, update_model_from_dict

# noinspection PyUnresolvedReferences
from playhouse.signals import Model

from mafw.db import trigger
from mafw.db.db_types import PeeweeModelWithMeta
from mafw.db.fields import FileNameField
from mafw.db.model_register import ModelRegister
from mafw.db.trigger import Trigger
from mafw.mafw_errors import MAFwException, UnsupportedDatabaseError

database_proxy = DatabaseProxy()
"""This is a placeholder for the real database object that will be known only at run time"""


mafw_model_register = ModelRegister()
"""
This is the instance of the ModelRegister

    .. seealso::
    
        :class:`.ModelRegister` for more information on how to retrieve models and :class:`.RegisteredMeta` and :class:`MAFwBaseModel` for the automatic registration of models`

"""


class RegisteredMeta(ModelBase):
    """
    Metaclass for registering models with the MAFw model registry.

    This metaclass automatically registers model classes with the global model registry
    when they are defined, allowing for dynamic discovery and management of database models.
    It ensures that only concrete model classes (not the base classes themselves) are registered.

    The registration process uses the table name from the model's metadata or generates
    a snake_case version of the class name if no explicit table name is set.
    """

    reserved_field_names = ['__logic__', '__conditional__']

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], **kwargs: dict[str, Any]) -> type:
        """
        Create a new model class and register it if applicable.

        This method is called during class definition to create the actual class
        and register it with the MAFw model registry if it's a concrete model class.

        :param name: The name of the class being created.
        :type name: str
        :param bases: The base classes of the class being created.
        :type bases: tuple
        :param attrs: The attributes of the class being created.
        :type attrs: dict
        :param kwargs: Other keyword attributes passed to the class.
        :type kwargs: dict[str, Any]
        :return: The newly created class.
        :rtype: type
        """
        # store here any extra argument that is passed to the class defition.
        extra_args = kwargs

        meta = attrs.get('Meta', None)
        if meta:
            custom_table_name = meta.__dict__.get('table_name', None)
        else:
            custom_table_name = None
        model = cast(RegisteredMeta, super().__new__(cls, name, bases, attrs))  # type: ignore[no-untyped-call]

        if TYPE_CHECKING:
            assert hasattr(model, '_meta')

        # for consistency, add the extra_args to the meta instance
        model._meta.extra_args = extra_args

        # check for the use of reserved field names.
        field_names = model._meta.sorted_field_names
        if any([reserved_name in field_names for reserved_name in RegisteredMeta.reserved_field_names]):
            warnings.warn(
                f'Model {model.__name__} is using a reserved field name. Filter configuration might not '
                f'work properly. Reserved names are f{RegisteredMeta.reserved_field_names}.'
            )

        # this super call is actually creating the Model class according to peewee ModelBase (that is a metaclass)
        # the model class will have an attribute (_meta) created by the ModelBase using the inner class Meta as a template.
        # The additional attributes (like suffix, prefix, ...) that we have added in the MAFwBaseModel Meta class will be
        # available. There is one problem, that the _meta.table_name is generated with our make_prefixed_suffixed_table_name
        # but before that the additional attributes are actually transferred to the instance of the meta class.
        # for this reason we need to regenerate the table_name now, when the whole Meta class is available.
        # We do so only if the user didn't specify a custom table name
        if custom_table_name is None:
            if model._meta.table_function is None:
                table_name = make_snake_case(model.__name__)
            else:
                table_name = model._meta.table_function(model)
            model._meta.table_name = table_name

        # Do we need to register the Model?
        # By default we want to register (so skip_registration = False)
        skip_registration = extra_args.get('do_not_register', False)
        if skip_registration:
            # no need to register, so just skip the registration.
            return model

        # Register only concrete model classes that are not base classes
        # Check that we're not processing base classes themselves
        is_base_class = name in ['Model', 'MAFwBaseModel', 'StandardTable']

        # Check that we have valid bases and that at least one inherits from Model
        has_valid_bases = bases and any(issubclass(base, Model) for base in bases)

        if not is_base_class and has_valid_bases:
            table_name = model._meta.table_name
            mafw_model_register.register_model(table_name, model)

            if hasattr(model._meta, 'suffix'):
                mafw_model_register.register_suffix(model._meta.suffix)

            if hasattr(model._meta, 'prefix'):
                mafw_model_register.register_prefix(model._meta.prefix)

        return model


class MAFwBaseModelDoesNotExist(MAFwException):
    """Raised when the base model class is not existing."""


def make_prefixed_suffixed_name(model_class: RegisteredMeta) -> str:
    """
    Generate a table name with optional prefix and suffix for a given model class.

    This function constructs a table name by combining the prefix, the snake_case
    version of the model class name, and the suffix. If either prefix or suffix
    are not defined in the model's metadata, empty strings are used instead.

    The prefix, table name, and suffix are joined using underscores. For example:

        - If a model class is named "UserAccount" with prefix="app", suffix="data",
          the resulting table name will be "app_user_account_data"

        - If a model class is named "Product" with prefix="ecommerce", suffix="_latest",
          the resulting table name will be "ecommerce_product_latest"

    .. note::

        Underscores (_) will be automatically added to prefix and suffix if not already present.

    :param model_class: The model class for which to generate the table name.
    :type model_class: RegisteredMeta
    :return: The constructed table name including prefix and suffix if applicable.
    :rtype: str
    """
    if TYPE_CHECKING:
        assert hasattr(model_class, '_meta')

    if hasattr(model_class._meta, 'suffix') and model_class._meta.suffix is not None:
        suffix = model_class._meta.suffix
    else:
        suffix = ''

    if hasattr(model_class._meta, 'prefix') and model_class._meta.prefix is not None:
        prefix = model_class._meta.prefix
    else:
        prefix = ''

    if not suffix.startswith('_') and suffix != '':
        suffix = '_' + suffix

    if not prefix.endswith('_') and prefix != '':
        prefix = prefix + '_'

    return f'{prefix}{make_snake_case(model_class.__name__)}{suffix}'


class MAFwBaseModel(Model, metaclass=RegisteredMeta):
    """The base model for the MAFw library.

    Every model class (table) that the user wants to interface must inherit from this base.

    This class extends peewee's Model with several additional features:

    1. Automatic model registration: Models are automatically registered with the MAFw model registry
       during class definition, enabling dynamic discovery and management of database models.

    2. Trigger support: The class supports defining database triggers through the :meth:`.triggers` method,
       which are automatically created when the table is created. File removal triggers can also be automatically
       generated using the `file_trigger_auto_create` boolean flag in the :ref:`meta class <auto_triggers>`. See also
       :meth:`.file_removal_triggers`.

    3. Standard upsert operations: Provides :meth:`.std_upsert` and :meth:`.std_upsert_many` methods for
       performing upsert operations that work with SQLite and PostgreSQL.

    4. Dictionary conversion utilities: Includes :meth:`.to_dict`, :meth:`.from_dict`, and :meth:`.update_from_dict`
       methods for easy serialization and deserialization of model instances.

    5. Customizable table naming: Supports table name prefixes and suffixes through the Meta class
       with `prefix` and `suffix` attributes. See :func:`.make_prefixed_suffixed_name`.

    6. Automatic table creation control: The `automatic_creation` Meta attribute controls whether
       tables are automatically created when the application starts.

    .. note::

        The automatic model registration can be disabled for one single model class using the keyword argument
        `do_not_register` passed to the :class:`.RegisteredMeta` meta-class. For example:

         .. code-block:: python

            class AutoRegisterModel(MAFwBaseModel):
                pass


            class NoRegisterModel(MAFwBaseModel, do_not_register=True):
                pass

        the first class will be automatically registered, while the second one will not. This is particularly useful if
        the user wants to define a base model class for the whole project without having it in the register where
        only concrete Model implementations are stored.

    """

    @classmethod
    def get_fields_by_type(cls, field_type: type[Field]) -> dict[str, Field]:
        """
        Return a dict {field_name: field_object} for all fields of the given type.

        .. versionadded:: v2.0.0

        :param field_type: Field type
        :type field_type: peewee.Field
        :return: A dict {field_name: field_object} for all fields of the given type.
        :rtype: dict[str, peewee.Field]
        """
        if TYPE_CHECKING:
            assert hasattr(cls, '_meta')

        return {name: field for name, field in cls._meta.fields.items() if isinstance(field, field_type)}

    @classmethod
    def file_removal_triggers(cls) -> list[Trigger]:
        """
        Generate a list of triggers for automatic file removal when records are deleted.

        This method creates database triggers that automatically handle file cleanup when
        records containing :class:`~mafw.db.fields.FileNameField` fields are removed from
        the database table. The triggers insert the filenames and checksums into the
        :class:`~mafw.db.std_tables.OrphanFile` table for later processing.

        The triggers are only created if the model has at least one field of type
        :class:`~mafw.db.fields.FileNameField`. If no such fields exist, an empty list
        is returned.

        :class:`.FileNameListField` is a subclass of :class:`.FileNameField` and is treated in the same
        way.

        .. versionadded:: v2.0.0

        .. note::

            This functionality requires the ``file_trigger_auto_create`` attribute in the
            model's Meta class to be set to ``True`` for automatic trigger creation.

        :return: A list containing the trigger object for file removal, or an empty list
            if no :class:`~mafw.db.fields.FileNameField` fields are found.
        :rtype: list[:class:`~mafw.db.trigger.Trigger`]
        """
        from mafw.db.std_tables import OrphanFile, TriggerStatus

        # it includes also FileNameListField that is a subclass of FileNameField
        file_fields = cls.get_fields_by_type(FileNameField)

        if len(file_fields) == 0:
            return []

        if TYPE_CHECKING:
            assert hasattr(cls, '_meta')

        new_trigger = Trigger(
            trigger_name=cls._meta.table_name + '_delete_files',
            trigger_type=(trigger.TriggerWhen.Before, trigger.TriggerAction.Delete),
            source_table=cls,
            safe=True,
            for_each_row=True,
        )
        sub_query = TriggerStatus.select(TriggerStatus.status).where(TriggerStatus.trigger_type == 'DELETE_FILES')  # type: ignore[no-untyped-call]
        trigger_condition = Value(1) == sub_query
        new_trigger.add_when(trigger_condition)
        data = []
        for f in file_fields:
            c = cast(FileNameField, file_fields[f]).checksum_field or f
            # the checksum is not really used in the OrphanFile.
            # in versions before 2.0.0, the checksum field in OrphanFile was not nullable,
            # so it should contain something. In order to be backward compatible, in case of a missing checksum field
            # we will just use the filename
            # note that the automatic filename to checksum conversion will not work in this case because the trigger
            # lives in the database and not in the application.
            data.append({'filenames': SQL(f'OLD.{f}'), 'checksum': SQL(f'OLD.{c}')})
        insert_query = OrphanFile.insert_many(data)
        new_trigger.add_sql(insert_query)

        return [new_trigger]

    @classmethod
    def triggers(cls) -> list[Trigger]:
        """
        Returns an iterable of :class:`~mafw.db.trigger.Trigger` objects to create upon table creation.

        The user must overload this returning all the triggers that must be created along with this class.
        """
        return []

    # noinspection PyUnresolvedReferences
    @classmethod
    def create_table(cls, safe: bool = True, **options: Any) -> None:
        """
        Create the table in the underlying DB and all the related trigger as well.

        If the creation of a trigger fails, then the whole table dropped, and the original exception is re-raised.

        .. warning::

            Trigger creation has been extensively tested with :link:`SQLite`, but not with the other database implementation.
            Please report any malfunction.

        :param safe: Flag to add an IF NOT EXISTS to the creation statement. Defaults to True.
        :type safe: bool, Optional
        :param options: Additional options passed to the super method.
        """
        super().create_table(safe, **options)

        # this is just use to make mypy happy.
        meta_cls = cast(PeeweeModelWithMeta, cls)

        # Get the database instance, it is used for trigger creation
        db = meta_cls._meta.database

        triggers_list = cls.triggers()

        if meta_cls._meta.file_trigger_auto_create:
            triggers_list.extend(cls.file_removal_triggers())

        if len(triggers_list):
            # Create tables with appropriate error handling
            try:
                for trigger in triggers_list:
                    trigger.set_database(db)
                    try:
                        db.execute_sql(trigger.create())
                    except UnsupportedDatabaseError as e:
                        warnings.warn(f'Skipping unsupported trigger {trigger.trigger_name}: {str(e)}')
                    except Exception:
                        raise
            except:
                # If an error occurs, drop the table and any created triggers
                meta_cls._meta.database.drop_tables([cls], safe=safe)
                for trigger in triggers_list:
                    try:
                        db.execute_sql(trigger.drop(True))
                    except Exception:
                        pass  # Ignore errors when dropping triggers during cleanup
                raise

    # noinspection PyProtectedMember
    @classmethod
    def std_upsert(cls, __data: dict[str, Any] | None = None, **mapping: Any) -> ModelInsert:
        """
        Perform a so-called standard upsert.

        An upsert statement is not part of the standard SQL and different databases have different ways to implement it.
        This method will work for modern versions of :link:`sqlite` and :link:`postgreSQL`.
        Here is a `detailed explanation for SQLite <https://www.sqlite.org/lang_upsert.html>`_.

        An upsert is a statement in which we try to insert some data in a table where there are some constraints.
        If one constraint is failing, then instead of inserting a new row, we will try to update the existing row
        causing the constraint violation.

        A standard upsert, in the naming convention of MAFw, is setting the conflict cause to the primary key with all
        other fields being updated. In other words, the database will try to insert the data provided in the table, but
        if the primary key already exists, then all other fields will be updated.

        This method is equivalent to the following:

        .. code-block:: python

            class Sample(MAFwBaseModel):
                sample_id = AutoField(
                    primary_key=True,
                    help_text='The sample id primary key',
                )
                sample_name = TextField(help_text='The sample name')


            (
                Sample.insert(sample_id=1, sample_name='my_sample')
                .on_conflict(
                    preserve=[Sample.sample_name]
                )  # use the value we would have inserted
                .execute()
            )

        :param __data: A dictionary containing the key/value pair for the insert. The key is the column name.
            Defaults to None
        :type __data: dict, Optional
        :param mapping: Keyword arguments representing the value to be inserted.
        """
        # this is used just to make mypy happy.
        # cls and meta_cls are exactly the same thing
        meta_cls = cast(PeeweeModelWithMeta, cls)

        if meta_cls._meta.composite_key:
            conflict_target = [meta_cls._meta.fields[n] for n in meta_cls._meta.primary_key.field_names]
        else:
            conflict_target = [meta_cls._meta.primary_key]

        conflict_target_names = [f.name for f in conflict_target]
        preserve = [f for n, f in meta_cls._meta.fields.items() if n not in conflict_target_names]
        return cast(
            ModelInsert, cls.insert(__data, **mapping).on_conflict(conflict_target=conflict_target, preserve=preserve)
        )

    # noinspection PyProtectedMember
    @classmethod
    def std_upsert_many(cls, rows: Iterable[Any], fields: list[str] | None = None) -> ModelInsert:
        """
        Perform a standard upsert with many rows.

        .. seealso::

            Read the :meth:`std_upsert` documentation for an explanation of this method.

        :param rows: A list with the rows to be inserted. Each item can be a dictionary or a tuple of values. If a
            tuple is provided, then the `fields` must be provided.
        :type rows: Iterable
        :param fields: A list of field names. Defaults to None.
        :type fields: list[str], Optional
        """
        # this is used just to make mypy happy.
        # cls and meta_cls are exactly the same thing
        meta_cls = cast(PeeweeModelWithMeta, cls)

        if meta_cls._meta.composite_key:
            conflict_target = [meta_cls._meta.fields[n] for n in meta_cls._meta.primary_key.field_names]
        else:
            conflict_target = [meta_cls._meta.primary_key]

        conflict_target_names = [f.name for f in conflict_target]
        preserve = [f for n, f in meta_cls._meta.fields.items() if n not in conflict_target_names]
        return cast(
            ModelInsert,
            (
                cls.insert_many(rows, fields).on_conflict(
                    conflict_target=conflict_target,
                    preserve=preserve,
                )
            ),
        )

    def to_dict(
        self,
        recurse: bool = True,
        backrefs: bool = False,
        only: list[str] | None = None,
        exclude: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Convert model instance to dictionary with optional parameters

        See full documentation directly on the `peewee documentation
        <https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#dict_to_model>`__.

        :param recurse: If to recurse through foreign keys. Default to True.
        :type recurse: bool, Optional
        :param backrefs: If to include backrefs. Default to False.
        :type backrefs: bool, Optional
        :param only: A list of fields to be included. Defaults to None.
        :type only: list[str], Optional
        :param exclude: A list of fields to be excluded. Defaults to None.
        :type exclude: list[str], Optional
        :param kwargs: Other keyword arguments to be passed to peewee `playhouse shortcut <https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#dict_to_model>`__.
        :return: A dictionary containing the key/value of the model.
        :rtype: dict[str, Any]
        """
        # the playhouse module of peewee is not typed.
        return model_to_dict(  # type: ignore[no-any-return]
            self,
            recurse=recurse,
            backrefs=backrefs,  # type: ignore[no-untyped-call]
            only=only,
            exclude=exclude,
            **kwargs,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any], ignore_unknown: bool = False) -> 'MAFwBaseModel':
        """
        Create a new model instance from dictionary

        :param data: The dictionary containing the key/value pairs of the model.
        :type data: dict[str, Any]
        :param ignore_unknown: If unknown dictionary keys should be ignored.
        :type ignore_unknown: bool
        :return: A new model instance.
        :rtype: MAFwBaseModel
        """
        # the playhouse module of peewee is not typed.
        return dict_to_model(cls, data, ignore_unknown=ignore_unknown)  # type: ignore[no-untyped-call,no-any-return]

    def update_from_dict(self, data: dict[str, Any], ignore_unknown: bool = False) -> 'MAFwBaseModel':
        """
        Update current model instance from dictionary

        The model instance is returned for daisy-chaining.

        :param data: The dictionary containing the key/value pairs of the model.
        :type data: dict[str, Any]
        :param ignore_unknown: If unknown dictionary keys should be ignored.
        :type ignore_unknown: bool
        """
        update_model_from_dict(self, data, ignore_unknown=ignore_unknown)  # type: ignore[no-untyped-call]
        return self

    class Meta:
        """The metadata container for the Model class"""

        database = database_proxy
        """The reference database. A proxy is used as a placeholder that will be automatically replaced by the real 
        instance of the database at runtime."""

        legacy_table_names = False
        """
        Set the default table name as the snake case of the Model camel case name.
        
        So for example, a model named ThisIsMyTable will corresponds to a database table named this_is_my_table.
        """

        suffix = ''
        """
        Set the value to append to the table name. 
        """

        prefix = ''
        """
        Set the value to prepend to the table name. 
        """

        table_function = make_prefixed_suffixed_name
        """
        Set the table naming function.
        """

        automatic_creation = True
        """
        Whether the table linked to the model should be created automatically
        """

        file_trigger_auto_create = False
        """
        Whether to automatically create triggers to delete files once a row with a FilenameField is removed
        """
