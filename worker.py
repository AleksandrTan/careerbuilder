"""
Class Worker
The main module
"""
from logsource.logmodule import LogModule
from rabbitmodule.rabbitworker import RabbitWorker


class Worker(LogModule):

    def __init__(self):
        super().__init__()
        self.rabbit_connect = RabbitWorker()
