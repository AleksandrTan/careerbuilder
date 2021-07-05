"""
Module for authorization on the target resource.
"""
import sys
import time

from bs4 import BeautifulSoup as bs

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
        """
        Parse the login page, generate a form to submit a login,
        submit a form, set cookies and headers. Check for captcha.
        :return:
        """
        # check whether installed password and login
        if not self.password or not self.login:
            return {"status": False, "key": "no_auth_data", "data": dict()}

        # get login page
        sys.stdout.write(f"Get login form!\n")
        auth_data = self.request.auth_html(self.order_id)
        if auth_data["status"]:
            # get data for login form
            sys.stdout.write(f"Set login data!\n")
            submit_login_data = self.auth_page_analyze(auth_data["page_content"])
            if submit_login_data["status"]:
                time.sleep(config.DELAY_REQUESTS)
                # send form login
                sys.stdout.write(f"Submit login data!\n")
                send_form_status = self.send_login_form(submit_login_data["action_url"],
                                                        submit_login_data["login_data"])
                if send_form_status["status"]:
                    return True
                else:
                    return {"status": False, "key": "fail_send_login_form", "data": send_form_status["data"]}
            else:
                return {"status": False, "key": "fail_login_form", "data": submit_login_data}

        else:
            return {"status": False, "key": "fail_login", "data": auth_data}

    def auth_page_analyze(self, data) -> dict:
        """
        Parse the login page, generate a data to submit.
        :param data: str
        :return:
        """
        soup = bs(data, "html.parser")
        form_data = soup.find(settings.LOGIN_FORM_TAGS["parent_tag"], id=settings.LOGIN_FORM_TAGS["parent_id"])
        if form_data:
            input_hidden = form_data.find_all(settings.LOGIN_FORM_TAGS["input_tag_hidden"],
                                              type=settings.LOGIN_FORM_TAGS["input_tag_type_hidden"])
            if input_hidden:
                login_data = self.get_data(input_hidden)
                action_url = settings.TARGET_HOST_LOGIN + form_data["action"]

                return {"status": True, "login_data": login_data, "action_url": action_url}
            else:
                return {"status": False, "key": "fail_login_form"}
        else:
            return {"status": False, "key": "fail_login_form"}

    def send_login_form(self, action_url, login_data):
        """
        Submit a login form
        :return:
        """
        submit = self.request.submit_login(action_url, self.order_id, login_data)
        if submit["status"]:
            return {"status": True}

        return {"status": False, "key": "fail_login_form", "data": submit}

    def captcha_work(self):
        pass

    def get_data(self, input_hidden) -> dict:
        # prepare form data
        login_data: dict = dict()
        for data in input_hidden:
            login_data[data["name"]] = data.get("value", False)
        login_data[settings.LOGIN_FORM_TAGS["login_field"]] = self.login
        login_data[settings.LOGIN_FORM_TAGS["password_field"]] = self.password
        login_data["remember"] = 0

        return login_data


