from os.path import dirname, getmtime, join, normpath, realpath
from pathlib import PurePath
from string import Template as StringTemplate

from jinja2 import (
    BaseLoader,
    Environment,
    Template as JinjaTemplate,
    TemplateNotFound)


class AssetStorage:

    def __init__(self, folder):
        self.folder = folder

    def load_raw_text(self, file_name):
        return (self.folder / file_name).read_text().strip()

    def load_string_text(self, file_name):
        return StringTemplate(self.load_raw_text(file_name))

    def load_jinja_text(self, file_name):
        return JinjaTemplate(self.load_raw_text(file_name), trim_blocks=True)


class PathTemplateLoader(BaseLoader):

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def get_source(self, environment, template):  # noqa: ARG002
        'Support absolute template paths.'
        try:
            modification_time = getmtime(template)  # noqa: PTH204
        except (OSError, TypeError) as e:
            raise TemplateNotFound(template) from e

        def is_latest():
            try:
                return modification_time == getmtime(template)  # noqa: PTH204
            except OSError:
                return False

        with open(template, mode='rt', encoding=self.encoding) as f:  # noqa: PTH123
            text = f.read()
        return text, realpath(template), is_latest


class RelativeTemplateEnvironment(Environment):

    def join_path(self, template, parent):
        'Support relative template paths via extends, import, include.'
        template = get_asset_path(template)
        return normpath(join(dirname(  # noqa: PTH118 PTH120
            parent), template)) if template else template


def get_asset_path(asset_uri):
    asset_parts = asset_uri.split(':')
    if len(asset_parts) > 1:
        package_name, relative_path = asset_parts
        package_name = package_name.strip()
    else:
        package_name, relative_path = '', asset_parts[0]
    if package_name:
        package = __import__(package_name)
        package_folder = PurePath(package.__file__).parent
        path = str(package_folder / relative_path)
    else:
        path = relative_path
    return path
