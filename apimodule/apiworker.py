"""
Class for working with system api
"""
import config
from logsource.logmodule import LogModule
from botmodule.apirequests import ApiRequestModule


class ApiWorker(LogModule):
    def __init__(self, order_id: int):
        super().__init__()
        self.request = ApiRequestModule()
        self.order_id = order_id
        self.api_url = config.API_HOST
        self.url_task_success = config.TASK_RESULT_SUCCESS
        self.url_task_fail = config.TASK_RESULT_FAIL
        self.messages = config.MESSAGES_ERROR_API

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
        Report about task results
        :param data_error: dict
        :param key_report:
        :return: bool
        """
        params = {"status": False}
        url = self.api_url + self.url_task_fail.replace("order_id", str(self.order_id))
        message = self.messages[key_report]["message"]
        if data_error:
            message = message.replace("message", data_error["message"])
            message = message.replace("status_code", data_error["status_code"])
        params["message"] = message
        result = self.request.make_post(url, params)
        # log in console(file)
        if key_report == "no_file" or 'no_links_found' or "no_button_found":
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
