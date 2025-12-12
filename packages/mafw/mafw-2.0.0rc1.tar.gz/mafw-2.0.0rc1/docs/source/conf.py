#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Path to the root of your project (the one containing 'src')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the 'src' directory to sys.path so Python can import mafw from source
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.append(os.path.abspath('_ext'))

import mafw  # noqa: E402

project = 'MAFw'
copyright = '2024, Antonio Bulgheroni'
author = 'Antonio Bulgheroni'
release = mafw.__about__.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx_click',
    'sphinx_design',
    'sphinxcontrib.external_links',
    'sphinx.ext.imgconverter',
    'procparams',
]

numfig = True
nitpicky = True
nitpick_ignore = [
    ('py:class', 'abc.ABC'),
    ('py:class', 'enum.IntEnum'),
    ('py:class', 'enum.StrEnum'),
    ('py:class', 'enum.Enum'),
    ('py:class', 'pluggy._manager.PluginManager'),
    ('py:class', 'pluggy.PluginManager'),
    ('py:class', 'PluginManager'),
    ('py:class', 'pathlib.Path'),
    ('py:class', 'Path'),
    ('py:exc', 'FileNotFound'),
    ('py:class', 'peewee.Model'),
    ('py:class', 'peewee.ModelBase'),
    ('py:class', 'peewee.Database'),
    ('py:class', 'peewee.DatabaseProxy'),
    ('py:class', 'peewee.TextField'),
    ('py:class', 'peewee.Expression'),
    ('py:class', 'peewee.FieldAccessor'),
    ('py:class', 'peewee.DoesNotExist'),
    ('py:class', 'peewee.ModelInsert'),
    ('py:class', 'peewee.Query'),
    ('py:class', 'peewee.Field'),
    ('py:class', 'peewee.Alias'),
    ('py:class', 'peewee.Function'),
    ('py:class', 'peewee.Node'),
    ('py:class', 'playhouse.reflection.Introspector'),
    ('py:class', 'Introspector'),
    ('py:class', 'Model'),
    ('py:class', 'Database'),
    ('py:class', 'tomlkit.toml_document.TOMLDocument'),
    ('py:class', 'TOMLDocument'),
    ('py:class', 'tomlkit.items.String'),
    ('py:class', 'tomlkit.items.Item'),
    ('py:class', 'playhouse.signals.Model'),
    ('py:class', 'collections.UserDict'),
    ('py:class', "dict[slice(<class 'str'>, <class 'peewee.ModelBase'>, None)]"),
    ('py:class', 'collections.abc.Callable'),
    ('py:class', 'collections.abc.Sequence'),
    ('py:class', 'collections.abc.Iterable'),
    ('py:class', 'collections.abc.MutableMapping'),
    ('py:class', 'collections.abc.Mapping'),
    ('py:class', 'collections.abc.ItemsView'),
    ('py:class', 're.Pattern'),
    ('py:class', 'pd.DataFrame'),
    ('py:class', 'pandas.DataFrame'),
    ('py:class', 'pandas.core.frame.DataFrame'),
    ('py:class', 'typing._ProtocolMeta'),
    ('py:class', 'sns.FacetGrid'),
    ('py:class', 'seaborn.axisgrid.FacetGrid'),
    ('py:class', 'datetime.date'),
    ('py:class', 'datetime.datetime'),
    ('py:class', 'datetime.timedelta'),
    ('py:class', 'pandas._libs.tslibs.timestamps.Timestamp'),
    ('py:class', 'pandas._libs.tslibs.timedeltas.Timedelta'),
    ('py:class', 'matplotlib.colors.Colormap'),
    ('py:class', 'Colormap'),
    ('py:class', 'click.core.Command'),
    ('py:class', 'click.core.Context'),
    ('py:class', 'click.core.Group'),
    ('py:class', 'rich.prompt.Confirm'),
    ('py:class', 'Version'),
    ('py:class', 'packaging.version.Version'),
    ('py:class', 'subprocess.CompletedProcess'),
    ('py:class', 'ExprNode'),
    ('py:class', 'concurrent.futures.Future'),
    ('py:class', 'concurrent.futures._base.Future'),
]

