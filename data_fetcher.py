import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import get_headers, retry

def fetch_nepse_api():
    def _fetch():
        url = "https://nepsealpha.com/api/symbols"
        r = requests.get(url, headers=get_headers(), timeout=10)
        return pd.DataFrame(r.json())
    return retry(_fetch)

def fetch_sharesansar():
    def _fetch():
        url = "https://www.sharesansar.com/today-share-price"
        r = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        table = soup.find("table")
        rows = table.find_all("tr")[1:]

        data = []
        for row in rows:
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) > 5:
                data.append(cols)

        df = pd.DataFrame(data)
        return df
    return retry(_fetch)

def fetch_nepsealpha():
    def _fetch():
        url = "https://nepsealpha.com/trading/1"
        r = requests.get(url, headers=get_headers(), timeout=10)
        return pd.read_html(r.text)[0]
    return retry(_fetch)

def fallback_data():
    import numpy as np
    symbols = ["NABIL", "NRIC", "NTC", "GBIME"]
    data = []

    for s in symbols:
        price = np.random.uniform(300, 1200)
        volume = np.random.randint(10000, 100000)

        data.append({
            "symbol": s,
            "close": price,
            "volume": volume,
            "high": price * 1.05,
            "low": price * 0.95
        })

    return pd.DataFrame(data)

def fetch_all():
    sources = [
        fetch_nepse_api,
        fetch_sharesansar,
        fetch_nepsealpha
    ]

    for src in sources:
        data = src()
        if data is not None and len(data) > 0:
            return data

    return fallback_data()
