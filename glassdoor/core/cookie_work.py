"""
Class for work with cookies
"""


class CookiesWork:

    def __init__(self):
        self.cookies_data: dict = dict()

    def set_cookies(self, data_cookies):
        for cookie in data_cookies.get_dict():
            self.set_attribute_cookies(cookie, data_cookies[cookie])

        print(self.cookies_data, 3500)

    def get_cookies(self) -> dict:
        return self.cookies_data

    def set_attribute_cookies(self, key: str, value: str):
        self.cookies_data[key] = value
