import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google Cloud
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "safe-cut-ai")
    GCP_REGION = "us-central1"
    
    # Gemini
    GEMINI_MODEL = "gemini-3-flash-001"
    
    # ClickHouse
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8443"))
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
    CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "safecut_compliance")
    
    # Paths
    LEGAL_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "legal_database.json")

settings = Settings()
