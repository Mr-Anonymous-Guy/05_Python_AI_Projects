# 🤖 AI Resume Builder

A production-grade AI-powered resume generation platform using local LLMs through **Ollama**. Built with Flask, this application provides professional resume creation, ATS optimization, cover letter generation, and LinkedIn profile optimization — all running locally without external API costs.

Part of the **05_Python_AI_Projects** repository — the first AI Engineering project.

---

## ✨ Features

### Resume Builder
- ✅ Personal Information Management
- ✅ Education History
- ✅ Work Experience with Achievements
- ✅ Skills Matrix
- ✅ Projects Portfolio
- ✅ Certifications
- ✅ Professional Summary

### AI-Powered Features
| Feature | Description |
|---|---|
| **Professional Summary** | Generate ATS-optimized summaries tailored to target roles |
| **Cover Letter** | Create customized cover letters for specific job applications |
| **LinkedIn About** | Generate engaging About sections with first-person storytelling |
| **Resume Tailoring** | Get specific recommendations to match job descriptions |

### ATS Optimization
- **Score Calculation** (0-100) with weighted components:
  - Keywords (30%)
  - Formatting (20%)
  - Experience (25%)
  - Skills (15%)
  - Education (10%)
- **Keyword Analysis** — Found vs Missing keywords
- **Actionable Recommendations** — Specific improvement suggestions
- **Strengths & Weaknesses** — Component-level analysis

### Export Formats
- 📄 **PDF** — Professional formatting with ReportLab
- 📝 **DOCX** — Microsoft Word compatible (python-docx)
- 📋 **TXT** — Plain text for ATS systems

### Supported LLMs (via Ollama)
- Llama 3 / 3.1 / 3.2
- Mistral
- Gemma / Gemma2
- Qwen / Qwen2

---

## 🏗️ Architecture

```
AI_Resume_Builder/
├── app.py                  # Flask application (REST API + web interface)
│
├── src/
│   ├── config.py           # Centralized configuration
│   ├── models.py           # Data models (Resume, PersonalInfo, etc.)
│   ├── ollama_client.py    # Ollama API client with retry logic
│   ├── ai_service.py       # High-level AI service orchestration
│   ├── ats_analyzer.py     # ATS scoring engine
│   └── exporters.py        # PDF/DOCX/TXT export implementations
│
├── prompts/                # Prompt templates for AI generation
│   ├── resume_summary.txt
│   ├── cover_letter.txt
│   ├── linkedin_about.txt
│   └── tailor_resume.txt
│
├── generated/              # Auto-generated exports (PDFs, DOCX, TXT)
│
├── tests/                  # Unit tests
│   └── test_ats_analyzer.py
│
├── requirements.txt
├── Makefile
├── run.sh                  # Linux/macOS launcher
├── run.bat                 # Windows launcher
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

**1. Python 3.8+**
```bash
python --version  # Should be 3.8 or higher
```

**2. Ollama**  
Install from [ollama.ai](https://ollama.ai)

```bash
# macOS / Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download installer from https://ollama.ai/download
```

**3. Pull an LLM model**
```bash
ollama pull llama3      # Recommended (7B parameters)
# OR
ollama pull mistral     # Alternative
ollama pull gemma2      # Google's model
```

### Installation

**1. Clone the repository**
```bash
cd AI_Resume_Builder
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Start Ollama server** (if not already running)
```bash
ollama serve
```

**4. Run the application**

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bat
run.bat
```

**Or directly:**
```bash
python app.py
```

**5. Open your browser**
```
http://localhost:5000
```

---

## 🎯 Usage

### REST API

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Generate Professional Summary
```bash
curl -X POST http://localhost:5000/api/generate/summary \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "target_role": "Senior Software Engineer",
    "years_experience": "8+ years",
    "skills": ["Python", "AWS", "Docker", "React"],
    "achievements": ["Led team of 5", "Reduced costs by 40%"]
  }'
