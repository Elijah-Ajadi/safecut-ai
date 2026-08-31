from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DetectedEntity(BaseModel):
    entity_type: str  # 'actor', 'music', 'logo'
    entity_name: str
    timestamp: str  # MM:SS
    confidence: float
    description: Optional[str] = None

class ComplianceVerdict(BaseModel):
    entity: DetectedEntity
    preliminary_verdict: str  # 'CLEARED', 'FLAGGED', 'NEEDS_REVIEW'
    legal_reasoning: str
    historical_risk: Optional[str] = None
    final_verdict: str

class ComplianceReport(BaseModel):
    project_id: str
    project_name: str
    analysis_timestamp: datetime
    video_duration: str
    overall_status: str  # 'GREENLIGHT', 'FLAGGED'
    entities_detected: List[ComplianceVerdict]
    risk_summary: dict
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
