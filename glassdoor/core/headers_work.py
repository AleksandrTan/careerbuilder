"""
Class for work with headers
"""


class HeadersWork:
    def __init__(self):
        self.initialization_headers = dict()
        self.make_headers()

    def set_headers(self, headers_data):
        for header in headers_data:
            pass

    def get_headers(self) -> dict:
        return self.initialization_headers

    def set_attribute_headers(self, key, value):
        self.initialization_headers[key] = value

    def make_headers(self):
        pass
