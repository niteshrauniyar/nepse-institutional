def generate_signal(row):
    score = 0
    reasons = []

    if row.get("accumulation"):
        score += 40
        reasons.append("Smart money accumulation")

    if row.get("large_trade"):
        score += 20
        reasons.append("Large trades detected")

    if row.get("amihud", 1) < 0.001:
        score += 20
        reasons.append("High liquidity")

    if row.get("distribution"):
        score -= 40
        reasons.append("Distribution phase")

    if score > 50:
        signal = "BUY"
    elif score < -20:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    return signal, min(max(score, 0), 100), ", ".join(reasons)


def add_signals(df):
    signals = df.apply(generate_signal, axis=1)
    df["signal"] = [s[0] for s in signals]
    df["confidence"] = [s[1] for s in signals]
    df["reason"] = [s[2] for s in signals]
    return df
