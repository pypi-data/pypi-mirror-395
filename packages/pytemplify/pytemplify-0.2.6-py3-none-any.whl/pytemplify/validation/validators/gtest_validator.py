"""
Google Test validator for pytemplify.

This validator discovers C++ test files, builds them in an isolated environment
using pytemplify's CMake templates, runs the tests, and generates coverage reports.

SOLID Principles:
    - SRP: Single responsibility - validate Google Tests
    - OCP: Open for extension through options
    - LSP: Substitutable for BaseValidator
    - DIP: Depends on abstractions (BaseValidator, CMakeTemplateManager)

DRY Principle:
    - Reuses CMakeTemplateManager for CMake rendering
    - Reuses BaseValidator pattern matching logic
"""

import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from pytemplify.validation.base import BaseValidator, ValidationResult
from pytemplify.validation.cmake_manager import CMakeTemplateManager, normalize_path_for_cmake
from pytemplify.validation.project_scanner import ProjectScanner

logger = logging.getLogger(__name__)


@dataclass
class BatchState:
    """State container for batch validation."""

    targets: List[Path] = field(default_factory=list)
    processed: bool = False
    results: Dict[str, ValidationResult] = field(default_factory=dict)


@dataclass
class BatchRunSummary:
    """Aggregated information produced by a batch run."""

    test_results: Dict[str, Dict[str, Any]]
    build_duration: float
    total_duration: float
    coverage_info: Optional[str]
    total_tests: int


