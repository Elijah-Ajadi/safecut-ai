import json
from config.settings import settings

class LegalDatabaseTool:
    def __init__(self):
        with open(settings.LEGAL_DB_PATH, 'r') as f:
            self.db = json.load(f)
    
    def verify_actor(self, actor_name: str, territory: str = "US") -> dict:
        """Check if actor is cleared for production."""
        for actor in self.db.get("talent", []):
            if actor["name"].lower() == actor_name.lower():
                result = {
                    "status": actor.get("contract_status", "UNKNOWN"),
                    "territories": actor.get("territories", []),
                    "expiry": actor.get("expiry", "N/A")
                }
                
                if territory not in actor.get("territories", []):
                    result["status"] = "FLAGGED"
                    result["reason"] = f"Not cleared for {territory}"
                else:
                    result["reason"] = "Cleared for distribution"
                
                return result
        
        return {
            "status": "NEEDS_REVIEW",
            "reason": "Actor not found in database",
            "territories": [],
            "expiry": "N/A"
        }
    
    def verify_music(self, song_title: str, territory: str = "US") -> dict:
        """Check music licensing."""
        for song in self.db.get("music", []):
            if song["title"].lower() == song_title.lower():
                result = {
                    "status": song.get("license_type", "UNKNOWN"),
                    "territories": song.get("territories", []),
                    "expiry": song.get("expiry", "N/A")
                }
                
                if territory not in song.get("territories", []):
                    result["status"] = "FLAGGED"
                    result["reason"] = f"License not available for {territory}"
                else:
                    result["reason"] = "License cleared"
                
                return result
        
        return {
            "status": "FLAGGED",
            "reason": "Music not found in licensed database",
            "territories": [],
            "expiry": "N/A"
        }
    
    def verify_trademark(self, brand_name: str) -> dict:
        """Check trademark/logo restrictions."""
        for brand in self.db.get("trademarks", []):
            if brand["name"].lower() == brand_name.lower():
                return {
                    "status": brand.get("status", "UNKNOWN"),
                    "rules": brand.get("allowed_contexts", []),
                    "reason": f"Trademark status: {brand.get('status')}"
                }
        
        return {
            "status": "NEEDS_REVIEW",
            "reason": "Brand not found in trademark database",
            "rules": []
        }
