"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
import time

from apimodule.apiworker import ApiWorker
from logsource.logmodule import LogModule
from botmodule.analyzermodule import AnalyzerModule


class BotWorker(LogModule):

    def __init__(self, data):
        super().__init__()
        self.target_link = data["target_link"]
        self.order_id = data["order_id"]
        self.file_mailing = data["file_mailing"]
        self.user_name = data["user_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.api_worker = ApiWorker(self.order_id)
        self.proxy_id = data["proxy"]["proxy_id"]
        self.host_proxy = data["proxy"]["host"]
        self.port_proxy = data["proxy"]["port"]
        self.protocol_proxy = data["proxy"]["protocol"]
        self.username_proxy = data["proxy"]["username"]
        self.password_proxy = data["proxy"]["password"]
        self.proxies = dict()
        self.set_proxy(host_proxy=self.host_proxy, port_proxy=self.port_proxy, protocol_proxy=self.protocol_proxy,
                       username_proxy=self.username_proxy, password_proxy=self.password_proxy)
        self.analyzer_module = AnalyzerModule(self.proxies, str(self.order_id))
        self.file_content = self.download_file()

    def start(self):
        # check if file for send download
        if not self.file_content:
            # send a report to the server, write log file
            self.api_worker.task_report_fail("no_file")
            return False
        # get main link
        main_content = self.main_page_worker()
        if main_content["status"]:
            # get other link
            button_links = self.other_page_worker()
            if button_links["status"]:
                # open form and send data
                sender = self.send_worker()
            else:
                # no links found, send a report to the server, write log file
                pass
        else:
            # no links found, send a report to the server, write log file
            main_content["order"] = str(self.order_id)
            self.api_worker.task_report_fail("target_connect_error", main_content)

    def main_page_worker(self) -> dict:
        """
        Parsing the main link
        :return: dict
        """
        return self.analyzer_module.parse_main_page(self.target_link)

    def other_page_worker(self) -> dict:
        """
        Parsing the other link on page, and get buttons for form to send data
        :return: dict
        """
        return self.analyzer_module.parse_other_page()

    def send_worker(self) -> dict:
        """
        Parsing links with submission forms,
        generating an array of data, submitting a form
        :return: dict
        """
        return self.analyzer_module.form_page()

    def set_proxy(self, **data):
        if data["protocol_proxy"] and data["username_proxy"] and data["password_proxy"] and \
                data["host_proxy"] and data["port_proxy"]:
            self.proxies.update(
                {'http': data["protocol_proxy"] + "://" + data["username_proxy"] + ":" + data["password_proxy"] + "@" +
                         data["host_proxy"] + ":" + str(data["port_proxy"])})

    def download_file(self):
        """
        Download file for sending
        :return: None
        """
        file = self.api_worker.get_file(self.file_mailing)
        if file["status"]:
            return file["message"]

        return False


if __name__ == "__main__":
    import requests

    url = 'http://127.0.0.1:8000/mspanel/bot/get_file/?name=/media/files_mailing/IGalgorithm_EjrhH1Z.txt'
    r = requests.get(url)
    print(r.content)
