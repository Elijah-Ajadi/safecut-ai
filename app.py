#!/usr/bin/env python3
"""SafeCut AI Web Interface"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from agents.legal_brain import LegalVerificationBrain
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Homepage with upload form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded video"""
    try:
        # Get form data
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        project_name = request.form.get('project_name', 'Untitled Project')
        project_id = request.form.get('project_id', f"proj_{datetime.now().timestamp()}")
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run analysis
        agent = LegalVerificationBrain()
        report = agent.analyze_video(filepath, project_id, project_name)
        
        # Return results
        return jsonify({
            'success': True,
            'report': report.model_dump(mode='json'),
            'status': report.overall_status,
            'clearance_rate': report.risk_summary['clearance_percentage']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
