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

    bots_array = dict()

    def __init__(self):
        super().__init__()
        self.rabbit_connect = RabbitWorker()

    def start(self):
        self.rabbit_connect.receive(Worker.worker)

    @staticmethod
    def worker(ch, method, properties, body):
        message = json.loads(body.decode())
        if message["status"]:
            # start bot
            bot_object = BotWorker()
            Worker.bots_array["id"] = bot_object
            print('Start thread')
            threading.Thread(target=bot_object.start, args=(message,)).start()
            # confirm task processing
            time.sleep(10)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            pass
        else:
            pass
        print(f"[x] Received {message}")


if __name__ == "__main__":
    worker = Worker()
    worker.start()
