"""
Module for working with requests to a target resource
"""
import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from botmodule import settings
import config


class RequestModule(LogModule):

    def __init__(self):
        super().__init__()
        self.cookie = dict()

    def get_content(self, link: str, proxy: dict, order_id):
        """
        Request page content for a given links.
        :param order_id: str
        :param proxy: dict
        :param link: str
        :return:
        """
        print(proxy)
        session = HTMLSession()
        session.proxies = proxy
        session.headers = settings.headers
        cookies = self.get_cookie()
        try:
            response = session.get(link, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT), cookies=cookies)
            print(response.url, response.status_code)
            session.close()
        except requests.exceptions.ConnectionError as error:
            self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": 0,
                                                                 "order": order_id})
            return {"status": False, "error": True, "status_code": 0, "message": error, "type_res": "request_module",
                    "proxy": proxy}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": proxy}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": proxy}
        # set cookies
        self.set_cookie(response.cookies)
        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module", "proxy": proxy}

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
            return {"status": False, "error": True, "status_code": 0, "message": error, "type_res": "request_module",
                    "proxy": proxy}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": proxy}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module", "proxy": proxy}
        # set cookies
        self.set_cookie(response.cookies)
        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module", "proxy": proxy}

    def set_cookie(self, cookies):
        if cookies:
            for cookie in cookies:
                self.cookie[cookie.name] = cookie.value

    def get_cookie(self):
        return self.cookie
