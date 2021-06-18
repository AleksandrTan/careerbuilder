"""
Class for work with cookies
"""
from indeedmodule import settings


class CookiesWork:

    def __init__(self):
        self.cookies_data: dict = dict()
        self.default_cookies = settings.LOGIN_COOKIES
        self.init_login_cookies()

    def get_cookies(self) -> dict:
        return self.cookies_data

    def set_attribute_cookies(self, key, value):
        self.cookies_data[key] = value

    def init_login_cookies(self):
        self.default_cookies["device"] = self.default_cookies['device']
        self.default_cookies["fbredirect"] = self.default_cookies['fbredirect']
        self.default_cookies["APPLE_N"] = self.default_cookies["APPLE_N"]
        self.default_cookies["G_ENABLED_IDPS"] = self.default_cookies['G_ENABLED_IDPS']
        self.default_cookies["LANG"] = self.default_cookies['LANG']
        self.default_cookies["preExtAuthParams"] = self.default_cookies['preExtAuthParams']
        self.default_cookies["conf_snt"] = self.default_cookies['conf_snt']
        self.default_cookies["PPDM"] = self.default_cookies['PPDM']