class GTestValidator(BaseValidator):
    """
    Validates generated C++ code using Google Test (SOLID: SRP, LSP).

    Responsibilities:
        - Discover test files (test_*.cpp, *_test.cpp)
        - Build tests in isolated environment
        - Run tests with CTest
        - Generate coverage reports
        - Clean up build artifacts

    DRY: Reuses CMakeTemplateManager for CMake template rendering.
    """

    # Default patterns for test file discovery (DRY: single source of truth)
    DEFAULT_TEST_PATTERNS = ["test_*.cpp", "*_test.cpp", "test_*.cc", "*_test.cc"]

    # Default workspace directory name (can be configured via options)
    DEFAULT_WORKSPACE_DIR = ".pytemplify_gtest"

    # Batch mode - simple boolean
    # True: all tests build together in single CMake project
    # False: each test builds independently (default)

    # Profile definitions with sensible defaults
    PROFILES = {
        "basic": {
            "build_type": "Debug",
            "cxx_standard": 17,
            "gtest_version": "release-1.12.1",
            "enable_coverage": False,
            "test_timeout": 300,
            "build_parallel_jobs": "auto",
            "keep_build_artifacts": True,
            "warnings_as_errors": False,
            "compile_definitions": [],  # e.g., ["_UNITTEST", "UNIT_TEST_BUILD"]
            "compile_options": [],
            "link_libraries": [],  # Empty by default (libdl is Linux-specific)
            "disable_windows": False,
            "clean_build": False,  # Use incremental builds for better performance
            "verbose": False,  # Suppress output, show only errors (gwgen2 pattern)
            "batch": False,  # Default: individual test builds (per-test coverage when enabled)
        },
        "coverage": {
            "build_type": "Debug",
            "cxx_standard": 17,
            "gtest_version": "release-1.12.1",
            "enable_coverage": True,
            "test_timeout": 300,
            "build_parallel_jobs": "auto",
            "keep_build_artifacts": True,
            "warnings_as_errors": False,
            "compile_definitions": [],  # e.g., ["_UNITTEST", "UNIT_TEST_BUILD"]
            "compile_options": [],
            "link_libraries": [],  # Empty by default (libdl is Linux-specific)
            "disable_windows": False,
            "clean_build": False,  # Use incremental builds for better performance
            "verbose": False,  # Suppress output, show only errors (gwgen2 pattern)
            "batch": False,  # Default: individual test builds (per-test coverage)
        },
        "strict": {
            "build_type": "Debug",
            "cxx_standard": 17,
            "gtest_version": "release-1.12.1",
            "enable_coverage": True,
            "test_timeout": 300,
            "build_parallel_jobs": "auto",
            "keep_build_artifacts": True,
            "warnings_as_errors": True,
            "compile_definitions": [],  # e.g., ["_UNITTEST", "UNIT_TEST_BUILD"]
            "compile_options": ["-Wall", "-Wextra", "-Wpedantic"],
            "link_libraries": [],  # Empty by default (libdl is Linux-specific)
            "disable_windows": False,
            "clean_build": False,  # Use incremental builds for better performance
            "verbose": False,  # Suppress output, show only errors (gwgen2 pattern)
            "batch": False,  # Default: individual test builds (per-test coverage)
        },
        "custom": {
            # Custom profile allows full control - no defaults set
        },
    }

    def __init__(self, config):
        """
        Initialize Google Test validator with profile-based configuration.

        Args:
            config: ValidatorConfig instance

        Configuration profiles:
            - basic: Minimal configuration, just run tests
            - coverage: Basic + code coverage reports
            - strict: Coverage + warnings as errors + strict compilation
            - custom: Full control over all options

        User options override profile defaults. For example:
            profile: "coverage"
            options:
              timeout: 600  # Only override timeout
        """
        super().__init__(config)
        self._cmake_manager = CMakeTemplateManager()
        self._logger = logging.getLogger(f"{__name__}.GTestValidator")
        self._project_scanner = ProjectScanner()
        self._current_test_config = {}
        self._batch_state = BatchState()

        # Get profile name from config
        # Profile can be in options dict OR as a top-level config attribute
        # Debug: log what we receive
        self._logger.debug("Received config.options: %s", self.config.options)
        self._logger.debug("Hasattr profile: %s", hasattr(self.config, "profile"))

        # Try to get profile from config object first, then from options dict
        if hasattr(self.config, "profile") and self.config.profile:
            profile_name = self.config.profile
        else:
            profile_name = self.config.options.get("profile", "basic")

        # Get profile defaults
        if profile_name not in self.PROFILES:
            raise ValueError(f"Unknown profile '{profile_name}'. Available profiles: {list(self.PROFILES.keys())}")

        profile_defaults = self.PROFILES[profile_name].copy()

        # Merge user options with profile defaults (DON'T mutate config.options!)
        # Store merged options in separate instance variable for runtime use
        self._runtime_options = profile_defaults.copy()

        # User options override profile defaults
        # If user provided nested "options" key, merge those
        if "options" in self.config.options:
            raw_user_options = dict(self.config.options["options"])
        else:
            # Otherwise merge all user options (except "profile")
            raw_user_options = {k: v for k, v in self.config.options.items() if k != "profile"}

        normalized_user_options = self._normalize_and_warn_options(raw_user_options)
        self._runtime_options.update(normalized_user_options)

        # Validate batch option (boolean)
        batch = self._runtime_options.get("batch", False)
        if not isinstance(batch, bool):
            self._logger.warning("Invalid batch value '%s'. Must be true or false. Using false.", batch)
            self._runtime_options["batch"] = False
            batch = False

        # Coverage strategy is automatic based on batch mode:
        # Individual mode (batch=false): per-test coverage
        # Batch mode (batch=true): aggregated coverage
        enable_coverage = self._runtime_options.get("enable_coverage", False)
        coverage_mode = "aggregated" if batch else "per-test"

        # Log final settings
        self._logger.info(
            "Profile: %s, enable_coverage: %s, batch: %s, coverage_mode: %s",
            profile_name,
            enable_coverage,
            batch,
            coverage_mode if enable_coverage else "disabled",
        )

        # Set default patterns if not specified
        if not self.config.patterns:
            self.config.patterns.extend(self.DEFAULT_TEST_PATTERNS)

    def _normalize_and_warn_options(self, user_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize user options, handling common misnamed keys and warning on unsupported ones.

        Returns a new dict to avoid mutating the caller's options.
        """
        options = user_options.copy()

        allowed_keys = {
            # Core settings
            "build_type",
            "cxx_standard",
            "gtest_version",
            "enable_coverage",
            "test_timeout",
            "test_discovery_timeout",
            "build_parallel_jobs",
            "keep_build_artifacts",
            "warnings_as_errors",
            "compile_definitions",
            "compile_options",
            "link_libraries",
            "disable_windows",
            "clean_build",
            "verbose",
            "batch",
            "use_gmock",
            "policy_cmp0135",
            "policy_cmp0105",
            # Structure detection
            "module_name",
            "sut_root_dir",
            "include_dirs",
            "source_patterns",
            "sut_sources",
            # Build tooling
            "cmake_generator",
            # Coverage handling
            "tolerate_coverage_failures",
        }

        unsupported = sorted(key for key in options.keys() if key not in allowed_keys)
        for key in unsupported:
            self._logger.warning("Ignoring unsupported GTest option '%s' in templates.yaml", key)
            options.pop(key, None)

        return options

    def discover(self, output_dir: Path) -> List[Path]:
        """
        Discover test files in the output directory.

        Args:
            output_dir: Directory to search for test files

        Returns:
            List of test file paths
        """
        self._logger.info("Discovering Google Test files in %s", output_dir)

        test_files = []
        for pattern in self.config.patterns:
            # Search recursively for test files
            matches = list(output_dir.rglob(pattern))
            test_files.extend(matches)
            self._logger.debug("Pattern '%s' found %d files", pattern, len(matches))

        # Filter out files in build/validation directories to avoid endless loops
        filtered_files = []
        skip_dir_names = [
            self.DEFAULT_WORKSPACE_DIR,
            "build",
            "_deps",
            "CMakeFiles",
            ".cmake",
            "googletest",
            "pytemplify_validation",  # Legacy name for backward compatibility
        ]
        for file_path in test_files:
            # Check if any parent directory matches our skip list
            skip = False
            for parent in file_path.parents:
                if parent.name in skip_dir_names or parent.name.startswith(".pytemplify"):
                    self._logger.debug("Skipping test file in build/framework directory: %s", file_path)
                    skip = True
                    break
            if not skip:
                filtered_files.append(file_path)

        # Remove duplicates while preserving order
        seen = set()
        unique_files = []
        for file_path in filtered_files:
            if file_path not in seen:
                seen.add(file_path)
                unique_files.append(file_path)

        self._logger.info("Discovered %d test files", len(unique_files))

        # Store targets for batch mode
        batch = self._runtime_options.get("batch", False)
        if batch:
            self._batch_state.targets = unique_files
            self._batch_state.processed = False
            self._batch_state.results = {}

        return unique_files

    def _handle_coverage(self, build_dir: Path, test_name: str, target: Path, start_time: float) -> Optional[str]:
        """
        Handle coverage generation with configurable failure tolerance.

        Args:
            build_dir: Build directory
            test_name: Name of the test
            target: Test file path
            start_time: Validation start time

        Returns:
            Coverage summary string if successful, None otherwise

        Raises:
            ValidationResult: If coverage fails and tolerate_coverage_failures is False
        """
        enable_cov = self._runtime_options.get("enable_coverage", False)
        self._logger.debug("Coverage enabled: %s", enable_cov)
        if not enable_cov:
            return None

        coverage_result = self._generate_coverage(build_dir)
        if coverage_result["success"]:
            return coverage_result.get("summary")

        # Coverage generation failures are warnings by default
        tolerate = self._runtime_options.get("tolerate_coverage_failures", True)
        self._logger.warning("Coverage generation result: %s", coverage_result.get("summary") or "failed")

        if not tolerate:
            duration = time.time() - start_time
            details = coverage_result.get("summary") or "Coverage generation failed"
            result = self._create_failure_result(
                test_name=test_name,
                target=target,
                message="Coverage generation failed",
                details=details,
                duration=duration,
            )
            # Raise the result as an exception to break out of validation flow
            raise RuntimeError(result)

        return None

    def validate(self, target: Path, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate test file(s) - handles both individual and batch modes.

        In batch mode, on the first call it processes all tests together and caches results.
        Subsequent calls return the cached result for that specific test.

        Args:
            target: Test file path
            context: Optional context (can contain 'output_dir' for relative path calculation)

        Returns:
            ValidationResult with test execution results
        """
        batch = self._runtime_options.get("batch", False)

        self._logger.debug(
            "validate() called: batch=%s, processed=%s, targets=%d",
            batch,
            self._batch_state.processed,
            len(self._batch_state.targets),
        )

        # Batch mode: process all tests together on first call
        if batch:
            if not self._batch_state.processed and self._batch_state.targets:
                # First call in batch mode - process all tests
                self._logger.info("Triggering batch mode processing for %d tests", len(self._batch_state.targets))
                self._batch_state.results = self._validate_batch_all(self._batch_state.targets, context)
                self._batch_state.processed = True

            # Return result for this specific test
            test_name = target.stem
            result = self._batch_state.results.get(test_name)
            if result:
                self._logger.debug("Returning cached batch result for %s", test_name)
                return result

            self._logger.error(
                "Test %s not found in batch results! Available: %s",
                test_name,
                list(self._batch_state.results.keys()),
            )
            return self._create_failure_result(
                test_name=test_name,
                target=target,
                message="Test not found in batch results",
                details="Internal error: test was discovered but not processed",
                duration=0.0,
            )

        # Individual mode - original behavior
        self._logger.debug("Running in individual mode")
        return self._validate_individual(target, context)

    def _validate_individual(self, target: Path, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate a single test file in individual mode (original behavior).

        Args:
            target: Test file path
            context: Optional context

        Returns:
            ValidationResult with test execution results
        """
        start_time = time.time()
        test_name = self._runtime_options.get("module_name") or target.stem

        self._logger.info("Validating Google Test: %s", test_name)

        try:
            # Setup isolated build environment
            build_dir = self._setup_isolated_env(target, context)

            # Build and run test
            build_result = self._build_test(build_dir)
            if not build_result["success"]:
                return self._create_failure_result(
                    test_name=test_name,
                    target=target,
                    message="Build failed",
                    details=build_result["output"],
                    duration=time.time() - start_time,
                )

            test_result = self._run_test(build_dir, test_name)
            if not test_result["success"]:
                return self._create_failure_result(
                    test_name=test_name,
                    target=target,
                    message="Test execution failed",
                    details=test_result["output"],
                    duration=time.time() - start_time,
                )

            # Handle coverage generation
            coverage_info = self._handle_coverage(build_dir, test_name, target, start_time)

            # Build success result
            duration = time.time() - start_time
            message = f"Test '{test_name}' passed"
            details = f"Build time: {build_result['duration']:.2f}s, Test time: {test_result['duration']:.2f}s"

            if coverage_info:
                details += f"\nCoverage: {coverage_info}"

            return self.create_success_result(
                target_name=test_name, message=message, details=details, file_path=target, duration_seconds=duration
            )

        except RuntimeError as e:
            # Coverage failure raised as RuntimeError with ValidationResult
            if isinstance(e.args[0], ValidationResult):
                return e.args[0]
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            duration = time.time() - start_time
            self._logger.error("Validation failed for %s: %s", test_name, e)
            return self._create_failure_result(
                test_name=test_name, target=target, message="Validation error", details=str(e), duration=duration
            )

    def _collect_module_test_files(self, test_file: Path) -> List[Path]:
        """
        Collect all test files in the same directory to support module-level builds.

        Uses configured discovery patterns but only within the current directory
        (non-recursive) to avoid pulling in unrelated tests.
        """
        test_dir = test_file.parent
        patterns = self.config.patterns or self.DEFAULT_TEST_PATTERNS

        collected: List[Path] = []
        for pattern in patterns:
            collected.extend(test_dir.glob(pattern))

        # Ensure the primary file is present even if it didn't match a pattern
        collected.append(test_file)

        # Deduplicate and keep deterministic ordering
        unique: List[Path] = []
        seen = set()
        for path in sorted(set(collected)):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                unique.append(resolved)

        return unique

    def _create_batch_test_result(self, target: Path, summary: BatchRunSummary) -> ValidationResult:
        """Create a ValidationResult for a single test in batch mode."""
        test_name = target.stem
        test_passed = summary.test_results.get(test_name, {}).get("success", False)
        duration_per_test = summary.total_duration / summary.total_tests

        if test_passed:
            details = f"Build time: {summary.build_duration:.2f}s, Total batch time: {summary.total_duration:.2f}s"
            if summary.coverage_info:
                details += f"\nAggregated Coverage: {summary.coverage_info}"
            return self.create_success_result(
                target_name=test_name,
                message=f"Test '{test_name}' passed (batch mode)",
                details=details,
                file_path=target,
                duration_seconds=duration_per_test,
            )

        return self._create_failure_result(
            test_name=test_name,
            target=target,
            message="Test execution failed (batch mode)",
            details=summary.test_results.get(test_name, {}).get("output", "No output"),
            duration=duration_per_test,
        )

    def _validate_batch_all(
        self, targets: List[Path], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, ValidationResult]:  # pylint: disable=too-many-locals
        """
        Validate all tests together in batch mode.

        Builds all tests in a single CMake project and runs them with CTest.
        Generates aggregated coverage report if enabled.

        Args:
            targets: List of test file paths
            context: Optional validation context

        Returns:
            Dictionary mapping test names to ValidationResult objects
        """
        start_time = time.time()
        results = {}

        self._logger.info("=" * 60)
        self._logger.info("BATCH MODE: Building and testing %d tests together", len(targets))
        self._logger.info("=" * 60)

        try:
            # Setup batch build environment
            build_dir = self._setup_batch_env(targets, context)

            # Build all tests
            build_result = self._build_test(build_dir)
            if not build_result["success"]:
                # Build failed - mark all tests as failed
                for target in targets:
                    results[target.stem] = self._create_failure_result(
                        test_name=target.stem,
                        target=target,
                        message="Batch build failed",
                        details=build_result["output"],
                        duration=time.time() - start_time,
                    )
                return results

            # Run all tests with CTest
            test_results = self._run_batch_tests(build_dir, targets)

            # Handle coverage - batch mode always uses aggregated coverage
            coverage_info = None
            if self._runtime_options.get("enable_coverage"):
                coverage_info = self._generate_aggregated_coverage(build_dir)

            # Create results for each test
            total_duration = time.time() - start_time
            summary = BatchRunSummary(
                test_results=test_results,
                build_duration=build_result["duration"],
                total_duration=total_duration,
                coverage_info=coverage_info,
                total_tests=len(targets),
            )
            for target in targets:
                results[target.stem] = self._create_batch_test_result(target, summary)

            self._logger.info("=" * 60)
            self._logger.info(
                "BATCH MODE COMPLETE: %d/%d tests passed", sum(1 for r in results.values() if r.success), len(results)
            )
            self._logger.info("=" * 60)

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.error("Batch validation error: %s", e)
            # Mark all tests as failed
            for target in targets:
                results[target.stem] = self._create_failure_result(
                    test_name=target.stem,
                    target=target,
                    message="Batch validation error",
                    details=str(e),
                    duration=time.time() - start_time,
                )

        return results

    def _check_generator_change(self, build_dir: Path, test_config: Dict[str, Any]) -> bool:
        """
        Check if CMake generator has changed and needs a clean build.

        Args:
            build_dir: Build directory path
            test_config: Test configuration with cmake_generator

        Returns:
            True if generator changed and clean build is needed, False otherwise
        """
        cmake_cache = build_dir / "CMakeCache.txt"
        if not cmake_cache.exists() or not test_config.get("cmake_generator"):
            return False

        try:
            cache_content = cmake_cache.read_text(encoding="utf-8")
            # Look for CMAKE_GENERATOR:INTERNAL=<generator> in cache
            for line in cache_content.splitlines():
                if line.startswith("CMAKE_GENERATOR:INTERNAL="):
                    cached_generator = line.split("=", 1)[1]
                    current_generator = test_config.get("cmake_generator")
                    if cached_generator != current_generator:
                        self._logger.info(
                            "CMake generator changed from '%s' to '%s' - forcing clean build",
                            cached_generator,
                            current_generator,
                        )
                        return True
                    break
        except (OSError, UnicodeDecodeError) as e:
            self._logger.debug("Could not read CMakeCache.txt: %s", e)

        return False

    def _resolve_source_pattern(self, name: str, path: str) -> str:
        """
        Resolve a source pattern to actual file names.

        Args:
            name: Pattern name (e.g., "STUB", "COMMON")
            path: File path or glob pattern

        Returns:
            Formatted string showing resolved files
        """
        pattern_path = Path(path)
        if "*" not in path:
            # Direct file reference
            return f"{name}: {pattern_path.name}"

        # It's a glob pattern - expand it
        parent = pattern_path.parent
        glob_pattern = pattern_path.name
        if not parent.exists():
            return f"{name}: {path} (parent dir not found)"

        matched_files = sorted(parent.glob(glob_pattern))
        if matched_files:
            files_str = ", ".join(f.name for f in matched_files)
            return f"{name}: {files_str}"

        return f"{name}: {path} (no matches)"

    def _get_include_dir_label(self, include_path: str, index: int, total_dirs: int) -> str:
        """
        Determine label for include directory based on its path.

        Args:
            include_path: Path to the include directory
            index: Index of this directory (0-based)
            total_dirs: Total number of include directories

        Returns:
            Label string (e.g., "STUB", "COMMON STUB", "SUT ROOT")
        """
        path_lower = include_path.lower()
        if "stub" in path_lower and "common" not in path_lower:
            return "STUB"
        if "common" in path_lower:
            return "COMMON STUB"
        # Last two are typically SUT root directories
        if index >= total_dirs - 2:
            return "SUT ROOT"
        return "INCLUDE"

    def _log_test_configuration(self, test_config: Dict[str, Any]) -> None:
        """
        Log test configuration details in verbose mode.

        Args:
            test_config: Test configuration dictionary
        """
        if not self._runtime_options.get("verbose", False):
            return

        # Log include directories in formatted multi-line output
        include_dirs = test_config.get("include_dirs", [])
        if include_dirs:
            self._logger.info("Include directories (available to SUT, stubs, and test files):")
            for idx, inc_dir in enumerate(include_dirs):
                label = self._get_include_dir_label(inc_dir, idx, len(include_dirs))
                self._logger.info("  [%d] [%-13s] %s", idx + 1, label, inc_dir)

        # Log source files in formatted multi-line output
        source_patterns = test_config.get("source_patterns", [])
        if source_patterns:
            self._logger.info("Source files to link (object files for test binary):")
            idx = 1
            for pattern in source_patterns:
                if isinstance(pattern, dict):
                    name = pattern.get("name", "UNKNOWN")
                    path = pattern.get("path", "")
                    resolved = self._resolve_source_pattern(name, path)
                    # Extract just the file names from resolved string
                    if ":" in resolved:
                        _, files = resolved.split(":", 1)
                        files = files.strip()
                        self._logger.info("  [%d] [%-13s] %s", idx, name, files)
                        idx += 1
                else:
                    self._logger.info("  [%d] [%-13s] %s", idx, "UNKNOWN", str(pattern))
                    idx += 1

    def _find_git_root(self, reference_path: Path) -> Path:
        """
        Find the root of the git repository by traversing up from the start path.

        This is inspired by gwgen2's find_git_root() utility function.

        Args:
            reference_path: Starting path (typically a test file or output directory)

        Returns:
            Path to git root, or the resolved reference_path if not in a git repo
        """
        path = reference_path.resolve()
        while path != path.parent:
            if (path / ".git").is_dir():
                self._logger.debug("Found git root at: %s", path)
                return path
            path = path.parent

        # Not in a git repository - return resolved reference path as fallback
        self._logger.debug("No git root found, using reference path: %s", reference_path.resolve())
        return reference_path.resolve()

    def _setup_isolated_env(self, test_file: Path, _context: Optional[Dict[str, Any]]) -> Path:
        """
        Setup isolated build environment for the test.

        Creates directory structure in workspace (auto-detected from git root):
            <git_root>/.pytemplify_gtest/<test_name>/
                CMakeLists.txt (rendered from template)
                build/ (CMake build directory)

        If not in a git repository, uses the test file's directory as workspace base.

        Args:
            test_file: Path to test file
            _context: Optional context (reserved for future use)

        Returns:
            Path to build directory

        Raises:
            RuntimeError: If environment setup fails
        """
        test_dir = test_file.parent
        git_root = self._find_git_root(test_dir)

        # Use module name when provided so all module-level test files share the same build folder
        module_name = self._runtime_options.get("module_name")
        target_name = module_name or test_file.stem

        workspace_base = git_root if git_root != test_dir.resolve() else test_dir
        self._logger.debug("Using workspace base: %s", workspace_base)

        isolated_dir = workspace_base / self.DEFAULT_WORKSPACE_DIR / target_name
        build_dir = isolated_dir / "build"
        self._logger.debug("Setting up isolated environment: %s", isolated_dir)

        module_test_files: List[Path] = []
        if module_name:
            module_test_files = self._collect_module_test_files(test_file)
            self._logger.debug(
                "Module mode enabled (%s): found %d test files in %s",
                module_name,
                len(module_test_files),
                test_dir,
            )

        config_options = self._auto_detect_project_structure(test_file, module_test_files or None)
        test_config = self._cmake_manager.create_test_config(test_file.parent, config_options, test_file)

        force_clean = self._check_generator_change(build_dir, test_config)
        if self._runtime_options.get("clean_build", True) or force_clean:
            if build_dir.exists():
                self._logger.debug(
                    "Cleaning existing build directory (%s): %s",
                    "generator changed" if force_clean else "clean_build enabled",
                    build_dir,
                )
                shutil.rmtree(build_dir)

        isolated_dir.mkdir(parents=True, exist_ok=True)
        build_dir.mkdir(parents=True, exist_ok=True)

        self._current_test_config = test_config

        cmake_path = isolated_dir / "CMakeLists.txt"
        self._cmake_manager.render_cmake_file(
            test_name=target_name,
            test_file=test_file.absolute(),
            test_files=module_test_files,
            output_path=cmake_path,
            **test_config,
        )

        self._log_test_configuration(test_config)
        self._logger.debug("Isolated environment ready: %s", build_dir)
        return build_dir

    def _auto_detect_project_structure(
        self, test_file: Path, module_test_files: Optional[List[Path]] = None
    ) -> Dict[str, Any]:
        """
        Auto-detect source files and include directories if not manually specified.

        Args:
            test_file: Path to the test file
            module_test_files: Optional list of module-level test files (module_name enabled)

        Returns:
            Updated configuration options with auto-detected values (with absolute paths)
        """
        config_options = self._runtime_options.copy()

        # Only scan once and cache results to avoid infinite loops
        # NOTE: ProjectScanner is kept for backward compatibility and finds SUT files.
        # cmake_manager's auto-detection is more robust for complex nested structures (stubs, common, etc.)
        # We store ProjectScanner results as "sut_sources" and let cmake_manager merge them with stubs.
        if not config_options.get("source_patterns"):
            self._logger.debug("Auto-detecting project structure for %s", test_file.name)
            scan_results = self._project_scanner.scan_project(test_file)

            # Get project root to convert relative paths to absolute
            test_dir = test_file.parent
            project_root = self._project_scanner.find_project_root(test_dir, 3)

            # Store ProjectScanner SUT sources for cmake_manager to merge with stubs
            if scan_results["sources"]:
                # Convert to absolute paths for the format expected by CMake template
                sut_sources = [
                    {"name": f"SRC{i}", "path": str((project_root / src).absolute())}
                    for i, src in enumerate(scan_results["sources"])
                ]
                # Store as "sut_sources" instead of "source_patterns" to allow cmake_manager to merge
                config_options["sut_sources"] = sut_sources
                self._logger.debug("ProjectScanner found %d SUT source files", len(scan_results["sources"]))
            else:
                # ProjectScanner found nothing - cmake_manager will handle everything
                self._logger.debug("ProjectScanner found no sources, deferring to cmake_manager auto-detection")

            # Default coverage root to detected project root when available, sources found, and not set
            # Only set if we actually found sources - otherwise let cmake_manager auto-detect from headers
            if project_root and scan_results["sources"] and not config_options.get("sut_root_dir"):
                config_options["sut_root_dir"] = str(project_root.resolve())
                self._logger.debug("Auto-set sut_root_dir to project root: %s", config_options["sut_root_dir"])

        # Module mode: ensure sibling SUT sources are included so all module test files link correctly
        if module_test_files:
            test_dir = test_file.parent
            sut_dir = test_dir.parent
            module_sources = []
            for cpp_file in sorted(sut_dir.glob("*.cpp")):
                # Skip test/stub files
                if cpp_file.name.startswith("test_") or cpp_file.name.endswith("_test.cpp"):
                    continue
                module_sources.append(cpp_file)

            if module_sources:
                existing_paths = {Path(src["path"]).resolve() for src in config_options.get("sut_sources", [])}
                for idx, cpp_file in enumerate(module_sources):
                    resolved = cpp_file.resolve()
                    if resolved in existing_paths:
                        continue
                    config_options.setdefault("sut_sources", []).append(
                        {"name": f"MODULE_SRC{idx}", "path": str(resolved)}
                    )
                self._logger.debug("Module mode detected %d sibling SUT sources in %s", len(module_sources), sut_dir)

            # Prefer the module SUT directory as coverage root in module mode
            config_options["sut_root_dir"] = str(sut_dir.resolve())
            self._logger.debug("Module mode set sut_root_dir to %s", config_options["sut_root_dir"])

        # IMPORTANT: Always defer include directory detection to cmake_manager
        # cmake_manager has superior auto-detection for nested structures (stubs/, ../common/, etc.)
        # and is the source of truth for include paths
        if not config_options.get("include_dirs"):
            self._logger.debug("Deferring include directory detection to cmake_manager")

        return config_options

    def _setup_batch_env(self, test_files: List[Path], _context: Optional[Dict[str, Any]]) -> Path:
        """
        Setup batch build environment for multiple tests.

        Creates directory structure in workspace:
            <git_root>/.pytemplify_gtest/_batch_all/
                CMakeLists.txt (rendered from batch template)
                build/ (CMake build directory)

        Args:
            test_files: List of test file paths
            _context: Optional context (reserved for future use)

        Returns:
            Path to build directory

        Raises:
            RuntimeError: If environment setup fails
        """
        # Use first test file to find git root
        git_root = self._find_git_root(test_files[0].parent)
        workspace_base = git_root

        # Create batch workspace
        batch_dir = workspace_base / self.DEFAULT_WORKSPACE_DIR / "_batch_all"
        build_dir = batch_dir / "build"

        self._logger.info("Setting up batch environment: %s", batch_dir)

        # Clean if configured
        if self._runtime_options.get("clean_build", False):
            if build_dir.exists():
                self._logger.debug("Cleaning existing batch build directory")
                shutil.rmtree(build_dir)

        # Create directories
        batch_dir.mkdir(parents=True, exist_ok=True)
        build_dir.mkdir(parents=True, exist_ok=True)

        # Prepare test configurations for batch template
        tests_config = []
        all_include_dirs = set()

        for test_file in test_files:
            test_name = test_file.stem

            # Auto-detect project structure for this test
            config_options = self._auto_detect_project_structure(test_file)
            test_config = self._cmake_manager.create_test_config(test_file.parent, config_options, test_file)

            # Collect include directories
            normalized_includes = [normalize_path_for_cmake(inc) for inc in test_config.get("include_dirs", [])]
            if normalized_includes:
                all_include_dirs.update(normalized_includes)

            normalized_sources = [
                {**pattern, "path": normalize_path_for_cmake(pattern["path"])}
                for pattern in test_config.get("source_patterns", [])
            ]

            tests_config.append(
                {
                    "name": test_name,
                    "test_file": normalize_path_for_cmake(test_file.absolute()),
                    "source_patterns": normalized_sources,
                    "include_dirs": normalized_includes,
                }
            )

        # Store config for _build_test
        self._current_test_config = self._runtime_options.copy()
        self._current_test_config["tests"] = tests_config
        self._current_test_config["global_include_dirs"] = sorted(all_include_dirs)

        # Render batch CMakeLists.txt
        cmake_path = batch_dir / "CMakeLists.txt"
        self._render_batch_cmake(cmake_path, tests_config, sorted(all_include_dirs))

        self._logger.info("Batch environment ready with %d tests", len(tests_config))
        return build_dir

    def _render_batch_cmake(
        self, output_path: Path, tests_config: List[Dict[str, Any]], global_include_dirs: List[str]
    ) -> None:
        """
        Render batch CMakeLists.txt from template.

        Args:
            output_path: Path to output CMakeLists.txt
            tests_config: List of test configurations
            global_include_dirs: Common include directories for all tests
        """
        from jinja2 import Environment, FileSystemLoader  # pylint: disable=import-outside-toplevel

        # Get template directory
        template_dir = Path(__file__).parent.parent / "templates" / "gtest"

        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template("CMakeLists_batch.txt.j2")

        # Render template with batch configuration
        context = self._runtime_options.copy()
        context["extra_compile_options"] = context.get("compile_options", [])
        context["tests"] = tests_config
        context["global_include_dirs"] = [normalize_path_for_cmake(path) for path in global_include_dirs]

        # Set SUT root directory for coverage - use the parent of the first test file
        # This ensures coverage reports include the actual source files
        if tests_config and len(tests_config) > 0:
            first_test_dir = Path(tests_config[0]["test_file"]).parent.parent
            context["sut_root_dir"] = normalize_path_for_cmake(first_test_dir.absolute())
            self._logger.debug("Set sut_root_dir for coverage: %s", context["sut_root_dir"])

        rendered = template.render(**context)

        # Write to file
        output_path.write_text(rendered, encoding="utf-8")
        self._logger.debug("Rendered batch CMakeLists.txt: %s", output_path)

    def _run_batch_tests(self, build_dir: Path, targets: List[Path]) -> Dict[str, Dict[str, Any]]:
        """
        Run all tests in batch mode using CTest.

        Args:
            build_dir: Build directory
            targets: List of test file paths

        Returns:
            Dictionary mapping test names to their results
        """
        self._logger.info("Running batch tests with CTest")
        results = {}

        try:
            # Run CTest with verbose output to see individual test results
            test_cmd = ["ctest", "--output-on-failure", "--verbose"]
            self._logger.info("Running: %s", " ".join(test_cmd))

            verbose = self._runtime_options.get("verbose", False)
            if verbose:
                test_result = subprocess.run(
                    test_cmd,
                    cwd=build_dir,
                    timeout=self._runtime_options.get("test_timeout", 600),
                    check=False,
                )
                # In verbose mode, parse from stdout (already displayed)
                output = "(see output above)"
            else:
                test_result = subprocess.run(
                    test_cmd,
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                    timeout=self._runtime_options.get("test_timeout", 600),
                    check=False,
                )
                output = test_result.stdout

            # Parse CTest output to determine individual test results
            # CTest returns 0 if all tests pass
            if test_result.returncode == 0:
                # All tests passed
                for target in targets:
                    test_name = target.stem
                    results[test_name] = {"success": True, "output": "Test passed"}
                    self._logger.info("  ✓ %s passed", test_name)
            else:
                # Some tests failed - parse output to determine which ones
                results = self._parse_ctest_output(output, targets)

        except subprocess.TimeoutExpired:
            self._logger.error("Batch test execution timed out")
            for target in targets:
                test_name = target.stem
                results[test_name] = {"success": False, "output": "Test execution timed out"}
        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.error("Batch test execution error: %s", e)
            for target in targets:
                test_name = target.stem
                results[test_name] = {"success": False, "output": f"Test execution error: {str(e)}"}

        return results

    def _parse_ctest_output(self, output: str, targets: List[Path]) -> Dict[str, Dict[str, Any]]:
        """
        Parse CTest output to determine individual test results.

        Args:
            output: CTest output text
            targets: List of test file paths

        Returns:
            Dictionary mapping test names to their results
        """
        results = {}

        # Initialize all tests as passed (will override if we find failures)
        for target in targets:
            test_name = target.stem
            results[test_name] = {"success": True, "output": "Test passed"}

        # Parse CTest output for test results
        # CTest format: "1/3 Test #1: test_name ...................   Passed    0.01 sec"
        # or:           "1/3 Test #1: test_name ...................***Failed    0.01 sec"
        for line in output.split("\n"):
            if "***Failed" in line or "***Timeout" in line:
                # Extract test name from line
                # Format: "1/3 Test #1: test_name ..."
                parts = line.split(":")
                if len(parts) >= 2:
                    test_name_part = parts[1].strip().split()[0]  # Get first word after colon
                    # Find matching test
                    for target in targets:
                        if target.stem == test_name_part:
                            results[test_name_part] = {"success": False, "output": f"Test failed: {line.strip()}"}
                            self._logger.error("  ✗ %s failed", test_name_part)
                            break
            elif "Passed" in line and "Test #" in line:
                # Extract test name for passed tests
                parts = line.split(":")
                if len(parts) >= 2:
                    test_name_part = parts[1].strip().split()[0]
                    for target in targets:
                        if target.stem == test_name_part:
                            self._logger.info("  ✓ %s passed", test_name_part)
                            break

        return results

    def _generate_aggregated_coverage(self, build_dir: Path) -> Optional[str]:
        """
        Generate aggregated coverage report for all tests.

        Args:
            build_dir: Build directory

        Returns:
            Coverage summary string if successful, None otherwise
        """
        self._logger.info("Generating aggregated coverage report")

        try:
            # Check for coverage tools
            has_gcovr = shutil.which("gcovr") is not None
            has_lcov = shutil.which("lcov") is not None

            if not has_gcovr and not has_lcov:
                self._logger.warning("No coverage tool found (gcovr or lcov)")
                return None

            # Use gcovr if available (cross-platform), otherwise use lcov
            if has_gcovr:
                return self._generate_aggregated_coverage_gcovr(build_dir)
            return self._generate_aggregated_coverage_lcov(build_dir)

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("Aggregated coverage generation error: %s", e)
            return None

    def _generate_aggregated_coverage_gcovr(self, build_dir: Path) -> Optional[str]:
        """
        Generate aggregated coverage report using gcovr.

        Args:
            build_dir: Build directory

        Returns:
            Coverage summary string if successful, None otherwise
        """
        try:
            # Run the aggregated gcovr coverage target
            coverage_cmd = ["cmake", "--build", ".", "--target", "aggregated_coverage_gcovr"]
            self._logger.debug("Running: %s", " ".join(coverage_cmd))

            coverage_result = subprocess.run(
                coverage_cmd, cwd=build_dir, capture_output=True, text=True, timeout=600, check=False
            )

            if coverage_result.returncode != 0:
                self._logger.warning("Aggregated gcovr coverage generation failed")
                return None

            # Extract coverage summary
            coverage_summary = self._parse_gcovr_output(coverage_result.stdout)

            report_path = build_dir / "aggregated_coverage_gcovr" / "index.html"
            report_url = str(report_path).replace("\\", "/")
            self._logger.info("Aggregated coverage report: file://%s", report_url)

            return coverage_summary

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("Aggregated gcovr coverage error: %s", e)
            return None

    def _generate_aggregated_coverage_lcov(self, build_dir: Path) -> Optional[str]:
        """
        Generate aggregated coverage report using lcov.

        Args:
            build_dir: Build directory

        Returns:
            Coverage summary string if successful, None otherwise
        """
        try:
            # Run the aggregated lcov coverage target
            coverage_cmd = ["cmake", "--build", ".", "--target", "aggregated_coverage_lcov"]
            self._logger.debug("Running: %s", " ".join(coverage_cmd))

            coverage_result = subprocess.run(
                coverage_cmd, cwd=build_dir, capture_output=True, text=True, timeout=600, check=False
            )

            if coverage_result.returncode != 0:
                self._logger.warning("Aggregated lcov coverage generation failed")
                return None

            # Extract coverage summary
            coverage_summary = self._parse_lcov_output(coverage_result.stdout)

            report_path = build_dir / "aggregated_coverage_lcov" / "index.html"
            report_url = str(report_path).replace("\\", "/")
            self._logger.info("Aggregated coverage report: file://%s", report_url)

            return coverage_summary

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("Aggregated lcov coverage error: %s", e)
            return None

    def _build_test(self, build_dir: Path) -> Dict[str, Any]:  # pylint: disable=too-many-branches
        """
        Build the test using CMake.

        Args:
            build_dir: CMake build directory

        Returns:
            Dictionary with 'success', 'output', 'duration'
        """
        self._logger.info("Building test in %s", build_dir)
        start_time = time.time()

        try:
            # Configure with CMake
            configure_cmd = ["cmake", ".."]

            # Add generator if specified (e.g., "MinGW Makefiles" for Windows MinGW)
            cmake_generator = self._current_test_config.get("cmake_generator")
            if cmake_generator:
                configure_cmd.extend(["-G", cmake_generator])
                self._logger.debug("Using CMake generator: %s", cmake_generator)

            self._logger.info("Running CMake configure: %s", " ".join(configure_cmd))

            # Conditional output capture based on verbose flag (gwgen2 pattern)
            verbose = self._runtime_options.get("verbose", False)
            if verbose:
                # Verbose mode: stream output to console in real-time
                configure_result = subprocess.run(
                    configure_cmd,
                    cwd=build_dir,
                    timeout=min(self._runtime_options.get("test_timeout", 300), 120),
                    check=False,
                )
            else:
                # Non-verbose mode: capture output and only show on error
                configure_result = subprocess.run(
                    configure_cmd,
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                    timeout=min(self._runtime_options.get("test_timeout", 300), 120),
                    check=False,
                )

            if configure_result.returncode != 0:
                self._logger.error("CMake configure failed with exit code %d", configure_result.returncode)
                # Show error output in non-verbose mode
                if not verbose and configure_result.stderr:
                    self._logger.error("CMake errors:\n%s", configure_result.stderr)
                return {
                    "success": False,
                    "output": f"CMake configure failed (exit code {configure_result.returncode})",
                    "duration": time.time() - start_time,
                }

            # Build with make/ninja
            parallel_jobs = self._runtime_options.get("build_parallel_jobs", "auto")
            if parallel_jobs == "auto":
                parallel_jobs = min(os.cpu_count() or 1, 4)  # Limit to 4 jobs max

            build_cmd = ["cmake", "--build", ".", "--parallel", str(parallel_jobs)]
            self._logger.info("Running CMake build: %s", " ".join(build_cmd))

            # Conditional output capture based on verbose flag (gwgen2 pattern)
            if verbose:
                # Verbose mode: stream output to console in real-time
                build_result = subprocess.run(
                    build_cmd,
                    cwd=build_dir,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )
            else:
                # Non-verbose mode: capture output and only show on error
                build_result = subprocess.run(
                    build_cmd,
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )

            duration = time.time() - start_time

            if build_result.returncode != 0:
                self._logger.error("Build failed with exit code %d", build_result.returncode)
                # Show error output in non-verbose mode
                if not verbose:
                    # Show last 20 lines of build output for errors
                    if build_result.stderr:
                        stderr_lines = build_result.stderr.strip().split("\n")[-20:]
                        self._logger.error("Build errors:\n%s", "\n".join(stderr_lines))
                    if build_result.stdout:
                        stdout_lines = build_result.stdout.strip().split("\n")[-20:]
                        self._logger.error("Build output:\n%s", "\n".join(stdout_lines))
                return {
                    "success": False,
                    "output": f"Build failed (exit code {build_result.returncode})",
                    "duration": duration,
                }

            self._logger.info("Build successful (%.2fs)", duration)
            return {"success": True, "output": "Build successful", "duration": duration}

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Build timed out",
                "duration": time.time() - start_time,
            }
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {
                "success": False,
                "output": f"Build error: {str(e)}",
                "duration": time.time() - start_time,
            }

    def _run_test(self, build_dir: Path, test_name: str) -> Dict[str, Any]:
        """
        Run the test using CTest with fallback to direct execution.

        Implements gwgen2-inspired robust execution with CTest fallback.

        Args:
            build_dir: CMake build directory
            test_name: Name of the test

        Returns:
            Dictionary with 'success', 'output', 'duration'
        """
        self._logger.info("Running test: %s", test_name)
        start_time = time.time()

        try:
            # Run with CTest for better output formatting
            test_cmd = ["ctest", "--output-on-failure", "--verbose"]
            self._logger.info("Running GTest: %s", " ".join(test_cmd))

            # Conditional output capture based on verbose flag (gwgen2 pattern)
            verbose = self._runtime_options.get("verbose", False)
            if verbose:
                # Verbose mode: stream output to console in real-time
                test_result = subprocess.run(
                    test_cmd,
                    cwd=build_dir,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )
            else:
                # Non-verbose mode: capture output and only show on failure
                test_result = subprocess.run(
                    test_cmd,
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )

            duration = time.time() - start_time

            # CTest returns 0 if all tests pass
            success = test_result.returncode == 0

            if success:
                self._logger.info("✓ Test %s passed (%.2fs)", test_name, duration)
            else:
                self._logger.error("✗ Test %s failed (%.2fs)", test_name, duration)
                # Show test failure output in non-verbose mode
                if not verbose and hasattr(test_result, "stdout") and test_result.stdout:
                    # Show only the relevant test failure output
                    output_lines = test_result.stdout.strip().split("\n")[-30:]  # Last 30 lines
                    self._logger.error("Test failure output:\n%s", "\n".join(output_lines))

            return {"success": success, "output": "Test output shown above", "duration": duration}

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Test execution timed out",
                "duration": time.time() - start_time,
            }
        except FileNotFoundError:
            # CTest not found - try direct execution (gwgen2 fallback pattern)
            self._logger.warning("CTest not found, trying direct execution")
            return self._run_test_direct(build_dir, test_name, start_time)
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {
                "success": False,
                "output": f"Test execution error: {str(e)}",
                "duration": time.time() - start_time,
            }

    def _run_test_direct(self, build_dir: Path, test_name: str, start_time: float) -> Dict[str, Any]:
        """
        Run test executable directly (fallback when CTest unavailable).

        Inspired by gwgen2's robust execution approach.

        Args:
            build_dir: CMake build directory
            test_name: Name of the test
            start_time: Test start time

        Returns:
            Dictionary with 'success', 'output', 'duration'
        """
        try:
            # Find the test executable
            test_executable = build_dir / test_name
            if not test_executable.exists():
                # Try common variations
                for variant in [f"test_{test_name}", f"{test_name}_test"]:
                    candidate = build_dir / variant
                    if candidate.exists() and os.access(candidate, os.X_OK):
                        test_executable = candidate
                        break

            if not test_executable.exists():
                return {
                    "success": False,
                    "output": f"Test executable not found: {test_executable}",
                    "duration": time.time() - start_time,
                }

            # Conditional output capture based on verbose flag (gwgen2 pattern)
            verbose = self._runtime_options.get("verbose", False)
            if verbose:
                # Verbose mode: stream output to console in real-time
                test_result = subprocess.run(
                    [str(test_executable)],
                    cwd=build_dir,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )
            else:
                # Non-verbose mode: capture output and only show on failure
                test_result = subprocess.run(
                    [str(test_executable)],
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                    timeout=self._runtime_options.get("test_timeout", 300),
                    check=False,
                )

            duration = time.time() - start_time
            success = test_result.returncode == 0

            # Show failure output in non-verbose mode
            if not success and not verbose and hasattr(test_result, "stdout") and test_result.stdout:
                output_lines = test_result.stdout.strip().split("\n")[-30:]
                self._logger.error("Test failure output:\n%s", "\n".join(output_lines))

            return {"success": success, "output": "Test output shown above", "duration": duration}

        except Exception as e:  # pylint: disable=broad-exception-caught
            return {
                "success": False,
                "output": f"Direct execution error: {str(e)}",
                "duration": time.time() - start_time,
            }

    def _generate_coverage(self, build_dir: Path) -> Dict[str, Any]:
        """
        Generate code coverage report using gcovr (cross-platform) or lcov (Linux/macOS).

        Prefers gcovr for Windows compatibility. Falls back to lcov on Unix-like systems.

        Args:
            build_dir: CMake build directory

        Returns:
            Dictionary with 'success', 'summary', 'report_path'
        """
        self._logger.info("Generating coverage report")

        try:
            # Check for coverage tools (cross-platform using shutil.which)
            has_gcovr = shutil.which("gcovr") is not None
            has_lcov = shutil.which("lcov") is not None

            if not has_gcovr and not has_lcov:
                self._logger.warning("No coverage tool found (gcovr or lcov), skipping coverage generation")
                return {"success": False, "summary": "No coverage tool available (install gcovr or lcov)"}

            # Use gcovr if available (cross-platform), otherwise use lcov
            if has_gcovr:
                return self._generate_coverage_gcovr(build_dir)
            return self._generate_coverage_lcov(build_dir)

        except subprocess.TimeoutExpired:
            return {"success": False, "summary": "Coverage generation timed out"}
        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("Coverage generation error: %s", e)
            return {"success": False, "summary": str(e)}

    def _generate_coverage_gcovr(self, build_dir: Path) -> Dict[str, Any]:
        """
        Generate coverage report using gcovr (cross-platform, Python-based).

        Args:
            build_dir: CMake build directory

        Returns:
            Dictionary with 'success', 'summary', 'report_path'
        """
        self._logger.debug("Using gcovr for coverage generation")

        try:
            # Run the gcovr coverage target (defined in CMakeLists.txt.j2)
            coverage_cmd = ["cmake", "--build", ".", "--target", "test_coverage_gcovr"]
            self._logger.debug("Running: %s", " ".join(coverage_cmd))

            coverage_result = subprocess.run(
                coverage_cmd, cwd=build_dir, capture_output=True, text=True, timeout=300, check=False
            )

            if coverage_result.returncode != 0:
                self._logger.warning("gcovr coverage generation failed: %s", coverage_result.stderr)
                return {"success": False, "summary": "gcovr coverage generation failed"}

            # Extract coverage summary from gcovr output
            coverage_summary = self._parse_gcovr_output(coverage_result.stdout)

            report_path = build_dir / "coverage_report_gcovr" / "index.html"
            # Convert to forward slashes for valid file:// URL (works on all platforms)
            report_url = str(report_path).replace("\\", "/")
            self._logger.info("Coverage report generated: file://%s", report_url)

            return {"success": True, "summary": coverage_summary, "report_path": str(report_path)}

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("gcovr coverage generation error: %s", e)
            return {"success": False, "summary": str(e)}

    def _generate_coverage_lcov(self, build_dir: Path) -> Dict[str, Any]:
        """
        Generate coverage report using lcov (Linux/macOS).

        Args:
            build_dir: CMake build directory

        Returns:
            Dictionary with 'success', 'summary', 'report_path'
        """
        self._logger.debug("Using lcov for coverage generation")

        try:
            # Run the lcov coverage target (defined in CMakeLists.txt.j2)
            coverage_cmd = ["cmake", "--build", ".", "--target", "test_coverage_lcov"]
            self._logger.debug("Running: %s", " ".join(coverage_cmd))

            coverage_result = subprocess.run(
                coverage_cmd, cwd=build_dir, capture_output=True, text=True, timeout=300, check=False
            )

            if coverage_result.returncode != 0:
                self._logger.warning("lcov coverage generation failed: %s", coverage_result.stderr)
                return {"success": False, "summary": "lcov coverage generation failed"}

            # Extract coverage summary from lcov output
            coverage_summary = self._parse_lcov_output(coverage_result.stdout)

            report_path = build_dir / "coverage_report_lcov" / "index.html"
            # Convert to forward slashes for valid file:// URL (works on all platforms)
            report_url = str(report_path).replace("\\", "/")
            self._logger.info("Coverage report generated: file://%s", report_url)

            return {"success": True, "summary": coverage_summary, "report_path": str(report_path)}

        except Exception as e:  # pylint: disable=broad-exception-caught
            self._logger.warning("lcov coverage generation error: %s", e)
            return {"success": False, "summary": str(e)}

    def _parse_lcov_output(self, output: str) -> str:
        """
        Parse lcov output to extract coverage summary.

        Args:
            output: lcov command output

        Returns:
            Coverage summary string (e.g., "Lines: 85.3%, Functions: 92.1%")
        """
        lines_coverage = None
        functions_coverage = None

        for line in output.split("\n"):
            if "lines......" in line:
                # Extract percentage from line like: "  lines......: 85.3% (123 of 144 lines)"
                parts = line.split(":")
                if len(parts) >= 2:
                    lines_coverage = parts[1].strip().split()[0]
            elif "functions.." in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    functions_coverage = parts[1].strip().split()[0]

        if lines_coverage and functions_coverage:
            return f"Lines: {lines_coverage}, Functions: {functions_coverage}"
        if lines_coverage:
            return f"Lines: {lines_coverage}"
        return "Coverage data not available"

    def _parse_gcovr_output(self, output: str) -> str:
        """
        Parse gcovr output to extract coverage summary.

        Args:
            output: gcovr command output

        Returns:
            Coverage summary string (e.g., "Lines: 85.3%, Functions: 92.1%")
        """
        lines_coverage = None
        functions_coverage = None
        branches_coverage = None

        for line in output.split("\n"):
            # Look for lines like: "lines: 85.3% (123 of 144)"
            # This is the format from --print-summary
            if line.strip().startswith("lines:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    lines_coverage = parts[1].strip().split()[0]
            # Look for functions coverage
            elif line.strip().startswith("functions:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    functions_coverage = parts[1].strip().split()[0]
            # Look for branches coverage
            elif line.strip().startswith("branches:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    branches_coverage = parts[1].strip().split()[0]

        # Build coverage summary string
        coverage_parts = []
        if lines_coverage:
            coverage_parts.append(f"{lines_coverage}")
        if functions_coverage:
            coverage_parts.append(f"Functions: {functions_coverage}")
        if branches_coverage and branches_coverage != "0.0%":
            coverage_parts.append(f"Branches: {branches_coverage}")

        if coverage_parts:
            return ", ".join(coverage_parts)
        return "Coverage data not available"

    def cleanup(self, output_dir: Path) -> None:
        """
        Clean up validation artifacts.

        This is the public interface for cleanup (implements BaseValidator abstract method).
        Respects the keep_build_artifacts configuration option.

        Uses git root detection to find workspace location (gwgen2 pattern).

        Args:
            output_dir: Directory where validation was run (used to detect git root)
        """
        # Only clean up if keep_build_artifacts is False
        if not self._runtime_options.get("keep_build_artifacts", True):
            # Auto-detect workspace location using git root (same logic as setup)
            git_root = self._find_git_root(output_dir)

            # Determine workspace base (same logic as setup)
            if git_root == output_dir.resolve():
                # Not in a git repo - use output_dir itself as workspace base
                workspace_base = output_dir
            else:
                # In a git repo - use git root as workspace base
                workspace_base = git_root

            # Clean up workspace
            workspace_path = workspace_base / self.DEFAULT_WORKSPACE_DIR
            if workspace_path.exists():
                self._cleanup(workspace_path)

    def _cleanup(self, isolated_dir: Path) -> None:
        """
        Clean up isolated build environment.

        Args:
            isolated_dir: Isolated environment directory to remove
        """
        try:
            if isolated_dir.exists():
                self._logger.debug("Cleaning up: %s", isolated_dir)
                shutil.rmtree(isolated_dir)
        except (OSError, PermissionError) as e:
            self._logger.warning("Failed to clean up %s: %s", isolated_dir, e)

    def _create_failure_result(  # pylint: disable=too-many-arguments
        self, *, test_name: str, target: Path, message: str, details: str, duration: float
    ) -> ValidationResult:
        """
        Create a failure ValidationResult.

        Args:
            test_name: Name of the test
            target: Test file path
            message: Failure message
            details: Detailed error information
            duration: Validation duration

        Returns:
            ValidationResult indicating failure
        """
        return ValidationResult(
            validator_name=self.config.name,
            target_name=test_name,
            success=False,
            message=message,
            details=details,
            file_path=target,
            errors=[message],
            duration_seconds=duration,
        )
