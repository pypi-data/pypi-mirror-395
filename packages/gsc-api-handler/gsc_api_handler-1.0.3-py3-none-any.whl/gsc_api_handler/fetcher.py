# src/gsc_api_handler/fetcher.py

import sqlite3
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .auth import authorize_creds
from .utils import execute_request

# === Configuration ===
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
DEFAULT_DIMENSIONS = ['country', 'device', 'query', 'page', 'date']
DEFAULT_DB_TABLE = 'gsc_data'

def fetch_and_store_gsc_data(
    site_url: str,
    db_path: str,
    creds_path: str,
    token_path: str,
    dimensions: list[str] = None,
    start_date: str = None,
    end_date: str = None,
    table_name: str = DEFAULT_DB_TABLE
) -> int:
    """
    Fetch GSC data and store it into SQLite DB.

    Returns number of rows saved.
    """
    # === Date ===
    today = datetime.today().date()
    if not end_date:
        end_date = (today - relativedelta(days=2)).strftime('%Y-%m-%d')
    if not start_date:
        start_date = (today - relativedelta(months=16)).strftime('%Y-%m-%d')

    if end_date > today.strftime('%Y-%m-%d'):
        logging.warning(f"⚠️ end_date lies in the future ({end_date}). Setting will be for ({today})")
        end_date = today.strftime('%Y-%m-%d')

    dims = dimensions if dimensions else DEFAULT_DIMENSIONS

    # === Auth ===
    service = authorize_creds(creds_path, token_path)

    # === SQLite Setup ===
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            country TEXT,
            device TEXT,
            query TEXT,
            page TEXT,
            date TEXT,
            clicks INTEGER,
            impressions INTEGER,
            ctr REAL,
            position REAL,
            UNIQUE(country, device, query, page, date) ON CONFLICT IGNORE
        )
    ''')
    conn.commit()

    # === Request setup ===
    request_body = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dims,
        'rowLimit': 15000
    }

    # === Fetching Data ===
    total_rows = 0
    start_row = 0

    while True:
        request_body['startRow'] = start_row
        response = execute_request(service, site_url, request_body)

        if "rows" not in response or not response["rows"]:
            logging.info("ℹ️ No more rows found or empty response. Breaking fetching loop.")
            break

        batch = []
        for row in response["rows"]:
            keys = row.get("keys", [])
            metrics = [row.get(k) for k in ['clicks', 'impressions', 'ctr', 'position']]

            if len(keys) == len(dims):
                batch.append(tuple(keys + metrics))
            else:
                logging.warning(f"❗ Unexpected number of dimensions. Skipping row: {row}")


        cursor.executemany(f'''
            INSERT OR IGNORE INTO {table_name} ({", ".join(dims)}, clicks, impressions, ctr, position)
            VALUES ({','.join(['?'] * (len(dims) + 4))})
        ''', batch)
        conn.commit()

        total_rows += len(batch)
        logging.info(f"📡 Batch fetched: {len(batch)}, total: {total_rows}")

        if len(batch) < request_body['rowLimit']:
            logging.info(f"✅ Last batch of data ({len(batch)} rows) fetched. Completing request.")
            break


        start_row += request_body['rowLimit']

    conn.close()
    return total_rows