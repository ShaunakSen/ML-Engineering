import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
## Simple Stock Price App

> Shown are the stock closing price and volume of Apple
""")

st.markdown("---")

tickerSymbol = "AAPL"

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

st.subheader("Closing Price")
st.line_chart(data=tickerDf.Close)
st.subheader("Volume")
st.line_chart(data=tickerDf.Volume)