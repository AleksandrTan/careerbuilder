"""
Module for working with requests to a target resource
"""
import requests
from requests_html import HTMLSession

from logsource.logmodule import LogModule
from botmodule import settings
import config


class RequestModule(LogModule):

    def get_content(self, link: str, proxy: dict):
        """
        Request page content for a given links.
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
            self._send_task_report("target_connect_error", data={"message": error.__repr__(),
                                                                 "code": 0})
            return {"status": False, "error": True, "status_code": 0, "message": error, "type_res": "request_module"}
        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": response.status_code})
            return {"status": False, "error": True, "status_code": response.status_code, "message": error,
                    "type_res": "request_module"}

        except requests.exceptions.RequestException as error:
            self._send_task_report("main_content_error", data={"message": error.__repr__(),
                                                               "code": response.status_code})
            return {"status": False, "error": True, "status_code": response.status_code, "message": error,
                    "type_res": "request_module"}

        return {"status": True, "error": False, "status_code": response.status_code, "message": response.text,
                "type_res": "request_module"}

    def send_data(self):
        pass
