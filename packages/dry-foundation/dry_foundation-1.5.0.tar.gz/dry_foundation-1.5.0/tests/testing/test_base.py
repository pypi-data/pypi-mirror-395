"""Tests for the test manager and other basic objects."""

from unittest.mock import Mock

import pytest

from dry_foundation.testing import AuthActions, transaction_lifetime


class TestAppTestManager:
    """Tests for the ``AppTestManager`` object."""

    ephemeral_apps = []

    def test_nontransaction(self, app_test_manager, app):
        assert app is app_test_manager.persistent_app
        assert app is not app_test_manager.ephemeral_app

    @pytest.mark.parametrize("execution_count", range(3))
    @transaction_lifetime
    def test_transaction(self, app_test_manager, app, execution_count):
        assert app is not app_test_manager.persistent_app
        assert app is app_test_manager.ephemeral_app
        assert app not in self.ephemeral_apps
        self.ephemeral_apps.append(app)


class TestAuthActions:
    """Tests for the `AuthActions`` object."""

    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def _use_auth(cls):
        cls.mock_client = Mock()
        cls.auth = AuthActions(cls.mock_client)

    def test_login(self):
        self.auth.login("test_user", "test_password")
        self.mock_client.post.assert_called_once_with(
            "/auth/login", data={"username": "test_user", "password": "test_password"}
        )

    def test_logout(self):
        self.auth.logout()
        self.mock_client.get.assert_called_once_with("/auth/logout")
