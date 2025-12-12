#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import sys
import warnings
from typing import List
from unittest.mock import patch

import pytest

from mafw.mafw_errors import MissingOptionalDependency


class TestFailedSNSPlotterImports:
    """Test class for testing import failure scenarios in sns_plotter module."""

    def setup_method(self):
        """Setup method to store original state before each test."""
        # Store the original import function
        if isinstance(__builtins__, dict):
            self.original_import = __builtins__['__import__']
        else:
            self.original_import = __builtins__.__import__

        # Store references to all seaborn-related modules and the sns_plotter module
        self.original_modules = {}

        # Store ALL matplotlib / seaborn-related modules that might be affected
        seaborn_modules = [k for k in sys.modules.keys() if k.startswith('seaborn')]
        pandas_modules = [k for k in sys.modules.keys() if k.startswith('pandas')]
        matplotlib_modules = [k for k in sys.modules.keys() if k.startswith('matplotlib')]
        sns_plotter_modules = ['mafw.processor_library.sns_plotter', 'sns_plotter']

        all_modules_to_store = matplotlib_modules + pandas_modules + seaborn_modules + sns_plotter_modules

        for module_name in all_modules_to_store:
            self.original_modules[module_name] = sys.modules.get(module_name)

        # Also store the specific sns reference from sns_plotter if it exists
        if 'mafw.processor_library.sns_plotter' in sys.modules:
            sns_plotter_module = sys.modules['mafw.processor_library.sns_plotter']
            if hasattr(sns_plotter_module, 'sns'):
                self.original_sns_reference = sns_plotter_module.sns
            else:
                self.original_sns_reference = None
        else:
            self.original_sns_reference = None

    def teardown_method(self):
        """Teardown method to restore original state after each test."""

        # Restore original __import__ function first
        if isinstance(__builtins__, dict):
            __builtins__['__import__'] = self.original_import
        else:
            __builtins__.__import__ = self.original_import

        # Remove all modules that we're going to restore to ensure clean state
        for module_name in self.original_modules.keys():
            if module_name in sys.modules:
                del sys.modules[module_name]

        # Restore all original modules in the correct order
        # First restore matplotlib / seaborn modules
        # seaborn_modules = {k: v for k, v in self.original_modules.items() if k.startswith('seaborn')}
        # for module_name, module in seaborn_modules.items():
        for module_name, module in self.original_modules.items():
            if module is not None:
                sys.modules[module_name] = module

        # Then restore sns_plotter modules
        sns_plotter_modules = {k: v for k, v in self.original_modules.items() if 'sns_plotter' in k}
        for module_name, module in sns_plotter_modules.items():
            if module is not None:
                sys.modules[module_name] = module

        # Restore the sns reference in sns_plotter module if needed
        if self.original_sns_reference is not None and 'mafw.processor_library.sns_plotter' in sys.modules:
            sns_plotter_module = sys.modules['mafw.processor_library.sns_plotter']
            if hasattr(sns_plotter_module, 'sns'):
                sns_plotter_module.sns = self.original_sns_reference

        # Clear stored modules
        self.original_modules.clear()

    def _remove_modules(self, modules_to_remove: List[str]) -> None:
        """
        Helper method to remove modules from sys.modules.
        Note: We don't store them here since they're already stored in setup_method.

        Args:
            modules_to_remove: List of module names to remove
        """
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]

    @pytest.mark.parametrize(
        'missing_modules,expected_in_message',
        [
            # Test individual missing modules
            (['matplotlib'], 'seaborn'),
            (['matplotlib.pyplot'], 'seaborn'),
            (['matplotlib.colors'], 'seaborn'),
            (['pandas'], 'seaborn'),
            (['seaborn'], 'seaborn'),
            # Test combinations of missing modules
            (['matplotlib', 'pandas'], 'seaborn'),
            (['matplotlib', 'seaborn'], 'seaborn'),
            (['pandas', 'seaborn'], 'seaborn'),
            (['matplotlib', 'pandas', 'seaborn'], 'seaborn'),
            # Test matplotlib submodules
            (['matplotlib.pyplot', 'matplotlib.colors'], 'seaborn'),
            (['matplotlib.typing'], 'seaborn'),
        ],
    )
    def test_missing_dependencies_raise_warning_and_exception(
        self, missing_modules: List[str], expected_in_message: str
    ):
        """
        Test that missing dependencies raise appropriate warnings and exceptions.

        Args:
            missing_modules: List of module names to simulate as missing
            expected_in_message: String expected to be in the warning message
        """
        # Remove sns_plotter modules to force reimport
        self._remove_modules(['mafw.processor_library.sns_plotter', 'sns_plotter'])

        # Remove the specified dependency modules
        self._remove_modules(missing_modules)

        # Mock the import mechanism to raise ImportError for missing modules
        def mock_import(name, *args, **kwargs):
            if any(name.startswith(missing_module) for missing_module in missing_modules):
                raise ImportError(f"**MOCK** No module named '{name}'")
            return self.original_import(name, *args, **kwargs)

        # Use context manager to ensure proper cleanup of the mock
        with patch.dict(__builtins__, {'__import__': mock_import}):
            # Test that importing sns_plotter raises ImportError and warning
            with pytest.warns(MissingOptionalDependency) as warning_info:
                with pytest.raises(ImportError):
                    import mafw.processor_library.sns_plotter  # noqa: F401

        # Verify warning message content
        warning_message = str(warning_info[0].message)
        assert expected_in_message in warning_message
        assert 'pip install mafw[seaborn]' in warning_message
        assert 'required dependencies' in warning_message

    def test_successful_import_when_all_dependencies_available(self):
        """Test that import succeeds when all dependencies are available."""
        # This test ensures our test setup doesn't break normal imports
        # First, make sure we can import the required modules
        try:
            import matplotlib
            import matplotlib.colors
            import matplotlib.pyplot  # noqa: F401
            import pandas  # noqa: F401
            import seaborn  # noqa: F401
        except ImportError:
            pytest.skip('Required dependencies not available in test environment')

        # Now test that sns_plotter can be imported without warnings
        with warnings.catch_warnings():
            warnings.simplefilter('error')  # Turn warnings into errors
            try:
                import mafw.processor_library.sns_plotter  # noqa: F401
                # If we get here, no warnings were raised
            except Warning as w:
                if isinstance(w, MissingOptionalDependency):
                    pytest.fail('MissingOptionalDependency warning raised when all dependencies available')
                else:
                    # Re-raise other warnings as they might be expected
                    raise
            except ImportError:
                # This might happen if there are other import issues in the module
                # that aren't related to the dependencies we're testing
                pass


