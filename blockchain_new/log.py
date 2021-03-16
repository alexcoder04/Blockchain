from datetime import datetime
from time import sleep
import os

wait = os.getenv("BLOCKCHAIN_LOG_WAIT")

def log(msg, cat="info"):
    print(f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] [{cat.upper()}] {msg}")
    if wait: sleep(float(wait))
