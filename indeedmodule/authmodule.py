"""
Module for authorization on the target resource.
"""
import config
from indeedmodule import settings
from indeedmodule.core.cookie_work import CookiesWork
from indeedmodule.core.headers_work import HeadersWork
from indeedmodule.requestmodule import RequestModule
from logsource.logmodule import LogModule


class AuthModule(LogModule):

    def __init__(self, order_id: str, data: dict, cookies_work: CookiesWork, headers_work: HeadersWork, api_worker,
                 proxy_worker, is_update_proxy):
        super().__init__()
        self.order_id = order_id
        self.user_name = data["user_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.login = data["login"]
        self.cookies_work = cookies_work
        self.headers_work = headers_work
        self.is_update_proxy = is_update_proxy
        self.api_worker = api_worker
        self.proxy_worker = proxy_worker
        self.delay_requests = config.DELAY_REQUESTS
        self.request = RequestModule(api_worker, proxy_worker, is_update_proxy, self.cookies_work, self.headers_work)

    def auth(self):
        # check password and email
        if not self.password or not self.login:
            return {"status": False}

        auth_data = self.request.auth_html()
        return {"status": False}
