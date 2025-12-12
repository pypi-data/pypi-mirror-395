"""A module containing objects with various configuration settings."""

import warnings

from .default_settings import Config, InstanceBasedConfig


class ProductionConfig(InstanceBasedConfig):
    """A configuration object with settings for production."""

    # Flask app object configuration parameters
    SECRET_KEY = "INSECURE"

    def __init__(
        self,
        import_name,
        instance_path,
        app_name=None,
        db_path=None,
        preload_data=None,
        preload_data_path=None,
        custom_config_filepaths=(),
    ):
        super().__init__(
            import_name,
            instance_path,
            app_name=app_name,
            db_path=db_path,
            preload_data=preload_data,
            preload_data_path=preload_data_path,
            custom_config_filepaths=custom_config_filepaths,
        )
        if self.SECRET_KEY == "INSECURE":
            # Give an alert while the secret key remains insecure
            warnings.formatwarning = lambda msg, *args, **kwargs: f"\n{msg}\n"
            warnings.warn(
                "INSECURE: Production mode has not yet been fully configured; "
                "a secret key is required."
            )


class DevelopmentConfig(InstanceBasedConfig):
    """A configuration object with settings for development."""

    # Flask app object configuration parameters
    DEBUG = True
    SECRET_KEY = "development key"

    def __init__(
        self,
        import_name,
        instance_path,
        app_name=None,
        db_path=None,
        preload_data=None,
        preload_data_path=None,
        custom_config_filepaths=(),
    ):
        super().__init__(
            import_name,
            instance_path,
            app_name=app_name,
            db_path=db_path,
            preload_data=preload_data,
            preload_data_path=preload_data_path,
            custom_config_filepaths=custom_config_filepaths,
        )

    def _set_preload_data_path(self, value):
        # Use a default path to an SQL file with preload data if not otherwise specified
        if value is None:
            dev_data_path = self._instance_path / "dev_data.sql"
            value = dev_data_path if dev_data_path.exists() else None
        super()._set_preload_data_path(value)

    @property
    def default_db_filename(self):
        return f"dev-{super().default_db_filename}"


class TestingConfig(Config):
    """A configuration object with settings for testing."""

    # Flask app object configuration parameters
    TESTING = True
    SECRET_KEY = "testing key"
    DATABASE_INTERFACE_ARGS = ()
    DATABASE_INTERFACE_KWARGS = {}
    WTF_CSRF_ENABLED = False
    # Do not use local app configurations when testing
    config_filepaths = []

    def __init__(
        self,
        import_name,
        app_name=None,
        db_path=None,
        preload_data=None,
        preload_data_path=None,
        custom_config_filepaths=(),
    ):
        super().__init__(
            import_name,
            app_name=app_name,
            db_path=db_path,
            preload_data=preload_data,
            preload_data_path=preload_data_path,
            custom_config_filepaths=custom_config_filepaths,
        )
