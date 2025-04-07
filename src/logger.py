import logging
import os 
from datetime import datetime

# creating log folder
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# creating log file with datetime..whenever generated
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# file name will be like: "log_2025-03-17.log"

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    # levels names can be like : INFO-general, ERROR-error, WARNING, etc.
    level=logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

# test_logger.py file:
# FOR TESTING IF LOGGER<PY IS WORKING OK
# ::
# from src.logger import get_logger
# logger = get_logger(__name__)
# logger.info("Hello ji")