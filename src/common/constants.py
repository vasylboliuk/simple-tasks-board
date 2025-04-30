"""Constants.

This module provides classes to represent constants.
"""

from pathlib import Path


class CommonPaths:
    """CommonPaths class that store paths to project root, directories, packages."""

    project_root = Path(__file__).parent.parent.resolve()  # src
    resource_path = project_root.joinpath("resources")
    log_path = project_root.joinpath("logs")
    tests_path = project_root.parent.joinpath("tests")
