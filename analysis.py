import numpy as np
from sklearn.cluster import KMeans

def safe_div(a, b):
    return a / (b + 1e-9)

def full_analysis(df):
    df = df.copy()

    df["return"] = df["close"].pct_change().fillna(0)

    df["amihud"] = abs(df["return"]) / (df["volume"] + 1)

    df["price_change"] = df["close"].diff().fillna(0)
    df["lambda"] = safe_div(df["price_change"], df["volume"])

    df["signed_volume"] = np.sign(df["price_change"]) * df["volume"]

    df["large_trade"] = df["volume"] > df["volume"].quantile(0.9)

    df["accumulation"] = (df["large_trade"]) & (df["price_change"] > 0)
    df["distribution"] = (df["large_trade"]) & (df["price_change"] < 0)

    # ML clustering
    try:
        X = df[["close", "volume"]].fillna(0)
        model = KMeans(n_clusters=3, n_init=10)
        df["cluster"] = model.fit_predict(X)
    except:
        df["cluster"] = 0

    return df
