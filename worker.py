"""
Server class RabbitWorker
"""
import json
import sys
import time
import pika
import threading
from multiprocessing import Process

import config
from logsource.logmodule import LogModule
from botmodule.botworker import BotWorker
from indeedmodule.indeebot import IndeedWorker


class RabbitWorker(LogModule):

    def __init__(self):
        super().__init__()
        self.connection = ''
        self.channel = ''
        self.connect()

    def connect(self):
        sys.stdout.write("Connect to Rabbit\n")
        counter = 0
        while counter < config.ATTEMPTS_TO_CONNECT_RABBIT:
            try:
                sys.stdout.write(f"{config.RABBIT_HOST}\n")
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST, port=config.RABBIT_PORT))
                self.channel = self.connection.channel()
                sys.stdout.write("Connected to Rabbit\n")
                return self.channel
            except pika.exceptions.AMQPConnectionError as error:
                sys.stdout.write(f"Connect error {counter}\n")
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
                self.channel.basic_consume(on_message_callback=callback, queue=config.QUEUE_NAME)
                sys.stdout.write(' [*] Waiting for messages. To exit press CTRL+C\n')
                self.channel.start_consuming()
            except pika.exceptions.ChannelWrongStateError as error:
                return False
            except pika.exceptions.ConnectionClosedByBroker as error:
                continue

    @staticmethod
    def worker(ch, method, properties, body):
        """
        Handler for receiving a message from the queue
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        # get task
        bot_objects = list()
        message = json.loads(body.decode())
        print(message)
        # start bot
        if message["portal"] == "careerbuilder":
            bot_object = BotWorker(message)
            threading.Thread(target=bot_object.start, args=()).start( )

        if message["portal"] == "indeed":
            bot_object = IndeedWorker(message)
            process1 = Process(target=bot_object.start, args=())
            process1.start()
            bot_objects.append(process1)
            # delete zombi process
            for process in bot_objects:
                if process.is_alive():
                    continue
                else:
                    process.terminate()
                    continue
        # confirm task processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(10)


if __name__ == "__main__":
    worker = RabbitWorker()
    worker.receive(RabbitWorker.worker)
