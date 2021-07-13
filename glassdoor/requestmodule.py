"""
Module for working with requests to a target resource
"""
import time

import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from glassdoor import settings
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
        session.headers = settings.HEADERS
        while count < self.number_attempts:
            try:
                response = session.get(link, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT))
                session.close()
                print(response.cookies)
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

            return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
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
        headers = settings.HEADERS
        files["upload_file"] = data["upload_file"]
        del data["upload_file"]
        cookies = dict()
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

