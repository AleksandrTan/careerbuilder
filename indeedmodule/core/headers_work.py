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
        print(headers_data)

    def get_headers(self) -> dict:
        return self.initialization_headers

    def set_attribute_headers(self, key, value):
        self.initialization_headers[key] = value

    def make_headers(self):
        self.initialization_headers["Accept"] = self.default_headers['Accept']
        self.initialization_headers["Accept-Encoding"] = self.default_headers['Accept-Encoding']
        self.initialization_headers["Accept-Language"] = self.default_headers["Accept-Language"]
        self.initialization_headers["Cache-Control"] = self.default_headers['Cache-Control']
        self.initialization_headers["Connection"] = self.default_headers['Connection']
        self.initialization_headers["Host"] = self.default_headers['Host']
        self.initialization_headers["Pragma"] = self.default_headers['Pragma']
        self.initialization_headers["Referer"] = self.default_headers['Referer']
        self.initialization_headers["sec-ch-ua"] = self.default_headers['sec-ch-ua']
        self.initialization_headers["sec-ch-ua-mobile"] = self.default_headers['sec-ch-ua-mobile']
        self.initialization_headers["Sec-Fetch-Dest"] = self.default_headers['Sec-Fetch-Dest']
        self.initialization_headers["Sec-Fetch-Mode"] = self.default_headers['Sec-Fetch-Mode']
        self.initialization_headers["Sec-Fetch-Site"] = self.default_headers['Sec-Fetch-Site']
        self.initialization_headers["Sec-Fetch-User"] = self.default_headers['Sec-Fetch-User']
        self.initialization_headers["Upgrade-Insecure-Requests"] = self.default_headers['Upgrade-Insecure-Requests']
        self.initialization_headers["User-Agent"] = self.default_headers['User-Agent']

