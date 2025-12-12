# coding=utf-8

import os
import shutil

from applyx.command.base import BaseCommand


class Command(BaseCommand):
    def register(self, subparser):
        subparser.add_parser('clean', help='clean compiled files')

    def invoke(self, args):
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            for dirname in dirnames:
                full_pathname = os.path.join(dirpath, dirname)
                if dirname == '__pycache__':
                    print(f'Removing {full_pathname}')
                    shutil.rmtree(full_pathname)
            for filename in filenames:
                full_pathname = os.path.join(dirpath, filename)
                if filename.endswith('.pyc'):
                    print(f'Removing {full_pathname}')
                    os.remove(full_pathname)
