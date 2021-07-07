"""
Class for work with headers
"""
from indeedmodule import settings


class HeadersWork:
    def __init__(self):
        self.initialization_headers = dict()
        self.default_headers = settings.LOGIN_HEADERS
        self.make_headers()

    def set_headers(self, headers_data):
        for header in headers_data:
            pass

    def get_headers(self) -> dict:
        return self.initialization_headers

    def set_attribute_headers(self, key, value):
        self.initialization_headers[key] = value

    def make_headers(self):
        for header in self.default_headers:
            self.initialization_headers[header] = self.default_headers[header]
