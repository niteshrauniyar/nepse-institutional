import random
import time

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/110.0"},
    {"User-Agent": "Safari/537.36"},
]

def get_headers():
    return random.choice(HEADERS_LIST)

def retry(func, retries=3, delay=2):
    for i in range(retries):
        try:
            return func()
        except Exception:
            time.sleep(delay)
    return None
