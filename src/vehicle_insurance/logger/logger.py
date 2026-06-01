import logging
import os
from datetime import datetime

# Folder where log files will be stored
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name based on current date and time
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure Python logging
logging.basicConfig(
    filename=LOG_PATH,
    format="[ %(asctime)s ] %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Export the configured logger
logger = logging