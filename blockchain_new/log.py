from datetime import datetime
from time import sleep

def log(msg, cat="info"):
    print(f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] [{cat.upper()}] {msg}")
    sleep(1)
