from typing import Dict

class GeminiVideoAnalyzer:
    """Mocked Gemini analyzer for testing. Swap with real Gemini on Day 3."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Mock video analysis.
        Returns different results based on video filename for testing.
        """
        mock_data = {
            "actors": [
                {"name": "Sample Actor", "timestamp": "00:15", "confidence": 0.95, "type": "actor"},
                {"name": "Another Actor", "timestamp": "00:45", "confidence": 0.88, "type": "actor"}
            ],
            "logos": [
                {"name": "Sample Brand Logo", "timestamp": "00:30", "confidence": 0.92, "type": "logo"}
            ],
            "audio_tracks": [
                {"language": "en", "description": "English dialogue", "type": "audio"}
            ],
            "music": [
                {"name": "Sample Song", "timestamp": "01:00", "confidence": 0.85, "type": "music"}
            ],
            "video_duration": "02:15"
        }
        
        # Test different scenarios based on filename
        if "flagged" in video_path.lower():
            mock_data["actors"].append(
                {"name": "Restricted Actor", "timestamp": "00:20", "confidence": 0.90, "type": "actor"}
            )
            mock_data["music"].append(
                {"name": "Unlicensed Track", "timestamp": "01:30", "confidence": 0.88, "type": "music"}
            )
        
        return mock_data
