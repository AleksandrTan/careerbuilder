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
        self.link = data["link"]
        self.order_id = data["order_id"]
        self.api_worker = ApiWorker()
        self.analyzer_module = AnalyzerModule()

    def start(self):
        # get main link
        main_content = self.main_page_worker()
        if main_content["status"]:
            # get other link
            button_links = self.other_page_worker()
            if button_links["status"]:
                # open form and send data
                print(button_links)
            else:
                pass
        else:
            # send a report to the server, write log file
            print(main_content)

    def main_page_worker(self) -> dict:
        """
        Parsing the main link
        :return: dict
        """
        return self.analyzer_module.parse_main_page(self.link)

    def other_page_worker(self) -> dict:
        """
        Parsing the other link on page, and get buttons for form to send data
        :return: dict
        """
        return self.analyzer_module.parse_other_page()
