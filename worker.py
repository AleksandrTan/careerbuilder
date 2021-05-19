"""
Class Worker
The main module
"""
import json
import time

from rabbitmodule.rabbitworker import RabbitWorker


class Worker:

    def __init__(self):
        super().__init__()
        self.rabbit_connect = RabbitWorker()

    def start(self):
        self.rabbit_connect.receive(Worker.worker)

    @staticmethod
    def worker(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f"[x] Received {message['link']}")
        time.sleep(10)


if __name__ == "__main__":
    worker = Worker()
    worker.start()
