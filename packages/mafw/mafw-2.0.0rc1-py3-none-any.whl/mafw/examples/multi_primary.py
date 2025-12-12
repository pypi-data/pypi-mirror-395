#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module demonstrates how to use multicolumn primary keys and foreign keys.
"""

import logging
import os
import random
from pathlib import Path
from typing import Iterable

from peewee import (
    JOIN,
    SQL,
    AutoField,
    CompositeKey,
    FloatField,
    ForeignKeyField,
    IntegerField,
    SqliteDatabase,
    TextField,
    fn,
)

from mafw.db.db_configurations import default_conf
from mafw.db.db_model import MAFwBaseModel, database_proxy
from mafw.db.fields import FileChecksumField, FileNameField

if __name__ == '__main__':
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    def generate_files(path: Path, n_total: int):
        output_files = []
        for i_file in range(1, n_total + 1):
            filename = path / Path(f'file_{i_file:03}.dat')
            filesize = random.randint(1024, 2048)
            with open(filename, 'wb') as fout:
                fout.write(os.urandom(filesize))
            output_files.append(filename)
        return output_files

    class Sample(MAFwBaseModel, do_not_register=True):
        sample_id = AutoField(primary_key=True, help_text='The sample id primary key')
        sample_name = TextField(help_text='The sample name')

    class Resolution(MAFwBaseModel, do_not_register=True):
        resolution_id = AutoField(primary_key=True, help_text='The resolution id primary key')
        resolution_value = FloatField(help_text='The resolution in µm')

    class Image(MAFwBaseModel, do_not_register=True):
        image_id = AutoField(primary_key=True, help_text='The image id primary key')
        filename = FileNameField(help_text='The filename of the image', checksum_field='checksum')
        checksum = FileChecksumField()
        sample = ForeignKeyField(Sample, on_delete='CASCADE', backref='+', lazy_load=False, column_name='sample_id')
        resolution = ForeignKeyField(
            Resolution, on_delete='CASCADE', backref='+', lazy_load=False, column_name='resolution_id'
        )

    class ProcessedImage(MAFwBaseModel, do_not_register=True):
        image = ForeignKeyField(
            Image,
            primary_key=True,
            backref='+',
            help_text='The image id, foreign key and primary',
            on_delete='CASCADE',
            lazy_load=False,
            column_name='image_id',
        )
        value = FloatField(default=0)

    class CalibrationMethod(MAFwBaseModel, do_not_register=True):
        method_id = AutoField(primary_key=True, help_text='The primary key for the calculation method')
        multiplier = FloatField(default=1.0, help_text='The multiplication factor of this method')

    class CalibratedImage(MAFwBaseModel, do_not_register=True):
        image = ForeignKeyField(
            ProcessedImage,
            on_delete='CASCADE',
            help_text='The reference to the processed image',
            backref='+',
            lazy_load=False,
            column_name='image_id',
        )
        method = ForeignKeyField(
            CalibrationMethod,
            on_delete='CASCADE',
            help_text='The reference to the calibration method',
            backref='+',
            lazy_load=False,
            column_name='method_id',
        )
        calibrated_value = FloatField(default=0.0, help_text='The calibrated value')

        @property
        def primary_key(self) -> Iterable:
            return self.image_id, self.method_id

        class Meta:
            primary_key = CompositeKey('image', 'method')

    class ColoredImage(MAFwBaseModel, do_not_register=True):
        image_id = IntegerField(help_text='The reference to the processed image. Combined FK with method_id')
        method_id = IntegerField(help_text='The reference to the calibration method. Combined FK with method_id')
        red = FloatField(default=0, help_text='Fake red. Only for testing')
        green = FloatField(default=0, help_text='Fake green. Only for testing')
        blue = FloatField(default=0, help_text='Fake blue. Only for testing')

        @property
        def primary_key(self) -> Iterable:
            return self.image_id, self.method_id

        class Meta:
            constraints = [
                SQL(
                    'FOREIGN KEY (image_id, method_id) REFERENCES '
                    'calibrated_image(image_id, method_id) ON DELETE CASCADE'
                )
            ]
            primary_key = CompositeKey('image_id', 'method_id')

    # end of model

    db_file = Path('advanced_db.db')

    database = SqliteDatabase(db_file, pragmas=default_conf['sqlite']['pragmas'])
    database_proxy.initialize(database)
    database.create_tables(
        [Sample, Resolution, Image, ProcessedImage, CalibrationMethod, CalibratedImage, ColoredImage]
    )

    # upsert samples
    n_samples = 10
    (
        Sample.insert_many(
            [(i, f'Sample_{i:03}') for i in range(n_samples)], fields=[Sample.sample_id, Sample.sample_name]
        )
        .on_conflict_replace()
        .execute()
    )

    # upsert resolution
    resolutions = [25, 50, 100]
    (
        Resolution.insert_many(
            [(i, res) for i, res in enumerate(resolutions, start=1)],
            fields=[Resolution.resolution_id, Resolution.resolution_value],
        )
        .on_conflict_replace()
        .execute()
    )

    n_images = 50

    from_scratch = True

    if from_scratch:
        tmpdir = Path.cwd() / 'tmp'
        tmpdir.mkdir(exist_ok=True)
        output_files = generate_files(tmpdir, n_images)

        with database.atomic() as txn:
            for file in output_files:
                sample = Sample.select().order_by(fn.Random()).limit(1).get()
                resolution = Resolution.select().order_by(fn.Random()).limit(1).get()

                image = Image()
                image.filename = file
                image.checksum = file
                image.sample_id = sample.sample_id
                image.resolution_id = resolution.resolution_id
                image.save()

    # calculate processed image
    with database.atomic() as txn:
        for image in Image.select().execute():
            processed_image = ProcessedImage(image_id=image.image_id)
            processed_image.value = random.uniform(0, 1000)
            processed_image.save(force_insert=True)

    # upsert calibration_methods
    n_methods = 4
    (
        CalibrationMethod.insert_many(
            [(i, (i + 1) * 0.5) for i in range(n_methods)],
            fields=[CalibrationMethod.method_id, CalibrationMethod.multiplier],
        )
        .on_conflict_replace()
        .execute()
    )
    #
    # make the multi calibration
    with database.atomic() as txn:
        cross_join = (
            ProcessedImage.select(ProcessedImage, CalibrationMethod).join(CalibrationMethod, JOIN.CROSS).execute()
        )
        for row in cross_join:
            calibrated_image = CalibratedImage()
            calibrated_image.image_id = row.image_id
            calibrated_image.method_id = row.method_id
            calibrated_image.calibrated_value = row.value * row.multiplier
            calibrated_image.save(force_insert=True)

    # assert that the table rows match
    assert CalibratedImage.select().count() == Image.select().count() * CalibrationMethod.select().count()

    # fill in the ColoredImage
    with database.atomic() as txn:
        full_list = CalibratedImage.select().execute()

        for row in full_list:
            colored_image = ColoredImage(image_id=row.image_id, method_id=row.method_id)
            colored_image.red = row.calibrated_value / 3
            colored_image.green = row.calibrated_value / 3
            colored_image.blue = row.calibrated_value / 3
            colored_image.save(force_insert=True)
    #

    ci = ColoredImage.select().order_by(database.random()).limit(1)[0]
    assert ci.primary_key == (ci.image_id, ci.method_id)

    # delete 5 row from Image
    n_image_del = 5
    rows_for_delete = Image.select().order_by(database.random()).limit(n_image_del)
    rows_for_delete = [r.image_id for r in rows_for_delete]
    Image.delete().where(Image.image_id.in_(rows_for_delete)).execute()

    assert Image.select().count() == n_images - n_image_del
    assert ProcessedImage.select().count() == (n_images - n_image_del)
    assert CalibratedImage.select().count() == (n_images - n_image_del) * n_methods
    assert ColoredImage.select().count() == (n_images - n_image_del) * n_methods

    # delete 1 method from CalibrationMethod
    n_method_del = 1
    rows_for_delete = CalibrationMethod.select().order_by(database.random()).limit(n_method_del)
    rows_for_delete = [r.method_id for r in rows_for_delete]
    CalibrationMethod.delete().where(CalibrationMethod.method_id.in_(rows_for_delete)).execute()

    assert Image.select().count() == n_images - n_image_del
    assert ProcessedImage.select().count() == (n_images - n_image_del)
    assert CalibratedImage.select().count() == (n_images - n_image_del) * (n_methods - n_method_del)
    assert ColoredImage.select().count() == (n_images - n_image_del) * (n_methods - n_method_del)

    # delete from calibrated image
    n_ci_del = 2
    rows_for_delete = Image.select().order_by(database.random()).limit(n_ci_del)
    rows_for_delete = [r.image_id for r in rows_for_delete]
    CalibratedImage.delete().where(CalibratedImage.image_id.in_(rows_for_delete)).execute()
    assert Image.select().count() == n_images - n_image_del
    assert ProcessedImage.select().count() == (n_images - n_image_del)
    assert CalibratedImage.select().count() == (n_images - n_image_del - n_ci_del) * (n_methods - n_method_del)
    assert ColoredImage.select().count() == (n_images - n_image_del - n_ci_del) * (n_methods - n_method_del)

    database.close()
