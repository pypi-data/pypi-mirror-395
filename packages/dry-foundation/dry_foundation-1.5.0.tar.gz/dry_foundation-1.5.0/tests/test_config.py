"""Tests for application configuration objects."""

from pathlib import Path
from unittest.mock import patch

import pytest

from dry_foundation.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
)
from dry_foundation.config import (
    TestingConfig as _TestingConfig,  # rename to avoid pytest collection
)

APP_IMPORT_NAME = "test"


class TestGenericConfig:
    """Test characteristics of generic configurations."""

    def test_db_path(self):
        config = Config(APP_IMPORT_NAME, db_path="test/path")
        assert config.DATABASE == Path("test/path")

    def test_no_db_path(self):
        config = Config(APP_IMPORT_NAME, db_path=None)
        assert config.DATABASE is None

    def test_invalid_db_path(self):
        with pytest.raises(TypeError):
            Config(APP_IMPORT_NAME, db_path=1)

    def test_preload_data(self):
        # Test a dummy callable for preloading data
        config = Config(APP_IMPORT_NAME, preload_data=lambda _: None)
        assert config.PRELOAD_DATA

    def test_no_preload_data(self):
        config = Config(APP_IMPORT_NAME, preload_data=None)
        assert config.PRELOAD_DATA is None

    def test_preload_data_invalid(self):
        with pytest.raises(TypeError):
            Config(APP_IMPORT_NAME, preload_data="test")

    def test_preload_data_path(self):
        config = Config(APP_IMPORT_NAME, preload_data_path="test/path")
        assert config.PRELOAD_DATA_PATH == Path("test/path")

    def test_no_preload_data_path(self):
        config = Config(APP_IMPORT_NAME, preload_data_path=None)
        assert config.PRELOAD_DATA_PATH is None

    def test_invalid_preload_data_path(self):
        with pytest.raises(TypeError):
            Config(APP_IMPORT_NAME, preload_data_path=1)


@pytest.fixture
def production_config_default_config_filepaths(default_config_filepath):
    with patch.object(
        ProductionConfig, "default_config_filepaths", new=[default_config_filepath]
    ):
        yield


@pytest.fixture
def production_config_default_global_config_filepath(default_config_filepath):
    with patch.object(
        ProductionConfig, "default_global_config_filepath", new=default_config_filepath
    ):
        yield


class TestProductionConfig:
    """Test the production configuration."""

    def test_initialization(self, instance_path):
        config = ProductionConfig(APP_IMPORT_NAME, instance_path)
        assert config.SECRET_KEY == "INSECURE"

    def test_initialization_default_file(
        self, instance_path, production_config_default_config_filepaths
    ):
        config = ProductionConfig(APP_IMPORT_NAME, instance_path)
        assert config.SECRET_KEY == "test secret key"

    def test_initialization_instance_file_supersedes(
        self,
        instance_path,
        production_config_default_global_config_filepath,
        instance_config_filepath,
    ):
        config = ProductionConfig(APP_IMPORT_NAME, instance_path)
        assert config.SECRET_KEY == "test secret key"
        assert config.OTHER == "test supersede"


class TestDevelopmentConfig:
    """Test the development configuration."""

    def test_initialization(self, instance_path):
        config = DevelopmentConfig(APP_IMPORT_NAME, instance_path)
        assert config.SECRET_KEY == "development key"
        assert config.PRELOAD_DATA_PATH is None

    def test_default_preload_data_path(self, instance_path):
        # Create (and use by default) a development data spec in the default location
        mock_preload_data_path = instance_path / "dev_data.sql"
        mock_preload_data_path.touch()
        config = DevelopmentConfig(APP_IMPORT_NAME, instance_path)
        assert config.PRELOAD_DATA_PATH == mock_preload_data_path

    def test_preload_data_path(self, tmp_path, instance_path):
        # Create and use a development data spec in an alternate location
        mock_preload_data_path = tmp_path / "test_data.sql"
        mock_preload_data_path.touch()
        config = DevelopmentConfig(
            APP_IMPORT_NAME, instance_path, preload_data_path=mock_preload_data_path
        )
        assert config.PRELOAD_DATA_PATH == mock_preload_data_path


class TestTestingConfig:
    """Test the development configuration."""

    def test_initialization(self):
        mock_db_path = Path("/path/to/test/db.sqlite")
        config = _TestingConfig(APP_IMPORT_NAME, db_path=mock_db_path)
        assert config.SECRET_KEY == "testing key"
        assert config.DATABASE == mock_db_path
