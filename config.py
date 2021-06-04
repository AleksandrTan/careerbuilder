import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_MODE = True
LINK_EXAMPLE = "https://www.careerbuilder.com/job/J301R0620YJ2PPJK564"

# ---------------------------------------------------- Requests--------------------------------------------------
# The number of attempts to request a change of proxy server
NUMBER_REQUESTS = 5

# delay requests
DELAY_REQUESTS = 10

# request timeout
REQUEST_TIMEOUT = 6

# response timeout
RESPONSE_TIMEOUT = 21

# ---------------------------------------------------- RabbitMQ--------------------------------------------------
RABBIT_HOST = os.getenv('RABBIT_HOST', default='localhost')
RABBIT_PORT = os.getenv('RABBIT_PORT', default=5672)

# The number of attempts to connect to the Rabbit server.
ATTEMPTS_TO_CONNECT_RABBIT = 5
# Delay interval, in seconds, after each attempt to connect to the Rabbit server.
TIME_TO_CONNECT_RABBIT = 5

# ------------------------------------------------ Systems urls---------------------------------------------------
API_HOST = os.getenv('API_HOST', default="http://127.0.0.1:8000")
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

# Messages to log file and console
MESSAGES_LOG = {
    "target_connect_error": {"message": "Attention! Target resource is not responding! message code"},
    "api_connect_error": {"message": "Attention! The system api is not responding! message code"},
    "no_file": {"message": "Order - order. Mailing file not found."},
    "main_content_error": {"message": "Order - order. When Requesting a start link, the target resource did not "
                                      "respond correctly!Perhaps the proxy server did not respond in time. code message"},
    "no_links_found": {"message": "Order - order. An error occurred while executing the task. No links found on the "
                                  "main page. The target resource may have changed the source code!"},

    "no_button_found": {"message": "Order - order. An error occurred while executing the task. No links to form pages "
                                   "were found. The target resource may have changed the source code!"}
}

MESSAGES_ERROR_API = {
    "no_file": {
        "message": "Mailing file not found."
    },
    "target_connect_error": {
        "message": "Attention! Target resource is not responding! If code 403 - Perhaps the proxy server did not "
                   "respond in time. \n Code - status_code \n Messages - message \n Proxy - pserver"
    },
    "no_links_found": {"message": "An error occurred while executing the task. No links found on the "
                                  "main page. The target resource may have changed the source code!"},
    "no_button_found": {"message": "An error occurred while executing the task. No links to form pages were found. "
                                   "The target resource may have changed the source code!"}
}

if __name__ == "__main__":
    print(os.getenv('DELAY_REQUESTS'))
    print(os.environ.get('DELAY_REQUESTS'))
