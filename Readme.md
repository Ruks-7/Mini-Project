# AI Mini Project: Superstore Sales Analysis Dashboard

## Overview

This project is a web-based dashboard for analyzing sales data from a superstore. It provides:
- **Sales Overview:** Total sales, profit, orders, and customer stats.
- **Time Series Forecasting:** Predicts future sales using ARIMA and shows seasonal trends.
- **Customer Segmentation:** Segments customers (Champions, Loyal, At Risk, Others) using RFM analysis.

The dashboard is built with **Flask** (Python backend) and **Bootstrap/Chart.js** (frontend).

---

## Folder Structure

```
Mini-Project/
│
├── Application/
│   ├── app.py                # Flask backend
│   ├── requirements.txt      # Python dependencies
│   └── templates/
│       └── index.html        # Dashboard frontend
│
├── analysis.ipynb            # Data analysis notebook
├── shopping_trends_updated.csv # Example dataset
├── Sample_Superstore.csv      # Main dataset
└── Readme.md                 # This file
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd "Mini-Project/Application"
```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv data_env
data_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you see `ModuleNotFoundError: No module named 'flask'`, make sure your virtual environment is activated and run the above command.

### 4. Run the Application

```bash
python app.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## Usage

1. Upload your sales CSV file via the dashboard.
2. View sales trends, forecasts, and customer segments interactively.

---

## Dataset Format

Your CSV should have at least these columns:
- `Order Date`, `Sales`, `Profit`, `Category`, `Customer ID`, `Row ID`

Sample data is provided as `shopping_trends_updated.csv`.

---

## Main Technologies

- Python, Flask, Pandas, Statsmodels
- HTML, Bootstrap, Chart.js

