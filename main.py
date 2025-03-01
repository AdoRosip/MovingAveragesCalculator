from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app = Flask(__name__)

def fetch_stock_data(ticker, period="6mo"):
    """Fetch stock data from Yahoo Finance."""
    stock_data = yf.download(ticker, period=period)
    return stock_data

def plot_moving_averages(stock_data, ticker, sma_periods):
    """Generate a plot with moving averages."""
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Close"], label="Close Price", color="blue")

    for period in sma_periods:
        stock_data[f"SMA_{period}"] = stock_data["Close"].rolling(window=period).mean()
        plt.plot(stock_data[f"SMA_{period}"], label=f"{period}-Day SMA")

    plt.title(f"{ticker.upper()} Stock Price with Moving Averages")
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
    sma_periods = [10, 50]  # Default SMA periods

    if request.method == "POST":
        ticker = request.form["ticker"]
        sma_periods = list(map(int, request.form.getlist("sma_periods")))

    try:
        stock_data = fetch_stock_data(ticker)
        image = plot_moving_averages(stock_data, ticker, sma_periods)
    except Exception as e:
        print("Error fetching stock data:", e)

    return render_template("index.html", image=image, ticker=ticker, sma_periods=sma_periods)

if __name__ == "__main__":
    app.run(debug=True)
