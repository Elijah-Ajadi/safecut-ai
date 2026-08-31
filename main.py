#!/usr/bin/env python3
"""SafeCut AI - Main entry point"""

import sys
import json
from agents.legal_brain import LegalVerificationBrain

def main():
    if len(sys.argv) < 6:
        print("Usage: python main.py --video <video_path> --project-id <id> --project-name <name>")
        print("Example: python main.py --video sample.mp4 --project-id proj_001 --project-name 'My Film'")
        sys.exit(1)
    
    # Parse arguments
    video_path = None
    project_id = None
    project_name = None
    
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--video" and i+1 < len(sys.argv):
            video_path = sys.argv[i+1]
        elif sys.argv[i] == "--project-id" and i+1 < len(sys.argv):
            project_id = sys.argv[i+1]
        elif sys.argv[i] == "--project-name" and i+1 < len(sys.argv):
            project_name = sys.argv[i+1]
    
    if not video_path or not project_id or not project_name:
        print("❌ Error: Missing required arguments")
        print("Usage: python main.py --video <video_path> --project-id <id> --project-name <name>")
        sys.exit(1)
    
    # Run agent
    print("\n" + "="*60)
    print("SafeCut AI - Legal Verification Agent")
    print("="*60)
    print(f"Project: {project_name} ({project_id})")
    print(f"Video: {video_path}")
    print("="*60)
    
    agent = LegalVerificationBrain()
    report = agent.analyze_video(video_path, project_id, project_name)
    
    # Output report (Pydantic v2)
    print("\n" + "="*60)
    print("COMPLIANCE REPORT")
    print("="*60)
    
    # Use model_dump() for Pydantic v2
    report_dict = report.model_dump(mode='json')
    print(json.dumps(report_dict, indent=2, default=str))
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
