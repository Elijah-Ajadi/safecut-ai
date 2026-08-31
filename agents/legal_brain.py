from agents.tools.gemini_analyzer import GeminiVideoAnalyzer
from agents.tools.legal_database import LegalDatabaseTool
from agents.tools.clickhouse_analytics import ClickHouseAnalyticsTool
from models.compliance import DetectedEntity, ComplianceVerdict, ComplianceReport
from datetime import datetime
from typing import List, Dict
import json

class LegalVerificationBrain:
    """Main agent that orchestrates compliance verification."""
    
    def __init__(self):
        self.gemini = GeminiVideoAnalyzer("safe-cut-ai")
        self.legal_db = LegalDatabaseTool()
        self.clickhouse = ClickHouseAnalyticsTool()
    
    def analyze_video(self, video_path: str, project_id: str, project_name: str) -> ComplianceReport:
        """
        Full compliance analysis pipeline:
        1. Analyze video with Gemini (mocked for now)
        2. Look up entities in legal database
        3. Query ClickHouse for historical trends
        4. Synthesize final verdicts
        5. Log to ClickHouse
        6. Generate report
        """
        
        print(f"\n[Agent] Starting compliance analysis for: {project_name}")
        print(f"[Agent] Video: {video_path}")
        
        # Step 1: Gemini Analysis
        print(f"[Agent] Step 1: Analyzing video with Gemini...")
        detected_data = self.gemini.analyze_video(video_path)
        
        # Step 2-3: Legal lookup + ClickHouse enrichment
        print(f"[Agent] Step 2: Querying legal database...")
        verdicts = []
        
        # Process actors
        for actor in detected_data.get("actors", []):
            verdict = self._verify_and_enrich_entity(actor, "actor")
            verdicts.append(verdict)
        
        # Process logos
        for logo in detected_data.get("logos", []):
            verdict = self._verify_and_enrich_entity(logo, "logo")
            verdicts.append(verdict)
        
        # Process music
        for music in detected_data.get("music", []):
            verdict = self._verify_and_enrich_entity(music, "music")
            verdicts.append(verdict)
        
        # Step 4: Log to ClickHouse
        print(f"[Agent] Step 3: Logging to ClickHouse...")
        self.clickhouse.log_audit_trail(project_id, project_name, verdicts)
        
        # Step 5: Generate report
        print(f"[Agent] Step 4: Generating compliance report...")
        report = self._generate_report(project_id, project_name, verdicts, detected_data)
        
        print(f"[Agent] ✅ Analysis complete!")
        
        return report
    
    def _verify_and_enrich_entity(self, entity_data: Dict, entity_type: str) -> ComplianceVerdict:
        """
        Verify entity in legal database + query ClickHouse for historical trends.
        """
        entity = DetectedEntity(
            entity_type=entity_type,
            entity_name=entity_data.get("name", "Unknown"),
            timestamp=entity_data.get("timestamp", "00:00"),
            confidence=entity_data.get("confidence", 0.5)
        )
        
        # Step 1: Look up in legal database
        if entity_type == "actor":
            legal_status = self.legal_db.verify_actor(entity.entity_name)
        elif entity_type == "music":
            legal_status = self.legal_db.verify_music(entity.entity_name)
        else:  # logo
            legal_status = self.legal_db.verify_trademark(entity.entity_name)
        
        preliminary_verdict = legal_status.get("status", "NEEDS_REVIEW")
        
        # Step 2: Query ClickHouse for historical trends
        history = self.clickhouse.has_entity_been_flagged_before(
            entity.entity_name, 
            entity.entity_type
        )
        
        # Step 3: Synthesize final verdict
        final_verdict = self._synthesize_verdict(
            preliminary_verdict,
            history,
            entity.confidence
        )
        
        print(f"  [{entity_type}] {entity.entity_name}: {final_verdict}")
        
        return ComplianceVerdict(
            entity=entity,
            preliminary_verdict=preliminary_verdict,
            legal_reasoning=legal_status.get("reason", ""),
            historical_risk=history.get("risk_level"),
            final_verdict=final_verdict
        )
    
    def _synthesize_verdict(self, legal_status: str, history: Dict, confidence: float) -> str:
        """
        Combine legal status + historical trends to make final decision.
        
        Logic:
        - If legal says FLAGGED → stay FLAGGED
        - If legal says CLEARED but high historical risk + low confidence → NEEDS_REVIEW
        - Otherwise use legal status
        """
        if legal_status == "FLAGGED":
            return "FLAGGED"
        
        if history.get("risk_level") == "HIGH" and confidence < 0.85:
            return "NEEDS_REVIEW"
        
        if legal_status == "NEEDS_REVIEW":
            return "NEEDS_REVIEW"
        
        return "CLEARED"
    
    def _generate_report(self, project_id: str, project_name: str, 
                        verdicts: List[ComplianceVerdict], 
                        detected: Dict) -> ComplianceReport:
        """Generate compliance report."""
        
        # Overall status: GREENLIGHT if all cleared, FLAGGED if any flagged
        flagged_count = sum(1 for v in verdicts if v.final_verdict == "FLAGGED")
        total = len(verdicts)
        
        overall_status = "GREENLIGHT" if flagged_count == 0 else "FLAGGED"
        
        report = ComplianceReport(
            project_id=project_id,
            project_name=project_name,
            analysis_timestamp=datetime.now(),
            video_duration=detected.get("video_duration", "00:00"),
            overall_status=overall_status,
            entities_detected=verdicts,
            risk_summary={
                "total_entities": total,
                "flagged": flagged_count,
                "cleared": total - flagged_count,
                "clearance_percentage": ((total - flagged_count) / total * 100) if total > 0 else 0
            }
        )
        
        return report
