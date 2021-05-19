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

    def start(self):
        pass


if __name__ == "__main__":
    worker = Worker()
    worker.start()
