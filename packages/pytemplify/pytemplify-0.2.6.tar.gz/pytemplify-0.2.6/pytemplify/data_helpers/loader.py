"""Helper loading and discovery utilities for data_helpers."""

import importlib
import importlib.util
import inspect
import logging
from pathlib import Path
from typing import List, Type, Union

from pytemplify.data_helpers.base import DataHelper
from pytemplify.exceptions import HelperLoaderError

logger = logging.getLogger(__name__)


class HelperLoader:
    """Utility class for loading and discovering DataHelper classes."""

    @staticmethod
    def load_helpers_from_string(helper_spec: str) -> List[Type[DataHelper]]:
        """Load helpers from string specification.

        Args:
            helper_spec: String specification in formats:
                - "module.HelperClass" - Single helper class
                - "module.Helper1,module.Helper2" - Multiple helper classes
                - "module.py" - All helpers from module file
                - "module" - All helpers from module

        Returns:
            List of DataHelper classes

        Raises:
            HelperLoaderError: If loading fails
        """
        helpers = []

        # Split by comma for multiple specifications
        specs = [spec.strip() for spec in helper_spec.split(",") if spec.strip()]

        for spec in specs:
            try:
                if "." in spec and not spec.endswith(".py"):
                    # Format: module.ClassName
                    module_name, class_name = spec.rsplit(".", 1)
                    helpers.extend(HelperLoader._load_helper_class(module_name, class_name))
                elif spec.endswith(".py"):
                    # Format: module.py file
                    helpers.extend(HelperLoader._load_helpers_from_file(Path(spec)))
                else:
                    # Format: module name
                    helpers.extend(HelperLoader._load_helpers_from_module(spec))
            except Exception as exc:
                raise HelperLoaderError(f"Failed to load helper from '{spec}': {exc}") from exc

        return helpers

    @staticmethod
    def _load_helper_class(module_name: str, class_name: str) -> List[Type[DataHelper]]:
        """Load specific helper class from module."""
        try:
            module = importlib.import_module(module_name)
            helper_class = getattr(module, class_name)

            if not (inspect.isclass(helper_class) and issubclass(helper_class, DataHelper)):
                raise HelperLoaderError(f"{class_name} is not a DataHelper subclass")

            logger.debug("Loaded helper class: %s.%s", module_name, class_name)
            return [helper_class]
        except ImportError as exc:
            raise HelperLoaderError(f"Cannot import module '{module_name}': {exc}") from exc
        except AttributeError as exc:
            raise HelperLoaderError(f"Class '{class_name}' not found in module '{module_name}': {exc}") from exc

    @staticmethod
    def _load_helpers_from_module(module_name: str) -> List[Type[DataHelper]]:
        """Load all DataHelper classes from module."""
        try:
            module = importlib.import_module(module_name)
            return HelperLoader._extract_helpers_from_module(module, module_name)
        except ImportError as exc:
            raise HelperLoaderError(f"Cannot import module '{module_name}': {exc}") from exc

    @staticmethod
    def _load_helpers_from_file(file_path: Path) -> List[Type[DataHelper]]:
        """Load all DataHelper classes from Python file."""
        if not file_path.exists():
            raise HelperLoaderError(f"Helper file not found: {file_path}")

        if not file_path.suffix == ".py":
            raise HelperLoaderError(f"Helper file must be .py file: {file_path}")

        try:
            # Create module spec and load
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                raise HelperLoaderError(f"Cannot create module spec for {file_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return HelperLoader._extract_helpers_from_module(module, str(file_path))
        except Exception as exc:
            raise HelperLoaderError(f"Failed to load module from {file_path}: {exc}") from exc

    @staticmethod
    def _extract_helpers_from_module(module, module_identifier: str) -> List[Type[DataHelper]]:
        """Extract all DataHelper classes from loaded module."""
        helpers = []

        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isclass(obj) and issubclass(obj, DataHelper) and obj is not DataHelper:  # Exclude base class
                helpers.append(obj)
                logger.debug("Found helper class: %s.%s", module_identifier, name)

        if not helpers:
            logger.warning("No DataHelper classes found in %s", module_identifier)

        return helpers

    @staticmethod
    def discover_helpers(search_paths: List[Union[str, Path]]) -> List[Type[DataHelper]]:
        """Discover DataHelper classes from search paths.

        Args:
            search_paths: List of directory paths to search for Python files

        Returns:
            List of discovered DataHelper classes

        Raises:
            HelperLoaderError: If discovery fails
        """
        helpers = []

        for search_path in search_paths:
            path = Path(search_path)
            if not path.exists():
                logger.warning("Helper search path does not exist: %s", path)
                continue

            if not path.is_dir():
                logger.warning("Helper search path is not a directory: %s", path)
                continue

            try:
                # Find all Python files in directory
                python_files = path.glob("*.py")
                for py_file in python_files:
                    if py_file.name.startswith("__"):
                        continue  # Skip __init__.py, __pycache__, etc.

                    try:
                        file_helpers = HelperLoader._load_helpers_from_file(py_file)
                        helpers.extend(file_helpers)
                    except HelperLoaderError as exc:
                        logger.warning("Skipping %s: %s", py_file, exc)
                        continue

            except Exception as exc:
                raise HelperLoaderError(f"Failed to discover helpers in {path}: {exc}") from exc

        logger.info("Discovered %d helper classes from %d search paths", len(helpers), len(search_paths))
        return helpers

    @staticmethod
    def validate_helpers(helpers: List[Type[DataHelper]], data: dict) -> List[Type[DataHelper]]:
        """Validate that helper classes can be instantiated and work with data.

        Args:
            helpers: List of helper classes to validate
            data: Sample data to test helpers against

        Returns:
            List of valid helper classes
        """
        valid_helpers = []

        for helper_class in helpers:
            try:
                # Test that matches method works
                matches = helper_class.matches(data)
                logger.debug("Helper %s.matches(data) = %s", helper_class.__name__, matches)

                # If it matches, try to instantiate it
                if matches:
                    # Test instantiation
                    helper_class(data)
                    logger.debug("Successfully instantiated %s", helper_class.__name__)

                valid_helpers.append(helper_class)

            except (TypeError, AttributeError, ValueError, RuntimeError) as exc:
                # Helper validation errors - expected during validation
                logger.warning("Helper %s validation failed: %s", helper_class.__name__, exc)
                continue

        return valid_helpers
