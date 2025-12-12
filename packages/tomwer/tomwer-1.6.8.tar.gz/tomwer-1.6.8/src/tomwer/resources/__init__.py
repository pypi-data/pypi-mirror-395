"""
project resources (icons... )
"""

from __future__ import annotations

import os
import sys
import contextlib
import atexit
from typing import NamedTuple
import importlib
import functools

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/data'
_RESOURCES_DIR = None

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/doc'
# Not in use, uncomment when functionality is needed
# _RESOURCES_DOC_DIR = None

# cx_Freeze frozen support
# See http://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
if getattr(sys, "frozen", False):
    # Running in a frozen application:
    # We expect resources to be located either in a silx/resources/ dir
    # relative to the executable or within this package.
    _dir = os.path.join(os.path.dirname(sys.executable), "tomwer", "resources")
    if os.path.isdir(_dir):
        _RESOURCES_DIR = _dir


# Manage resource files life-cycle
_file_manager = contextlib.ExitStack()
atexit.register(_file_manager.close)


class _ResourceDirectory(NamedTuple):
    """Store a source of resources"""

    package_name: str
    forced_path: str | None = None


_TOMWER_DIRECTORY = _ResourceDirectory(
    package_name=__name__,
    forced_path=_RESOURCES_DIR,
)

_RESOURCE_DIRECTORIES = {}
_RESOURCE_DIRECTORIES["tomwer"] = _TOMWER_DIRECTORY


def _get_package_and_resource(
    resource, default_directory=None
) -> tuple[_ResourceDirectory, str]:
    """
    Return the resource directory class and a cleaned resource name without
    prefix.

    :param resource: Name of the resource with resource prefix.
    :param default_directory: If the resource is not prefixed, the resource
        will be searched on this default directory of the silx resource
        directory.
    :raises ValueError: If the resource name uses an unregistered resource
        directory name
    """
    if ":" in resource:
        prefix, resource = resource.split(":", 1)
    else:
        prefix = "tomwer"
        if default_directory is not None:
            resource = f"{default_directory}/{resource}"
    if prefix not in _RESOURCE_DIRECTORIES:
        raise ValueError("Resource '%s' uses an unregistred prefix", resource)
    resource_directory = _RESOURCE_DIRECTORIES[prefix]
    return resource_directory, resource


# Manage resource files life-cycle
_file_manager = contextlib.ExitStack()
atexit.register(_file_manager.close)


@functools.lru_cache(maxsize=None)
def _get_resource_filename(package: str, resource: str) -> str:
    """Returns path to requested resource in package

    :param package: Name of the package in which to look for the resource
    :param resource: Resource path relative to package using '/' path separator
    :return: Abolute resource path in the file system
    """
    # Caching prevents extracting the resource twice
    file_context = importlib.resources.as_file(
        importlib.resources.files(package) / resource
    )
    path = _file_manager.enter_context(file_context)
    return str(path.absolute())


def _resource_filename(resource: str, default_directory: str | None = None) -> str:
    """Return filename corresponding to resource.

    The existence of the resource is not checked.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx". See also :func:`register_resource_directory`.

    :param resource: Resource path relative to resource directory
                     using '/' path separator. It can be either a file or
                     a directory.
    :param default_directory: If the resource is not prefixed, the resource
        will be searched on this default directory of the silx resource
        directory. It should only be used internally by silx.
    :return: Absolute resource path in the file system
    """
    resource_directory, resource_name = _get_package_and_resource(
        resource, default_directory=default_directory
    )

    if resource_directory.forced_path is not None:
        # if set, use this directory
        base_dir = resource_directory.forced_path
        resource_path = os.path.join(base_dir, *resource_name.split("/"))
        return resource_path

    return _get_resource_filename(resource_directory.package_name, resource_name)
