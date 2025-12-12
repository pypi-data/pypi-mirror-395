# Changelog

"MAFw: Modular Analysis Framework"

## Unreleased (2025-12-03)

#### New Features

* (runner): add support for creating standard tables configuration
* (processor): add option to skip standard table creation
* (tools): support lazy import processors in steering file generation
* add lazy import classes for plugins
* (scripts): load external plugins in parallel and update processor listing
* (plugin): implement lazy loading for processors and user interfaces
* (processor): use db model register to handle standard tables
* (plugin): extend processor and UI registration to support lazy plugins
* (plugin): add thread-safe lazy plugin loader
* (db): add method to retrieve standard table models and update type checking
* (runner): load plugins in parallel and update plugin manager usage
* (plugin): implement parallel plugin loading with thread pool executor
* (db): make model registration thread-safe with locking mechanism
* (processor_library): use replica_name instead of name for plotter output storage
* (processor): add support for disabling inheritance in processor replicas
* (runner): enable multiple processor instances with replica support
* (tools): support multiple processor instances in steering file
* (processor): using replica names instead of names
* (processor): add support for multiple processor instances with replica identifiers
* (tools): add deep_update utility function for recursive dictionary updates
* (processor): add replica identifier support and tests
* (tools): add processor name parsing with replica support
* (db): add reserved field name checking and warning
* (db): enhance model registration with dual lookup support
* (tools): add mafw version to steering files
* (db): introduce autobinding for MAFwBaseModels and simplify bind method
* (tools): add new_only boolean field to TOML document
* (processor): extend reserved names and update filter handling
* (db): implement conditional filters and logical expressions
* (db): add named conditional filters and enhance logic evaluation
* (db_filter): implement logical expression parsing and evaluation for filters
* (processor): add reserved names validation for ActiveProcessorParameter
* (db): implement equality comparison for ConditionalFilterCondition
* (db): add conditional filtering support
* (processor_library): add SQLScriptRunner processor to execute SQL initialization scripts
* (processor): add configuration validation
* add InvalidConfigurationError
* (processor_library): add the soft recreate parameter to TableCreator
* (processor_library): add TriggerRefresher processor
* (db): extend the trigger dialect
* (processor_library): add output_folder and force_replot parameters to plotter processors
* (processor): modify processor parameter handling
* update docs command to use multiversion-doc for current version
* update build command in warning message and remove open URL print
* (docs): enhance build reporting and add current-only build command
* (db): improve generation of when conditions
* (db): implement automatic creation of delete_file trigger
* (db): support peewee Node objects in add_when method
* (db): implement automatic creation of delete_file trigger
* (mafw_exe): handle AbortProcessorException in main execution loop
* (mafw_exe): add display_exception function
* (ci): simplify gitlab ci by removing duplicate job definitions and updating image references
* (ci): add landing page copy to public directory in CI pipeline
* update format_size parameter type to float
* add automated documentation pruning feature
* (docs): add symlink support and root landing page generation
* (ci): update job extensions and remove debug ls commands
* (ci): update multidoc build version to v1.3.0
* add multidoc script for multiversion documentation generation
* add GitLab Pages redirects support and favicon for PDF downloads
* (docs): enhance version switcher and add PDF generation support
* (docs): add version switcher page existence check
* add multiversion-doc script with build and clean commands
* (docs): implement version mirroring and update dev/stable alias creation
* (docs): add version switcher and build script for multi-version docs
* (examples): mark example models as do_not_register
* (plugin): register database model modules through hookspec
* (db): add items() and clear() methods to ModelRegister
* (processor_library): add database initialization processor with table creation capabilities
* (ui): extend user interface with interactive mode and question prompting
* (db): extend metaclass to support registration control via keyword arguments
* (db): implement dynamic table name registration for models
* (db): add automatic table creation flag
* (db): extend model registration with prefix and suffix support
* (db): implement automatic model registration with metaclass
* (db): implement model registration and retrieval with prefix/suffix support
#### Fixes

