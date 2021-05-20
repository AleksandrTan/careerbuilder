"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
import time

from apimodule.apiworker import ApiWorker
from logsource.logmodule import LogModule
from botmodule.requestmodule import RequestModule
from botmodule.analyzermodule import AnalyzerModule


class BotWorker(LogModule):

    def __init__(self, data):
        super().__init__()
        self.link = data["link"]
        self.order_id = data["order_id"]
        self.api_worker = ApiWorker()
        self.request = RequestModule()
        self.analyzer_module = AnalyzerModule()

    def start(self):
        content = self.request.get_content(self.link)
        if content["status"]:
            print("Analyser start!!!")
        else:
            pass
        print(self.link, 3500)
