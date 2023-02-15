import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# CoinGecko API URL and parameters
base_url = 'https://api.coingecko.com/api/v3'
price_endpoint = '/simple/price'
history_endpoint = '/coins/{id}/market_chart'
params = {'vs_currency': 'usd'}

# List of available ticker IDs
ticker_ids = ['bitcoin', 'ethereum', 'cardano', 'binancecoin', 'dogecoin', 'polkadot', 'ripple', 'uniswap', 'chainlink', 'litecoin']

# Render the HTML form with the drop-down menu
@app.route('/')
def index():
    return render_template('index.html', ticker_ids=ticker_ids)

# Get current price data for a cryptocurrency
@app.route('/price', methods=['POST'])
def get_current_price():
    ticker_id = request.form['ticker_id']
    if ticker_id not in ticker_ids:
        return jsonify({'error': 'Invalid ticker ID'})
    url = base_url + price_endpoint
    params['ids'] = ticker_id
    response = requests.get(url, params=params).json()
    return jsonify(response[ticker_id]['usd'])

# Get historical price data for a cryptocurrency
@app.route('/history', methods=['POST'])
def get_historical_price():
    ticker_id = request.form['ticker_id']
    days = request.form['days']
    if ticker_id not in ticker_ids:
        return jsonify({'error': 'Invalid ticker ID'})
    url = base_url + history_endpoint.format(id=ticker_id)
    params['vs_currency'] = 'usd'
    params['days'] = days
    response = requests.get(url, params=params).json()
    prices = response['prices']
    data = {'date': [p[0] for p in prices], 'price': [p[1] for p in prices]}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