* (plugins): preserve plugin loading order and simplify conditional logic
* (runner): remove std_tables from plugin loading
* (processor_library): use get_table_names() instead of get_model_names() for accurate table detection
* add type hint to _config attribute in processor module
* use explicit PDF file name instead of first file in directory
* (tools): handle comments for boolean fields in TOML output
* (doc): add procparams extension for documentation versioning to the patch files
* (db): replace logging with log alias in warning message
* (db): change log level from warning to debug for model fallback
* (db): fix mypy errors
* update assertion for tables_to_be_rebuilt to use empty set
* (processor_library): enhance type checking and disable untyped call warning for database atomic transaction
* wrong reference to MAFwModelBase
* remove static typing error
* (db): missing table name in PostgreSQL trigger drop
* fix mypy errors
* (ci): prefix job templates with dot to reference correctly
* (ci): correct docs build path for index.html landing page
* (ci): correct documentation and redirects deployment paths in gitlab-ci.yml
* (docs): enhance version switcher with DOM ready check
* (db): enhance table name generation with prefix and suffix handling
* (db): include StandardTable in model registration check
* (db): invert condition to warn when model already exists
* (db): update model type annotations and suppress attribute error
* update version regex pattern to include additional characters
#### Refactorings

* rename create_std_tables to create_standard_tables for clarity
* (processor): enhance orphan file pruning with robust error handling
* (processor): enhance type checking and model casting
* (plugins): load external plugins in parallel using LazyImportProcessor and LazyImportUserInterface
* (plugins): load external plugins in parallel
* (db): remove unnecessary type casting in model retrieval
* (scripts): rename LazyPlugin to LazyImportProcessor
* (plugins): simplify type hints for processor and user interface registration
* (db): remove standard_tables dictionary from std_tables module
* (ci): prefix basic hatch job with dot and update docs artifact path
* (doc): reorganize redirect generation and CI deployment script
* (ci): remove dot prefix from doc_build job definition
* rename build_versions.py to doc_versioning.py and enhance type hints
* (docs): replace argparse with click for command-line interface
#### Docs

* remove outdated documentation about pluggable standard tables
* enhance database documentation with standard tables details and clarify model registration
* update tutorial and processor docs for multiple processor instances
* update doc_runner with replica id and inheritance documentation
* add documentation for running processor replicas in steering file
* update graphviz diagrams to png format and fix rendering issues
* add schematic drawing of hierarchical filtering
* migrate and consolidate filter documentation
* add doc_filters to index
* correct ModelFilter class reference in get_filter docstring
* improve documentation and type hints consistency
* add ExprNode to excluded objects in documentation build
* add SQL script execution documentation
* update parameter documentation format with colon separator
* add processor parameter automatic documentation
* add mention to configuration validation
* add section on the TriggerRefresher
* remove reference to PassiveParameter
* update CONTRIBUTING.md with simplified doc command syntax
* update processor parameter documentation and examples
* implement automatic creation of file removal triggers
* update build directory and add missing class references
* update PDF link to local path
* update version switcher styling and layout
* update configuration for multiversion support and theme enhancements
* update tutorial with TableCreator processor configuration
* add missing class references for collections.abc.ItemsView and rich.prompt.Confirm
* update database documentation with model registration and table creation details
* update importer example with InputElement model definition
* (db): update ModelRegister docstring with seealso reference
* update database documentation with MAFwBaseModel features and fixes
* (db): add documentation for manual model registration control
* (db): update table naming documentation and reference
* (db): update documentation for table naming and creation attributes
* (db): enhance base model documentation with feature overview
#### Others

