"""
Class for working with system api
Use ApiRequestModule to make requests to the main system
"""
import json

import config
from botmodule import settings
from logsource.logmodule import LogModule
from apimodule.apirequests import ApiRequestModule
from apimodule.proxy_work import ProxyWork


class ApiWorker(LogModule):
    def __init__(self, order_id: int, proxy_worker: ProxyWork):
        super().__init__()
        self.request = ApiRequestModule()
        self.proxy_worker = proxy_worker
        self.order_id = order_id
        self.api_url = config.API_HOST
        self.url_task_success = config.TASK_RESULT_SUCCESS
        self.url_task_fail = config.TASK_RESULT_FAIL
        self.url_update_proxy = config.UPDATE_PROXY
        self.messages = settings.MESSAGES_ERROR_API

    def get_file(self, target_link):
        """
        Get file for download to form
        :param target_link: str
        :return:
        """
        url = config.API_HOST + config.FILE_DOWNLOAD + '?file_url=' + target_link
        result = self.request.make_get(url)
        if not result["status"]:
            return {"status": False}

        return result

    def task_report_fail(self, key_report: str = '', data_error: dict = None) -> bool:
        """
        Report about fail task results
        :param data_error: dict
        :param key_report:
        :return: bool
        """
        params = {"status": False, "proxy_id": self.proxy_worker.get_proxy_id()}
        url = self.api_url + self.url_task_fail.replace("order_id", str(self.order_id))
        message = self.messages[key_report]["message"]
        del data_error["status"]
        if data_error:
            for data in data_error:
                if data == "proxy":
                    message = message.replace("pserver", list(self.proxy_worker.get_proxy_dict().values())[0])
                    continue
                message = message.replace(data, str(data_error[data]))
                continue
        params["message"] = message
        result = self.request.make_post(url, params)
        # log in console(file)
        self._send_task_report(key_report, data={"order": self.order_id})
        if not result["status"]:
            return False

        return True

    def task_report_success(self, data_success: dict = None) -> bool:
        """
        Report about task results
        :param data_success:
        :return: bool
        """
        params = {"status": True}
        url = self.api_url + self.url_task_success.replace("order_id", str(self.order_id))
        params["status_order"] = "success"
        params["all_links"] = data_success["count_link_button"]
        params["send_links"] = data_success["success_count_link"]
        params["fail_links"] = data_success["fail_count_link"]
        result = self.request.make_post(url, params)
        return True

    def update_proxy(self, proxy_id: int = 0, fail: bool = True) -> tuple:
        """
        If fail=True  means the request was unsuccessful with proxy(403 status)
        :param fail: bool
        :param proxy_id: int
        :return:
        """
        url = self.api_url + self.url_update_proxy + "?proxy_id=" + str(proxy_id) + "&fail=" + str(fail)
        result = self.request.make_get(url)
        if result["status"]:
            return json.loads(result["message"])["proxy_id"], {"https": json.loads(result["message"])["proxy"]}
        else:
            return tuple()
