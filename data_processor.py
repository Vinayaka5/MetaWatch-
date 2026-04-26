"""
data_processor.py
Processes raw OpenMetadata API responses into clean, dashboard-ready data.
"""

import pandas as pd
from openmetadata_client import get_tables, get_test_cases, get_trend_data
from datetime import datetime


def _extract_table_name(entity_link: str) -> str:
    """Extract table name from entityLink like <#E::table::orders::col>"""
    if '::' in entity_link:
        parts = entity_link.strip('<>').split('::')
        # parts: ['#E', 'table', 'table_name', ...]
        if len(parts) >= 3:
            return parts[2]
    return 'Unknown'


def get_tables_with_health():
    """Returns a list of tables enriched with health status and score."""
    tables = get_tables()
    test_cases = get_test_cases()

    # Build dict: table_name -> list of test statuses
    table_tests = {}
    for tc in test_cases:
        entity_link = tc.get('entityLink', '')
        table_name = _extract_table_name(entity_link)
        if table_name == 'Unknown':
            continue
        if table_name not in table_tests:
            table_tests[table_name] = []
        status = tc.get('testCaseResult', {}).get('testCaseStatus', 'Unknown')
        test_name = tc.get('name', 'Unnamed Test')
        table_tests[table_name].append({'status': status, 'name': test_name})

    result = []
    for table in tables:
        name = table.get('name', 'Unknown')
        fqn = table.get('fullyQualifiedName', name)
        tests = table_tests.get(name, [])
        statuses = [t['status'] for t in tests]

        if not statuses:
            health = 'No Tests'
            score = 0
        else:
            success_count = statuses.count('Success')
            score = int((success_count / len(statuses)) * 100)
            if score >= 80:
                health = 'Healthy'
            elif score >= 50:
                health = 'Warning'
            else:
                health = 'Critical'

        result.append({
            'name': name,
            'fqn': fqn,
            'owner': table.get('owner', {}).get('name', 'N/A'),
            'health': health,
            'score': score,
            'test_count': len(statuses),
            'passed': statuses.count('Success'),
            'failed': statuses.count('Failed'),
            'database': table.get('database', {}).get('name', 'N/A'),
            'tests': tests,
        })

    return result


def get_summary_stats():
    """Returns summary numbers for the home page cards."""
    tables = get_tables_with_health()
    total = len(tables)
    healthy = sum(1 for t in tables if t['health'] == 'Healthy')
    warning = sum(1 for t in tables if t['health'] == 'Warning')
    critical = sum(1 for t in tables if t['health'] == 'Critical')
    no_tests = sum(1 for t in tables if t['health'] == 'No Tests')
    health_pct = int((healthy / total * 100)) if total > 0 else 0

    # Total tests run
    total_tests = sum(t['test_count'] for t in tables)
    total_passed = sum(t['passed'] for t in tables)
    total_failed = sum(t['failed'] for t in tables)

    return {
        'total': total,
        'healthy': healthy,
        'warning': warning,
        'critical': critical,
        'no_tests': no_tests,
        'health_pct': health_pct,
        'total_tests': total_tests,
        'total_passed': total_passed,
        'total_failed': total_failed,
        'critical_tables': [t for t in tables if t['health'] == 'Critical'],
        'warning_tables': [t for t in tables if t['health'] == 'Warning'],
        'last_refreshed': datetime.now().strftime('%d %b %Y, %H:%M'),
        'trend': get_trend_data(),
    }


def get_tests_detail():
    """Returns a flat list of all test cases with their table and status."""
    test_cases = get_test_cases()
    result = []
    for tc in test_cases:
        entity_link = tc.get('entityLink', '')
        table_name = _extract_table_name(entity_link)
        status = tc.get('testCaseResult', {}).get('testCaseStatus', 'Unknown')
        result.append({
            'test_name': tc.get('name', 'Unnamed Test'),
            'table': table_name,
            'status': status,
            'description': tc.get('description', '—'),
        })
    return result