* update multidoc build min version and add max-size limit
* introduce .basic_hatch_job2 and update doc_build to use multidoc with new artifact structure
* change dependencies in test envs
* update tomlkit dependency to version 0.13.3
* remove un-used argument from doc command
* update doc tutorial redirect to stable branch
* (ci): add debug listings for docs and redirects deployment
* (ci): replace hardcoded runner tag with variable
* add update_notice.py to the coverage exclude list
* add simple-test environment with seaborn feature and pytest dependencies
* bump version to 2.0.0-rc.1
* update ruff version from v0.12.9 to v0.14.3
* add comments about replica_name
* add bullet point in front of the processor parameter list
* replace graphviz with mermaid diagrams
* add v to versionadded and versionchanged
* format docstring for update_db method
* implement lazy loading for plugin processors in full integration test
* update plugin manager tests to use load_plugins method
* add test for retrieving standard tables
* add unit tests for lazy import functionality
* update use of get_model_names to get_table_names
* include join table for filtering
* update plotter output path configuration for integration tests
* enable multiple GenerateDataFiles instances in steering file
* add test case for replica processor instances in steering file
* enable multiple processor instances in steering file
* adjust log level for fallback warning test
* enhance filter testing with autobind functionality
* enable new_only filter in integration test steering file
* add parameter name validation tests and update filter patching
* replace old filter tests with new implementation
* implement conditional filter logic and parsing tests
* add conditional filter functionality tests
* add SQLScriptRunner processor tests
* add unit test for TriggerRefresher
* extend tests for TableCreator
* include test for trigger drop and select
* add comprehensive tests for SQL generation and parameter interpolation
* remove manual table creation and register db models from full integration test
* add db model modules registration to mock plugin manager
* update plugin manager tests to include register_db_model_modules hook
* add tests for items() and clear() methods
* add comprehensive unit tests for database initialization processor
* add comprehensive tests for interactive mode and prompt question functionality
* add tests for metaclass registration control and extra arguments
* add comprehensive tests for RegisteredMeta
* add comprehensive tests for make_prefixed_suffixed_name function
* add comprehensive tests for ModelRegister class

## v1.4.0 (2025-11-05)

#### New Features

* (tools): introduce database tools module with key-value mapping and primary key utilities
* add citation file
#### Docs

* add documentation for new_only flag and processor parameters
* update type annotations and add peewee class references
* add advanced filtering tutorial with multiple column primary keys
* fix some typos
* add citing mafw section
#### Others

* bump version to 1.4.0
* add comprehensive tests for db tools functions

## v1.3.0 (2025-10-02)

#### New Features

* add a tool to automatically update the NOTICE.txt
* add LMPlot mixin
* (db): add model manipulations with dictionary
* extend the filter functionality
#### Fixes

* update the file regexp
* replace console printout with file writing
* (db): fix mypy errors
* (processor): orphan file pruning displaying the right number
* (sns_plotter): matplotlib backends are case insensitive
* remove warning for not found field
* the name of some operators were misspelled
#### Refactorings

* fix typing annotation
* move LogicalOP enum
#### Docs

* fix links
* add reference to CONTRIBUTING.md
* add note about conventional commit
* add missing import to a code example
* add note about hatch
* add API documentation
* include requirements section
* add note about the regexp operator in sqlite
* add note about matplotlib backend
* add note about lazy orphan file pruning
* expand filter documentation
* fix a typo
* improve the tutorial section
* add notes for eager readers
* fix mistyped prompt
* improve getting started instructions
* improve README
#### Others

* update version number
* fix a typo in a script
* change the unittest logic
* attempt to fix missing coverage
* update hash number of the maintenance image
* update MAFw version in NOTICE.txt
* add hook to update NOTICE.txt version
* update ruff to ruff-check
* change formatting
* change quotation mark style
* add unit tests for the explicit filtering

## v1.2.0 (2025-06-21)

#### New Features

* improve pandas grouping tools
* (cli): implement exit code
* (plotter): implement a new approach for the plotter
* (decorators): add suppress_warnings
#### Fixes

* (plugin): missing hook for standard tables
* (std_tables): fix issue with orphan file model and proper removal of files
* fix the order of a specific test
* remove useless conditions
* fix a bug in the usage of global filter as default value
* avoid double registration of parameters
* fix the PassiveProcessor repr method
* (type): fix a missing type annotation
* change handling of warnings
* fix a bug with python 3.11
* typo in the hatch-test definition
* modify the UnknownField
* fix a bug in the safe and for each setter
* fix two edge cases
* fix a bug in the bind_all of FilterRegister
* fix two bugs in Filter
* missing steering file setting
* missing steering file setting
* remove unused fixture
* fix a bug in the MAFwGroup main
* add exception for edge cases
* (decorators): add missing docstring
#### Docs

