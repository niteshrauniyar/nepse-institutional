import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import random
import time
from datetime import datetime

# ---------------- HEADERS ---------------- #
HEADERS = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120.0"},
    {"User-Agent": "Safari/537.36"},
]

def get_headers():
    return random.choice(HEADERS)


# ---------------- RETRY WRAPPER ---------------- #
def retry(func, retries=3, delay=1):
    for _ in range(retries):
        try:
            result = func()
            if result is not None and len(result) > 0:
                return result
        except Exception:
            time.sleep(delay)
    return None


# =========================
# 1. SHARESSANSAR SCRAPER
# =========================
def fetch_sharesansar():
    def _fetch():
        url = "https://www.sharesansar.com/today-share-price"
        r = requests.get(url, headers=get_headers(), timeout=10)

        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find("table")

        if table is None:
            return None

        rows = table.find_all("tr")
        data = []

        for row in rows[1:]:
            cols = [c.text.strip() for c in row.find_all("td")]

            if len(cols) >= 6:
                try:
                    data.append({
                        "symbol": cols[1],
                        "ltp": float(cols[2].replace(",", "")),
                        "close": float(cols[3].replace(",", "")),
                        "volume": float(cols[5].replace(",", "")),
                        "source": "sharesansar"
                    })
                except:
                    continue

        return pd.DataFrame(data)

    return retry(_fetch)


# =========================
# 2. NEPSE ALPHA (cleaner fallback)
# =========================
def fetch_nepsealpha():
    def _fetch():
        url = "https://www.nepsealpha.com/trading/1"
        r = requests.get(url, headers=get_headers(), timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find_all("tr")

        data = []
        for row in rows:
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) >= 5:
                try:
                    data.append({
                        "symbol": cols[0],
                        "ltp": float(cols[1].replace(",", "")),
                        "close": float(cols[2].replace(",", "")),
                        "volume": float(cols[4].replace(",", "")),
                        "source": "nepsealpha"
                    })
                except:
                    continue

        return pd.DataFrame(data)

    return retry(_fetch)


# =========================
# 3. FALLBACK (always works)
# =========================
def fallback_data():
    symbols = ["NABIL", "GBIME", "NICA", "SCB", "HBL"]

    data = []
    for s in symbols:
        price = np.random.uniform(300, 2000)

        data.append({
            "symbol": s,
            "ltp": round(price, 2),
            "close": round(price * 0.99, 2),
            "volume": int(np.random.randint(10000, 500000)),
            "source": "simulated"
        })

    return pd.DataFrame(data)


# =========================
# MASTER PIPELINE (IMPORTANT)
# =========================
def fetch_market_data():
    """
    Priority order:
    1. Sharesansar
    2. NepseAlpha
    3. fallback simulation
    """

    df = fetch_sharesansar()

    if df is not None and len(df) > 0:
        df["timestamp"] = datetime.now()
        return df

    df = fetch_nepsealpha()

    if df is not None and len(df) > 0:
        df["timestamp"] = datetime.now()
        return df

    df = fallback_data()
    df["timestamp"] = datetime.now()
    return df
