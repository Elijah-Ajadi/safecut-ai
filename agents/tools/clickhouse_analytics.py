import requests
from typing import Dict, List
from config.settings import settings

class ClickHouseAnalyticsTool:
    def __init__(self):
        self.host = settings.CLICKHOUSE_HOST
        self.port = settings.CLICKHOUSE_PORT
        self.user = settings.CLICKHOUSE_USER
        self.password = settings.CLICKHOUSE_PASSWORD
        self.database = settings.CLICKHOUSE_DATABASE
        self.url = f"https://{self.host}:{self.port}/"
    
    def _execute_query(self, query: str) -> str:
        """Execute ClickHouse query via HTTP API."""
        try:
            response = requests.post(
                self.url,
                params={'database': self.database, 'query': query},
                auth=(self.user, self.password),
                verify=False,
                timeout=10
            )
            if response.status_code == 200:
                return response.text.strip()
            else:
                print(f"Query error: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            print(f"ClickHouse query failed: {e}")
            return ""
    
    def has_entity_been_flagged_before(self, entity_name: str, entity_type: str, days: int = 365) -> Dict:
        """Check if entity has been flagged before."""
        query = f"""
        SELECT 
            COUNT(*) as flagged_count,
            COUNT(DISTINCT project_id) as projects_affected
        FROM compliance_audit
        WHERE entity_name = '{entity_name}'
            AND entity_type = '{entity_type}'
            AND verdict = 'FLAGGED'
            AND analysis_timestamp > now() - INTERVAL {days} DAY
        """
        
        result = self._execute_query(query)
        if result:
            try:
                flagged_count, projects_affected = map(int, result.split('\t'))
                return {
                    "has_been_flagged": flagged_count > 0,
                    "flagged_count": flagged_count,
                    "projects_affected": projects_affected,
                    "risk_level": "HIGH" if flagged_count > 5 else "MEDIUM" if flagged_count > 0 else "LOW"
                }
            except:
                pass
        
        return {"has_been_flagged": False, "flagged_count": 0, "projects_affected": 0, "risk_level": "LOW"}
    
    def log_audit_trail(self, project_id: str, project_name: str, verdicts: List[Dict]) -> bool:
        """Log compliance verdicts to ClickHouse."""
        try:
            for verdict in verdicts:
                entity = verdict["entity"]
                insert_query = f"""
                INSERT INTO compliance_audit VALUES (
                    '{project_id}',
                    '{project_name}',
                    now(),
                    '{entity.entity_type}',
                    '{entity.entity_name}',
                    '{entity.timestamp}',
                    '{verdict["final_verdict"]}',
                    {entity.confidence},
                    '{verdict["legal_reasoning"]}',
                    'US'
                )
                """
                self._execute_query(insert_query)
            return True
        except Exception as e:
            print(f"Error logging to ClickHouse: {e}")
            return False
