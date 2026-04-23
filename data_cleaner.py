import pandas as pd

# 🔥 COLUMN DETECTION ENGINE
COLUMN_MAP = {
    "symbol": ["symbol", "company", "stock", "scrip"],
    "close": ["close", "ltp", "last traded price", "price"],
    "volume": ["volume", "qty", "quantity", "totaltradedquantity"],
    "high": ["high"],
    "low": ["low"]
}

def detect_column(df, target):
    for col in df.columns:
        col_clean = str(col).lower().strip()
        if col_clean in COLUMN_MAP[target]:
            return col
    return None


def normalize_df(df):
    df = df.copy()
    df.columns = [str(c).lower().strip() for c in df.columns]

    clean_df = pd.DataFrame()

    for key in COLUMN_MAP.keys():
        col = detect_column(df, key)
        if col:
            clean_df[key] = df[col]
        else:
            clean_df[key] = None

    # 🔥 CLEAN VALUES
    for col in clean_df.columns:
        clean_df[col] = (
            clean_df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("-", "")
        )
        try:
            clean_df[col] = pd.to_numeric(clean_df[col])
        except:
            pass

    # SYMBOL fallback
    if clean_df["symbol"].isnull().all():
        clean_df["symbol"] = [f"STOCK_{i}" for i in range(len(clean_df))]

    clean_df["volume"] = clean_df["volume"].fillna(0)
    clean_df["close"] = clean_df["close"].fillna(0)

    return clean_df


def clean_data(data_list):
    if isinstance(data_list, list):
        cleaned = [normalize_df(df) for df in data_list]
        merged = pd.concat(cleaned, ignore_index=True)

        # 🔥 GROUP + MERGE MULTI-SOURCE
        merged = (
            merged.groupby("symbol")
            .agg({
                "close": "mean",
                "volume": "sum",
                "high": "max",
                "low": "min"
            })
            .reset_index()
        )

        return merged

    return normalize_df(data_list)
