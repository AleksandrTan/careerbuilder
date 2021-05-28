"""
Class for working with system api
"""
import requests

import config
from logsource.logmodule import LogModule
from botmodule.apirequests import ApiRequestModule


class ApiWorker(LogModule):
    def __init__(self, order_id: int):
        super().__init__()
        self.request = ApiRequestModule()
        self.order_id = order_id
        self.api_url = config.API_HOST
        self.url_task_done = config.TASK_RESULT_DONE
        self.url_task_fail = config.TASK_RESULT_FAIL

    def get_file(self, target_link):
        """
        Get file for download to form
        :param target_link: str
        :return:
        """
        url = config.API_HOST + config.FILE_DOWNLOAD + '?name=' + target_link
        result = self.request.make_get(url)
        if not result["status"]:
            return {"status": False}

        return result

    def task_report(self, status: bool = True, key_report: str = '', data_result: dict = None) -> bool:
        """
        Report about task results
        :param status: bool
        :param key_report:
        :param data_result: dict
        :return: bool
        """
        if status:
            url = self.api_url + self.url_task_done
        else:
            url = self.api_url + self.url_task_done
        result = self.request.make_get(url)
        if not result["status"]:
            return False

        return True
