"""
Module for authorization on the target resource.
"""
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
        # check password and email
        if not self.password or not self.login:
            return {"status": False, "key": "no_auth_data"}

        auth_data = self.request.auth_html(self.order_id)
        if auth_data["status"]:
            pass
        else:
            return auth_data

    def auth_page_analyze(self, data: str):
        """
        Parse the login page, generate a form to submit.
        :param data: str
        :return:
        """
        pass

    def send_login_form(self):
        """
        Submit a login form
        :return:
        """
        pass

    def captcha_work(self):
        pass

    def get_data(self, contents) -> dict:
        # prepare form data
        form = dict()
        soup = bs(contents["message"], "html.parser")
        form["firstname"] = self.user_name
        form["lastname"] = self.last_name
        form["email"] = self.email
        form["cv_data"] = "SGVsbG8hCg=="
        form["cv_file_name"] = self.file_name
        form["upload_file"] = open(config.BASE_DIR + '/tmp/' + self.file_name, "rb")
        form["ai_resume_builder"] = False
        form["dropbox_cv_url"] = ''
        form["copy_paste"] = ''
        # set authenticity_token param
        authenticity_token_name = soup.find(settings.TARGET_FORM["authenticity_token"]["tag"],
                                            attrs={
                                                "name": settings.TARGET_FORM["authenticity_token"]["name_param"]
                                            }).get("content")
        authenticity_token_value = soup.find(settings.TARGET_FORM["authenticity_token"]["tag"],
                                             attrs={
                                                 "name": settings.TARGET_FORM["authenticity_token"]["name_value"]
                                             }).get("content")
        form[authenticity_token_name] = authenticity_token_value
        # set url param
        url = soup.find(settings.TARGET_FORM["parent_tag"],
                        attrs={"class": settings.TARGET_FORM["parent_class"]}).get("action")
        if config.TEST_MODE == "True":
            url = settings.TEST_HOST + url
        else:
            url = settings.TARGET_HOST + url

        return {"form": form, "url": url}


