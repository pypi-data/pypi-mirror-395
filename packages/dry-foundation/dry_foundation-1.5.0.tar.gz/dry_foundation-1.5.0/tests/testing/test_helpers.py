"""Tests for testing helper objects."""

from unittest.mock import Mock, PropertyMock, patch

import pytest
from flask.testing import FlaskClient

from dry_foundation.testing.helpers import TestRoutes as _TestRoutes

TEST_HTML = b"""
    <html>
      <title>Title</title>
      <h1>Heading 1</h1>
      <h2>Heading 2</h2>

      <div>one</div>
      <div>none</div>
      <div>done</div>

      <div id="block">
        <a href="http://github.com">GitHub</a>
        <span>Information</span>
      </div>

      <form id="data">
        <input class="data-value" name="name" value="test"/>
      </form>
    </html>
    """


class MockResponse:
    data = TEST_HTML


class TestRoutesHelper(_TestRoutes):
    """A class for testing the ``TestRoutes`` test class."""

    @pytest.fixture
    def mock_client(self):
        with patch.object(_TestRoutes, "client", new_callable=PropertyMock):
            self.client.get.return_value = MockResponse
            self.client.post.return_value = MockResponse
            yield

    @pytest.fixture
    def mock_get_request(self, mock_client):
        self.get_route("/mock/route")

    def test_client(self):
        assert isinstance(self.client, FlaskClient)

    def test_get_route(self, mock_client):
        self.get_route("/mock/route")
        assert self.active_response.response == MockResponse

    @patch.object(_TestRoutes, "blueprint_prefix", new="prefixed")
    def test_get_route_alternate_prefix(self, mock_client):
        self.get_route("/mock/route")
        assert self.active_response.response == MockResponse
        self.client.get.assert_called_once_with("/prefixed/mock/route")

    @patch.object(MockResponse, "data", new=b'["<html></html>","<html></html>"]')
    def test_get_route_soup_list(self, mock_client):
        self.get_route("/mock/route")
        assert isinstance(self.html, list)
        assert isinstance(self.soup, list)

    @patch.object(MockResponse, "data", new=b"null")
    def test_get_route_soup_none(self, mock_client):
        self.get_route("/mock/route")
        assert self.html is None
        assert self.soup is None

    def test_post_route(self, mock_client):
        self.post_route("/mock/route", data=Mock())
        assert self.active_response.response == MockResponse

    def test_page_title_includes_substring(self, mock_get_request):
        self.page_title_includes_substring("Title")

    @pytest.mark.parametrize(
        ("substring", "level"),
        [("Heading 1", "h1"), ("Heading 2", "h2")],
    )
    def test_page_heading_includes_substring(self, mock_get_request, substring, level):
        self.page_heading_includes_substring(substring, level=level)

    def test_tag_count_is_equal(self, mock_get_request):
        assert self.tag_count_is_equal(3, "div", string=self.match_substring("one"))

    def test_tag_exists(self, mock_get_request):
        assert self.tag_exists("div", string="done")

    def test_tag_exists_invalid(self):
        with (
            patch.object(
                _TestRoutes, "soup", new_callable=PropertyMock, return_value=None
            ),
            pytest.raises(RuntimeError),
        ):
            self.tag_exists("div", string="done")

    def test_anchor_exists(self, mock_get_request):
        assert self.anchor_exists(href="http://github.com")

    def test_div_exists(self, mock_get_request):
        assert self.div_exists(id="block")

    def test_span_exists(self, mock_get_request):
        assert self.span_exists(string="Information")

    def test_form_exists(self, mock_get_request):
        assert self.form_exists(id="data")

    def test_input_exists(self, mock_get_request):
        assert self.input_exists(class_="data-value")

    def test_input_has_value(self, mock_get_request):
        assert self.input_has_value("test")

    def test_match_substring(self):
        # Create a filter to test for the string "one"
        match_filter = self.match_substring("one")
        match_filter("lonely")

    def test_match_substring_invalid(self):
        # Create a filter to test for the string "one"
        match_filter = self.match_substring("one")
        with pytest.raises(TypeError):
            match_filter(None)
