"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""

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
        self.api_worker = ApiWorker()
        self.proxy_id = data["proxy"]["proxy_id"]
        self.host_proxy = data["proxy"]["host"]
        self.port_proxy = data["proxy"]["port"]
        self.protocol_proxy = data["proxy"]["protocol"]
        self.username_proxy = data["proxy"]["username"]
        self.password_proxy = data["proxy"]["password"]
        self.proxies = dict()
        self.set_proxy(host_proxy=self.host_proxy, port_proxy=self.port_proxy, protocol_proxy=self.protocol_proxy,
                       username_proxy=self.username_proxy, password_proxy=self.password_proxy)
        self.analyzer_module = AnalyzerModule(self.proxies)

    def start(self):
        # get main link
        main_content = self.main_page_worker()
        if main_content["status"]:
            # get other link
            button_links = self.other_page_worker()
            if button_links["status"]:
                # open form and send data
                sender = self.send_worker()
            else:
                pass
        else:
            # no links found, send a report to the server, write log file
            print(main_content)

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
        Send data
        :return: dict
        """
        return self.analyzer_module.form_page()

    def set_proxy(self, **data):
        if data["protocol_proxy"] and data["username_proxy"] and data["password_proxy"] and data["host_proxy"] and data["port_proxy"]:
            self.proxies.update(
                {'http': data["protocol_proxy"] + "://" + data["username_proxy"] + ":" + data["password_proxy"] + "@"
                         + data["host_proxy"] + ":" + str(data["port_proxy"])})

