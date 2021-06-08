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
                time.sleep(TIME_TO_CONNECT)
                continue
        if counter == ATTEMPTS_TO_CONNECT:
            self._send_task_report("api_connect_error", data={})
            return {"status": False}

        if response.status_code == 200:
            return {"status": True, "error": False, "status_code": response.status_code, "message": response.text,
                    "type_res": "api_request_module", "content": response.content}

    def make_post(self, url: str, data: dict = None):
        response = ''
        counter = 0
        while counter < ATTEMPTS_TO_CONNECT:
            try:
                if data:
                    response = requests.post(url, data=data)
                else:
                    response = requests.post(url)
                break
            except requests.exceptions.RequestException as error:
                # write logs and console
                self._send_task_report("api_connect_error", data={"message": error.__repr__(),
                                                                  "code": 500})
                counter += 1
                time.sleep(TIME_TO_CONNECT)
                continue
        if type(response) != str:
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                self._send_task_report("api_connect_error", data={"message": error.__repr__(),
                                                                  "code": str(response.status_code)})
                return {"status": False}
        if counter == ATTEMPTS_TO_CONNECT:
            self._send_task_report("api_connect_error", data={})
            return {"status": False}

        if response.status_code == 200:
            return {"status": True, "error": False, "status_code": response.status_code, "message": response.text,
                    "type_res": "api_request_module"}
