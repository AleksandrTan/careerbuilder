import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_MODE = os.getenv('TEST_MODE', default=False)

# ---------------------------------------------------- Requests--------------------------------------------------
# The number of attempts to request a change of proxy server
NUMBER_REQUESTS = 5

# delay requests
DELAY_REQUESTS = 5

# request timeout
REQUEST_TIMEOUT = 6

# response timeout
RESPONSE_TIMEOUT = 21

# ---------------------------------------------------- RabbitMQ--------------------------------------------------
RABBIT_HOST = os.getenv('RABBIT_HOST', default='127.0.0.1')
RABBIT_PORT = os.getenv('RABBIT_PORT', default=5672)
QUEUE_NAME = os.getenv('QUEUE_NAME', default="jobspamer")

# The number of attempts to connect to the Rabbit server.
ATTEMPTS_TO_CONNECT_RABBIT = 5
# Delay interval, in seconds, after each attempt to connect to the Rabbit server.
TIME_TO_CONNECT_RABBIT = 5

# ------------------------------------------------ Systems urls---------------------------------------------------
API_HOST = os.getenv('API_HOST', default="http://127.0.0.1:8001")
FILE_DOWNLOAD = "/mainsystem/bot/get_file/"
TASK_RESULT_SUCCESS = "/mainsystem/api/order/order_id/success/"
TASK_RESULT_FAIL = "/mainsystem/api/order/order_id/fail/"
UPDATE_PROXY = "/mainsystem/proxy/update/"
# The number of attempts to connect to the main server.
ATTEMPTS_TO_CONNECT = 5
# Delay interval, in seconds, after each attempt to connect to the main server.
TIME_TO_CONNECT = 5

# ----------------------------------------logs---------------------------------------------------------------------
# Write errors to a log file
IS_LOG_FILE_WRITE = True

# Outputting notifications to the console
IS_CONSOLE = True
