"""Tests for package utilities."""

from datetime import date, datetime
from unittest.mock import patch

from dry_foundation.utils import define_basic_template_global_variables, get_timestamp


@patch("dry_foundation.utils.date")
@patch("dry_foundation.utils.import_module")
def test_template_global_variables(mock_import_function, mock_date_cls):
    # Set some mock return values
    mock_import_function.return_value.version = "M.m.p.devX"
    mock_date_cls.today.return_value = date(2000, 1, 1)
    # Check the variable values
    template_global_variables = define_basic_template_global_variables("module.name")
    assert template_global_variables == {
        "app_version": "M.m.p.devX",
        "copyright_statement": "© 2000",
        "date_today": date(2000, 1, 1),
    }


@patch("dry_foundation.utils.import_module")
def test_template_global_variables_invalid_version_module(mock_import_function):
    mock_import_function.side_effect = ModuleNotFoundError
    template_global_variables = define_basic_template_global_variables("module.name")
    assert template_global_variables["app_version"] == ""


@patch("dry_foundation.utils.import_module")
def test_template_global_variables_hashed_version(mock_import_function):
    mock_import_function.return_value.version = "M.m.p.devX+abcdef"
    template_global_variables = define_basic_template_global_variables("module.name")
    assert template_global_variables["app_version"] == "M.m.p.devX"


@patch("dry_foundation.utils.datetime")
def test_get_timestamp(mock_datetime_cls):
    mock_datetime_cls.now.return_value = datetime(2000, 1, 2, 3, 4, 5)
    assert get_timestamp() == "20000102_030405"