# find a better solution for the graphviz_dot path. this works for my local
# installation but for sure it won't work for the gitlab container.
# can we set an enviromental variable?
graphviz_dot = r'C:\Program Files\Graphviz\bin\fdp.exe'
graphviz_output_format = 'svg'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # Add other theme options as needed
}
html_static_path = ['_static']
html_js_files = [
    'js/version-switcher.js',
]
todo_include_todos = True
html_sidebars = {'**': ['localtoc.html', 'sourcelink.html', 'searchbox.html', 'relations.html']}
html_css_files = [
    'css/table_custom.css',
]

# Context for multiversion
html_context = {
    'current_version': os.environ.get('SPHINX_MULTIVERSION_NAME', 'main'),
    'versions': [],  # This will be populated by sphinx-multiversion
}

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'member-order': 'groupwise',
    'show-inheritance': True,
    'private-members': True,
}

autodoc_mock_imports = ['pluggy', 'pluggy._manager', 'typing']
autoclass_content = 'both'
autosectionlabel_prefix_document = True

copybutton_exclude = '.linenos, .gp'

match_simple_bash = r'\$ '
match_env_bash = r'\([\w\-]+\)\s*\$ '
match_simple_dos = r'\w\:\\[\w\s\-]*\\*\> '
match_env_dos = r'\([\w\-]*\)\s*\w\:\\[\w\-]*\\*\> '

copybutton_prompt_text = '|'.join([match_simple_bash, match_simple_dos, match_env_dos, match_env_bash])
copybutton_prompt_is_regexp = True


rst_prolog = """
    .. role:: python(code)
        :language: python
"""

external_links = {
    'Google': 'https://google.com',  # matches ":link:`google`", ":link:`Google`", etc
    'pandas': 'https://pandas.pydata.org/',
    'peewee': 'http://docs.peewee-orm.com/',
    'dbeaver': 'https://dbeaver.io/',
    'SQLite': 'https://www.sqlite.org/',
    'ORACLE': 'https://www.oracle.com/',
    'PostgreSQL': 'https://www.postgresql.org/',
    'MySQL': 'https://www.mysql.com/',
    'matplotlib': 'https://matplotlib.org/',
    'seaborn': 'https://seaborn.pydata.org/',
    'numpy': 'https://numpy.org/',
    'toml': 'https://toml.io/',
    'textual': 'https://textual.textualize.io/',
    'jupyter': 'https://jupyter.org/',
    'marimo': 'https://marimo.io/',
    'marlin': 'https://ilcsoft.desy.de/portal/software_packages/marlin/',
    'EUTelescope': 'https://iopscience.iop.org/article/10.1088/1748-0221/15/09/P09020',
    'lcio': 'https://ilcsoft.desy.de/portal/software_packages/lcio/',
    'click': 'https://click.palletsprojects.com/en/stable/',
}
external_links_substitutions = {}

extlinks = {
    'issue': ('https://code.europa.eu/kada/mafw/-/issues%s', 'issue %s'),
}

html_favicon = '_static/images/general/mafw-logo.svg'

## options for latex/pdf output
latex_documents = [
    ('index', 'mafw.tex', 'MAFw: Modular Analysis Framework', 'Antonio Bulgheroni et al.', 'manual', True)
    # (startdocname, targetname, title, author, theme, toctree_only)
]


latex_logo = '_static/images/general/mafw-logo.pdf'
latex_elements = {'papersize': 'a4paper', 'fncychap': r'\usepackage[Glenn]{fncychap}'}

modindex_common_prefix = ['mafw.']

master_doc = 'index'

processor_base_class = 'mafw.processor.Processor'
processor_param_class = 'mafw.processor.ActiveParameter'
