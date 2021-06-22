"""
Module for working with requests to a target resource
"""
import os
import time
import zipfile

from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from indeedmodule import settings
import config
from apimodule.proxy_work import ProxyWork


class RequestModule(LogModule):

    def __init__(self, api_worker, proxy_worker: ProxyWork, is_update_proxy: bool, cookies_work, headers_work):
        super().__init__()
        self.is_update_proxy = is_update_proxy
        self.api_worker = api_worker
        self.proxy_worker = proxy_worker
        self.number_attempts = config.NUMBER_REQUESTS
        self.cookies_work = cookies_work
        self.headers_work = headers_work

    def get_chromedriver(self, use_proxy=False, user_agent=None):
        """
        Used proxy for Selenium Chrome Driver.
        Can not work with "--headless"
        :param use_proxy:
        :param user_agent:
        :return:
        """
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", self.proxy_worker.get_manifest_json())
                zp.writestr("background.js", self.proxy_worker.get_background_js())
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % settings.LOGIN_HEADERS["User-Agent"])
            # chrome_options.add_argument("--headless") not work
        driver = webdriver.Chrome(chrome_options=chrome_options)

        return driver

    def auth_selenium(self):
        browser = self.get_chromedriver(use_proxy=True, user_agent=True)
        browser.get(settings.LOGIN_PAGE)
        html = browser.page_source
        print(html, browser)

    def auth_html(self):
        session = HTMLSession()
        print(self.proxy_worker.get_proxy_dict())
        session.proxies = self.proxy_worker.get_proxy_dict()
        session.headers = self.headers_work.get_headers()
        cookies = self.cookies_work.get_cookies()
        response = session.get(settings.LOGIN_PAGE, cookies=cookies)
        response.html.render()
        data = response.html.html
        # print(data)

    def get_content(self, link: str, order_id: str):
        """
        Request page content for a given links.
        If the request status is 403,
        it requests an updated proxy server from the system api.
        :param order_id: str
        :param link: str
        :return: None
        """
        count: int = 0
        session = HTMLSession()
        session.proxies = self.proxy_worker.get_proxy_dict()
        session.headers = settings.LOGIN_HEADERS
        cookies = self.cookies_work.get_cookies()
        while count < self.number_attempts:
            try:
                response = session.get(link, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT), cookies=cookies)
                session.close()
            except requests.exceptions.ConnectionError as error:
                self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": '',
                                                                     "order": order_id})

                return {"status": False, "error": True, "status_code": '0', "message": error.__repr__(),
                        "type_res": "request_module", "proxy": tuple([self.proxy_worker.get_proxy_id(),
                                                                      self.proxy_worker.get_proxy_dict()])}
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                if response.status_code == 403:
                    if self.is_update_proxy:
                        # update proxy server settings
                        proxy = self.api_worker.update_proxy(self.proxy_worker.get_proxy_id())
                        if proxy:
                            self.proxy_worker.set_proxy_data(proxy[1], proxy[0])
                            session.proxies = self.proxy_worker.get_proxy_dict()
                    count += 1
                    time.sleep(config.DELAY_REQUESTS)
                    self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                       "code": str(response.status_code),
                                                                       "order": order_id})
                    continue
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module",
                        "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}

            except requests.exceptions.RequestException as error:
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module",
                        "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}
            # set cookies

            return {"status": False, "error": False, "status_code": str(response.status_code), "message": response.text,
                    "type_res": "request_module", "proxy": tuple([self.proxy_worker.get_proxy_id(),
                                                                  self.proxy_worker.get_proxy_dict()])}

        return {"status": False, "error": True, "status_code": "403",
                "message": "Perhaps the proxy server did not respond in time. 403 HTTPError",
                "type_res": "request_module", "proxy": tuple([self.proxy_worker.get_proxy_id(),
                                                              self.proxy_worker.get_proxy_dict()])}

    def send_data(self, url: str, order_id, data: dict):
        """
        Send form to target portal.
        :param url:
        :param order_id:
        :param data:
        :return: dict
        """
        count = 0
        response = ''
        files = dict()
        headers = settings.headers
        files["upload_file"] = data["upload_file"]
        del data["upload_file"]
        cookies = self.cookies_work.get_cookies()
        while count < self.number_attempts:
            try:
                if not self.proxy_worker.get_proxy_dict():
                    response = requests.post(url, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT),
                                             allow_redirects=True, files=files, data=data, headers=headers,
                                             cookies=cookies)
                else:
                    response = requests.post(url, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT),
                                             headers=headers, proxies=self.proxy_worker.get_proxy_dict(), files=files,
                                             data=data, allow_redirects=True, cookies=cookies)
            except requests.exceptions.ConnectionError as error:
                self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": 0,
                                                                     "order": order_id})
                return {"status": False, "error": True, "status_code": 0, "message": error.__repr__(),
                        "type_res": "request_module",
                        "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                if response.status_code == 403:
                    if self.is_update_proxy:
                        # update proxy server settings
                        proxy = self.api_worker.update_proxy(self.proxy_worker.get_proxy_id())
                        if proxy:
                            self.proxy_worker.set_proxy_data(proxy[1], proxy[0])
                    count += 1
                    time.sleep(config.DELAY_REQUESTS)
                    self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                       "code": str(response.status_code),
                                                                       "order": order_id})
                    continue
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module",
                        "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}

            except requests.exceptions.RequestException as error:
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module",
                        "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}
            # set cookies

            break

        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module",
                "proxy": tuple([self.proxy_worker.get_proxy_id(), self.proxy_worker.get_proxy_dict()])}