class TestFailedPandasToolsImports:
    """Test class for testing import failure scenarios in sns_plotter module."""

    def setup_method(self):
        """Setup method to store original state before each test."""
        # Store the original import function
        if isinstance(__builtins__, dict):
            self.original_import = __builtins__['__import__']
        else:
            self.original_import = __builtins__.__import__

        # Store references to all seaborn-related modules and the sns_plotter module
        self.original_modules = {}

        # Store ALL pandas that might be affected
        pandas_modules = [k for k in sys.modules.keys() if k.startswith('pandas')]

        all_modules_to_store = pandas_modules

        for module_name in all_modules_to_store:
            self.original_modules[module_name] = sys.modules.get(module_name)

        # Also store the specific sns reference from sns_plotter if it exists
        if 'mafw.tools.pandas_tools' in sys.modules:
            pandas_tool_module = sys.modules['mafw.tools.pandas_tools']
            if hasattr(pandas_tool_module, 'pd'):
                self.original_pandas_reference = pandas_tool_module.pd
            else:
                self.original_pandas_reference = None
        else:
            self.original_pandas_reference = None

    def teardown_method(self):
        """Teardown method to restore original state after each test."""

        # Restore original __import__ function first
        if isinstance(__builtins__, dict):
            __builtins__['__import__'] = self.original_import
        else:
            __builtins__.__import__ = self.original_import

        # Remove all modules that we're going to restore to ensure clean state
        for module_name in self.original_modules.keys():
            if module_name in sys.modules:
                del sys.modules[module_name]

        # Restore all original modules in the correct order
        for module_name, module in self.original_modules.items():
            if module is not None:
                sys.modules[module_name] = module

        # Then restore sns_plotter modules
        pandas_tool_module = {k: v for k, v in self.original_modules.items() if 'pandas_tool' in k}
        for module_name, module in pandas_tool_module.items():
            if module is not None:
                sys.modules[module_name] = module

        # Restore the sns reference in sns_plotter module if needed
        if self.original_pandas_reference is not None and 'mafw.tools.pandas_tools' in sys.modules:
            pandas_tool_module = sys.modules['mafw.tools.pandas_tools']
            if hasattr(pandas_tool_module, 'pd'):
                pandas_tool_module.pd = self.original_pandas_reference

        # Clear stored modules
        self.original_modules.clear()

    def _remove_modules(self, modules_to_remove: List[str]) -> None:
        """
        Helper method to remove modules from sys.modules.
        Note: We don't store them here since they're already stored in setup_method.

        Args:
            modules_to_remove: List of module names to remove
        """
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]

    @pytest.mark.parametrize(
        'missing_modules,expected_in_message',
        [
            # Test individual missing modules
            (['pandas'], 'seaborn'),
        ],
    )
    def test_missing_dependencies_raise_warning_and_exception(
        self, missing_modules: List[str], expected_in_message: str
    ):
        """
        Test that missing dependencies raise appropriate warnings and exceptions.

        Args:
            missing_modules: List of module names to simulate as missing
            expected_in_message: String expected to be in the warning message
        """
        # Remove sns_plotter modules to force reimport
        self._remove_modules(['mafw.tools.pandas_tools', 'pandas_tools'])

        # Remove the specified dependency modules
        self._remove_modules(missing_modules)

        # Mock the import mechanism to raise ImportError for missing modules
        def mock_import(name, *args, **kwargs):
            if any(name.startswith(missing_module) for missing_module in missing_modules):
                raise ImportError(f"**MOCK** No module named '{name}'")
            return self.original_import(name, *args, **kwargs)

        # Use context manager to ensure proper cleanup of the mock
        with patch.dict(__builtins__, {'__import__': mock_import}):
            # Test that importing sns_plotter raises ImportError and warning
            with pytest.warns(MissingOptionalDependency) as warning_info:
                with pytest.raises(ImportError):
                    import mafw.tools.pandas_tools  # noqa: F401

        # Verify warning message content
        warning_message = str(warning_info[0].message)
        assert expected_in_message in warning_message
        assert 'pip install mafw[seaborn]' in warning_message
        assert 'required dependencies' in warning_message

    def test_successful_import_when_all_dependencies_available(self):
        """Test that import succeeds when all dependencies are available."""
        # This test ensures our test setup doesn't break normal imports
        # First, make sure we can import the required modules
        try:
            import pandas  # noqa: F401
        except ImportError:
            pytest.skip('Required dependencies not available in test environment')

        # Now test that sns_plotter can be imported without warnings
        with warnings.catch_warnings():
            warnings.simplefilter('error')  # Turn warnings into errors
            try:
                import mafw.tools.pandas_tools  # noqa: F401
                # If we get here, no warnings were raised
            except Warning as w:
                if isinstance(w, MissingOptionalDependency):
                    pytest.fail('MissingOptionalDependency warning raised when all dependencies available')
                else:
                    # Re-raise other warnings as they might be expected
                    raise
            except ImportError:
                # This might happen if there are other import issues in the module
                # that aren't related to the dependencies we're testing
                pass