```

#### Generate Cover Letter
```bash
curl -X POST http://localhost:5000/api/generate/cover-letter \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "position": "Machine Learning Engineer",
    "company": "Tech Corp",
    "job_description": "We are seeking an experienced ML engineer...",
    "skills": ["Python", "TensorFlow", "PyTorch"],
    "experience_summary": "5 years building production ML systems",
    "achievements": ["Improved model accuracy by 25%"]
  }'
```

#### ATS Analysis
```bash
curl -X POST http://localhost:5000/api/analyze/ats \
  -H "Content-Type: application/json" \
  -d '{
    "resume": { /* Resume JSON */ },
    "job_description": "Job posting text..."
  }'
```

#### Export to PDF
```bash
curl -X POST http://localhost:5000/api/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "resume": { /* Resume JSON */ }
  }' \
  --output resume.pdf
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_ats_analyzer.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📊 ATS Scoring Breakdown

The ATS engine analyzes resumes across five dimensions:

### 1. Keywords (30% weight)
- Extracts keywords from job description
- Compares against resume content
- Identifies found vs missing keywords

### 2. Formatting (20% weight)
- Complete contact information
- Clear section structure
- Professional links (LinkedIn, GitHub)
- Quantifiable achievements

### 3. Experience (25% weight)
- Number of roles
- Detail level (responsibilities + achievements)
- Action verb usage
- Measurable results

### 4. Skills (15% weight)
- Number of skills listed
- Technical vs soft skill balance
- Relevance to job description

### 5. Education (10% weight)
- Degree presence
- GPA listing
- Academic achievements

### Score Ratings

| Score | Rating | Meaning |
|---|---|---|
| 80-100 | Excellent | Ready to submit |
| 60-79 | Good | Minor improvements needed |
| 40-59 | Fair | Significant gaps to address |
| 0-39 | Poor | Major overhaul required |

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file:

```bash
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Flask configuration
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here

# Logging
LOG_LEVEL=INFO
```

### Prompt Customization

Edit prompt templates in `prompts/`:
- `resume_summary.txt` — Professional summary generation
- `cover_letter.txt` — Cover letter template
- `linkedin_about.txt` — LinkedIn About section
- `tailor_resume.txt` — Job-specific tailoring

---

## 🎨 Extending the Project

### Add New Export Formats

```python
# In src/exporters.py
def export_to_html(resume: Resume, output_path: Path) -> None:
    # Your implementation
    pass
```

### Add New AI Features

```python
# In src/ai_service.py
def generate_interview_prep(
    self,
    job_description: str,
    resume: Resume,
) -> str:
    # Load prompt template
    # Call Ollama
    # Return response
    pass
```

### Add Custom ATS Rules

```python
# In src/ats_analyzer.py
def score_custom_metric(resume: Resume) -> float:
    # Your scoring logic
    return score
```

---

## 🐛 Troubleshooting

### "Ollama connection failed"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3

# List available models
ollama list
```

### "PDF export fails"
```bash
# Reinstall ReportLab
pip install --upgrade reportlab
```

### Port 5000 already in use
```bash
# Change port in src/config.py or .env
FLASK_PORT=8000
```

---

## 📚 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Web Framework** | Flask 3.0+ | REST API and web interface |
| **LLM Client** | Ollama (local) | Text generation without API costs |
| **PDF Export** | ReportLab 4.0+ | Professional PDF generation |
| **DOCX Export** | python-docx 1.1+ | Microsoft Word compatibility |
| **Testing** | pytest 8.0+ | Unit and integration tests |

---

## 🎯 Roadmap

- [ ] React/Vue.js frontend
- [ ] User authentication
- [ ] Resume template library
- [ ] Multi-language support
- [ ] Interview question generator
- [ ] Salary negotiation assistant
- [ ] Job application tracker
- [ ] Resume version history
- [ ] Browser extension
- [ ] Mobile app

---

## 📄 License

MIT — free to use, modify, and deploy commercially.

---

## 🙏 Acknowledgments

- **Ollama** — Local LLM inference engine
- **Flask** — Lightweight Python web framework
- **ReportLab** — PDF generation library
- **python-docx** — Word document manipulation

---

**Built with ❤️ as part of the 05_Python_AI_Projects learning series.**
