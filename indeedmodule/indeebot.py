"""
The class describes a bot object that mimics user behavior in the target portal https://www.indeed.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
import datetime
import os, signal
import sys
import time

import config
from apimodule.apiworker import ApiWorker
from apimodule.proxy_work import ProxyWork
from indeedmodule.analyzermodule import AnalyzerModule
from indeedmodule.authmodule import AuthModule
from indeedmodule.core.cookie_work import CookiesWork
from indeedmodule.core.headers_work import HeadersWork
from logsource.logmodule import LogModule


class IndeedWorker(LogModule):

    def __init__(self, data):
        super().__init__()
        self.is_update_proxy = data["is_update_proxy"]
        self.target_link = data["target_link"]
        self.link_id = self.target_link.split('/')[-1]
        self.order_id = data["order_id"]
        self.file_mailing = data["file_mailing"]
        self.file_name = data["file_name"]
        self.user_name = data["user_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.email = data["email"]
        self.login = data["login"]
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
        self.cookies_work = CookiesWork()
        self.headers_work = HeadersWork()
        self.auth = AuthModule(str(self.order_id), data, self.cookies_work, self.headers_work, self.api_worker,
                               self.proxy_worker,
                               self.is_update_proxy)

    def start(self):
        begin_time = datetime.datetime.now()
        sys.stdout.write(f"Start work - {datetime.datetime.now()}\n")
        # check if file for send download
        if not self.file_content:
            # send a report to the server, write log file
            self.api_worker.task_report_fail("no_file")
            return False

        # Authorization
        auth_status = self.auth.auth()
        print(auth_status)
        if not auth_status["status"]:
            self.api_worker.task_report_fail(auth_status["key"], {"order": self.order_id})

            return False
        else:
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
    data = {'proxy': {
        'proxy_id': 13,
        'host': '196.17.78.225',
        'port': 8000,
        'protocol': 'http',
        'username': '2DxLL0',
        'password': 'fwcZsa'
    },
        'status': True,
        'is_update_proxy': True,
        'target_link': 'http://127.0.0.1:8000/mainsystem/testpage/',
        'order_id': 246,
        'file_mailing': '/media/files_mailing/%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B2%D0%B8%D1%87_%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9_jV6LGKb.docx',
        'file_name': 'Андревич_Андрей_jV6LGKb.docx',
        'user_name': 'dfg',
        'last_name': 'dfg',
        'password': '1',
        'email': 'rumych2013@gmail.com',
        'login': '1',
        'portal': 'indeed'
    }
    b = IndeedWorker(data)
    b.start()
