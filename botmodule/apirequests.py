"""
Module for working with requests to a system api
"""
import time

import requests

from logsource.logmodule import LogModule
from config import ATTEMPTS_TO_CONNECT, TIME_TO_CONNECT


class ApiRequestModule(LogModule):

    def make_get(self, url: str, params: dict = None) -> dict:
        """
        :param params: dict
        :param url: str
        :return: dict
        """
        response = ''
        counter = 0
        while counter < ATTEMPTS_TO_CONNECT:
            try:
                response = requests.get(url)
                break
            except requests.exceptions.RequestException as error:
                # write logs and console
                self._send_task_report("api_connect_error", data={})
                counter += 1
                print(counter)
                time.sleep(TIME_TO_CONNECT)
                continue
        if counter == ATTEMPTS_TO_CONNECT:
            self._send_task_report("api_connect_error", data={})
            return {"status": False}

        if response.status_code == 200:
            return {"status": True, "error": False, "status_code": response.status_code, "message": response.text,
                    "type_res": "api_request_module"}

    def make_post(self):
        pass
