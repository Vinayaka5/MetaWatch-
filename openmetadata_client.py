"""
openmetadata_client.py
Handles all communication with the OpenMetadata REST API.
Falls back to rich mock data if OpenMetadata is not running locally.
"""

import requests
import base64
from datetime import datetime, timedelta
import random

# OpenMetadata running locally on Docker
BASE_URL = 'http://localhost:8585/api/v1'

# Auth header: Base64 encode of admin:admin
credentials = base64.b64encode(b'admin:admin').decode('utf-8')
HEADERS = {
    'Authorization': f'Basic {credentials}',
    'Content-Type': 'application/json'
}

# ─────────────────────────────────────────────
# Mock data — used when OpenMetadata is offline
# ─────────────────────────────────────────────

MOCK_TABLES = [
    {"name": "orders", "fullyQualifiedName": "retail_db.public.orders",
     "database": {"name": "retail_db"}, "owner": {"name": "data_team"}},
    {"name": "customers", "fullyQualifiedName": "retail_db.public.customers",
     "database": {"name": "retail_db"}, "owner": {"name": "analytics"}},
    {"name": "products", "fullyQualifiedName": "retail_db.public.products",
     "database": {"name": "retail_db"}, "owner": {"name": "analytics"}},
    {"name": "transactions", "fullyQualifiedName": "finance_db.public.transactions",
     "database": {"name": "finance_db"}, "owner": {"name": "finance_team"}},
    {"name": "inventory", "fullyQualifiedName": "retail_db.public.inventory",
     "database": {"name": "retail_db"}, "owner": {"name": "ops_team"}},
    {"name": "user_events", "fullyQualifiedName": "analytics_db.public.user_events",
     "database": {"name": "analytics_db"}, "owner": {"name": "data_science"}},
    {"name": "sessions", "fullyQualifiedName": "analytics_db.public.sessions",
     "database": {"name": "analytics_db"}, "owner": {"name": "data_science"}},
    {"name": "payments", "fullyQualifiedName": "finance_db.public.payments",
     "database": {"name": "finance_db"}, "owner": {"name": "finance_team"}},
    {"name": "returns", "fullyQualifiedName": "retail_db.public.returns",
     "database": {"name": "retail_db"}, "owner": {"name": "ops_team"}},
    {"name": "dim_date", "fullyQualifiedName": "warehouse.public.dim_date",
     "database": {"name": "warehouse"}, "owner": {"name": "N/A"}},
]

MOCK_TEST_CASES = [
    # orders: 2 pass, 1 fail → Warning
    {"entityLink": "<#E::table::orders>", "name": "orders_no_nulls",
     "testCaseResult": {"testCaseStatus": "Success"}},
    {"entityLink": "<#E::table::orders>", "name": "orders_row_count",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    {"entityLink": "<#E::table::orders>", "name": "orders_no_dupes",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # customers: all pass → Healthy
    {"entityLink": "<#E::table::customers>", "name": "customers_no_nulls",
     "testCaseResult": {"testCaseStatus": "Success"}},
    {"entityLink": "<#E::table::customers>", "name": "customers_pk_unique",
     "testCaseResult": {"testCaseStatus": "Success"}},
    {"entityLink": "<#E::table::customers>", "name": "customers_email_valid",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # products: all pass → Healthy
    {"entityLink": "<#E::table::products>", "name": "products_price_positive",
     "testCaseResult": {"testCaseStatus": "Success"}},
    {"entityLink": "<#E::table::products>", "name": "products_no_nulls",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # transactions: 1 pass, 2 fail → Critical
    {"entityLink": "<#E::table::transactions>", "name": "txn_amount_positive",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    {"entityLink": "<#E::table::transactions>", "name": "txn_no_nulls",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    {"entityLink": "<#E::table::transactions>", "name": "txn_row_count",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # inventory: all pass → Healthy
    {"entityLink": "<#E::table::inventory>", "name": "inventory_stock_nonneg",
     "testCaseResult": {"testCaseStatus": "Success"}},
    {"entityLink": "<#E::table::inventory>", "name": "inventory_no_nulls",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # user_events: 1 fail → Warning
    {"entityLink": "<#E::table::user_events>", "name": "events_timestamp_valid",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    {"entityLink": "<#E::table::user_events>", "name": "events_user_id_notnull",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # sessions: all pass
    {"entityLink": "<#E::table::sessions>", "name": "sessions_no_nulls",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # payments: all fail → Critical
    {"entityLink": "<#E::table::payments>", "name": "payments_amount_check",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    {"entityLink": "<#E::table::payments>", "name": "payments_no_dupes",
     "testCaseResult": {"testCaseStatus": "Failed"}},
    # returns: pass
    {"entityLink": "<#E::table::returns>", "name": "returns_ref_valid",
     "testCaseResult": {"testCaseStatus": "Success"}},
    # dim_date: no tests
]


def _generate_trend_data():
    """Generate 7-day quality score trend data."""
    base = 72
    trend = []
    for i in range(7):
        day = datetime.now() - timedelta(days=6 - i)
        score = max(40, min(100, base + random.randint(-8, 12)))
        base = score
        trend.append({
            "date": day.strftime("%b %d"),
            "score": score
        })
    return trend


def check_connection():
    """Test if OpenMetadata is reachable."""
    try:
        r = requests.get(f'{BASE_URL}/system/status', headers=HEADERS, timeout=4)
        return r.status_code == 200
    except Exception:
        return False


def get_tables(limit=50):
    """Fetch list of tables. Falls back to mock data if offline."""
    try:
        url = f'{BASE_URL}/tables?limit={limit}'
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json().get('data', [])
    except Exception:
        pass
    return MOCK_TABLES


def get_test_cases(limit=100):
    """Fetch all data quality test cases. Falls back to mock data if offline."""
    try:
        url = f'{BASE_URL}/dataQuality/testCases?limit={limit}'
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json().get('data', [])
    except Exception:
        pass
    return MOCK_TEST_CASES


def get_test_results(test_case_fqn):
    """Fetch result history for a specific test case."""
    try:
        url = f'{BASE_URL}/dataQuality/testCases/{test_case_fqn}/testCaseResult'
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json().get('data', [])
    except Exception:
        pass
    return []


def get_trend_data():
    """Return 7-day quality score trend. Uses mock data."""
    return _generate_trend_data()
