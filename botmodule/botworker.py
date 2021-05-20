"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
import time

from apimodule.apiworker import ApiWorker
from logsource.logmodule import LogModule
from botmodule.requestmodule import GetContent


class BotWorker(LogModule):

    def __init__(self):
        super().__init__()
        self.api_worker = ApiWorker()
        self.content = GetContent()

    def start(self, data: dict):
        """

        :param data:
        :return: None
        """
        content = self.content.get_content(data["link"])
        print(content)
        print(data["link"], 3500)
