import logging
import os 
from datetime import datetime

# creating log folder
LOGS_DIR = "logs"
os.mekedir(LOGS_DIR, exist_ok=True)

# creating log file with datetime..whenever generated
LOG_FILE = os