"""
Class for work with cookies
"""
from indeedmodule import settings


class CookiesWork:

    def __init__(self):
        self.cookies_data: dict = dict()
        self.default_cookies = settings.LOGIN_COOKIES

    def set_cookies(self, data_cookies):
        for cookie in data_cookies.get_dict():
            self.set_attribute_cookies(cookie, data_cookies[cookie])

        print(self.cookies_data)

    def get_cookies(self) -> dict:
        return self.cookies_data

    def set_attribute_cookies(self, key: str, value: str):
        self.cookies_data[key] = value

    def init_login_cookies(self):
        self.cookies_data["device"] = self.default_cookies['device']
        self.cookies_data["fbredirect"] = self.default_cookies['fbredirect']
        self.cookies_data["APPLE_N"] = self.default_cookies["APPLE_N"]
        self.cookies_data["G_ENABLED_IDPS"] = self.default_cookies['G_ENABLED_IDPS']
        self.cookies_data["LANG"] = self.default_cookies['LANG']
        self.cookies_data["preExtAuthParams"] = self.default_cookies['preExtAuthParams']
        self.cookies_data["conf_snt"] = self.default_cookies['conf_snt']
        self.cookies_data["PPDM"] = self.default_cookies['PPDM']