* remove sphix-prompt
* add a basic readme file to the plugin sub-project.
* add the test subsection
* add the tutorial section
* include installation instructions
* fix wrong indentation in a code-block
* Include the code snippets directly
* update db general documentation
* (db): improve filter API doc
* (db): improve filter API doc
* fix a broken reference
* update module documentation
* update references in the documentation
* (general): replace code snippet from test
#### Others

* add optional environment
* minor changes
* add sphix_prompt to the doc environment
* modify test extra dependencies and options
* improve test environment
* include coverage report
* (release): prepare for v1.2.0
* add copyright PyCharm configuration
* update copyright headers across source files
* update license
* add comments for literal include in doc
* remove unused code
* ruff format
* (type): improve typing annotation for some decorators.
* (type): add type ignore
* fix typo
* modify the import strategy
* rename SNSGenericPlotter to SNSPlotter
* add pragma no cover statements to abstract methods
* add pragme no cover statments to abstract methods
* remove test processor
* (integration): improve the integration test to make it more realistic
* minor improvements to the plugin processors
* final implementation of full integration
* change the scope of a fixture
* first version of the integration test
* mark integration test with @pytest.mark.integration_test
* improve test suite for processor
* improve test for optional dependencies
* add test suite for pandas tools
* add test suite for file_tools
* remove old test suite for db
* add test suite for wizard
* add test suite for database trigger
* add test suite for fields
* add test suite for db_model
* remove db_types from coverage
* improve test suite for toml tools
* improve test suite for db filter
* improve test suite for toml tools
* improve test suite for runner
* improve test suite for mafw_exe
* improve test suite for sns_plotter
* improve test suite for decorators
* improve test suite for optional dependencies in sns plotter
* add test suite for abstract_plotter module
* improve test suite for plotter
* improve test suite for std table
* improve test suite for plugin manager
* add test suite for the console ui interface
* add test suite for the abstract ui interface
* improve test suite for rich based ui interface
* improve test suite for timer
* improve test suite for importer
* improve test suite for enumerators
* improve test suite for decorators
* improve test suite for active

## v1.1.0 (2025-05-28)

#### New Features

* (db): extension to other DBs
#### Fixes

* (test): add sorted to the file list
#### Others

* (env): add a types environment, set uv as installer
* (deps): loose the dependency requirements
* bump version number to 1.1.0

## v1.0.0 (2025-04-07)

#### Others

* update version number
* remove old CEE CI config file

## v1.0.0rc6 (2025-04-07)

#### New Features

* add auto-commit argument
* add function to commit changelog changes
* add function to retrieve last tag
* add function to retrieve last commit message
* change return values
* add silent option
* add CLI options
* add retry condition to the basic jobs
* add logic to skip unittest when no relevant changes.
* add unittest partial exclusion from merge request.
#### Fixes

* change master to main as target branch.
#### Others

* update version number
* remove debug print outs
* typing and documentation
* modify hook name

## v1.0.0rc5 (2025-04-04)

#### Fixes

* disabling SSL verification
#### Others

* version update

## v1.0.0rc4 (2025-04-04)

#### Fixes

* add missing proxy declaration for JRC
#### Others

* version update

## v1.0.0rc3 (2025-04-04)

#### New Features

* add release cloning job
#### Others

* version update

## v1.0.0rc2 (2025-04-04)

#### New Features

* add rules as in CEE
* add package_local_publishing
* add package_build job
* restore the LISA jobs
* try to run unit-test with hatch
* debug private CI/CD
* implement the maintenance stage
#### Fixes

* scans not scan
* re-add scan
* move the before_script in the job definition.
* stage order
* add missing export of PROXY variables
* change the name of the scheduled pipelines token
* adjust page rule
* change order of conditions
* add sha signature
* debug retry_pipelines
* add exclusion criteria to all not maintenance jobs
* add private token
#### Others

