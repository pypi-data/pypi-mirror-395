from datetime import date, datetime
import ipaddress
from logging import getLogger
import re
import sys
from typing import Iterator, IO

import urllib.error
import urllib.parse


logger = getLogger(__name__)

LOG_REGEXES = {
    "apache": (
        r"(?P<ip_address>\d+\.\d+\.\d+\.\d+) "
        r"(?P<users>.+ .+) "
        r"\[(?P<timestamp>.+)\] "
        r'"(?P<request>.+)" '
        r"(?P<status_code>\d+) "        
        r"(?P<sent_bytes>\d+) "         
        r'(?P<referer>".+") '
        r'"(?P<user_agent>.+)"'
    ),
    "aws_alb": (  # AWS Application Load Balancer
        r"[^ ]+ "                           # type (e.g. h2)
        r"(?P<timestamp>[^ ]+) "            
        r"[^ ]+ "                           # elb_id
        r"(?P<ip_address>[^:]+):[^ ]+ "     # client:port (Capture IP only)
        r"[^ ]+ "                           # target:port
        r"[^ ]+ [^ ]+ [^ ]+ "               # processing times
        r"(?P<status_code>\d+) "            # elb_status_code
        r"[^ ]+ [^ ]+ "                     # target_status_code received_bytes
        r"(?P<sent_bytes>\d+) "             
        r"\"(?P<request>[^\"]+)\" "         
        r"\"(?P<user_agent>[^\"]+)\" "      
        r".*"                               # Ignore the rest (ssl, arn, etc)
    )
}


class Request:
    """Represent the data in a single line of the Apache log file."""

    def __init__(
            self,
            ip_address: str,
            url_prefix: str,
            url: str,
            response_code: int,
            content_length: int,
            timestamp: datetime,
            user_agent: str,
    ):
        self.ip_address = ip_address
        self.timestamp = timestamp
        self.user_agent = user_agent or ""
        self.url = self.parse_url(url, url_prefix)
        self.response_code = response_code
        self.content_length = content_length

    def parse_url(self, url: str, url_prefix: str) -> str:
        try:
            if url.startswith("http"):
                return url_prefix + urllib.parse.urlparse(url).path.lower()
            return self.normalise_url(url_prefix + url.lower())
        except ValueError:
            raise ValueError(f"Error parsing: {url}, {sys.stderr}")

    @staticmethod
    def normalise_url(url: str) -> str:
        try:
            return url[:-1] if url[-1] == "/" else url
        except IndexError as err:
            raise IndexError(f"Error parsing: {url}, {err}")

    def fmttime(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"Request {self.fmttime()}, {self.ip_address}, {self.url}"

    def __iter__(self):
        for _item in self.as_tuple():
            yield _item

    def as_tuple(self) -> tuple[str, str, str, str]:
        return self.fmttime(), self.ip_address, self.url, self.user_agent

    def sanitise_url(self, regexes: str) -> None:
        for regex in regexes:
            matched = re.search(re.compile(regex), self.url)
            if matched is not None:
                self.url = matched.group(0)
                break


class LogProcessor:
    """Consumes an open file stream, parses lines, applies filters,
    and yields Request objects.
    """

    def __init__(
            self,
            filter_groups: list,
            url_prefix: str,
            start_date: str,
            end_date: str,
            log_type: str = "apache",
            log_re_pattern: str | None = None,
    ) -> None:
        self.filter_groups = filter_groups
        self.url_prefix = url_prefix
        self.start_date = date.fromisoformat(start_date)
        self.end_date = date.fromisoformat(end_date)

        self.log_regex_patterns = LOG_REGEXES
        self.log_type = log_type
        self._set_log_regex(log_type, log_re_pattern)

    def _set_log_regex(self, log_type: str, log_pattern) -> None:
        """Attempt to determine regex pattern to use based on log type."""
        if log_type is None:
            self.log_regex = None
            return None
        elif log_type in LOG_REGEXES:
            log_pattern = LOG_REGEXES[log_type]
        elif log_type == "custom":
            if not log_pattern:
                ValueError(
                    f"`log_re_pattern` must be specified for "
                    f"`log_type` value 'custom'."
                )

        self.log_regex = re.compile(log_pattern)
        return None

    def _determine_log_regex(self, line: str) -> tuple:
        """Determine the regex pattern that matches the log line. If no pattern
        matches, raises a ValueError.

        Args:
            line (str): Log line to match against the registered regex patterns.

        Raises:
            ValueError: If no regex pattern matches the log line.

        Returns:
            tuple: The regex pattern that matches the given log line.
        """
        for log_type, log_pattern in self.log_regex_patterns.items():
            match = re.search(log_pattern, line)
            if match:
                return log_type, log_pattern
        else:
            raise ValueError(
                f"No regex patterns found that match the format of the log file. "
                f"Please set a custom regex pattern."
            )

    def process(self, file_stream: IO[str]) -> Iterator[tuple]:
        """Takes a file-like object (text mode), iterates it, and yields
         filtered results.
        """
        for line in file_stream:
            if isinstance(line, bytes):  # Handle mixed bytes/string input.
                line = line.decode("utf-8")

            if line := line.strip():
                request_obj = self._parse_line(line)
                if request_obj:
                    for filter_group in self.filter_groups:
                        measure_uri, filters, regex = filter_group

                        if self._apply_filters(filters, request_obj):
                            request_obj.sanitise_url(regex)
                            yield measure_uri, request_obj
                            break  # only allow one measure to match per line

    def _parse_line(self, line: str) -> Request | None:
        """Internal method to match regex and create a Request object"""
        if not self.log_regex:
            self.log_type, log_pattern = self._determine_log_regex(line)
            self._set_log_regex(self.log_type, log_pattern)

        match = self.log_regex.search(line)
        data = match.groupdict()

        try:
            if self.log_type == "apache":
                timestamp = datetime.strptime(
                    data.pop("timestamp"),
                    "%d/%b/%Y:%H:%M:%S %z"
                )
            elif self.log_type == "aws_alb":
                ts_str = data.pop("timestamp")
                timestamp = datetime.fromisoformat(ts_str)
            else:
                logger.error(
                    f"Log type {self.log_type} is not currently supported."
                )  # TODO: Add support for custom timestamp format.
                raise ValueError("Invalid log type")
        except ValueError:
            return None

        if not self.start_date <= timestamp.date() <= self.end_date:
            return None

        user_agent = data.get("user_agent", "-")
        ip = data.pop("ip_address")
        if not self._validate_ip(ip):
            return None

        if url := self._validate_request(data.pop("request")):
            return Request(
                ip_address=ip,
                url_prefix=self.url_prefix,
                url=url,
                response_code=int(data["status_code"]),
                content_length=int(data["sent_bytes"]),
                timestamp=timestamp,
                user_agent=user_agent,
            )

    @staticmethod
    def _apply_filters(filters, request_obj) -> bool:
        return all(f(request_obj) for f in filters)

    @staticmethod
    def _validate_request(request_str):
        parts = request_str.split()
        if len(parts) == 3:
            return parts[1]
        return None

    @staticmethod
    def _validate_ip(ip_address_str):
        """Validates whether the string is a valid IPv4 or IPv6 address."""
        try:
            ipaddress.ip_address(ip_address_str)
            return True
        except ValueError:
            return False  # TODO: fix country code for IP6 Addresses
