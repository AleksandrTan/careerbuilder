"""
Module for working with requests to a target resource
"""
import time

import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from botmodule import settings
import config


class RequestModule(LogModule):

    def __init__(self, api_worker, proxy_worker:object):
        super().__init__()
        self.api_worker = api_worker
        self.proxy_worker = proxy_worker
        self.number_attempts = config.NUMBER_REQUESTS
        self.cookie = dict()

    def get_content(self, link: str, order_id: str):
        """
        Request page content for a given links.
        If the request status is 403,
        it requests an updated proxy server from the system api.
        :param order_id: str
        :param link: str
        :return:
        """
        count = 0
        session = HTMLSession()
        session.proxies = self.api_worker.get_proxy_dict()
        proxy_id = self.api_worker.get_proxy_id()
        session.headers = settings.headers
        cookies = self.get_cookie()
        while count < self.number_attempts:
            try:
                response = session.get(link, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT), cookies=cookies)
                print(response.url, response.status_code, self.api_worker.get_proxy_dict())
                session.close()
            except requests.exceptions.ConnectionError as error:
                self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": '',
                                                                     "order": order_id})
                return {"status": False, "error": True, "status_code": '0', "message": error.__repr__(),
                        "type_res": "request_module", "proxy": tuple([self.api_worker.get_proxy_id(),
                                                                      self.api_worker.get_proxy_dict()])}
            try:
                response.raise_for_status()

            except requests.HTTPError as error:
                if response.status_code == 403:
                    print("Update proxy")
                    # update proxy server settings
                    proxy = self.api_worker.update_proxy(proxy_id)
                    if proxy:
                        print(proxy)
                        self.api_worker.set_proxy_data(proxy[1], proxy[0])
                        session.proxies = self.api_worker.get_proxy_dict()
                        proxy_id = self.api_worker.get_proxy_id()
                        count += 1
                    time.sleep(config.DELAY_REQUESTS)
                    continue
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module", "proxy": tuple([self.api_worker.get_proxy_id(),
                                                                                                   self.api_worker.get_proxy_dict()])}

            except requests.exceptions.RequestException as error:
                self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                                   "code": str(response.status_code),
                                                                   "order": order_id})
                return {"status": False, "error": True, "status_code": str(response.status_code),
                        "message": error.__repr__(), "type_res": "request_module", "proxy": tuple([self.api_worker.get_proxy_id(),
                                                                                                   self.api_worker.get_proxy_dict()])}
            # set cookies
            self.set_cookie(response.cookies)
            return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                    "type_res": "request_module", "proxy": tuple([self.api_worker.get_proxy_id(), self.api_worker.get_proxy_dict()])}

        return {"status": False, "error": True, "status_code": "403",
                "message": "Perhaps the proxy server did not respond in time. 403 HTTPError",
                "type_res": "request_module", "proxy": tuple([self.api_worker.get_proxy_id(), self.api_worker.get_proxy_dict()])}

    def send_data(self, url: str, proxy: dict, order_id, data: dict):
        """
        Send form to target portal.
        :param url:
        :param proxy:
        :param order_id:
        :param data:
        :return: dict
        """
        files = dict()
        headers = settings.headers
        files["upload_file"] = data["upload_file"]
        del data["upload_file"]
        cookies = self.get_cookie()
        try:
            if not proxy:
                response = requests.post(url, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT),
                                         allow_redirects=True, files=files, data=data, headers=headers, cookies=cookies)
            else:
                response = requests.post(url, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT),
                                         headers=headers, proxies=proxy, files=files, data=data,
                                         allow_redirects=True, cookies=cookies)
        except requests.exceptions.ConnectionError as error:
            self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": 0,
                                                                 "order": order_id})
            return {"status": False, "error": True, "status_code": 0, "message": error.__repr__(),
                    "type_res": "request_module", "proxy": tuple([self.proxy_id, proxy])}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": tuple([self.proxy_id, proxy])}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": tuple([self.proxy_id, proxy])}
        # set cookies
        self.set_cookie(response.cookies)
        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module", "proxy": tuple([self.proxy_id, proxy])}

    def set_cookie(self, cookies):
        if cookies:
            for cookie in cookies:
                self.cookie[cookie.name] = cookie.value

    def get_cookie(self) -> dict:
        return self.cookie