* version update
* restore full unittest
* rename some jobs for consistency
* remove debug ls

## v1.0.0rc1 (2025-03-31)

#### New Features

* add latest release and modify coverage badge
* add the possibility to generate URL from code.europa.eu
* add the cov-xml command
* add latex target document
#### Fixes

* wrong path
#### Refactorings

* (test): improve some plotter tests
* (plotter): modify the keyword attributes
#### Docs

* add badges and remove todo
* fix conflict
* revise the general and the API documentation
* polish general documentation
* typo fixing
* add reference to the PDF documentation
* fix issue with missing reflection image
* update documentation
* change from code block to screenshot
* change tabs to tab-set
* add external links
* add introduction
* change footnotes to autonumbering
* Remove unexpected word
* improve general documentation
#### Others

* update version number
* add version number (~=) to direct dependencies
* add types stubs
* add sphinx-design
* update license
* update version number to 0.0.5
* add coverage regexp
* implement the CI for the code.europa.eu
* fix licence declaration
* update the issue base link
* update the project urls
* update version number
* update documentation link
* ruff format
* update copyright statement
* (documentation): fix typos and style
* (plotter): implement seaborn mocking

## v0.0.4 (2025-01-21)

#### New Features

* add pages deployment
* add pages deployment
* (db): add file delete trigger to PlotterOutput
* (db): change OrphanFile model
* (db): change OrphanFile model
* (plotter): implement customize_plot
* (plotter): implement the CatPlot
* (plotter): implement the DisPlot
* (plotter): implement the RelPlotter
* (plotter): add facet_grid attribute
* (plotter): add FromDataset data retriever
* (plotter): implement HDF data retriever, slicing and grouping
* (db): add new_only setter
* (plotter): preliminary implementation
* (decorators): add decorators for optional dependencies
* (examples): add an example of concrete file importer
* (library): add the basic importer processor
* (library): implement the FilenameParser
* (library): implement FilenameElement
* (mafw_exe): add warning catcher
* (examples): add examples to compare for and while loop
* (processor): implement the _execute_while_loop
* (decorators): implement looper decorators
* (processor): implement the check for overloaded and super methods.
* (processor): implement the use of loop type enumerator
* (enumerators): add the LoopType enumerator
#### Fixes

* (library): fix a bug in the FilenameElement
* (toml_tools): fixing bug with boolean items
* (coverage): change the test scripts
* fix a static typing issue
#### Performance improvements

* ci
#### Refactorings

* (documentation): include svg instead of dot files
* replace pytest with hatch test
* (plotter): modify test suite
* (plotter): modify test suite
* (plotter): change inheritance metaclass
* (plotter): improve code quality
* (plotter): Modify the SQL retriever mixin
* (processor): change the method with super check
* (plugin_manager): remove the load_external_plugin flag
* (plugin_manager): make the plugin_manager singleton
* (processor): replace log.warning with warnings.warn
#### Docs

* (plotter): add the general documentation about plotter
* add some API documentation.
* add doc_plotting page
* (plotter): API documentation
* fix some references
* fix typo in Optional parameter type
* (importer): implement the general documentation
* add the general documentation about execution workflow
* (examples): modify the description of the looper parameter.
* (processor): modify the execution workflow
#### Others

* (pyproject): add explicit types-seaborn to dev
* include pandas[hdf5] to seaborn feature
* (tests): add seaborn extra dep to hatch-test
* add seaborn optional dependency
* add coverage html report
* bump version number to v0.0.4
* (ci): remove two todos
* (documentation): remove todo about PlotterOutput
* add external links
* add nitpick_ignore
* (processor): API documentation
* (test): add missing looper to a processor
* (documentation): add mafw logo
* apply ruff format
* remove unused type ignore
* doc type
* (test): remove unused imports
* (toml_tools): remove white spaces
* (plotter): add test for standard table PlotterOutput
* (plotter): add test for looping plotter
* (plotter): add direct plot
* (plotter): mixin arguments in constructor and existing output
* (importer): add test for documentation purpose
* (mafw_exe): additional processor and warning catcher
* (plugin_manager): inclusion of additional processors

