import sys
import json

from logsource.logconfig import logger
import config


class LogModule:
    def __init__(self):
        self.map_messages = config.MESSAGES_LOG
        self.is_console = config.IS_CONSOLE
        self.is_file_write = config.IS_LOG_FILE_WRITE

    def _send_task_report(self, key: str, data: dict = None):
        message = self.map_messages[key]["message"]
        if data:
            for key in data:
                if type(data[key]) is dict:
                    strings = json.dumps(str(data[key]))
                    message = message.replace(key, strings)
                    continue
                message = message.replace(key, str(data[key]))
                continue
        if self.is_file_write:
            logger.warning(message)

        if self.is_console:
            sys.stdout.write(message)
