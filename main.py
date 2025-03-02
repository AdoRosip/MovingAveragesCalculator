from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import io
import base64
import matplotlib
matplotlib.use("Agg")  # Non-GUI backend for Flask
import matplotlib.pyplot as plt

app = Flask(__name__)

def fetch_stock_data(ticker, period="1y"):
    """Fetch stock data from Yahoo Finance."""
    stock_data = yf.download(ticker, period=period)
    return stock_data

def analyze_stock(stock_data):
    """Generate stock interpretation based on indicators."""
    latest_price = float(stock_data["Close"].dropna().iloc[-1])
    analysis = []

    print("\n---- DEBUG INFO ----")
    print(f"Latest Price: {latest_price}")

    # Ensure SMA_20 exists and has valid values
    if "SMA_20" in stock_data:
        print(f"SMA_20 Last 5 Values:\n{stock_data['SMA_20'].tail()}")  # Debugging print
        clean_sma = stock_data["SMA_20"].dropna()

        if not clean_sma.empty:
            latest_sma = clean_sma.iloc[-1]  # Ensure only a single value is used
            print(f"Latest SMA_20: {latest_sma}")  # Debugging print
            print(f"comapre latest_price,")
            print(f"comapre latestSMA,{latest_sma}")
            if latest_price > float(latest_sma):  # Convert to float for safety
                analysis.append("📈 The stock is trading above its 20-day SMA, which may indicate an uptrend.")
            else:
                analysis.append("📉 The stock is trading below its 20-day SMA, suggesting a potential downtrend.")
        else:
            analysis.append("⚠️ SMA_20 data is missing or insufficient to generate insights.")

    # Ensure EMA_10 exists and has valid values
    if "EMA_10" in stock_data:
        print(f"EMA_10 Last 5 Values:\n{stock_data['EMA_10'].tail()}")  # Debugging print
        clean_ema = stock_data["EMA_10"].dropna()

        if not clean_ema.empty:
            latest_ema = clean_ema.iloc[-1]  # Ensure only a single value is used
            print(f"Latest EMA_10: {latest_ema}")  # Debugging print

            if latest_price > float(latest_ema):  # Convert to float for safety
                analysis.append("✅ The stock is above its 10-day EMA, signaling short-term bullish momentum.")
            else:
                analysis.append("⚠️ The stock is below its 10-day EMA, indicating potential weakness.")
        else:
            analysis.append("⚠️ EMA_10 data is missing or insufficient.")

    # Ensure Bollinger Bands exist and are not empty
    if "BB_Upper" in stock_data and "BB_Lower" in stock_data:
        print(f"BB_Upper Last 5 Values:\n{stock_data['BB_Upper'].tail()}")  # Debugging print
        print(f"BB_Lower Last 5 Values:\n{stock_data['BB_Lower'].tail()}")  # Debugging print

        clean_bb_upper = stock_data["BB_Upper"].dropna()
        clean_bb_lower = stock_data["BB_Lower"].dropna()

        if not clean_bb_upper.empty and not clean_bb_lower.empty:
            latest_bb_upper = clean_bb_upper.iloc[-1]  # Ensure only a single value is used
            latest_bb_lower = clean_bb_lower.iloc[-1]  # Ensure only a single value is used
            print(f"Latest BB_Upper: {latest_bb_upper}")  # Debugging print
            print(f"Latest BB_Lower: {latest_bb_lower}")  # Debugging print

            if latest_price > float(latest_bb_upper):  # Convert to float for safety
                analysis.append("🚀 The stock price is above the upper Bollinger Band, suggesting it may be overbought.")
            elif latest_price < float(latest_bb_lower):  # Convert to float for safety
                analysis.append("📉 The stock is below the lower Bollinger Band, which could indicate an oversold condition.")
        else:
            analysis.append("⚠️ Bollinger Band data is missing or insufficient.")

    print("\n---- END DEBUG ----\n")

    return analysis


def plot_stock_indicators(stock_data, ticker, sma_periods, ema_periods, show_bollinger):
    """Generate a plot with SMA, EMA, and Bollinger Bands."""
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Close"], label="Close Price", color="blue")

    for period in sma_periods:
        stock_data[f"SMA_{period}"] = stock_data["Close"].rolling(window=period).mean()
        plt.plot(stock_data[f"SMA_{period}"], label=f"{period}-Day SMA", linestyle="dashed")

    for period in ema_periods:
        stock_data[f"EMA_{period}"] = stock_data["Close"].ewm(span=period, adjust=False).mean()
        plt.plot(stock_data[f"EMA_{period}"], label=f"{period}-Day EMA", linestyle="solid")

    if show_bollinger:
        stock_data["SMA_20"] = stock_data["Close"].rolling(window=20).mean()
        stock_data["BB_Std"] = stock_data["Close"].rolling(window=20).std()
        stock_data["BB_Upper"] = stock_data["SMA_20"] + (2 * stock_data["BB_Std"])
        stock_data["BB_Lower"] = stock_data["SMA_20"] - (2 * stock_data["BB_Std"])

        plt.plot(stock_data["BB_Upper"], label="Bollinger Upper", linestyle="dotted", color="green")
        plt.plot(stock_data["BB_Lower"], label="Bollinger Lower", linestyle="dotted", color="red")

    plt.title(f"{ticker.upper()} Stock Price with Indicators")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()

    # Save plot to a string buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return encoded_image

@app.route("/", methods=["GET", "POST"])
def index():
    image = None
    ticker = "AAPL"  # Default stock
    sma_periods = [10, 50]  # Default SMA
    ema_periods = [10, 50]  # Default EMA
    show_bollinger = False
    stock_analysis = []

    if request.method == "POST":
        ticker = request.form["ticker"]
        sma_periods = list(map(int, request.form.getlist("sma_periods")))
        ema_periods = list(map(int, request.form.getlist("ema_periods")))
        show_bollinger = "bollinger" in request.form

    try:
        stock_data = fetch_stock_data(ticker)

        # Ensure SMA_20 is always calculated
        stock_data["SMA_20"] = stock_data["Close"].rolling(window=20).mean()

        # Ensure EMA_10 is always calculated
        stock_data["EMA_10"] = stock_data["Close"].ewm(span=10, adjust=False).mean()

        # Ensure Bollinger Bands are calculated if enabled
        if show_bollinger:
            stock_data["BB_Std"] = stock_data["Close"].rolling(window=20).std()
            stock_data["BB_Upper"] = stock_data["SMA_20"] + (2 * stock_data["BB_Std"])
            stock_data["BB_Lower"] = stock_data["SMA_20"] - (2 * stock_data["BB_Std"])

        # Generate stock analysis
        stock_analysis = analyze_stock(stock_data)

        # Generate the plot
        image = plot_stock_indicators(stock_data, ticker, sma_periods, ema_periods, show_bollinger)

    except Exception as e:
        print("Error fetching stock data:", e)

    return render_template(
        "index.html",
        image=image,
        ticker=ticker,
        sma_periods=sma_periods,
        ema_periods=ema_periods,
        show_bollinger=show_bollinger,
        stock_analysis=stock_analysis
    )


if __name__ == "__main__":
    app.run(debug=True)
