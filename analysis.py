import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def amihud(df):
    df["return"] = df["close"].pct_change()
    df["amihud"] = abs(df["return"]) / (df["volume"] + 1)
    return df

def kyle_lambda(df):
    df["price_change"] = df["close"].diff()
    df["lambda"] = df["price_change"] / (df["volume"] + 1)
    return df

def order_flow(df):
    df["signed_volume"] = np.sign(df["close"].diff()) * df["volume"]
    df["flow_autocorr"] = df["signed_volume"].autocorr()
    return df

def trade_size(df):
    threshold = df["volume"].quantile(0.9)
    df["large_trade"] = df["volume"] > threshold
    return df

def clustering(df):
    X = df[["close", "volume"]].fillna(0)
    model = KMeans(n_clusters=3, n_init=10)
    df["cluster"] = model.fit_predict(X)
    return df

def smart_money(df):
    df["accumulation"] = (df["volume"] > df["volume"].mean()) & (df["close"].diff() > 0)
    df["distribution"] = (df["volume"] > df["volume"].mean()) & (df["close"].diff() < 0)
    return df

def full_analysis(df):
    df = amihud(df)
    df = kyle_lambda(df)
    df = order_flow(df)
    df = trade_size(df)
    df = clustering(df)
    df = smart_money(df)
    return df
