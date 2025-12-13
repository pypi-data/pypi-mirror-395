# coding=utf-8

import os
from importlib import import_module

from fastmcp import FastMCP


class FastMCPBuilder:
    @classmethod
    def get_app(cls, project, transport='') -> FastMCP | None:
        module_path = f'{project.__package__}.mcp.builder'
        try:
            module = import_module(module_path)
        except ModuleNotFoundError:
            builder_cls = cls
        else:
            builder_cls = getattr(module, 'Builder', None)
            if builder_cls is None or not issubclass(builder_cls, cls):
                print(f'Invalid mcp builder path {module_path}.Builder')
                return None

        builder = builder_cls(project, transport)
        builder.make()
        return builder.app

    def __init__(self, project=None, transport=''):
        self.project = project
        self.transport = transport
        self.server_dir = os.path.realpath(os.path.join(project.__path__[0], 'mcp'))
        self.app = None

    def make(self):
        package_dir = os.path.realpath(os.path.join(self.project.__path__[0], os.pardir))
        module_path = self.server_dir[len(package_dir) + 1:].replace(os.sep, '.')
        module = import_module(module_path)
        self.app = getattr(module, 'server', None)
