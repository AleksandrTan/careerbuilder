"""
Server class RabbitWorker
"""
import json
import time
import pika
import threading

import config
from logsource.logmodule import LogModule
from botmodule.botworker import BotWorker


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
                time.sleep(config.TIME_TO_CONNECT_RABBIT)
                continue
        if counter == config.ATTEMPTS_TO_CONNECT_RABBIT:
            return False
        self.channel = self.connection.channel()
        return self.channel

    def receive(self, callback):
        while True:
            try:
                self.channel.queue_declare(queue=config.QUEUE_NAME)
                self.channel.basic_consume(on_message_callback=callback, queue='target')
                print(' [*] Waiting for messages. To exit press CTRL+C')
                self.channel.start_consuming()
            except pika.exceptions.ChannelWrongStateError as error:
                return False
            except pika.exceptions.ConnectionClosedByBroker as error:
                continue

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
    worker = RabbitWorker()
    worker.receive(RabbitWorker.worker)
