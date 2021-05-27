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

    def start(self):
        if not self.rabbit_connect:
            return False
        self.rabbit_connect.receive(Worker.worker)

    @staticmethod
    def worker(ch, method, properties, body):
        # get task
        message = json.loads(body.decode())
        print(message)
        # start bot
        bot_object = BotWorker(message)
        print('Start thread')
        threading.Thread(target=bot_object.start, args=()).start()
        # confirm task processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(10)


if __name__ == "__main__":
    worker = Worker()
    worker.start()
