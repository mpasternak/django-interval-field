#!/usr/bin/env python
import sys

try:
    from django.core.management import execute_manager
    def boot(settings):
        execute_manager(settings)

except ImportError:
    from django.core.management import execute_from_command_line
    def boot(settings):
        execute_from_command_line(sys.argv)

import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    boot(settings)
