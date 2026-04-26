"""
app.py — MetaWatch Dashboard
Flask web application for Data Quality Monitoring via OpenMetadata.
"""

from flask import Flask, render_template, jsonify
from data_processor import get_tables_with_health, get_summary_stats, get_tests_detail
from openmetadata_client import check_connection, get_trend_data

app = Flask(__name__)


@app.route('/')
def index():
    """Home page: summary cards, alert panel, trend chart."""
    connected = check_connection()
    stats = get_summary_stats()
    return render_template('index.html', stats=stats, connected=connected)


@app.route('/tables')
def tables():
    """Table Health page: sortable list with health scores."""
    tables_data = get_tables_with_health()
    return render_template('tables.html', tables=tables_data)


@app.route('/tests')
def tests():
    """Test Results page: detailed view of all test cases."""
    test_data = get_tests_detail()
    return render_template('tests.html', test_cases=test_data)


@app.route('/api/trend')
def api_trend():
    """JSON endpoint for Chart.js trend data."""
    return jsonify(get_trend_data())


@app.route('/api/status')
def api_status():
    """Quick health check endpoint."""
    connected = check_connection()
    return jsonify({'connected': connected, 'mode': 'live' if connected else 'demo'})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  MetaWatch Dashboard — Starting Up")
    print("  Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