## v0.0.3 (2024-12-17)

#### New Features

* improve the update changelog script
#### Fixes

* (ci): fix a bug related to the removal of the type env
* fix a typo in the script entry point
#### Refactorings

* improve quality.
#### Docs

* add contributing section
#### Others

* modify the pre-push command
* removed pyproject-pre-commit
* change the pre-commit config
* update version number
* attempt to use pip cache

## v0.0.2 (2024-12-15)

#### New Features

* (mafw_exe): add db group and wizard command
* (db): add db_wizard module
* (decorators): implement a orphan_protector decorator
* (db): modify the PlotterOutput table
* (db): implement the FileNameListField
* (db): implement std_upsert and std_upsert_many
* (db): implement external library standard tables
* (db): add standard tables
* (processor): remove filter_list and rename get_item_list
* (db): change signature of FileChecksumField
* (db): implement the automatic linking a fields
* (db): add the FilterRegister
* (processor): modify filter loading
* (db): improve the Filter
* (processor): add support for filter registration
* (db): implement the Filter
* (db): implement the FileChecksumField
* (db): implement the FileNameField
* (db): add possibility to add when conditions to triggers
* (db): add helper function to and and or conditions
* (db): add support for trigger generation to MAFwBaseModel
* (db): add the trigger drop
* (mafw_errors): add exception for missing SQL statements
* (db): add Trigger class
* (examples): modify the FillTableProcessor
* (doc): add sphinx_code_tabs to the extensions
* (plugins): add FillTableProcessor
* (processor): implement parameter type conversion
* (examples): add an example of DB processor
* (tools): add toml encoder for Path
* (runner): add database configuration to the ProcessorList
* (toml): add generate_hexdigest_from_files
* (decorators): add database required decorator
* (mafw_errors): add MissingDatabase
* (processor): add database to the ProcessorList class
* (processor): add database to the Processor class
* (mafw_exe): add db configuration options to steering command
* (db): add db_scheme
* (db): add test for db configuration to toml
* (db): add test for db configuration to toml
* (db): add default configuration parameters
* (mafw_errors): add UnknownDBEngine
* (db): Implement the basic db model
#### Fixes

* (db): fix a small bug in the multi_primary example
* (decorators): fix wrong wrapping of database_required.
* (db): fix a bug with the trigger status
* (db): fix a bug in the drop table
* (processor): fix a bug with the closure of the database
* (tests): fix several SqliteDatabase connection
* (db): fix add_when that was not returin self.
* (db): fix a bug with the implementation og getattr
* typo in the doc dependency
* (toml): fix problem with escaping of windows path
* (tools): add missing hashlib import
* (processor): fixed creation of a db instance
* (processor): fix a bug in the assignement of database_conf
* (processor): fix a bug in the validate_database_conf
* (processor): fix missing validate_database_conf meth
* (db): set no inspection for playhouse
* (db): set no inspection for playhouse
#### Refactorings

* (db): change dump_models signature
* add view for testing
* (db): move the dump model test to a separate test unit
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* add typing hints
* (active): add typing hints
* change the definition of foreign key
* (filter): change the definition of the advanced model
* (timer): add typing hints
* (processor): improve decorator annotation
* (processor): implement changes for static typing
* (processor): implement changes for static typing
* (processor): implement changes for static typing
* (processor): implement changes for static typing
* (processor): implement changes for static typing
* (decorators): annotating ensure_parameter_registration
* (processor): change to comply to static typing
* (processor): apply no_implict_optional
* (processor): change annotation
* (db): adapt remove_widow and verify_checksum
* (db): improve the std_upsert signature
* (db): improve trigger interface
* (db): change the add_sql signature
* (processor): change the way the filters are loaded from conf file
* (db): move Trigger to trigger module
* (db): adopt new naming convention for tables
* (db): move Trigger to trigger module
* (db): adopt new naming convention for tables
* (db): change the MAFwBaseModel
* (db): rename to_sql in create
* (db): rename to_sql in create
* (doc): add a substitutions.rst
* (plugins): change the name of a processor
* (doc): add external links extension
* (processor): remove the atomic transaction creation
* (processor): add database and database_conf to Processor constructor
* (processor): add database and database_conf to Processor constructor
#### Docs

