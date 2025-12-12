import logging
import os
import sys

# LOG_PATH = os.environ.get("LOG_PATH", "logs")

# create log directory if it does not exist
# if not os.path.exists(LOG_PATH):
    # os.makedirs(LOG_PATH)

# Logging

# log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_format = logging.Formatter("%(levelname)s\t[%(name)s]\t%(message)s")

logger_ai4cehelper = logging.getLogger("ai4ce_helper")
logger_ai4cehelper.setLevel(logging.DEBUG)
logger_ai4cehelper.propagate = False

stream_handler_ai4cehelper = logging.StreamHandler(sys.stdout)
stream_handler_ai4cehelper.setFormatter(log_format)
# file_handler_ai4cehelper = logging.FileHandler(f"{LOG_PATH}/ai4ce-helper.log", encoding="utf-8")
# file_handler_ai4cehelper.setFormatter(log_format)

# logger_ai4cehelper.addHandler(file_handler_ai4cehelper)
logger_ai4cehelper.addHandler(stream_handler_ai4cehelper)
