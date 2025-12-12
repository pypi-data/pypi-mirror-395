#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from peewee import SQL, AutoField, FloatField, ForeignKeyField, TextField

from mafw.db.db_model import MAFwBaseModel
from mafw.db.fields import FileChecksumField, FileNameField
from mafw.db.std_tables import StandardTable
from mafw.db.trigger import Trigger, TriggerAction, TriggerWhen, or_


class Detector(StandardTable):
    detector_id = AutoField(primary_key=True, help_text='Primary key for the detector table')
    name = TextField(help_text='The name of the detector')
    description = TextField(help_text='A longer description for the detector')

    @classmethod
    def init(cls) -> None:
        data = [
            dict(detector_id=1, name='Normal', description='Standard detector'),
            dict(detector_id=2, name='HighGain', description='High gain detector'),
            dict(detector_id=3, name='NoDark', description='Low dark current detector'),
        ]

        cls.insert_many(data).on_conflict(
            conflict_target=[cls.detector_id],
            update={'name': SQL('EXCLUDED.name'), 'description': SQL('EXCLUDED.description')},
        ).execute()


class InputFile(MAFwBaseModel):
    @classmethod
    def triggers(cls) -> list[Trigger]:
        update_file_trigger = Trigger(
            trigger_name='input_file_after_update',
            trigger_type=(TriggerWhen.After, TriggerAction.Update),
            source_table=cls,
            safe=True,
            for_each_row=True,
        )
        update_file_trigger.add_when(or_('NEW.exposure != OLD.exposure', 'NEW.checksum != OLD.checksum'))
        update_file_trigger.add_sql('DELETE FROM data WHERE file_pk = OLD.file_pk;')

        return [update_file_trigger]

    file_pk = AutoField(primary_key=True, help_text='Primary key for the input file table')
    filename = FileNameField(unique=True, checksum_field='checksum', help_text='The filename of the element')
    checksum = FileChecksumField(help_text='The checksum of the element file')
    exposure = FloatField(help_text='The duration of the exposure in h')
    detector = ForeignKeyField(
        Detector, Detector.detector_id, on_delete='CASCADE', backref='detector', column_name='detector_id'
    )
    # finish input file


class Data(MAFwBaseModel):
    @classmethod
    def triggers(cls) -> list[Trigger]:
        delete_plotter_sql = 'DELETE FROM plotter_output WHERE plotter_name = "PlugPlotter";'

        insert_data_trigger = Trigger(
            trigger_name='data_after_insert',
            trigger_type=(TriggerWhen.After, TriggerAction.Insert),
            source_table=cls,
            safe=True,
            for_each_row=False,
        )
        insert_data_trigger.add_sql(delete_plotter_sql)

        update_data_trigger = Trigger(
            trigger_name='data_after_update',
            trigger_type=(TriggerWhen.After, TriggerAction.Update),
            source_table=cls,
            safe=True,
            for_each_row=False,
        )
        update_data_trigger.add_when('NEW.value != OLD.value')
        update_data_trigger.add_sql(delete_plotter_sql)

        delete_data_trigger = Trigger(
            trigger_name='data_after_delete',
            trigger_type=(TriggerWhen.After, TriggerAction.Delete),
            source_table=cls,
            safe=True,
            for_each_row=False,
        )
        delete_data_trigger.add_sql(delete_plotter_sql)

        return [insert_data_trigger, delete_data_trigger, update_data_trigger]

    file_pk = ForeignKeyField(InputFile, on_delete='cascade', backref='file', primary_key=True, column_name='file_id')
    value = FloatField(help_text='The result of the measurement')
