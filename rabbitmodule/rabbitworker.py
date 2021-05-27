"""
Server class RabbitWorker
"""
import json
import time
import pika

import config
from logsource.logmodule import LogModule


class RabbitWorker(LogModule):

    def __init__(self):
        super().__init__()
        self.connection = ''
        self.channel = ''
        self.connect()

    def connect(self):
        counter = 0
        while counter < config.ATTEMPTS_TO_CONNECT_RABBIT:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
                self.channel = self.connection.channel()
                return self.channel
            except pika.exceptions.AMQPConnectionError as error:
                counter += 1
                print(counter)
                time.sleep(config.TIME_TO_CONNECT_RABBIT)
                continue
        if counter == config.ATTEMPTS_TO_CONNECT_RABBIT:
            return False
        self.channel = self.connection.channel()
        return self.channel

    def receive(self, callback):
        self.channel.queue_declare(queue="target")
        self.channel.basic_consume(on_message_callback=callback, queue='target')
        print(' [*] Waiting for messages. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker as error:
            print(4000)
            self.connect()

    @staticmethod
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f"[x] Received {message['link']}")
        time.sleep(10)


if __name__ == "__main__":
    worker = RabbitWorker()
    worker.receive(RabbitWorker.callback)

