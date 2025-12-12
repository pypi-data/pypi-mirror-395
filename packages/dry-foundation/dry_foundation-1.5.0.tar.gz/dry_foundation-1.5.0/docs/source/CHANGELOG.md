# Changelog


## 1.0.0

- Initial release
  - This application was created by combining and adapting elements of both the [_Fuisce_](https://github.com/mitchnegus/fuisce/blob/main/CHANGELOG.md) and [_Authanor_](https://github.com/mitchnegus/authanor/blob/main/CHANGELOG.md) packages

### 1.0.1

- Extend the Python version range to include 3.13

### 1.0.2

- Catch errors where the application factory function may not exist

### 1.1.0

- Refactor views to enable compatibility with SQLAlchemy 2.0.39
- Allow the `Factory` to accept database interface parameters
- Use type annotations for declarative mappings
- Accommodate systems with pre-defined configurations when testing

### 1.2.0

- Allow handlers to pass subset selectors (e.g., offset and limit keywords) to the SQLAlchemy `Select` object

### 1.3.0

- Provide constructor arguments that facilitate passing Gunicorn configurations and configuration options to the launch mode

### 1.3.1

- Dispose of engine sessions (closing connections) after test contexts have completed
- Fix bug in `noxfile.py` format/linting checks

### 1.3.2

- Limit click version to (temporarily) handle [updates to default value processing introduced in version 8.3.0](https://github.com/pallets/click/blob/main/CHANGES.rst#version-830)

### 1.3.3

- Use `None` rather than `False` as the `echo_engine` keyword argument for database interfaces to better support sensible defaults

### 1.3.4

- Remove double query for acquiring authorized entries

### 1.4.0

- Generalize custom configuration parameters
- Add a configuration parameter for a preloadable data callable
- Improve generality of the app test manager configurations and fixup docstrings
- Set `TESTING` attribute to `False` as default for configurations

### 1.4.1

- Fix a bug assigning `preload_data_path` values to configurations

### 1.5.0

- Provide basic template global variables for injection as context processors
- Provide utilities for common user authorization tests
- Add the `TestRoutes` pytest-style test class for assisting with route endpoint tests
