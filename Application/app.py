import pandas as pd
from flask import Flask, request, jsonify, render_template
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import io

def analyze_overview(df):
    monthly_sales = df.set_index('Order Date')['Sales'].resample('M').sum()
    category_sales = df.groupby('Category')['Sales'].sum()
    return {
        "totalSales": df['Sales'].sum(),
        "totalProfit": df['Profit'].sum(),
        "totalOrders": len(df),
        "totalCustomers": df['Customer ID'].nunique(),
        "salesTrend": {
            "labels": monthly_sales.index.strftime('%Y-%m').tolist(),
            "data": monthly_sales.values.tolist()
        },
        "categoryPerformance": {
            "labels": category_sales.index.tolist(),
            "data": category_sales.values.tolist()
        }
    }

def analyze_forecasting(df):
    monthly_sales = df.set_index('Order Date')['Sales'].resample('M').sum()
    if len(monthly_sales) < 24: # ARIMA and seasonal decomp need sufficient data
        return {"error": "Not enough monthly data for reliable forecasting (requires at least 24 months)."}

    model = ARIMA(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    fitted_model = model.fit()
    forecast = fitted_model.forecast(steps=6)
    decomposition = seasonal_decompose(monthly_sales, model='additive', period=12)
    
    return {
        "forecastChart": {
            "labels": monthly_sales.index.strftime('%Y-%m').tolist() + pd.date_range(start=monthly_sales.index[-1], periods=7, freq='M')[1:].strftime('%Y-%m').tolist(),
            "historical": monthly_sales.values.tolist(),
            "forecast": forecast.values.tolist()
        },
        "seasonalChart": {
            "labels": decomposition.seasonal.index.strftime('%b').tolist(),
            "data": decomposition.seasonal.values.tolist()
        }
    }

def analyze_customers(df):
    reference_date = df['Order Date'].max()
    rfm = df.groupby('Customer ID').agg(
        Recency=('Order Date', lambda x: (reference_date - x.max()).days),
        Frequency=('Row ID', 'count'),
        Monetary=('Sales', 'sum')
    ).reset_index()

    def segment_customer(row):
        if row['Recency'] < 30 and row['Frequency'] > 5: return 'Champions'
        if row['Recency'] < 90 and row['Frequency'] > 3: return 'Loyal Customers'
        if row['Recency'] > 365: return 'At Risk'
        return 'Others'
    
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    segment_counts = rfm['Segment'].value_counts()
    
    return {
        "segmentChart": {
            "labels": segment_counts.index.tolist(),
            "data": segment_counts.values.tolist()
        },
        "riskAlerts": {
            "atRisk": int(segment_counts.get('At Risk', 0)),
            "champions": int(segment_counts.get('Champions', 0))
        }
    }

# --- Flask App ---

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        csv_data = request.data.decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Preprocessing from notebook
        df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
        df.dropna(subset=['Sales', 'Profit', 'Order Date'], inplace=True)

        # Run all analyses
        overview_results = analyze_overview(df.copy())
        forecasting_results = analyze_forecasting(df.copy())
        customer_results = analyze_customers(df.copy())
        
        # Handle potential errors from analysis functions
        if 'error' in forecasting_results:
            return jsonify(forecasting_results)

        full_results = {
            "overview": overview_results,
            "forecasting": forecasting_results,
            "customers": customer_results,
        }
        return jsonify(full_results)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to process the data. Please check the CSV format."}), 500

if __name__ == '__main__':
    app.run(debug=True)