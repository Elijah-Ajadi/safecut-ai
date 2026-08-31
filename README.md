# SafeCut AI

**Video Compliance Analytics Engine**  
Real-Time Legal Risk Aggregation Across Studio Catalogs

![Agentic Cinema](https://img.shields.io/badge/Hackathon-Agentic%20Cinema%202026-blue)
![ClickHouse Track](https://img.shields.io/badge/Track-ClickHouse%20Partner-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎬 Problem Statement

**The Hollywood Compliance Bottleneck:**

Before any film or TV show is broadcast or streamed, it must pass legal clearance. This process involves:
- Human lawyers watching video footage frame-by-frame (weeks of work)
- Manual cross-referencing against licensing databases
- Checking actor contracts, music licenses, and trademark permissions
- Documenting compliance for legal protection

**Current Cost:** $200K-$500K per film in legal fees + 2-3 weeks of review time

**Risk:** Missed licenses result in $50K-$500K lawsuits per instance

---

## ✨ Solution: SafeCut AI

SafeCut AI automates video compliance verification using:

1. **Gemini Multimodal Vision** - Analyzes video content (actors, logos, audio)
2. **ClickHouse Analytics** - Real-time aggregation across entire catalog
3. **Intelligent Agent** - Synthesizes legal data + historical trends into compliance verdicts

**Result:** Reduce compliance review from 21 days to 3 minutes

---

## 🏗️ Architecture
Video Upload
↓
Vertex AI Agent (ADK + Agent Engine)
├─ Gemini Vision analyzes video (actors, logos, audio)
├─ Queries internal legal database (mocked)
├─ Queries ClickHouse for historical risk trends
├─ Synthesizes final verdict (GREENLIGHT/FLAGGED)
└─ Logs audit trail to ClickHouse
↓
ClickHouse (Load-Bearing Partner)
├─ Real-time compliance audit logging
├─ Historical risk aggregation
├─ Trend analysis (are flags up/down?)
└─ Clearance rate by territory
↓
Compliance Report (JSON + PDF)


---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent Orchestration** | Vertex AI Agent Development Kit (ADK) + Agent Engine | Manages Legal Verification Brain workflow |
| **Video Intelligence** | Gemini 3 Multimodal | Analyzes video content |
| **Analytics Engine** | ClickHouse (MCP) | Real-time aggregation, risk trending |
| **Mocked Database** | Python JSON (in-repo) | Talent contracts, music licenses, trademarks |
| **Backend Logic** | Python 3.11+ | Agent orchestration, entity extraction |

---

## 📋 Prerequisites

- **Python 3.11+**
- **Google Cloud Account** with:
  - Vertex AI API enabled
  - Generative Language API enabled
  - Service account with Agent Platform Administrator role
  - JSON key file
- **ClickHouse Cloud Account** with:
  - Service instance created
  - `safecut_compliance` database
  - `compliance_audit` table

---

## 🚀 Setup

### **1. Clone Repository**

```bash
git clone https://github.com/YOUR-USERNAME/safecut-ai.git
cd safecut-ai
```

### **2. Create Virtual Environment**

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure Environment**

Create `.env` file:

Google Cloud

GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key-file.json

ClickHouse

CLICKHOUSE_HOST=your-instance.cloud.clickhouse.cloud
CLICKHOUSE_PORT=8443
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your-password
CLICKHOUSE_DATABASE=safecut_compliance


### **5. Test ClickHouse Connection**

```bash
python test_clickhouse_http.py
```

You should see:

✅ SUCCESS!
Compliance Audit Table rows: 0


---

## 💻 Usage

### **Analyze a Video**

```bash
python main.py --video sample_video.mp4 --project-id proj_001 --project-name "My Film"
```

### **Output**

```json
{
  "project_id": "proj_001",
  "project_name": "My Film",
  "analysis_timestamp": "2026-09-07T12:00:00",
  "overall_status": "GREENLIGHT",
  "entities_detected": [
    {
      "entity_type": "actor",
      "entity_name": "Sample Actor",
      "timestamp": "00:15",
      "final_verdict": "CLEARED",
      "confidence": 0.98
    }
  ],
  "risk_summary": {
    "total_entities": 12,
    "cleared": 11,
    "flagged": 1,
    "clearance_percentage": 91.7
  }
}
```

---

## 📁 Project Structure

safecut-ai/
├── agents/
│ ├── legal_brain.py # Main agent orchestration
│ └── tools/
│ ├── gemini_analyzer.py # Video analysis
│ ├── legal_database.py # Legal DB queries
│ └── clickhouse_analytics.py # ClickHouse queries
├── config/
│ └── settings.py # Configuration
├── models/
│ └── compliance.py # Pydantic schemas
├── data/
│ └── legal_database.json # Mocked legal data
├── tests/
│ ├── test_gemini.py
│ ├── test_legal_db.py
│ └── test_clickhouse.py
├── main.py # Entry point
├── requirements.txt
├── .env # Secrets (not in repo)
├── .env.example # Template for .env
├── LICENSE
├── README.md
└── .gitignore


---

## 🔌 API Reference

### **LegalVerificationBrain**

```python
from agents.legal_brain import LegalVerificationBrain

agent = LegalVerificationBrain()
report = agent.analyze_video(
    video_path="video.mp4",
    project_id="proj_001",
    project_name="My Film"
)
```

**Returns:** `ComplianceReport` object with all verdicts and audit trail

---

## 🌩️ Deployment

### **Local Development**

```bash
python main.py --video sample.mp4 --project-id test --project-name "Test"
```

### **Google Cloud Run (Production)**

```bash
# Build and push Docker image
docker build -t safecut-ai .
docker tag safecut-ai:latest gcr.io/YOUR-PROJECT/safecut-ai:latest
docker push gcr.io/YOUR-PROJECT/safecut-ai:latest

# Deploy to Cloud Run
gcloud run deploy safecut-ai \
  --image gcr.io/YOUR-PROJECT/safecut-ai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## ⚠️ Known Limitations

- **MVP Phase:** Mocked legal database (not connected to real IBM/Yandex data)
- **No auto-redaction:** Flagged content is identified but not automatically edited
- **CLI only:** No web UI (coming in Phase 2)
- **Single agent:** Designed for linear workflows (can extend to multi-agent)
- **Test data:** Uses royalty-free sample videos (not production content)

---

## 🗺️ Phase 2 Roadmap

- [ ] Integration with real IBM Governance Framework
- [ ] Auto-video redaction for flagged content
- [ ] Web UI for video upload and dashboard
- [ ] Real actor likeness detection (ML models)
- [ ] User authentication and multi-tenant support
- [ ] Grafana executive dashboards
- [ ] REST API for production use
- [ ] Batch processing for large catalogs

---

## 📜 License

MIT License — See `LICENSE` file

---

## 👥 Contributors

**Precorium Labs**
- Built for Agentic Cinema: The Blockbuster Hackathon 2026
- ClickHouse Partner Track

---

## 📞 Support

For issues or questions:
1. Check `Known Limitations` above
2. Open an issue on GitHub
3. Review the sprint plan in project documentation

---

**Built with ❤️ for the Agentic Cinema Hackathon**