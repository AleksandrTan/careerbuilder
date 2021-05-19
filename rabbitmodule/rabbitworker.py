"""
Server class RabbitWorker
"""
import pika
import config
from logsource.logmodule import LogModule


class RabbitWorker(LogModule):

    def __init__(self):
        super().__init__()
        self.connect = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_HOST))
