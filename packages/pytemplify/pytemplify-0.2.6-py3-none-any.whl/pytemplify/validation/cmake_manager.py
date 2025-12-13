"""
CMake template manager for isolated test environments.

This module manages CMake templates for running Google Tests independently
of the generated project's build system.
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from pytemplify.renderer import TemplateRenderer

logger = logging.getLogger(__name__)


def normalize_path_for_cmake(path: Any) -> str:
    """
    Convert path to forward-slash format for CMake compatibility.

    CMake accepts forward slashes on all platforms (Windows, Linux,
    macOS). This avoids issues with Windows backslashes being
    interpreted as escape sequences.

    Args:
        path: Path object or string to normalize

    Returns:
        Path string with forward slashes
    """
    return str(path).replace("\\", "/")


class CMakeTemplateManager:
    """
    Manages CMake templates for isolated test environments (SOLID: SRP).

    Responsibilities:
        - Load CMake templates
        - Render CMake files with test configuration
        - Manage template versions
        - Auto-detect project structure

    DRY Principle:
        - Reuses pytemplify's TemplateRenderer for rendering
    """

    # Template files (DRY: single source of truth)
    DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates" / "gtest"
    MAIN_TEMPLATE = "CMakeLists.txt.j2"

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize CMake template manager.

        Args:
            template_dir: Custom template directory (default: built-in)

        Raises:
            FileNotFoundError: If template directory doesn't exist
        """
        self.template_dir = template_dir or self.DEFAULT_TEMPLATE_DIR

        if not self.template_dir.exists():
            raise FileNotFoundError(f"CMake template directory not found: {self.template_dir}")

        self._logger = logging.getLogger(f"{__name__}.CMakeTemplateManager")
        self._logger.debug("CMakeTemplateManager initialized with template dir: %s", self.template_dir)

    def render_cmake_file(self, test_name: str, test_file: Path, output_path: Path, **template_vars) -> None:
        """
        Render CMakeLists.txt for a test.

        DRY: Reuses existing TemplateRenderer.

        Args:
            test_name: Name of the test
            test_file: Path to test file (can be relative to parent)
            output_path: Where to write CMakeLists.txt
            **template_vars: Additional template variables

        Raises:
            FileNotFoundError: If template file doesn't exist
            TemplateRendererException: If rendering fails
        """
        # Normalize paths for CMake (convert backslashes to forward slashes)
        # CMake accepts forward slashes on all platforms
        data = {
            "test_name": test_name,
            "test_file": normalize_path_for_cmake(test_file),
            **self._normalize_template_vars(template_vars),
        }

        # Render template (DRY: reuse TemplateRenderer)
        renderer = TemplateRenderer(data)
        template_path = self.template_dir / self.MAIN_TEMPLATE

        if not template_path.exists():
            raise FileNotFoundError(f"CMake template not found: {template_path}")

        self._logger.debug("Rendering CMake template: %s", template_path)
        rendered = renderer.render_file(template_path)

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")

        self._logger.info("Generated CMakeLists.txt: %s", output_path)

    def _normalize_template_vars(self, template_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize path variables in template vars for CMake.

        Converts all paths to forward-slash format. This handles:
        - source_patterns: List of dicts with 'path' keys
        - include_dirs: List of path strings
        - Any other path-like values

        Args:
            template_vars: Template variables dictionary

        Returns:
            Normalized dictionary with forward-slash paths
        """
        normalized = template_vars.copy()

        # Normalize source_patterns (list of dicts with 'path' keys)
        if "source_patterns" in normalized:
            normalized["source_patterns"] = [
                {
                    **pattern,
                    "path": normalize_path_for_cmake(pattern["path"]),
                }
                for pattern in normalized["source_patterns"]
            ]

        # Normalize include_dirs (list of strings)
        if "include_dirs" in normalized:
            normalized["include_dirs"] = [normalize_path_for_cmake(inc_dir) for inc_dir in normalized["include_dirs"]]

        # Normalize multiple test files (module-level builds)
        if "test_files" in normalized and normalized["test_files"]:
            normalized["test_files"] = [normalize_path_for_cmake(path) for path in normalized["test_files"]]

        return normalized

    def _convert_to_absolute_paths(
        self, test_dir: Path, source_patterns: List[Dict[str, str]], include_dirs: List[str]
    ) -> tuple:
        """
        Convert relative paths to absolute paths for CMake and deduplicate source files.

        CMake's file(GLOB_RECURSE) and target_include_directories() need absolute paths
        when CMakeLists.txt is in a different location than the test file.

        Deduplication: If multiple patterns resolve to the same actual file (e.g., specific
        SUT file and wildcard pattern both include the same .c file), keep only the first
        occurrence to avoid linker errors from duplicate symbols.

        Args:
            test_dir: Test directory
            source_patterns: List of source pattern dicts with 'name' and 'path' keys
            include_dirs: List of include directory paths

        Returns:
            Tuple of (absolute_source_patterns, absolute_include_dirs)
        """
        seen_files: Set[Path] = set()
        absolute_source_patterns = [
            pattern
            for pattern in (self._process_source_pattern(test_dir, pattern, seen_files) for pattern in source_patterns)
            if pattern
        ]
        absolute_include_dirs = [self._to_absolute_include_dir(test_dir, inc_dir) for inc_dir in include_dirs]

        return absolute_source_patterns, absolute_include_dirs

    def _process_source_pattern(self, test_dir: Path, pattern: Dict[str, str], seen_files: Set[Path]) -> Dict[str, str]:
        abs_path = self._resolve_pattern_path(test_dir, pattern["path"])
        if "*" in str(abs_path):
            return self._collect_wildcard_pattern(pattern["name"], abs_path, seen_files)
        return self._collect_specific_pattern(pattern["name"], abs_path, seen_files)

    @staticmethod
    def _resolve_pattern_path(test_dir: Path, path: str) -> Path:
        if Path(path).is_absolute():
            return Path(path)
        return (test_dir / path).absolute()

    def _collect_specific_pattern(self, name: str, abs_path: Path, seen_files: Set[Path]) -> Dict[str, str]:
        if abs_path.exists():
            resolved_path = abs_path.resolve()
            if resolved_path in seen_files:
                self._logger.debug("Skipping duplicate source file: %s", resolved_path)
                return {}
            seen_files.add(resolved_path)
        return {"name": name, "path": str(abs_path)}

    def _collect_wildcard_pattern(self, name: str, abs_path: Path, seen_files: Set[Path]) -> Dict[str, str]:
        parent_dir = abs_path.parent
        if not parent_dir.exists():
            return {}

        matched_files = []
        for matched_file in parent_dir.glob(abs_path.name):
            resolved = matched_file.resolve()
            if resolved in seen_files:
                self._logger.debug("Skipping duplicate source file from wildcard: %s", resolved)
                continue
            matched_files.append(matched_file)
            seen_files.add(resolved)

        if not matched_files:
            return {}

        return {"name": name, "path": str(abs_path)}

    @staticmethod
    def _to_absolute_include_dir(test_dir: Path, inc_dir: str) -> str:
        inc_path = Path(inc_dir)
        if inc_path.is_absolute():
            return inc_dir
        return str((test_dir / inc_dir).absolute())

    def create_test_config(
        self, test_dir: Path, options: Dict[str, Any], test_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Create test configuration from options and test directory structure.

        This method auto-detects common project structures and builds
        the configuration for CMake template rendering.

        Args:
            test_dir: Test directory (where test file is located)
            options: Validator options from YAML config
                     - sut_root_dir: Optional root directory for SUT source/headers
                                     (for projects where SUT and tests are in separate trees)
            test_file: Optional path to test file (used for extracting SUT name from filename)

        Returns:
            Template variables for CMake rendering
        """
        # Auto-detect source patterns
        source_patterns = self._detect_source_patterns(test_dir, options)

        # Auto-detect include directories
        include_dirs = self._detect_include_dirs(test_dir, options, source_patterns)

        # Get SUT root directory for coverage filtering
        sut_root_dir = self._get_sut_root_dir(test_dir, options, test_file)

        # Find gcovr executable path for coverage generation
        gcovr_path = shutil.which("gcovr")

        # Convert relative paths to absolute paths
        absolute_source_patterns, absolute_include_dirs = self._convert_to_absolute_paths(
            test_dir, source_patterns, include_dirs
        )

        # Normalize paths for CMake (use forward slashes everywhere)
        normalized_source_patterns = [
            {**pattern, "path": normalize_path_for_cmake(pattern["path"])} for pattern in absolute_source_patterns
        ]
        normalized_include_dirs = [normalize_path_for_cmake(path) for path in absolute_include_dirs]

        # Build configuration
        config = {
            # C++ settings
            "cxx_standard": options.get("cxx_standard", 17),
            "build_type": options.get("build_type", "Debug"),
            "policy_cmp0135": True,  # GoogleTest FetchContent policy
            "policy_cmp0105": True,  # Suppress cmake_minimum_required warnings
            # GoogleTest settings
            "gtest_version": options.get("gtest_version", "v1.15.2"),
            "use_gmock": options.get("use_gmock", True),  # Enable Google Mock by default
            # Platform settings
            "disable_windows": options.get("disable_windows", False),
            # Compile definitions (e.g., _UNITTEST, UNIT_TEST_BUILD)
            # These are passed to target_compile_definitions() in CMake
            "compile_definitions": options.get("compile_definitions", []),
            # Source files and includes (using absolute paths)
            "source_patterns": normalized_source_patterns,
            "include_dirs": normalized_include_dirs,
            # SUT root directory (for coverage filtering)
            "sut_root_dir": normalize_path_for_cmake(sut_root_dir) if sut_root_dir else None,
            # Coverage tool paths
            "gcovr_path": normalize_path_for_cmake(gcovr_path) if gcovr_path else None,
            # Linking
            # Note: Empty by default. libdl is Linux-specific and not needed on Windows.
            # Users can specify link_libraries in options if needed.
            "link_libraries": options.get("link_libraries", []),
            # Compiler flags
            "extra_compile_options": options.get("compile_options", []),
            "warnings_as_errors": options.get("warnings_as_errors", False),
            # Coverage
            "enable_coverage": options.get("enable_coverage", True),
            # GTest discovery timeout (seconds) for gtest_discover_tests
            "test_discovery_timeout": options.get("test_discovery_timeout", 30),
            # CMake generator (e.g., "MinGW Makefiles", "Unix Makefiles", "Ninja")
            # If not specified, CMake will use its default generator for the platform
            "cmake_generator": options.get("cmake_generator", None),
        }

        self._logger.debug(
            "Created test config: %d source patterns, %d include dirs",
            len(source_patterns),
            len(include_dirs),
        )

        return config

    def _find_stub_directory(self, test_dir: Path) -> tuple:
        """
        Find stub directory (supports both 'stub' and 'stubs').

        Args:
            test_dir: Test directory

        Returns:
            Tuple of (child_dir, sibling_dir) - BOTH can be non-None
        """
        child_dir = None
        sibling_dir = None

        # Check for child stubs (prefer "stubs" over "stub")
        for stub_name in ["stubs", "stub"]:
            if (test_dir / stub_name).exists():
                child_dir = test_dir / stub_name
                break

        # Check for sibling stubs (prefer "stubs" over "stub")
        for stub_name in ["stubs", "stub"]:
            if (test_dir.parent / stub_name).exists():
                sibling_dir = test_dir.parent / stub_name
                break

        return (child_dir, sibling_dir)

    def _extract_sut_name_from_filename(self, filename: str) -> str:
        """
        Extract SUT name from test filename.

        Supports patterns:
        - test_sensor_api.cpp -> sensor_api
        - sensor_api_test.cpp -> sensor_api
        - test_sensor_api.c -> sensor_api

        Args:
            filename: Test filename (not full path, just the filename)

        Returns:
            Extracted SUT name (empty string if no pattern matches)
        """
        # Remove file extension
        base_name = filename.rsplit(".", 1)[0] if "." in filename else filename

        # Pattern 1: test_<sut_name>
        if base_name.startswith("test_"):
            return base_name[5:]  # Remove "test_" prefix

        # Pattern 2: <sut_name>_test or <sut_name>_tests
        if base_name.endswith("_test"):
            return base_name[:-5]  # Remove "_test" suffix
        if base_name.endswith("_tests"):
            return base_name[:-6]  # Remove "_tests" suffix

        return ""

    def _extract_sut_name_from_test_dir(self, test_dir: Path) -> str:
        """
        Extract SUT name from test directory name.

        Supports patterns:
        - test_sensor_api -> sensor_api
        - sensor_api_test -> sensor_api
        - test_sensor_api_tests -> sensor_api

        Args:
            test_dir: Test directory path

        Returns:
            Extracted SUT name (empty string if no pattern matches)
        """
        dir_name = test_dir.name

        # Pattern 1: test_<sut_name>
        if dir_name.startswith("test_"):
            return dir_name[5:]  # Remove "test_" prefix

        # Pattern 2: <sut_name>_test or <sut_name>_tests
        if dir_name.endswith("_test"):
            return dir_name[:-5]  # Remove "_test" suffix
        if dir_name.endswith("_tests"):
            return dir_name[:-6]  # Remove "_tests" suffix

        return ""

    def _find_sut_root_by_name(self, test_dir: Path, sut_name: str, max_levels: int = 5) -> Optional[Path]:
        """
        Search upward from test directory to find the directory containing SUT source or header files.

        This enables automatic detection of SUT location even when tests are generated
        to a different output tree than the SUT source code. Searches for both source files
        (.c/.cpp) and header files (.h/.hpp) to support header-only implementations.

        Args:
            test_dir: Test directory to start searching from
            sut_name: SUT filename to search for (e.g., "display_api")
            max_levels: Maximum number of parent levels to search (default: 5)

        Returns:
            Path to directory containing SUT files, or None if not found
        """
        current = test_dir
        for _ in range(max_levels):
            # Check if current directory has the SUT source file (prefer source over headers)
            for ext in ["c", "cpp", "cc", "cxx"]:
                sut_file = current / f"{sut_name}.{ext}"
                if sut_file.exists():
                    self._logger.debug("Auto-detected SUT root: %s (found %s)", current, sut_file.name)
                    return current

            # Also check for header files (for header-only implementations)
            for ext in ["h", "hpp"]:
                sut_file = current / f"{sut_name}.{ext}"
                if sut_file.exists():
                    self._logger.debug("Auto-detected SUT root: %s (found %s)", current, sut_file.name)
                    return current

            # Also check common subdirectories at this level
            for subdir in ["src", "lib", "components", "sut"]:
                subdir_path = current / subdir
                if subdir_path.exists():
                    # Check for source files first
                    for ext in ["c", "cpp", "cc", "cxx"]:
                        sut_file = subdir_path / f"{sut_name}.{ext}"
                        if sut_file.exists():
                            self._logger.debug(
                                "Auto-detected SUT root in subdir: %s (found %s)", current, sut_file.name
                            )
                            return current
                    # Check for headers if no source found
                    for ext in ["h", "hpp"]:
                        sut_file = subdir_path / f"{sut_name}.{ext}"
                        if sut_file.exists():
                            self._logger.debug(
                                "Auto-detected SUT root in subdir: %s (found %s)", current, sut_file.name
                            )
                            return current

            # Move up one level
            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

        return None

    def _find_sut_file_by_name(
        self, test_dir: Path, sut_name: str, search_paths: List[str], sut_root_dir: Optional[Path] = None
    ) -> List[Dict[str, str]]:
        """
        Search for SUT source files matching the given name in multiple locations.

        Args:
            test_dir: Test directory
            sut_name: SUT filename to search for (e.g., "sensor_api")
            search_paths: List of relative paths to search (e.g., ["../..", "../../src"])
            sut_root_dir: Optional SUT root directory to search (absolute path)

        Returns:
            List of source pattern dictionaries for found SUT files
        """
        patterns = []

        # If sut_root_dir is specified, search there first
        if sut_root_dir and sut_root_dir.exists():
            # Search for C++ files in SUT root
            for ext in ["cpp", "cc", "cxx"]:
                sut_file = sut_root_dir / f"{sut_name}.{ext}"
                if sut_file.exists():
                    # Use absolute path for SUT files
                    patterns.append({"name": f"SUT_{ext.upper()}", "path": str(sut_file.absolute())})
                    self._logger.debug("Found SUT C++ file in sut_root_dir: %s", sut_file)

            # Search for C files in SUT root
            sut_c_file = sut_root_dir / f"{sut_name}.c"
            if sut_c_file.exists():
                patterns.append({"name": "SUT_C", "path": str(sut_c_file.absolute())})
                self._logger.debug("Found SUT C file in sut_root_dir: %s", sut_c_file)

            # If we found files in sut_root_dir, return immediately
            if patterns:
                return patterns

        # Otherwise, search relative to test_dir
        for search_path in search_paths:
            search_dir = test_dir / search_path
            if not search_dir.exists():
                continue

            # Search for C++ files
            for ext in ["cpp", "cc", "cxx"]:
                sut_file = search_dir / f"{sut_name}.{ext}"
                if sut_file.exists():
                    rel_path = f"{search_path}/{sut_name}.{ext}"
                    patterns.append({"name": f"SUT_{ext.upper()}", "path": rel_path})
                    self._logger.debug("Found SUT C++ file by name: %s", sut_file)

            # Search for C files
            sut_c_file = search_dir / f"{sut_name}.c"
            if sut_c_file.exists():
                rel_path = f"{search_path}/{sut_name}.c"
                patterns.append({"name": "SUT_C", "path": rel_path})
                self._logger.debug("Found SUT C file by name: %s", sut_c_file)

        return patterns

    def _add_src_patterns(self, patterns: List[Dict[str, str]], test_dir: Path) -> None:
        """Add source directory patterns at different levels."""
        # Pattern 2: src directory at same level as test
        src_dir = test_dir.parent / "src"
        if src_dir.exists():
            patterns.append({"name": "SRC", "path": "../src/*.cpp"})
            self._logger.debug("Detected src directory: %s", src_dir)
            return  # Stop if found at level 1

        # Pattern 3: src directory two levels up
        src_dir_up2 = test_dir.parent.parent / "src"
        if src_dir_up2.exists():
            patterns.append({"name": "SRC", "path": "../../src/*.cpp"})
            self._logger.debug("Detected src directory (2 levels up): %s", src_dir_up2)
            return  # Stop if found at level 2

        # Pattern 4: src directory three levels up
        src_dir_up3 = test_dir.parent.parent.parent / "src"
        if src_dir_up3.exists():
            patterns.append({"name": "SRC", "path": "../../../src/*.cpp"})
            self._logger.debug("Detected src directory (3 levels up): %s", src_dir_up3)

    def _detect_stub_patterns(self, test_dir: Path, patterns: List[Dict[str, str]]) -> None:
        """
        Detect and add stub directory patterns.

        Args:
            test_dir: Test directory
            patterns: List to append stub patterns to
        """
        stub_dir_child, stub_dir_sibling = self._find_stub_directory(test_dir)

        if stub_dir_child:
            # Add patterns for both C and C++ files in child stubs
            has_cpp = (
                list(stub_dir_child.glob("*.cpp"))
                or list(stub_dir_child.glob("*.cc"))
                or list(stub_dir_child.glob("*.cxx"))
            )
            has_c = list(stub_dir_child.glob("*.c"))
            if has_cpp:
                patterns.append({"name": "STUB", "path": f"{stub_dir_child.name}/*.cpp"})
            if has_c:
                patterns.append({"name": "STUB_C", "path": f"{stub_dir_child.name}/*.c"})
            self._logger.debug("Detected stub directory (child): %s", stub_dir_child)

        if stub_dir_sibling:  # Note: 'if' not 'elif' - can have both!
            # Add patterns for both C and C++ files in sibling stubs
            has_cpp = (
                list(stub_dir_sibling.glob("*.cpp"))
                or list(stub_dir_sibling.glob("*.cc"))
                or list(stub_dir_sibling.glob("*.cxx"))
            )
            has_c = list(stub_dir_sibling.glob("*.c"))
            if has_cpp:
                patterns.append({"name": "STUB_SIBLING", "path": f"../{stub_dir_sibling.name}/*.cpp"})
            if has_c:
                patterns.append({"name": "STUB_SIBLING_C", "path": f"../{stub_dir_sibling.name}/*.c"})
            self._logger.debug("Detected stub directory (sibling): %s", stub_dir_sibling)

    def _detect_common_patterns(self, test_dir: Path, patterns: List[Dict[str, str]]) -> None:
        """
        Detect and add common directory patterns (shared stubs across tests).

        Args:
            test_dir: Test directory
            patterns: List to append common patterns to
        """
        common_dir = test_dir.parent / "common"
        if common_dir.exists() and common_dir.is_dir():
            has_cpp = list(common_dir.glob("*.cpp")) or list(common_dir.glob("*.cc")) or list(common_dir.glob("*.cxx"))
            has_c = list(common_dir.glob("*.c"))
            if has_cpp:
                patterns.append({"name": "COMMON", "path": "../common/*.cpp"})
            if has_c:
                patterns.append({"name": "COMMON_C", "path": "../common/*.c"})
            if has_cpp or has_c:
                self._logger.debug("Detected common directory: %s", common_dir)

    def _detect_sut_patterns(self, test_dir: Path, options: Dict[str, Any], patterns: List[Dict[str, str]]) -> None:
        """
        Detect and add SUT source file patterns.

        Args:
            test_dir: Test directory
            options: User options (may contain sut_root_dir)
            patterns: List to append SUT patterns to
        """
        # Extract SUT name from test directory name (e.g., test_sensor_api -> sensor_api)
        sut_name = self._extract_sut_name_from_test_dir(test_dir)

        # Get SUT root directory (user-specified or auto-detected)
        sut_root_dir = self._get_sut_root_dir(test_dir, options)
        if sut_root_dir:
            self._logger.info("Using SUT root directory: %s", sut_root_dir)

        if sut_name:
            # Search for SUT files by name in common locations
            search_paths = [
                "../..",  # Project root
                "../../src",  # src/ at project root
                "../../lib",  # lib/ at project root
                "../../components",  # components/ at project root
                "../src",  # src/ at parent level
                "../../sut",  # sut/ directory
            ]
            name_based_patterns = self._find_sut_file_by_name(test_dir, sut_name, search_paths, sut_root_dir)
            patterns.extend(name_based_patterns)

        # Fallback - generic SUT source files at project root (if name-based failed)
        # Only use wildcard matching if we didn't find specific files by name
        if not sut_name or not any(p["name"].startswith("SUT") for p in patterns):
            sut_dir = test_dir.parent.parent
            if sut_dir.exists() and sut_dir.is_dir():
                sut_cpp_files = list(sut_dir.glob("*.cpp")) + list(sut_dir.glob("*.cc")) + list(sut_dir.glob("*.cxx"))
                sut_c_files = list(sut_dir.glob("*.c"))
                if sut_cpp_files:
                    patterns.append({"name": "SUT", "path": "../../*.cpp"})
                    self._logger.debug("Detected SUT C++ files at project root (wildcard): %s", sut_dir)
                if sut_c_files:
                    patterns.append({"name": "SUT_C", "path": "../../*.c"})
                    self._logger.debug("Detected SUT C files at project root (wildcard): %s", sut_dir)

    def _detect_test_dir_sources(self, test_dir: Path, patterns: List[Dict[str, str]]) -> None:
        """
        Detect and add source files in same directory as test files.

        Args:
            test_dir: Test directory
            patterns: List to append source patterns to
        """
        # Look for *.cpp files in the test directory (but not *_test.cpp files)
        test_cpp_files = list(test_dir.glob("*.cpp"))
        test_files_to_exclude = {"test_", "*_test"}

        for cpp_file in test_cpp_files:
            exclude = False
            for exclude_pattern in test_files_to_exclude:
                if exclude_pattern in cpp_file.name:
                    exclude = True
                    break
            if not exclude:
                # Add specific file pattern relative to build directory
                rel_path = f"../{cpp_file.name}"
                patterns.append({"name": cpp_file.stem.upper(), "path": rel_path})
                self._logger.debug("Detected source file: %s", rel_path)

    def _detect_source_patterns(self, test_dir: Path, options: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Auto-detect source file patterns based on common project structures.

        Common patterns:
            - test/stub/*.cpp (stub implementations)
            - ../src/*.cpp (source files relative to test dir)
            - ../../../src/*.cpp (nested test structure)

        Args:
            test_dir: Test directory
            options: User options (can override auto-detection)

        Returns:
            List of source pattern dictionaries with 'name' and 'path' keys
        """
        patterns = []

        # User-specified patterns take precedence
        if "source_patterns" in options:
            patterns.extend(options["source_patterns"])
            self._logger.debug("Using %d user-specified source patterns", len(patterns))
            return patterns

        # Auto-detect common patterns (stubs, common, SUT)
        self._detect_stub_patterns(test_dir, patterns)
        self._detect_common_patterns(test_dir, patterns)
        self._detect_sut_patterns(test_dir, options, patterns)
        self._add_src_patterns(patterns, test_dir)
        self._detect_test_dir_sources(test_dir, patterns)

        # Merge with ProjectScanner-found SUT sources if provided
        # ProjectScanner finds SUT files that our auto-detection might miss
        if "sut_sources" in options:
            sut_sources = options["sut_sources"]
            self._logger.debug("Merging %d ProjectScanner SUT sources with auto-detected patterns", len(sut_sources))
            patterns.extend(sut_sources)

        if not patterns:
            self._logger.warning("No source files detected for %s", test_dir)

        return patterns

    def _add_inc_dir_patterns(self, include_dirs: List[str], test_dir: Path) -> None:
        """Add include directory patterns at different levels."""
        # Pattern 2: inc directory at same level as test
        inc_dir = test_dir.parent / "inc"
        if inc_dir.exists():
            include_dirs.append("../inc")
            self._logger.debug("Detected inc directory: %s", inc_dir)

        # Pattern 3: include directory at same level as test
        include_dir = test_dir.parent / "include"
        if include_dir.exists():
            include_dirs.append("../include")
            self._logger.debug("Detected include directory: %s", include_dir)

        # Pattern 4: inc directory two levels up
        inc_dir_up2 = test_dir.parent.parent / "inc"
        if inc_dir_up2.exists() and not inc_dir.exists():
            include_dirs.append("../../inc")
            self._logger.debug("Detected inc directory (2 levels up): %s", inc_dir_up2)

        # Pattern 5: inc directory three levels up
        inc_dir_up3 = test_dir.parent.parent.parent / "inc"
        if inc_dir_up3.exists() and not inc_dir.exists() and not inc_dir_up2.exists():
            include_dirs.append("../../../inc")
            self._logger.debug("Detected inc directory (3 levels up): %s", inc_dir_up3)

    def _detect_stub_include_dirs(self, test_dir: Path, include_dirs: List[str]) -> None:
        """
        Detect and add stub directory include paths.

        Args:
            test_dir: Test directory
            include_dirs: List to append include paths to
        """
        stub_dir_child, stub_dir_sibling = self._find_stub_directory(test_dir)

        if stub_dir_child:
            include_dirs.append(stub_dir_child.name)
            self._logger.debug("Detected stub include (child): %s", stub_dir_child)
        if stub_dir_sibling:  # Note: 'if' not 'elif' - can have both!
            include_dirs.append(f"../{stub_dir_sibling.name}")
            self._logger.debug("Detected stub include (sibling): %s", stub_dir_sibling)

    def _detect_common_include_dirs(self, test_dir: Path, include_dirs: List[str]) -> None:
        """
        Detect and add common directory include paths.

        Args:
            test_dir: Test directory
            include_dirs: List to append include paths to
        """
        common_dir = test_dir.parent / "common"
        if common_dir.exists() and common_dir.is_dir():
            include_dirs.append("../common")
            self._logger.debug("Detected common directory: %s", common_dir)

    def _detect_test_dir_headers(self, test_dir: Path, include_dirs: List[str]) -> None:
        """
        Detect header files in same directory as test files.

        Args:
            test_dir: Test directory
            include_dirs: List to append include paths to
        """
        test_h_files = list(test_dir.glob("*.h")) + list(test_dir.glob("*.hpp"))
        if test_h_files:
            include_dirs.append(".")
            self._logger.debug("Detected header files in test directory, adding '.' to includes")

    def _detect_sut_header_dirs(self, test_dir: Path, options: Dict[str, Any], include_dirs: List[str]) -> None:
        """
        Detect and add SUT header directories.

        Args:
            test_dir: Test directory
            options: User options (may contain sut_root_dir)
            include_dirs: List to append include paths to
        """
        candidate_roots = self._build_sut_root_candidates(test_dir, options)
        for candidate in candidate_roots:
            rel_path = self._relative_include_if_headers(test_dir, candidate)
            if rel_path and rel_path not in include_dirs:
                include_dirs.append(rel_path)
                self._logger.debug("Detected SUT headers at: %s (relative: %s)", candidate, rel_path)
                break

    def _build_sut_root_candidates(self, test_dir: Path, options: Dict[str, Any]) -> List[Path]:
        """
        Build an ordered list of directories to search for SUT headers.
        """
        candidates: List[Path] = []
        sut_root = self._get_sut_root_dir(test_dir, options)
        if sut_root:
            candidates.append(sut_root)

        parent = test_dir.parent
        if parent not in candidates:
            candidates.append(parent)

        grandparent = parent.parent
        if grandparent not in candidates:
            candidates.append(grandparent)

        return [c for c in candidates if c and c.exists() and c.is_dir()]

    def _relative_include_if_headers(self, test_dir: Path, directory: Path) -> Optional[str]:
        """
        Return relative include path if directory contains headers, otherwise None.
        """
        headers = list(directory.glob("*.h")) + list(directory.glob("*.hpp"))
        if not headers:
            return None

        try:
            rel_path = os.path.relpath(directory, test_dir)
        except ValueError:
            rel_path = str(directory.absolute())
        return rel_path.replace("\\", "/")

    def _detect_sut_source_include_dirs(
        self, test_dir: Path, source_patterns: Optional[List[Dict[str, str]]], include_dirs: List[str]
    ) -> None:
        """
        Detect include directories for SUT source file locations.

        If we found SUT source files via name-based detection in src/, lib/, etc.,
        also add those directories as include paths.

        Args:
            test_dir: Test directory
            source_patterns: List of source patterns (may contain SUT patterns)
            include_dirs: List to append include paths to
        """
        if not source_patterns:
            return

        for pattern in source_patterns:
            # Skip non-SUT patterns
            if not pattern["name"].startswith("SUT"):
                continue

            # Extract directory from the source path (e.g., "../../src/sensor_api.c" -> "../../src")
            path_parts = pattern["path"].split("/")
            if len(path_parts) <= 1:
                continue

            dir_path = "/".join(path_parts[:-1])  # Remove filename
            if dir_path in include_dirs:
                continue

            # Check if this directory actually has headers
            abs_dir = test_dir / dir_path
            if not abs_dir.exists():
                continue

            headers = list(abs_dir.glob("*.h")) + list(abs_dir.glob("*.hpp"))
            if headers:
                include_dirs.append(dir_path)
                self._logger.debug("Detected SUT headers in source directory: %s", abs_dir)

    def _get_sut_root_dir(
        self, test_dir: Path, options: Dict[str, Any], test_file: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Get SUT root directory from options or auto-detect it.

        Args:
            test_dir: Test directory
            options: User options (may contain sut_root_dir)
            test_file: Optional test file path (used to extract SUT name from filename)

        Returns:
            Path to SUT root directory, or None if not found
        """
        # Step 1: Check if user specified sut_root_dir
        if "sut_root_dir" in options and options["sut_root_dir"]:
            sut_root_dir = Path(options["sut_root_dir"])
            if not sut_root_dir.is_absolute():
                # Make relative to test_dir
                sut_root_dir = (test_dir / sut_root_dir).resolve()
            return sut_root_dir

        # Step 2: Try to auto-detect SUT root by name
        # First try extracting from test file name, then fall back to directory name
        sut_name = ""
        if test_file:
            sut_name = self._extract_sut_name_from_filename(test_file.name)
        if not sut_name:
            sut_name = self._extract_sut_name_from_test_dir(test_dir)

        if sut_name:
            sut_root_dir = self._find_sut_root_by_name(test_dir, sut_name)
            if sut_root_dir:
                self._logger.debug("Auto-detected SUT root directory: %s", sut_root_dir)
                return sut_root_dir

        return None

    def _detect_include_dirs(
        self, test_dir: Path, options: Dict[str, Any], source_patterns: Optional[List[Dict[str, str]]] = None
    ) -> List[str]:
        """
        Auto-detect include directories based on common project structures.

        Common patterns:
            - ../inc or ../include (headers relative to test dir)
            - ../stub (stub headers)
            - ../../../inc (nested structure)

        Args:
            test_dir: Test directory
            options: User options (can override auto-detection)
            source_patterns: Optional list of source patterns (used for SUT header detection)

        Returns:
            List of include directory paths (relative to build directory)
        """
        include_dirs = []

        # Auto-detect common patterns
        self._detect_stub_include_dirs(test_dir, include_dirs)
        self._detect_common_include_dirs(test_dir, include_dirs)
        self._add_inc_dir_patterns(include_dirs, test_dir)
        self._detect_test_dir_headers(test_dir, include_dirs)
        self._detect_sut_header_dirs(test_dir, options, include_dirs)
        self._detect_sut_source_include_dirs(test_dir, source_patterns, include_dirs)

        # Add user-specified include directories (in addition to auto-detected ones)
        if "include_dirs" in options and options["include_dirs"]:
            user_includes = options["include_dirs"]
            include_dirs.extend(user_includes)
            self._logger.debug(
                "Added %d user-specified include directories to %d auto-detected ones",
                len(user_includes),
                len(include_dirs) - len(user_includes),
            )

        # If no include dirs detected but source files were found in parent, add parent
        if not include_dirs and source_patterns:
            # Check if any pattern points to parent directory
            for pattern in source_patterns:
                if pattern["path"].startswith("../"):
                    include_dirs.append("..")
                    self._logger.debug("Adding parent directory to includes for source files")
                    break

        if not include_dirs:
            self._logger.warning("No include directories detected for %s", test_dir)

        return include_dirs

    def validate_template(self, template_name: str = MAIN_TEMPLATE) -> bool:
        """
        Validate that a template exists and is readable.

        Args:
            template_name: Name of the template file

        Returns:
            True if template is valid

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        if not template_path.is_file():
            raise ValueError(f"Template is not a file: {template_path}")

        # Try to read template
        try:
            template_path.read_text(encoding="utf-8")
            return True
        except Exception as e:
            raise ValueError(f"Cannot read template {template_path}: {e}") from e
