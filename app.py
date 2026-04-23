import streamlit as st
from data_fetcher import fetch_all
from data_cleaner import clean_data
from analysis import full_analysis
from signals import add_signals
from charts import plot_chart

st.set_page_config(layout="wide")

st.title("🏦 NEPSE Institutional Intelligence System")

@st.cache_data(show_spinner=False)
def load_data():
    raw = fetch_all()
    clean = clean_data(raw)
    analyzed = full_analysis(clean)
    final = add_signals(analyzed)
    return final

try:
    df = load_data()
except Exception as e:
    st.error("Data pipeline failed. Using fallback.")
    from data_fetcher import fallback_data
    df = fallback_data()

tab1, tab2, tab3, tab4 = st.tabs([
    "Market Overview",
    "Institutional Analysis",
    "Signals",
    "Charts"
])

with tab1:
    st.dataframe(df)

with tab2:
    st.dataframe(df[["symbol", "amihud", "lambda", "cluster", "accumulation", "distribution"]])

with tab3:
    st.dataframe(df[["symbol", "signal", "confidence", "reason"]])

with tab4:
    st.plotly_chart(plot_chart(df), use_container_width=True)
