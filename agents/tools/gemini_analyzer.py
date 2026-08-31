from typing import Dict

class GeminiVideoAnalyzer:
    """Mocked Gemini analyzer for testing. Swap with real Gemini on Day 3."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Mock video analysis.
        On Day 3, replace with real Gemini Vision API call.
        """
        # TODO: Replace with real Gemini Vision API
        # from google.cloud import aiplatform
        # model = GenerativeModel("gemini-3-flash-001")
        # response = model.generate_content([video_file, prompt])
        
        # For now, return mock data based on video path
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
        
        return mock_data
