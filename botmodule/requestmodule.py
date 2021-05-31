"""
Module for working with requests to a target resource
"""
import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from botmodule import settings
import config


class RequestModule(LogModule):

    def get_content(self, link: str, proxy: dict, order_id):
        """
        Request page content for a given links.
        :param order_id: str
        :param proxy: dict
        :param link: str
        :return:
        """
        response = ''
        session = HTMLSession()
        session.headers = settings.headers
        try:
            if not proxy:
                response = session.get(link, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT))
                session.close()
            else:
                response = session.get(link, proxies=proxy, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT))
                session.close()
        except requests.exceptions.ConnectionError as error:
            self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": 0,
                                                                 "order": order_id})
            return {"status": False, "error": True, "status_code": 0, "message": error, "type_res": "request_module"}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module"}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module"}

        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module"}

    def send_data(self, url: str, proxy: dict, order_id, data: dict):
        """
        Send form.
        :param url:
        :param proxy:
        :param order_id:
        :param data:
        :return: dict
        """
        print(data)
        headers = settings.headers
        try:
            if not proxy:
                response = requests.post(url, timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT), files=data,
                                         headers=headers)
            else:
                response = requests.post(url, headers=headers, proxies=proxy,
                                         timeout=(config.REQUEST_TIMEOUT, config.RESPONSE_TIMEOUT),
                                         files=data)
        except requests.exceptions.ConnectionError as error:
            self._send_task_report("target_connect_error", data={"message": error.__repr__(), "code": 0,
                                                                 "order": order_id})
            return {"status": False, "error": True, "status_code": 0, "message": error, "type_res": "request_module"}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module"}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": str(response.status_code), "order": order_id})
            return {"status": False, "error": True, "status_code": str(response.status_code),
                    "message": error.__repr__(), "type_res": "request_module"}

        return {"status": True, "error": False, "status_code": str(response.status_code), "message": response.text,
                "type_res": "request_module"}
