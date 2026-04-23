def generate_signal(row):
    score = 0
    reasons = []

    if row["accumulation"]:
        score += 40
        reasons.append("Accumulation detected")

    if row["large_trade"]:
        score += 25
        reasons.append("Institutional volume spike")

    if row["amihud"] < 0.001:
        score += 15
        reasons.append("High liquidity")

    if row["distribution"]:
        score -= 50
        reasons.append("Distribution detected")

    if score >= 50:
        signal = "BUY"
    elif score <= -20:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    return signal, max(min(score, 100), 0), ", ".join(reasons)


def add_signals(df):
    results = df.apply(generate_signal, axis=1)

    df["signal"] = [r[0] for r in results]
    df["confidence"] = [r[1] for r in results]
    df["reason"] = [r[2] for r in results]

    return df
