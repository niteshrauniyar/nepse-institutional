import numpy as np

def full_analysis(df):
    df = df.copy()

    df["return"] = df["close"].pct_change().fillna(0)

    df["amihud"] = abs(df["return"]) / (df["volume"] + 1)

    df["price_change"] = df["close"].diff().fillna(0)

    df["lambda"] = df["price_change"] / (df["volume"] + 1)

    df["signed_volume"] = np.sign(df["price_change"]) * df["volume"]

    df["large_trade"] = df["volume"] > df["volume"].quantile(0.9)

    df["accumulation"] = (df["large_trade"]) & (df["price_change"] > 0)
    df["distribution"] = (df["large_trade"]) & (df["price_change"] < 0)

    return df
