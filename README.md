# Stock Price Analysis Web App

## 📌 Overview

This project is a **Flask web application** that allows users to analyze stock prices using **Moving Averages, Bollinger Bands, and Stock Analysis**. Users can select a stock, apply technical indicators, and visualize the results in an interactive chart.

## 🚀 Features

- 📥 **Fetch real-time stock data** using `yfinance`
- 📊 **Simple Moving Averages (SMA)** & **Exponential Moving Averages (EMA)** calculation
- 📈 **Bollinger Bands** for volatility analysis
- 📉 **Stock interpretation** based on SMA, EMA, and Bollinger Bands
- 🎨 **Styled UI** with CSS
- 🖼️ **Dynamic charts** using `matplotlib`

## 🔹 Tech Stack

- **Backend**: Python, Flask
- **Data Processing**: Pandas, Matplotlib, yfinance
- **Frontend**: HTML, CSS, Jinja2

## 📂 Project Structure

```
📁 movingAveragesCalculator/
│── 📁 static/           # CSS stylesheets
│   └── style.css
│── 📁 templates/        # HTML templates
│   └── index.html
│── main.py             # Flask backend
│── requirements.txt    # Dependencies
│── README.md           # Documentation
```

## 📌 How to Run the App

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd movingAveragesCalculator
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask server**
   ```bash
   python main.py
   ```
5. **Open the app in a browser**
   - URL: `http://127.0.0.1:5000/`

## 📈 Indicators & Calculations

### **1️⃣ Simple Moving Average (SMA)**

Formula:

```
SMA = Sum of Closing Prices over N days / N
```

### **2️⃣ Exponential Moving Average (EMA)**

Formula:

```
EMA = (Today's Price * K) + (Yesterday's EMA * (1 - K))
```

where **K = 2 / (N+1)**

### **3️⃣ Bollinger Bands**

```
Upper Band = SMA_20 + (2 * Std Dev)
Lower Band = SMA_20 - (2 * Std Dev)
```

## 📊 Stock Analysis Interpretation

- **Stock trading above SMA_20** → Potential **uptrend** 📈
- **Stock below SMA_20** → Possible **downtrend** 📉
- **Above Upper Bollinger Band** → Might be **overbought** 🚀
- **Below Lower Bollinger Band** → Might be **oversold** 🔻

## 🛠️ Future Improvements

- ✅ **Deploy the app online**
- ✅ **Add a Discounted Cash Flow (DCF) valuation model**
- ✅ **Use Plotly for interactive charts**
- ✅ **Enhance the UI with Bootstrap or Tailwind**

---

📌 **Author:** [Your Name]  
📌 **License:** MIT  
📌 **Contributions:** Open for pull requests! 🚀
