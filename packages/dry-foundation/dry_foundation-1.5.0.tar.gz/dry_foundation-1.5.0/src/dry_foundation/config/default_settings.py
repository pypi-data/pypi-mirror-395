"""Default configuration settings."""

import json
from pathlib import Path

DEFAULT_CONFIG_DIR = Path("/etc")


class Config:
    """A base configuration object with some default settings."""

    # Flask app object configuration parameters
    REGISTRATION = True
    TESTING = False
    # Set defaults for property-based custom configuration parameters
    _database = None
    _preload_data = None
    _preload_data_path = None

    def __init__(
        self,
        import_name,
        app_name=None,
        db_path=None,
        preload_data=None,
        preload_data_path=None,
        custom_config_filepaths=(),
    ):
        # App slug loosely corresponds to Flask `import_name`
        self.SLUG = import_name
        self.NAME = app_name or import_name
        self._custom_config_filepaths = custom_config_filepaths
        # Read parameters from the configuration files in order of specificity
        for config_filepath in filter(lambda p: p.exists(), self.config_filepaths):
            self._read_config_json(config_filepath)
        # Set property-based custom configuration parameters
        self.DATABASE = db_path
        self.PRELOAD_DATA = preload_data
        self.PRELOAD_DATA_PATH = preload_data_path

    @property
    def DATABASE(self):
        return self._database

    @DATABASE.setter
    def DATABASE(self, value):
        self._set_database(value)

    def _set_database(self, value):
        self._database = Path(value) if value else None

    @property
    def PRELOAD_DATA(self):
        return self._preload_data

    @PRELOAD_DATA.setter
    def PRELOAD_DATA(self, value):
        self._set_preload_data(value)

    def _set_preload_data(self, value):
        if value is not None and not callable(value):
            raise TypeError(
                "The `preload_data` argument must be a callable that loads data into "
                "the database."
            )
        self._preload_data = value

    @property
    def PRELOAD_DATA_PATH(self):
        return self._preload_data_path

    @PRELOAD_DATA_PATH.setter
    def PRELOAD_DATA_PATH(self, value):
        self._set_preload_data_path(value)

    def _set_preload_data_path(self, value):
        self._preload_data_path = Path(value) if value else None

    @property
    def config_filename(self):
        return f"{self.SLUG}-config.json"

    @property
    def default_global_config_filepath(self):
        return DEFAULT_CONFIG_DIR / self.config_filename

    @property
    def default_config_filepaths(self):
        return [self.default_global_config_filepath]

    @property
    def config_filepaths(self):
        # Set config filepaths in increasing order of importance
        return [*self.default_config_filepaths, *self._custom_config_filepaths]

    def _read_config_json(self, config_path):
        # Read keys and values from a configuration JSON
        with config_path.open() as config_json:
            config_mapping = json.load(config_json)
        for key, value in config_mapping.items():
            setattr(self, key, value)


class InstanceBasedConfig(Config):
    """
    A base configuration object for app modes using instance directories.

    Notes
    -----
    Instance-based configurations will, by default, look for a database
    in the instance directory with a name derived from the app's slug.
    """

    # Flask app object configuration parameters
    TESTING = False

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
        self._instance_path = Path(instance_path)
        self._instance_path.mkdir(parents=True, exist_ok=True)
        super().__init__(
            import_name,
            app_name=app_name,
            db_path=db_path,
            preload_data=preload_data,
            preload_data_path=preload_data_path,
            custom_config_filepaths=custom_config_filepaths,
        )

    def _set_database(self, value):
        # Use a default instance-relative database path if not otherwise specified
        if value is None:
            value = self._instance_path / self.default_db_filename
        super()._set_database(value)

    @property
    def default_config_filepaths(self):
        # Include a config file in the instance path as a default configuration
        filepaths = super().default_config_filepaths
        if self.config_filename:
            filepaths.append(self._instance_path / self.config_filename)
        return filepaths

    @property
    def default_db_filename(self):
        return f"{self.SLUG}.sqlite"
