#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import os
import shutil
import subprocess
import tempfile
import venv
from pathlib import Path

import pytest
import tomlkit
from peewee import SqliteDatabase
from tomlkit.toml_file import TOMLFile

from mafw.db.db_configurations import default_conf


@pytest.mark.slow_integration_test
class TestFullIntegration:
    # For a reason not yet understood, when this test is executed from inside PyCharm, some additional options are
    # added to the subprocess command lines. This is particularly annoying when having to do the debugging of various
    # steps.
    #
    # To overcome this issue, it is possible to set the debug flag in the class to True. This executes the tests creating
    # a virtual environment in /tmp/full-int. This folder will not be removed by the teardown method, so you can
    # use it to manually test the various steps.
    #
    # Moreover, when debug is set to True, both the plugin and the mafw packages are installed in editable mode, so
    # that you can see directly the effect of code changes.

    @pytest.fixture
    def plugin_processors(self):
        return ['GenerateDataFiles', 'PlugImporter', 'Analyser', 'PlugPlotter']

    @classmethod
    def setup_class(cls):
        cls.debug = False

        # set the root of the mafw project
        cls.mafw_project_root = Path(__file__).parents[1]

        # manually set the data dir folder
        cls.datadir_path = Path(__file__).parent / Path(__file__).stem

        # set the plugin project
        cls.plugin_project_root = cls.datadir_path / 'plug'

        # set the steering file template dir
        cls.steering_template_dir = cls.datadir_path / 'steering_files'

        # create a temporary directory for the virtual environment
        if cls.debug:
            cls.env_path = Path('/tmp/full-int')
            if cls.env_path.exists():
                shutil.rmtree(cls.env_path)
            cls.env_path.mkdir(parents=True)
        else:
            cls.env_dir = tempfile.TemporaryDirectory()
            cls.env_path = Path(cls.env_dir.name)

        # Create a virtual environment without pip first
        venv.create(cls.env_path, with_pip=False, symlinks=True)

        # # get the venv python executable
        cls.python_bin = cls.env_path / ('Scripts' if os.name == 'nt' else 'bin') / 'python'
        assert cls.python_bin.exists()

        # Explicitly bootstrap pip with ensurepip
        subprocess.run([str(cls.python_bin), '-m', 'ensurepip', '--upgrade'], check=True)

        # Update pip
        subprocess.run([str(cls.python_bin), '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)

        # Install UV as part of the setup
        subprocess.run([str(cls.python_bin), '-m', 'pip', 'install', 'uv'], check=True)
        cls.uv_bin = cls.env_path / ('Scripts' if os.name == 'nt' else 'bin') / 'uv'

        # Install mafw project in the local env
        # we need to install mafw first, because we want to have the current version and not the one
        # available from the repository
        if cls.debug:
            subprocess.run(
                [
                    str(cls.python_bin),
                    '-m',
                    'uv',
                    'pip',
                    'install',
                    '--link-mode=copy',
                    '-e',
                    f'{str(cls.mafw_project_root)}[seaborn]',
                ],
                check=True,
            )
        else:
            subprocess.run(
                [
                    str(cls.python_bin),
                    '-m',
                    'uv',
                    'pip',
                    'install',
                    '--link-mode=copy',
                    f'{str(cls.mafw_project_root)}[seaborn]',
                ],
                check=True,
            )
        cls.mafw_bin = cls.env_path / ('Scripts' if os.name == 'nt' else 'bin') / 'mafw'

        # Install the plugin project
        if cls.debug:
            subprocess.run(
                [
                    str(cls.python_bin),
                    '-m',
                    'uv',
                    'pip',
                    'install',
                    '--link-mode=copy',
                    '-e',
                    f'{str(cls.plugin_project_root)}',
                ],
                check=True,
            )
        else:
            subprocess.run(
                [
                    str(cls.python_bin),
                    '-m',
                    'uv',
                    'pip',
                    'install',
                    '--link-mode=copy',
                    f'{str(cls.plugin_project_root)}',
                ],
                check=True,
            )
        cls.num_of_files = 25
        cls.dets = [1, 2, 3]

    @classmethod
    def teardown_class(cls):
        if not cls.debug:
            cls.env_dir.cleanup()

    @pytest.mark.order(0)
    def test_presence_of_mafw_in_new_env(self):
        assert (self.mafw_project_root / 'pyproject.toml').exists()
        assert self.python_bin.exists()
        assert self.uv_bin.exists()
        assert self.mafw_bin.exists()

    @pytest.mark.order(1)
    def test_availability_of_plugin_processors(self, plugin_processors):
        p = subprocess.run([str(self.mafw_bin), 'l'], check=True, capture_output=True)
        std_output = str(p.stdout)
        for proc in plugin_processors:
            assert proc in std_output

    @pytest.mark.order(2)
    def test_run_data_file_generation(self):
        orig_steering_file = self.steering_template_dir / 'generate-data-file.toml'
        actual_steering_file = self.env_path / 'generate-data-file.toml'
        data_dir = self.env_path / 'raw_data'

        # change the output path in the steering file.
        doc = TOMLFile(orig_steering_file).read()
        doc['GenerateDataFiles']['output_path'] = str(data_dir)

        # dump the modified steering file in actual_steering_file
        with open(actual_steering_file, 'w') as fp:
            tomlkit.dump(doc, fp)

        # run mafw
        subprocess.run([str(self.mafw_bin), 'r', f'{str(actual_steering_file)}'], check=True)

        for det in self.dets:
            # check that there are the right number of files in the data_dir
            digits = len(str(self.num_of_files))
            for i in range(self.num_of_files):
                assert Path(data_dir / f'rawfile_exp{i:0{digits}}_det{det}.dat').exists()

    @pytest.mark.order(3)
    def test_run_analysis(self):
        orig_steering_file = self.steering_template_dir / 'analysis.toml'
        actual_steering_file = self.env_path / 'analysis.toml'
        input_data_dir = self.env_path / 'raw_data'
        parser_configuration = self.steering_template_dir / 'importer_config.toml'
        database_file = self.env_path / 'plug.db'
        output_plot_path = self.env_path

        doc = TOMLFile(orig_steering_file).read()
        doc['PlugImporter']['input_folder'] = str(input_data_dir)
        doc['PlugImporter']['parser_configuration'] = str(parser_configuration)
        doc['DBConfiguration']['URL'] = 'sqlite:///' + str(database_file)
        doc['PlugPlotter']['output_folder'] = str(output_plot_path)

        with open(actual_steering_file, 'w') as fp:
            tomlkit.dump(doc, fp)

        # run mafw
        subprocess.run([str(self.mafw_bin), 'r', str(actual_steering_file)], check=True)

        # check if the output png exists
        assert output_plot_path.exists()

        # check the content of the DB.
        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        assert len(database.execute_sql('SELECT * FROM input_file').fetchall()) == self.num_of_files * len(self.dets)
        assert len(database.execute_sql('SELECT * FROM data').fetchall()) == self.num_of_files * len(self.dets)
        assert (
            len(database.execute_sql('SELECT * FROM plotter_output WHERE plotter_name = "PlugPlotter"').fetchall()) == 1
        )
        database.close()

    @pytest.mark.order(4)
    def test_trigger_of_input_file_remove_a_line(self):
        database_file = self.env_path / 'plug.db'
        output_plot_path = self.env_path / 'output.png'
        actual_steering_file = self.env_path / 'analysis.toml'

        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        database.execute_sql('DELETE FROM input_file WHERE exposure = 12 AND detector_id = 1;')
        database.close()

        output = subprocess.run([str(self.mafw_bin), 'r', str(actual_steering_file)], check=False, capture_output=True)
        print(output.stdout)
        assert '[1/1] Importing element 1 of 1' in str(output.stdout)
        assert '[1/1] Analysing rawfile_exp12_det1.dat' in str(output.stdout)
        assert 'Generating plot' in str(output.stdout)
        assert output_plot_path.exists()

        # check the content of the DB.
        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        assert len(database.execute_sql('SELECT * FROM input_file').fetchall()) == self.num_of_files * len(self.dets)
        assert len(database.execute_sql('SELECT * FROM data').fetchall()) == self.num_of_files * len(self.dets)
        assert (
            len(database.execute_sql('SELECT * FROM plotter_output WHERE plotter_name = "PlugPlotter"').fetchall()) == 1
        )
        database.close()

    @pytest.mark.order(5)
    def test_trigger_of_data_remove_a_line(self):
        database_file = self.env_path / 'plug.db'
        output_plot_path = self.env_path / 'output.png'
        actual_steering_file = self.env_path / 'analysis.toml'

        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        database.execute_sql(
            'DELETE FROM data WHERE file_id = (SELECT file_pk FROM input_file WHERE exposure = 14 and detector_id = 2)'
        )
        database.close()

        output = subprocess.run([str(self.mafw_bin), 'r', str(actual_steering_file)], check=True, capture_output=True)
        assert '[1/1] Analysing rawfile_exp14_det2.dat' in str(output.stdout)
        assert 'Generating plot' in str(output.stdout)
        assert output_plot_path.exists()

        # check the content of the DB.
        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        assert len(database.execute_sql('SELECT * FROM input_file').fetchall()) == self.num_of_files * len(self.dets)
        assert len(database.execute_sql('SELECT * FROM data').fetchall()) == self.num_of_files * len(self.dets)
        assert (
            len(database.execute_sql('SELECT * FROM plotter_output WHERE plotter_name = "PlugPlotter"').fetchall()) == 1
        )
        database.close()

    @pytest.mark.order(6)
    def test_generation_of_missing_plot_file(self):
        database_file = self.env_path / 'plug.db'
        output_plot_path = self.env_path / 'output.png'
        actual_steering_file = self.env_path / 'analysis.toml'

        output_plot_path.unlink()

        output = subprocess.run([str(self.mafw_bin), 'r', str(actual_steering_file)], check=True, capture_output=True)
        assert 'Generating plot' in str(output.stdout)
        assert output_plot_path.exists()

        # check the content of the DB.
        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        assert len(database.execute_sql('SELECT * FROM input_file').fetchall()) == self.num_of_files * len(self.dets)
        assert len(database.execute_sql('SELECT * FROM data').fetchall()) == self.num_of_files * len(self.dets)
        assert (
            len(database.execute_sql('SELECT * FROM plotter_output WHERE plotter_name = "PlugPlotter"').fetchall()) == 1
        )
        database.close()

    @pytest.mark.order(7)
    def test_alteration_of_input_file(self):
        database_file = self.env_path / 'plug.db'
        output_plot_path = self.env_path / 'output.png'
        actual_steering_file = self.env_path / 'analysis.toml'
        data_dir = self.env_path / 'raw_data'

        mod_file = data_dir / 'rawfile_exp14_det3.dat'
        with open(mod_file, 'r') as f:
            value = float(f.read())

        with open(mod_file, 'wt') as f:
            f.write(str(value + 0.1))

        output = subprocess.run([str(self.mafw_bin), 'r', str(actual_steering_file)], check=True, capture_output=True)
        assert '[1/1] Importing element 1 of 1 ' in str(output.stdout)
        assert '[1/1] Analysing rawfile_exp14_det3.dat' in str(output.stdout)
        assert 'Generating plot' in str(output.stdout)
        assert output_plot_path.exists()

        # check the content of the DB.
        database = SqliteDatabase(database_file, pragmas=default_conf['sqlite']['pragmas'])
        assert len(database.execute_sql('SELECT * FROM input_file').fetchall()) == self.num_of_files * len(self.dets)
        assert len(database.execute_sql('SELECT * FROM data').fetchall()) == self.num_of_files * len(self.dets)
        assert (
            len(database.execute_sql('SELECT * FROM plotter_output WHERE plotter_name = "PlugPlotter"').fetchall()) == 1
        )
        database.close()
