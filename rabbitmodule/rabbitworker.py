"""
Server class RabbitWorker
"""
import pika
import config
# from logsource.logmodule import LogModule


class RabbitWorker:

    def __init__(self):
        super().__init__()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        self.channel = self.connection.channel()

    def receive(self):
        self.channel.queue_declare(queue="target")
        self.channel.basic_consume(on_message_callback=RabbitWorker.callback, queue='target', auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


if __name__ == "__main__":
    worker = RabbitWorker()
    worker.receive()

