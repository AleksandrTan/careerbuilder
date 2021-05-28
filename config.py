TEST_MODE = True
TARGET_HOST = "https://www.careerbuilder.com"
TEST_HOST = "http://127.0.0.1:8000"

# ---------------------------------------------------- RabbitMQ--------------------------------------------------
RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672

# The number of attempts to connect to the Rabbit server.
ATTEMPTS_TO_CONNECT_RABBIT = 5
# Delay interval, in seconds, after each attempt to connect to the Rabbit server.
TIME_TO_CONNECT_RABBIT = 5

# ------------------------------------------------ systems urls---------------------------------------------------
API_HOST = "http://127.0.0.1:8000"
FILE_DOWNLOAD = "/mspanel/bot/get_file/"
TASK_RESULT_DONE = "/mspanel/api/order/order_id/done/"
TASK_RESULT_FAIL = "/mspanel/api/order/order_id/fail/"
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
    "api_connect_error": {"message": "Attention! The system api is not responding! message code"},
    "no_file": {"message": "Order - order. Mailing file not found."}
}

MESSAGES_ERROR_API = {
    "no_file": {
        "message": "Mailing file not found."
    }
}
