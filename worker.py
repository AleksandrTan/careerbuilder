"""
Class Worker
The main module
"""
import json
import time
import threading

from logsource.logmodule import LogModule
from rabbitmodule.rabbitworker import RabbitWorker
from botmodule.botworker import BotWorker


class Worker(LogModule):

    def __init__(self):
        super().__init__()
        self.rabbit_connect = RabbitWorker()
        self.bot_worker = BotWorker()
        self.bots_array = dict()

    def start(self):
        self.rabbit_connect.receive(Worker.worker)

    @staticmethod
    def worker(ch, method, properties, body):
        message = json.loads(body.decode())
        if message["status"]:
            # start bot
            # confirm task processing
            pass
        else:
            pass
        print(f"[x] Received {message}")
        time.sleep(10)


if __name__ == "__main__":
    worker = Worker()
    worker.start()
