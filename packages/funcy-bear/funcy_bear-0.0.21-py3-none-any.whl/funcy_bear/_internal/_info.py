from dataclasses import dataclass, field
from typing import Literal

from funcy_bear._internal._version import __commit_id__, __version__, __version_tuple__


@dataclass(slots=True)
class _Package:
    """Dataclass to store package information."""

    name: str
    """Package name."""
    version: str = "0.0.0"
    """Package version."""
    description: str = "No description available."
    """Package description."""

    def __str__(self) -> str:
        """String representation of the package information."""
        return f"{self.name} v{self.version}: {self.description}"


def _get_package_info(dist: str) -> _Package:
    """Get package information for the given distribution.

    Parameters:
        dist: A distribution name.

    Returns:
        Package information with version, name, and description.
    """
    return _Package(name=dist, version=_get_version(dist), description=_get_description(dist))


def _get_version(dist: str) -> str:
    """Get version of the given distribution or the current package.

    Parameters:
        dist: A distribution name.

    Returns:
        A version number.
    """
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version(dist)
    except PackageNotFoundError:
        return "0.0.0"


def _get_description(dist: str) -> str:
    """Get description of the given distribution or the current package.

    Parameters:
        dist: A distribution name.

    Returns:
        A description string.
    """
    from importlib.metadata import PackageNotFoundError, distribution

    try:
        return distribution(dist).metadata.get("summary", "No description available.")
    except PackageNotFoundError:
        return "No description available."


# fmt: off
@dataclass(slots=True, frozen=True)
class _ProjectName:
    """A class to represent the project name and its metadata as literals for type safety.

    This is done this way to make it easier to see the values in the IDE and to ensure that the values are consistent throughout the codebase.
    """

    package_distribution: Literal["funcy-bear"] = "funcy-bear"
    project: Literal["funcy_bear"] = "funcy_bear"
    project_upper: Literal["FUNCY_BEAR"] = "FUNCY_BEAR"
    env_variable: Literal["FUNCY_BEAR_ENV"] = ("FUNCY_BEAR_ENV")
# fmt: on


@dataclass(slots=True, frozen=True)
class _ModulePaths:
    """A class to hold the module import paths, mostly for the CLI."""

    _internal: str = "funcy_bear._internal"
    _commands: str = f"{_internal}._cmds"


def project_version() -> str:
    """Get the current project version string."""
    return __version__ if __version__ != "0.0.0" else _get_version("funcy-bear")


@dataclass(slots=True)
class _ProjectMetadata:
    """Dataclass to store the current project metadata."""

    names: _ProjectName = field(default_factory=_ProjectName)
    paths: _ModulePaths = field(default_factory=_ModulePaths)
    version: str = field(default_factory=project_version)
    version_tuple: tuple[int, int, int] = __version_tuple__
    commit_id: str = __commit_id__

    @property
    def cmds(self) -> str:
        """Get the commands module path."""
        return self.paths._commands

    @property
    def full_version(self) -> str:
        """Get the full version string."""
        return f"{self.name} v{self.version}"

    @property
    def description(self) -> str:
        """Get the project description from the distribution metadata."""
        return _get_description(self.name)

    @property
    def name(self) -> Literal["funcy-bear"]:
        """Get the package distribution name."""
        return self.names.package_distribution

    @property
    def name_upper(self) -> Literal["FUNCY_BEAR"]:
        """Get the project name in uppercase with underscores."""
        return self.names.project_upper

    @property
    def project_name(self) -> Literal["funcy_bear"]:
        """Get the project name."""
        return self.names.project

    @property
    def env_variable(self) -> Literal["FUNCY_BEAR_ENV"]:
        """Get the environment variable name for the project.

        Used to check if the project is running in a specific environment.
        """
        return self.names.env_variable

    def __str__(self) -> str:
        """String representation of the project metadata."""
        return f"{self.full_version}: {self.description}"


METADATA = _ProjectMetadata()


__all__ = ["METADATA", "_Package"]

# ruff: noqa: PLC0415
