from unittest import TestCase
from requests.models import Response
from src.access_logs_local_driver.process_download_logs import (
    make_filters,
    no_plus_http,
    no_star,
    only_successful,
)


class TestProcessDownLogs(TestCase):
    def setUp(self) -> None:
        self.modes = [
            {
                "measure": "https://test.test-eu.org/abc/downloads/v1",
                "name": "download",
                "regex": [
                    (
                        "https://abcdef.hijkl.info/articles/10.\\d{4,9}"
                        "/[-._;()/:a-zA-Z0-9]+/galley/\\d+/download"
                    )
                ],
            },
            {
                "measure": "tag:test.eu,2018:test:abc-html",
                "name": "htmlreader",
                "regex": [
                    (
                        "https://abcdef.hijkl.info/articles/10.\\d{4,9}/"
                        "[-._;()/:a-zA-Z0-9]+"
                    ),
                    (
                        "https://abcdef.hijkl.info/articles/abstract/10.\\"
                        "d{4,9}/[-._;()/:a-zA-Z0-9]+"
                    ),
                ],
            },
        ]
        self.spiders = (
            "user-agent=Mozilla/3.01Gold",
            "versus 0.2 (+http://testing.test.ch)",
            "versus crawler eda.testing@epfl.ch",
            "testing.nl - testing Bot/x.x",
            "testing/0.2",
            "testing",
            "test12345-hc/1.0",
            "test12345/1.0",
            "test12345/2.0 (http://www.testing.com/crawler.html)",
            "test12345/2.0 (http://www.testing.com/html/crawler.html)",
            "vspider",
            "vspider/3.x",
            "wadaino.jp-crawler 0.2 (http://testing.jp/)",
            "web-test12345 (Version: 1.02, powered by www.testing-test.de)",
            "web-test12345 (Version: 1.02, powered by www.web-test12345.de)",
            (
                "testing.org/test12345-0.9-dev (leveled playing field;"
                "http://test.org/; info at web2test.org)"
            ),
        )
        self.excluded_ips = '["8.8.8.8","9.9.9.9"]'
        self.excluded_urls = '["https://malformed_url.com"]'

    def test_only_successful_response(self):
        """Returns true for only 200 and 304 responses"""
        the_response = Response()
        the_response.response_code = 200
        self.assertTrue(only_successful(the_response))
        the_response.response_code = 304
        self.assertTrue(only_successful(the_response))
        the_response.response_code = 404
        self.assertFalse(only_successful(the_response))
        the_response.response_code = 302
        self.assertFalse(only_successful(the_response))

    def test_response_has_no_star(self):
        the_response = Response()
        the_response.url = "nice_url/"
        self.assertTrue(no_star(the_response))
        the_response.url = "*"
        self.assertFalse(no_star(the_response))

    def test_response_no_plus_http(self):
        the_response = Response()
        the_response.user_agent = "http"
        self.assertTrue(no_plus_http(the_response))
        the_response.user_agent = "+http"
        self.assertFalse(no_plus_http(the_response))

    def test_make_filters(self):
        """Check the make_filters method is successful with the
        modes sample and returns the deisred methods."""
        for mode in self.modes:
            filters = (
                make_filters(
                    mode["regex"], ["8.8.8.8", "9.9.9.9"], self.spiders
                ),
                mode["regex"],
            )
        self.assertTrue(len(filters) > 0)
        self.assertIn(only_successful, filters[0])
        self.assertIn(no_star, filters[0])
        self.assertIn(no_plus_http, filters[0])
