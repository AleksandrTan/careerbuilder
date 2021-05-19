"""
The class describes a bot object that mimics user behavior in the target portal https://www.careerbuilder.com/.
It is launched from a workflow, initialized, and then executed, accompanying its work with logging at
the database level, logging to a file or standard output.
"""
from apimodule.apiworker import ApiWorker
from logsource.logmodule import LogModule


class BotWorker(LogModule):

    def __init__(self):
        super().__init__()
        self.api_worker = ApiWorker()

    def start(self, data: dict):
        """

        :param data:
        :return: None
        """
        print(data)
