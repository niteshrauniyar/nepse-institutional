import plotly.graph_objects as go

def plot_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"],
        mode='lines',
        name='Price'
    ))

    buys = df[df["signal"] == "BUY"]
    sells = df[df["signal"] == "SELL"]

    fig.add_trace(go.Scatter(
        x=buys.index,
        y=buys["close"],
        mode='markers',
        name='BUY',
        marker=dict(symbol='triangle-up', size=10)
    ))

    fig.add_trace(go.Scatter(
        x=sells.index,
        y=sells["close"],
        mode='markers',
        name='SELL',
        marker=dict(symbol='triangle-down', size=10)
    ))

    fig.update_layout(template="plotly_dark")

    return fig
