"""
Pytest configuration and fixtures for geobank tests.
"""

import os

import django


def pytest_configure():
    """Configure Django settings for tests."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geobank.tests.settings")
    django.setup()


def pytest_collection_modifyitems(config, items):
    """Ensure database tables exist before running tests."""
    import contextlib

    from django.core.management import call_command

    with contextlib.suppress(Exception):
        call_command("migrate", "--run-syncdb", verbosity=0)
