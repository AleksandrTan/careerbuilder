TEST_MODE = True
LINK_EXAMPLE = "https://www.careerbuilder.com/job/J301R0620YJ2PPJK564"
TARGET_HOST = "https://www.careerbuilder.com"
TEST_HOST = "http://127.0.0.1:8000"

# request timeout
REQUEST_TIMEOUT = 6
# response timeout
RESPONSE_TIMEOUT = 21


# ---------------------------------------------------- RabbitMQ--------------------------------------------------
RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672

# The number of attempts to connect to the Rabbit server.
ATTEMPTS_TO_CONNECT_RABBIT = 5
# Delay interval, in seconds, after each attempt to connect to the Rabbit server.
TIME_TO_CONNECT_RABBIT = 5

# ------------------------------------------------ systems urls---------------------------------------------------
API_HOST = "http://127.0.0.1:8000"
FILE_DOWNLOAD = "/mainsystem/bot/get_file/"
TASK_RESULT_DONE = "/mainsystem/api/order/order_id/done/"
TASK_RESULT_FAIL = "/mainsystem/api/order/order_id/fail/"
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
                                      "respond correctly! code message"}
}

MESSAGES_ERROR_API = {
    "no_file": {
        "message": "Mailing file not found."
    },
    "target_connect_error": {
        "message": "Attention! Target resource is not responding! \n Code - status_code \n Messages - message"
    },
}
