"""
Automatic stub generation integration for pyz3.

This module integrates stub generation into the build process,
ensuring type stubs are always up-to-date with the compiled modules.
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class AutoStubGenerator:
    """Automatic stub file generator for pyz3 modules."""

    def __init__(self, package_name: str, destination: str = "."):
        self.package_name = package_name
        self.destination = Path(destination)
        self.destination.mkdir(parents=True, exist_ok=True)

    def generate(self) -> bool:
        """Generate stub files for the package.

        Returns:
            bool: True if generation succeeded, False otherwise
        """
        try:
            logger.info(f"Generating stubs for {self.package_name}")

            # Import the generate_stubs module
            from pyz3.generate_stubs import generate_stubs

            # Generate stubs
            generate_stubs(self.package_name, str(self.destination), check=False)

            logger.info(f"Stubs generated successfully in {self.destination}")
            return True

        except Exception as e:
            logger.error(f"Failed to generate stubs: {e}")
            return False

    def create_py_typed_marker(self, package_path: Optional[Path] = None) -> None:
        """Create py.typed marker file for PEP 561 compliance.

        Args:
            package_path: Path to the package directory. If None, uses package_name
        """
        if package_path is None:
            # Try to find the package path
            try:
                module = importlib.import_module(self.package_name.split('.')[0])
                if hasattr(module, '__path__'):
                    package_path = Path(module.__path__[0])
                elif hasattr(module, '__file__'):
                    package_path = Path(module.__file__).parent
                else:
                    logger.warning("Could not determine package path for py.typed marker")
                    return
            except ImportError:
                logger.warning(f"Could not import {self.package_name} to create py.typed marker")
                return

        if package_path:
            py_typed_file = package_path / "py.typed"
            py_typed_file.touch(exist_ok=True)
            logger.info(f"Created py.typed marker at {py_typed_file}")


def generate_stubs_for_modules(
    modules: List[str],
    destination: str = ".",
    create_py_typed: bool = True
) -> bool:
    """Generate stubs for multiple modules.

    Args:
        modules: List of module names to generate stubs for
        destination: Destination directory for stub files
        create_py_typed: Whether to create py.typed marker files

    Returns:
        bool: True if all stubs generated successfully
    """
    success = True

    for module_name in modules:
        generator = AutoStubGenerator(module_name, destination)

        if not generator.generate():
            success = False
            logger.error(f"Failed to generate stubs for {module_name}")
            continue

        if create_py_typed:
            generator.create_py_typed_marker()

    return success


def integrate_stub_generation_into_build(
    pyproject_path: Path,
    destination: str = "."
) -> bool:
    """Integrate stub generation into the build process.

    Reads pyproject.toml to find all ext_modules and generates stubs for them.

    Args:
        pyproject_path: Path to pyproject.toml
        destination: Destination directory for stub files

    Returns:
        bool: True if all stubs generated successfully
    """
    try:
        import tomli
    except ImportError:
        try:
            import tomllib as tomli
        except ImportError:
            logger.error("Neither tomli nor tomllib available. Install tomli for Python < 3.11")
            return False

    try:
        with open(pyproject_path, 'rb') as f:
            config = tomli.load(f)

        # Get list of extension modules
        ext_modules = config.get('tool', {}).get('pyz3', {}).get('ext_module', [])

        if not ext_modules:
            logger.warning("No extension modules found in pyproject.toml")
            return True

        module_names = [mod['name'] for mod in ext_modules if 'name' in mod]

        logger.info(f"Found {len(module_names)} modules to generate stubs for")

        return generate_stubs_for_modules(module_names, destination)

    except Exception as e:
        logger.error(f"Error reading pyproject.toml: {e}")
        return False


def post_build_hook(build_lib: str, pyproject_path: Optional[Path] = None) -> None:
    """Post-build hook to automatically generate stubs.

    This function should be called after building extension modules.

    Args:
        build_lib: Path to the build library directory
        pyproject_path: Path to pyproject.toml (defaults to current directory)
    """
    if pyproject_path is None:
        pyproject_path = Path.cwd() / "pyproject.toml"

    if not pyproject_path.exists():
        logger.warning(f"pyproject.toml not found at {pyproject_path}")
        return

    logger.info("Running post-build stub generation...")
    success = integrate_stub_generation_into_build(pyproject_path, build_lib)

    if success:
        logger.info("Stub generation completed successfully")
    else:
        logger.warning("Some stub files may not have been generated")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        print("Usage: python -m pyz3.auto_stubs <package_name> [destination]")
        sys.exit(1)

    package_name = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else "."

    generator = AutoStubGenerator(package_name, destination)
    if generator.generate():
        generator.create_py_typed_marker()
        sys.exit(0)
    else:
        sys.exit(1)
