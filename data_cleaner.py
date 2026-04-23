import pandas as pd

def clean_data(df):
    df = df.copy()

    df.columns = [c.lower().strip() for c in df.columns]

    rename_map = {
        "ltp": "close",
        "last traded price": "close",
        "totaltradedquantity": "volume"
    }

    df.rename(columns=rename_map, inplace=True)

    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", "")
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    df = df.dropna(subset=["close"], errors="ignore")

    return df
