"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
import datetime
import os
import sys

import config
from apimodule.apiworker import ApiWorker
from logsource.logmodule import LogModule
from botmodule.analyzermodule import AnalyzerModule
from apimodule.proxy_work import ProxyWork


class BotWorker(LogModule):

    def __init__(self, data):
        super().__init__()
        # ProxyWork.__init__(self)
        self.is_update_proxy = data["is_update_proxy"]
        self.target_link = data["target_link"]
        self.link_id = self.target_link.split('/')[-1]
        self.order_id = data["order_id"]
        self.file_mailing = data["file_mailing"]
        self.file_name = data["file_name"]
        self.user_name = data["user_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.proxy_id = data["proxy"]["proxy_id"]
        self.host_proxy = data["proxy"]["host"]
        self.port_proxy = data["proxy"]["port"]
        self.protocol_proxy = data["proxy"]["protocol"]
        self.username_proxy = data["proxy"]["username"]
        self.password_proxy = data["proxy"]["password"]
        self.proxies = dict()
        self.proxy_worker = ProxyWork({"host": self.host_proxy, "port": self.port_proxy,
                                       "username": self.username_proxy, "password": self.password_proxy})
        self.set_proxy(host_proxy=self.host_proxy, port_proxy=self.port_proxy, protocol_proxy=self.protocol_proxy,
                       username_proxy=self.username_proxy, password_proxy=self.password_proxy)
        self.proxy_worker.set_proxy_data(self.proxies, self.proxy_id)
        self.api_worker = ApiWorker(self.order_id, self.proxy_worker)
        self.file_content = self.download_file()
        self.analyzer_module = AnalyzerModule(str(self.order_id), self.link_id, self.user_name, self.last_name,
                                              self.email, self.file_content, self.file_name, self.api_worker,
                                              self.proxy_worker, self.is_update_proxy)

    def start(self):
        begin_time = datetime.datetime.now()
        sys.stdout.write(f"Start work - {datetime.datetime.now()}\n")
        # check if file for send download
        if not self.file_content:
            # send a report to the server, write log file
            self.api_worker.task_report_fail("no_file")
            sys.stdout.write(f"End time - {datetime.datetime.now() - begin_time}\n")
            return False
        # get main link
        sys.stdout.write("Get main page\n")
        main_content = self.main_page_worker()
        if main_content["status"]:
            # get other link
            sys.stdout.write("Get other page\n")
            button_links = self.other_page_worker()
            if button_links["status"]:
                # open form and send data
                sys.stdout.write("Send form\n")
                sender = self.send_worker()
                # send data to system api
                self.api_worker.task_report_success(sender)
            else:
                # no links found, send a report to the server, write log file
                button_links["order"] = str(self.order_id)
                if button_links.get("error", False):
                    # wrong request
                    self.api_worker.task_report_fail("target_connect_error", button_links)
                else:
                    # no links found
                    self.api_worker.task_report_fail("no_button_found")
                sys.stdout.write(f"End time - {datetime.datetime.now() - begin_time}")
                self.delete_file()
                return False
        else:
            # no links found(or have some errors), send a report to the server, write log file
            main_content["order"] = str(self.order_id)
            if main_content.get("error", False):
                # wrong request
                self.api_worker.task_report_fail("target_connect_error", main_content)
            else:
                # no links found
                self.api_worker.task_report_fail("no_links_found")
            self.delete_file()
            return False
        self.delete_file()
        sys.stdout.write(f"End time - {datetime.datetime.now() - begin_time}\n")
        return True

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
        """
        Init start proxy(self.proxies)
        :param data: dict
        :return: None
        """
        self.proxies = self.proxy_worker.set_proxy(**data)

    def download_file(self):
        """
        Download file for sending
        :return: None
        """
        file = self.api_worker.get_file(self.file_mailing)
        if file["status"]:
            files = open(config.BASE_DIR + '/tmp/' + self.file_name, "wb")
            files.write(file["content"])
            files.close()
            return True

        return False

    def delete_file(self):
        if os.path.exists(config.BASE_DIR + '/tmp/' + self.file_name):
            os.remove(config.BASE_DIR + '/tmp/' + self.file_name)


if __name__ == "__main__":
    print(config.BASE_DIR, 3500)
