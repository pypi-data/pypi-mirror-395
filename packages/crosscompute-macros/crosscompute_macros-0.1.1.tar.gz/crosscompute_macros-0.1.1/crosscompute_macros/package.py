from importlib import import_module
from packaging.version import InvalidVersion, Version as PackageVersion

from .error import PackageError


class Version(PackageVersion):

    def __init__(self, version_text):
        try:
            super().__init__(version_text)
        except InvalidVersion as e:
            x = f'version "{version_text}" is not valid'
            raise PackageError(x) from e

    def is_equivalent(self, version, depth=None):
        if self.epoch != version.epoch:
            return False
        this_release = self.release
        that_release = version.release
        if depth:
            this_release = this_release[:depth]
            that_release = that_release[:depth]
        return this_release == that_release


def import_attribute(attribute_string):
    module_string, attribute_name = attribute_string.rsplit('.', maxsplit=1)
    return getattr(import_module(module_string), attribute_name)


def is_newer_version(new_version_text, old_version_text):
    return Version(new_version_text) > Version(old_version_text)


def is_equivalent_version(
        new_version_text, old_version_text, version_depth=None):
    new_version = Version(new_version_text)
    old_version = Version(old_version_text)
    return new_version.is_equivalent(old_version, depth=version_depth)
