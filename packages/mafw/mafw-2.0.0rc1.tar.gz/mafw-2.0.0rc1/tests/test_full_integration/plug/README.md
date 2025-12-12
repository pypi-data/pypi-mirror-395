A MAFw plugin example
=====================

This is to test the functionality of plugin import from an external project to MAFw. 

The project contains four processors to:

1. **GenerateDataFiles**: Generate synthetic data into test files. 
2. **PlugImporter**: Import data file into a database
3. **Analyser**: Analyse the data file and fill the results into a database table
4. **PlugPlotter**: Generate a plot starting from the analysis table

Installation
------------

The plugin module can be installed in a virtual environment using ``pip install plug_test`` 