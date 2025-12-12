"""Utilities for general package functions."""

from datetime import date, datetime
from importlib import import_module


def define_basic_template_global_variables(app_version_module):
    """
    Define a set template global variables.

    Parameters
    ----------
    app_version_module : str
        The name of the version module to load for introspecting the
        application version.

    Notes
    -----
    The returned dictionary is intended to be merged with a dictionary
    defined by the local application (if desired), and then injected
    into templates using a context processor.
    """
    return {
        "app_version": _display_version(app_version_module),
        "copyright_statement": f"© {date.today().year}",
        "date_today": date.today(),
    }


def _display_version(app_version_module):
    """Show the version (without commit information)."""
    try:
        version = import_module(app_version_module).version
    except ModuleNotFoundError:
        # Fallback action in case Hatch VCS fails
        display_version = ""
    else:
        display_version = version.split("+")[0]
    return display_version


def get_timestamp():
    """Get a timestamp for backup filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
