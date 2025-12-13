import re

from requests.models import Response


def only_successful(request: Response) -> bool:
    return request.response_code in [200, 304]


def no_star(request: Response) -> bool:
    return request.url != "*"


def no_plus_http(request: str) -> bool:
    return "+http" not in request.user_agent


def make_filters(regexes: re, excluded: list) -> list:

    def not_excluded_ip(request):
        return request.ip_address not in excluded

    def filter_url(request):
        for regex in regexes:
            if re.search(re.compile(regex), request.url) is not None:
                return True
        return False

    return [
        filter_url,
        only_successful,
        no_star,
        no_plus_http,
        not_excluded_ip,
    ]
