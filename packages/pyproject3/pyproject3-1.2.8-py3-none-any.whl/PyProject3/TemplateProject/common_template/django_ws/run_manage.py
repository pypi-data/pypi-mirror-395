
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asr_api.settings")
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc
django.setup()

def run_migrations():
    execute_from_command_line(sys.argv + ["makemigrations"])
    execute_from_command_line(sys.argv + ["migrate"])
    return


def rollback_migration(app, name):
    execute_from_command_line(sys.argv + ["migrate", app, name])
    return


def make_empty_migration(app):
    execute_from_command_line(sys.argv + ["makemigrations", "--empty", app])
    return


def run_test():
    return


def run_server():
    execute_from_command_line(sys.argv + ["runserver", "0.0.0.0:8001"])
    return


def run_shell():
    execute_from_command_line(sys.argv + ["shell"])
    return


def main():
    # run_migrations()
    run_server()
    # make_empty_migration("asr")
    return


if __name__ == "__main__":
    main()
