import gzip
import os
import pathlib as pl
from unittest import TestCase

from src.access_logs_local_driver import LogStream
from src.access_logs_local_driver import (
    make_filters
)


class TestLogData(TestCase):
    def setUp(self) -> None:
        self.modes_cjs = [
            {
                "measure": "https://testing.test-eu.org/abc/downloads/v1",
                "name": "download",
                "regex": [
                    (
                        "https://abc.test.testing/testing-url/10.\\d{4,9}/"
                        "[-._;()/:a-zA-Z0-9]+/galley/\\d+/download"
                    )
                ],
            },
            {
                "measure": "tag:testing.eu,2023:readership:abc-html",
                "name": "htmlreader",
                "regex": [
                    (
                        "https://abc.test.testing/testing-url/10.\\d{4,9}/"
                        "[-._;()/:a-zA-Z0-9]+"
                    ),
                    (
                        "https://abc.test.testing/testing-url/abstract/10.\\d"
                        "{4,9}/[-._;()/:a-zA-Z0-9]+"
                    ),
                ],
            },
        ]
        self.modes_nginx = [
            {
                "measure": "https://testing.test-eu.org/abc/v1",
                "name": "download",
                "regex": [
                    "https://abc.test.testing/test" "[-._;()/:a-zA-Z0-9]+"
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
        self.file_log_apache = "test_access.log-20230602.gz"
        self.file_log_nginx = "test_access.log-20230705.gz"
        self.cache_dir = "tests/files/"
        self.logs_files = self.cache_dir + "logs_test/"
        self.url_prefix = "https://abc.test.testing"

    def tearDown(self):
        """Check whether the file has been created by any test and
        delete them, useful when running tests separately."""
        if self.file_exists(self.logs_files + self.file_log_apache):
            os.remove(self.logs_files + self.file_log_apache)
        if self.file_exists(self.logs_files + "test_access.log-NODATE.gz"):
            os.remove(self.logs_files + "test_access.log-NODATE.gz")
        if self.file_exists(self.logs_files + self.file_log_nginx):
            os.remove(self.logs_files + self.file_log_nginx)

    def create_file_log(self, file_name, content):
        file = gzip.open(self.logs_files + file_name, "wb")
        file.write(content)
        file.close()

    def file_exists(self, path):
        if not pl.Path(path).resolve().is_file():
            return False
        return True

    def test_apache_log_stream_creates_is_succesful_one_match_cjs(self) -> None:
        """Test the class LogStream the same way as is executed
        from the plugin"""
        start_date = '2023-06-01'
        end_date = '2023-06-03'
        content = str.encode(
            "cjs.testing-url.com:123 12.90.253.37 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.3456768/cjs.abcde.1234/image/1234/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)
        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        result = result.return_output()
        # Assert the result has got the right content
        self.assertEqual(
            result[0][0],
            'tag:testing.eu,2023:readership:abc-html',
        )
        self.assertEqual(
            str(result[0][1]),
            (
                "Request 2023-06-02 04:55:37, 12.90.253.37, "
                "https://abc.test.testing/testing-url/10.3456768"
                "/cjs.abcde.1234/image/1234/download"
            )
        )

    def test_apache_log_stream_creates_is_succesful_two_matches_cjs(
        self
    ) -> None:
        """Test the class LogStream the same way as is executed
        from the plugin"""
        start_date = '2023-06-01'
        end_date = '2023-06-02'
        content = str.encode(
            "cjs.testing-url.com:123 12.34.253.12 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.3456768/cjs.abcde.1234/image/1234/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"\n'
            "cjs.testing-url222.com:123 34.34.253.34 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.56789/cjs.fghijk/testing/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"\n'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)
        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        result = result.return_output()
        # Assert the result has got the right content
        self.assertEqual(
            result[0][0],
            'tag:testing.eu,2023:readership:abc-html',
        )
        self.assertEqual(
            str(result[0][1]),
            (
                'Request 2023-06-02 04:55:37, 12.34.253.12, '
                'https://abc.test.testing/testing-url/10.3456768/cjs'
                '.abcde.1234/image/1234/download'
            )
        )
        self.assertEqual(
            result[1][0],
            'tag:testing.eu,2023:readership:abc-html',
        )
        self.assertEqual(
            str(result[1][1]),
            (
                'Request 2023-06-02 04:55:37, 34.34.253.34, '
                'https://abc.test.testing/testing-url/10.56789/cjs.'
                'fghijk/testing/download'
            )
        )

    def test_apache_log_start_date_and_end_date_no_match(self) -> None:
        """Test the class LogStream the same way as is executed
        from the plugin"""
        start_date = '2023-05-01'
        end_date = '2023-05-21'
        content = str.encode(
            "cjs.testing-url.com:123 12.90.253.37 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.3456768/cjs.abcde.1234/image/1234/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)
        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        # Assert the result has got the right content
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_no_match_file_structure_is_ok(self) -> None:
        """Test no match with the current filters even if
        the file structure is fine, will return empty list."""
        start_date = '2023-06-01'
        end_date = '2023-06-03'
        content = str.encode(
            "abcdef.tyestset.com:123 12.34.253.37 - - "
            '[03/Jun/2023:04:51:45 +0000] "GET /test'
            '/test/12.3456/abc.v12a1.1234/ HTTP/1.1" '
            '200 49221 "-" "test/5.0 (Windows NT 10.0; '
            'Win64; x64; ab:123.4) test/20100101 test/112.0"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)
        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_raises_error_no_matches_timestamp(self) -> None:
        """Test the class LogStream fails because there is no match.
        The file test_access.log-NODATE.gz should have a date
        at the end."""
        start_date = '2023-06-02'
        end_date = '2023-06-03'
        content = str.encode(
            "abcdef.presstest.com:123 12.12.345.67 - - "
            '[03/Jun/2023:04:51:45 +0000] "GET /articles/'
            'abstract/12.3456/abc.v12a1.1234/ HTTP/1.1" 200 '
            '49221 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; '
            'x64; ab:123.4) Gecko/12345678 Firefox/112.0"'
        )
        self.create_file_log(self.file_log_apache, content)
        os.rename(
            self.logs_files + self.file_log_apache,
            self.logs_files + "test_access.log-NODATE.gz",
        )
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        with self.assertRaises(AttributeError) as err:
            result = LogStream(
                self.logs_files,
                filter_groups,
                self.url_prefix,
                start_date,
                end_date
            )
            result = result.return_output()
        self.assertEqual(
            str(err.exception),
            "Your file has to have a date at the end of its name"
        )

    def test_apache_log_stream_raises_error_no_matches_lines(self) -> None:
        """Test the class LogStream fails because there is no match.
        The line method will raise exception because the structure of
        the input file is wrong."""
        start_date = '2023-06-02'
        end_date = '2023-06-04'
        content = b'test_worng - wrong structure"'
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_no_match_request_is_wrong_right_structure(
        self
    ) -> None:
        start_date = '2023-06-03'
        end_date = '2023-06-04'
        """Test the class LogStream there is no match.
        The file structure is right but the request is wrong."""
        content = str.encode(
            "abcdef.presstest.com:123 12.34.253.37 - - "
            '[03/Jun/2023:04:51:45 +0000] "ERROR /articles/'
            'abstract/12.3456/abc.v12a1.1234/ HTTP/1.1" 200 '
            '49221 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; '
            'x64; ab:123.4) Gecko/12345678 Firefox/112.0"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_raises_error_there_is_no_timestamp(self) -> None:
        """Test the class LogStream there is no match because of
        missing timestamp."""
        start_date = '2023-06-03'
        end_date = '2023-06-04'
        content = str.encode(
            "abcdef.presstest.com:123 12.12.345.67 - - 'NO TIMESTAMP ' GET "
            "/articles/abstract/12.3456/abcdef.v52i2.8160/ "
            'HTTP/1.1" 200 4522 "-" "Scoop.it"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_wrong_request_and_wrong_structure_raises_error(
        self,
    ) -> None:
        start_date = '2023-06-03'
        end_date = '2023-06-04'
        """Test the class LogStream fails because there is no match.
        The file structure is wrong and the request is wrong."""
        content = str.encode(
            "abcdef.presstest.com:123 146.249.11.3 - - "
            "[02/Jun/2023:08:18:56 +0000] --->ErrorHEADtest "
            '"-" "Scoop.it"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_no_matches_line_r_n_ua_re(self) -> None:
        """Test the class LogStream fails because there is no match.
        The content of the files doesn't match r_n_ua_re regex."""
        start_date = '2023-06-01'
        end_date = '2023-06-02'
        content = str.encode(
            "abcdef.presstest.com:123 12.34.253.37 - - "
            '[01/Jun/2023:06:52:43 +0000] "GET /jms/public'
            '/journals/1/journalFavicon_en_US.ico HTTP/1.1" 404 '
            '5010 "test error!"test error!"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_ignores_reuqest_if_its_missing_parts(
        self
    ) -> None:
        """Test the class LogStream ignores urls that have a missing method,
        url or version."""
        start_date = '2023-06-01'
        end_date = '2023-06-02'
        content = str.encode(
            "abc.presstest.com:123 12.34.253.37 - - "
            '[01/Jun/2023:06:52:43 +0000] "GET /jms/public'
            '/journals/1/journalFavicon_en_US.ico" 404 5010 '
            '"https://abc.defg.info/'
            'abc.v52i2.8023/" "Mozilla/5.0 (Linux; Android 10; K) '
            "Appltest_log_stream_ignores_reuqest_if_its_missing_parts"
            "eWebKit/537.36 (KHTML, like Gecko) Chrome/"
            '113.0.0.0 Mobile Safari/537.36"abc.presstest.'
            "com:123 12.12.345.67 - - [01/Jun/2023:06:52:50 +0000] "
            '"GET /jms/public/journals/1/journalFavicon_en_US.ico" '
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_log_stream_the_ip_address_is_wrong_no_match(
        self,
    ) -> None:
        """Test the class LogStream fails because there is no match.
        The file structure is wrong and the request is wrong."""
        start_date = '2023-06-01'
        end_date = '2023-06-02'
        content = str.encode(
            "cjs.testing-url.com:123 99.999.999.999 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.3456768/cjs.abcde.1234/image/1234/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_apache_logs_no_matches_start_date_wrong_file(self):
        """The search date is in august and the file name is in June."""
        start_date = '2023-08-01'
        end_date = '2023-08-02'
        content = str.encode(
            "cjs.testing-url.com:123 12.90.253.37 - - "
            '[02/Jun/2023:04:55:37 +0000] "GET /testing-url/'
            "10.3456768/cjs.abcde.1234/image/1234/download/ "
            'HTTP/1.1" 200 123456 "https://www.google.com/" '
            '"Mozilla/5.0 (Linux; Android 13; testPhone ABCDEF) '
            "TestPhone/123.45 (KHTML, like Gecko) TestBrowser"
            '/21.0 Chrome/120.3.4567.890 Mobile Safari/537.36"'
        )
        self.create_file_log(self.file_log_apache, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual(result.return_output(), [])

    def test_nginx_logs_is_successful_two_matches(self):
        """Test the nginx logs are processed as well
        the four lines will be matched."""
        start_date = '2023-07-05'
        end_date = '2023-07-06'
        content = str.encode(
            '25.123.123.1 - - [06/Jul/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
            '25.123.123.2 - - [06/Jul/2023:15:49:29 +0000] "GET '
            '/test/books/e/10.5334/bbc HTTP/1.0" 200 547 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 "'
            "prüfen/123.1\n"
            '25.123.123.3 - - [06/Jul/2023:20:15:19 +0000] "GET '
            '/test-query HTTP/1.0" 404 502 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
            '25.123.123.4 - - [06/Jul/2023:21:23:18 +0000] "GET '
            '/test/10.5334/bay HTTP/1.0" 200 496 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 '
            'prüfen/123.1"'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        result = result.return_output()
        self.assertEqual(
            result[0][0],
            'https://testing.test-eu.org/abc/v1'
        )
        self.assertEqual(
            str(result[0][1]),
            (
                'Request 2023-07-06 15:49:29, 25.123.123.2, '
                'https://abc.test.testing/test/books/e/10.5334/bbc'
            )
        )
        self.assertEqual(
            result[1][0],
            'https://testing.test-eu.org/abc/v1'
        )
        self.assertEqual(
            str(result[1][1]),
            (
                'Request 2023-07-06 21:23:18, 25.123.123.4, '
                'https://abc.test.testing/test/10.5334/bay'
            )
        )

    def test_nginx_logs_no_matches_line_r_n_ua_re(self):
        """Test the nginx logs are processed as well
        the four lines will be matched."""
        start_date = '2023-07-05'
        end_date = '2023-07-07'
        content = str.encode(
            '25.123.123.1 - - [06/Jul/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"WrongTESTUSERAGENT"\n'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual(result.return_output(), [])

    def test_nginx_logs_no_matches_start_date_wrong_file(self):
        """The search date is in august and the file name is in July."""
        start_date = '2023-07-31'
        end_date = '2023-08-02'
        content = str.encode(
            '25.123.123.1 - - [06/Jul/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual(result.return_output(), [])

    def test_nginx_logs_no_matches_start_date_wrong_line(self):
        """The search date is in July and the line is in august."""
        start_date = '2023-07-06'
        end_date = '2023-07-07'
        content = str.encode(
            '25.123.123.1 - - [06/Aug/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual(result.return_output(), [])

    def test_nginx_log_stream_no_match_file_structure_is_ok(self) -> None:
        """Test the nginx logs are processed as well
        the four lines will be matched."""
        start_date = '2023-07-06'
        end_date = '2023-07-07'
        content = str.encode(
            '25.123.123.1 - - [06/Jul/2023:15:04:34 +0000] "GET '
            'NOMATCH/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
            '25.123.123.2 - - [06/Jul/2023:15:49:29 +0000] "GET '
            '/NOMATCH/books/e/10.5334/bbc HTTP/1.0" 200 547 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 "'
            "prüfen/123.1\n"
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual(result.return_output(), [])

    def test_nginx_log_stream_no_match_request_is_wrong_right_structure(
        self
    ) -> None:
        """Test the class LogStream there is no match.
        The file structure is right but the request is wrong."""
        start_date = '2023-07-06'
        end_date = '2023-07-07'
        content = str.encode(
            '25.123.123.3 - - [06/Jul/2023:20:15:19 +0000] "ERROR '
            '/test-query HTTP/1.0" 404 502 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
            '25.123.123.4 - - [06/Jul/2023:21:23:18 +0000] "WRONG REQUEST '
            '/test/10.5334/bay HTTP/1.0" 200 496 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 '
            'prüfen/123.1"'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_nginx_log_stream_raises_error_there_is_no_timestamp(self) -> None:
        """Test the class LogStream there is no match because of
        missing timestamp."""
        start_date = '2023-07-06'
        end_date = '2023-07-07'
        content = str.encode(
            '25.123.123.3 - - NO TIMESTAMPP "GET '
            '/test-query HTTP/1.0" 404 502 "-" '
            '"Mozitest (http://Moziddler.io/about)"'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_nginx:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_nginx_log_stream_no_match_wrong_request_and_structure_raises_error(
        self,
    ) -> None:
        start_date = '2023-07-06'
        end_date = '2023-07-07'
        """Test the class LogStream fails because there is no match.
        The file structure is wrong and the request is wrong."""
        content = str.encode(
            '146.249.11.159 - - [06/Jul/2023:21:23:18 +0000] ----> ERRORRR'
            '/wrong/10.5334/bay HTTP/1.0" 200 496 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 '
            'prüfen/123.1"'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_nginx_log_stream_the_ip_address_is_wrong_will_raise_error(
        self,
    ) -> None:
        start_date = '2023-07-05'
        end_date = '2023-07-07'
        """Test the class LogStream fails because there is no match.
        The file structure is wrong and the request is wrong."""
        content = str.encode(
            '999.999.999.999 - - [06/Jul/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"'
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())

    def test_nginx_log_stream_the_start_date_and_end_date_no_match(
        self,
    ) -> None:
        start_date = '2023-07-01'
        end_date = '2023-07-02'
        """Test the class LogStream fails because there is no match.
        The file structure is wrong and the request is wrong."""
        content = str.encode(
            '25.123.123.1 - - [06/Jul/2023:15:04:34 +0000] "GET '
            '/test.txt HTTP/1.0" 302 555 "-" '
            '"Mozitest (http://Moziddler.io/about)"\n'
            '25.123.123.2 - - [06/Jul/2023:15:49:29 +0000] "GET '
            '/test/books/e/10.5334/bbc HTTP/1.0" 200 547 "-" '
            '"Ozitest/7.7 (X11; Xunil x86_64; rh:123.1) SalaTest/20100101 "'
            "prüfen/123.1\n"
        )
        self.create_file_log(self.file_log_nginx, content)
        filter_groups = []
        for mode in self.modes_cjs:
            filters = (
                mode.get("measure"),
                make_filters(
                    mode.get("regex"),
                    ["8.8.8.8", "9.9.9.9"],
                    self.spiders
                ),
                mode.get("regex")
            )
            filter_groups.append(filters)

        result = LogStream(
            self.logs_files,
            filter_groups,
            self.url_prefix,
            start_date,
            end_date
        )
        self.assertEqual([], result.return_output())
