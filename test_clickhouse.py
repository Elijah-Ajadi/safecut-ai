#!/usr/bin/env python3
"""Test ClickHouse Connection via HTTP API"""

import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

print("=" * 60)
print("Testing ClickHouse Connection (HTTP API)")
print("=" * 60)

try:
    host = os.getenv("CLICKHOUSE_HOST")
    port = os.getenv("CLICKHOUSE_PORT")
    user = os.getenv("CLICKHOUSE_USER")
    password = os.getenv("CLICKHOUSE_PASSWORD")
    database = os.getenv("CLICKHOUSE_DATABASE")
    
    print(f"\nConnecting to:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    
    # HTTP API endpoint
    url = f"https://{host}:{port}/"
    
    # Query
    query = "SELECT COUNT() FROM compliance_audit"
    
    print(f"\nExecuting query: {query}")
    
    response = requests.post(
        url,
        params={
            'database': database,
            'query': query
        },
        auth=(user, password),
        verify=False  # Ignore SSL warnings for now
    )
    
    if response.status_code == 200:
        count = int(response.text.strip())
        print(f"\n✅ SUCCESS!")
        print(f"Compliance Audit Table rows: {count}")
        print(f"\n✅ ClickHouse is ready to use!")
    else:
        print(f"\n❌ Query failed: {response.status_code}")
        print(f"Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)