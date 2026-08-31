#!/usr/bin/env python3
"""Test Google Cloud and ClickHouse connections"""

import os
from dotenv import load_dotenv
from google.cloud import aiplatform
from clickhouse_driver import Client

# Load environment variables
load_dotenv()

print("=" * 60)
print("SafeCut AI - Connection Test")
print("=" * 60)

# Test 1: Google Cloud
print("\n[TEST 1] Google Cloud Connection...")
try:
    project_id = os.getenv("GCP_PROJECT_ID")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    print(f"  Project ID: {project_id}")
    print(f"  Credentials: {credentials_path}")
    
    aiplatform.init(project=project_id, location="us-central1")
    print("  ✅ Google Cloud initialized successfully!")
except Exception as e:
    print(f"  ❌ Google Cloud connection failed: {e}")

# Test 2: ClickHouse
print("\n[TEST 2] ClickHouse Connection...")
try:
    host = os.getenv("CLICKHOUSE_HOST")
    port = int(os.getenv("CLICKHOUSE_PORT", "9440"))
    user = os.getenv("CLICKHOUSE_USER")
    password = os.getenv("CLICKHOUSE_PASSWORD")
    database = os.getenv("CLICKHOUSE_DATABASE")
    
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    
    client = Client(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        settings={'use_numpy': False}
    )
    
    # Test query
    result = client.execute("SELECT COUNT() FROM compliance_audit LIMIT 1")
    print(f"  Query result: {result}")
    print("  ✅ ClickHouse connected successfully!")
    
except Exception as e:
    print(f"  ❌ ClickHouse connection failed: {e}")

print("\n" + "=" * 60)
print("✅ All tests complete!")
print("=" * 60)