* remove todo concerning mafw db wizard
* (db): add section on the database reflection
* fix typo
* (mafw_exe): add API documentation
* (db): improve api doc of db_wizard
* fix nitpicky missing refs
* fix a missing docstring
* (db): add general documentation about orphan files
* (toml): update documentation.
* update general documentation
* fix typos
* update API documentation
* (db): add documentation about multi column pk / fk
* (db): update standard table documentation
* (db): add documentation about standard tables
* (db): update the documentation
* (filter): add documentation image
* (filter): update the API documentation
* (db): add section on filters
* (db): add documentation to the db_filter module
* (db): add documentation about Filter api
* (db): add section on custom fields
* (db): add warning box about triggers with MySQL and PostreSQL
* (db): add section on triggers
* add extlinks for gitlab issue
* (db): add signal example
* (db): add a section about triggers.
* (db): add missing docstring
* (database): add the section about running the FillFileTableProcessor
* (database): add section about database processors
* (database): add description of peewee
* (tutorial): add some text
* (examples): add documentation to FillTableProcessor
* add a tutorial page
* add note about the use of custom types as parameters
* fix nitpicky warnings
* fix nitpicky warnings
* add section about parameter typing
* (processor): improve module doc
#### Others

* add pre-commit config
* add pre-commit config
* add pre-push script
* add ruff scripts
* add scripts and dependency
* add mypy to CI
* include different version of python
* modify the pyproject.toml
* make the dev environment a matrix with different python versions.
* remove hardcoded env path
* update gitlab-ci
* add Deprecation
* add changelog file
* (doc): add external links extension
* (doc): add sphinx_code_tabs
* add peewee
* update changelog
* fix nitpick missing refs
* update repo version to v0.3.6
* update changelog
* update changelog
* update changelog
* update changelog
* add todo
* update changelog
* update changelog
* update changelog
* update changelog
* (doc): add classes to the nitpicky list
* update changelog
* (doc): add UserDict to nitpick_ignore
* update changelog
* (doc): update some line numbers
* updated changelog
* updated changelog
* (doc): use :link: role
* (db): add warning message
* (doc): add peewee link
* (processor): add database property
* (db): add automatically generated exception
* (doc): add some missing classes to nitpick_ignore
* (doc): add peewee.Model to nitpick_ignore
* (test_mafw_exe): remove useless duplicated assert
* (test_mafw_exe): remove useless runner
* bumped version number
* apply ruff format
* apply ruff format
* apply ruff format to all project files.
* apply ruff format to all project files
* apply ruff check to all projects
* add some comments to disable inspections
* (tools): fix wrong link in docstring
* (tools): rename widowed in widow
* (db): remove some warnings
* (db): remove unresolvedreferences for playhouse
* (db): add noinspection for _meta
* (examples): change formatting
* (mafw_exe): add test for the db wizard
* (db): add test suite for the db wizard
* (db): add full funcionality of orphan file removal
* (db): add test for FileNameListField
* (db): implement test for file_tools
* (filter): adapt to new default behavior of filter
* (filter): adapt to the new filter
* (db): add additional test on signals.
* (db): add test of the signal functionality
* (db): add test on trigger with when conditions
* (db): add test for automatic trigger creation
* (db): add test for drop and modification of triggers
* (db): add trigger tests
* (toml): add test for encoding of Path
* (processor): add test for processors with database required decorator
* (decorators): add test for database_required
* (processor): test the validate_database_conf
* (db): add test to check connection failure
* (test_mafw_exe): add test for steering options
* (db): add tests for the basic functionality

## v0.0.1 (2024-11-22)

