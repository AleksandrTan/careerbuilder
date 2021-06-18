"""
Module for authorization on the target resource.
"""
from indeedmodule.core.cookie_work import CookiesWork
from indeedmodule.core.headers_work import HeadersWork


class AuthModule:

    def __init__(self, data: dict,  cookies_work: CookiesWork, headers_work: HeadersWork):
        self.user_name = data["user_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.email = data["email"]
        self.cookies_work = cookies_work
        self.headers_work = headers_work

    def auth(self):
        pass
