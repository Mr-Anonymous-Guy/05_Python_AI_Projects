# EduSense - AI Learning Platform

EduSense is a professional AI-powered learning platform that transforms study materials into personalized learning experiences.

## Features
- **Subject Management**: Organize study materials by subject.
- **AI Tutor**: RAG-powered tutor that cites your uploaded PDFs, DOCX, and TXT files.
- **Study Planners**: Generate custom weekly, daily, and exam cram plans.
- **Assessments**: Generate flashcards and quizzes automatically.
- **Analytics**: Track your quiz scores and let the AI identify your weak topics.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, SQLAlchemy (SQLite)
- **AI/Vector**: LangChain, Ollama, FAISS

## Setup & Run

### Windows
1. Ensure Python 3.10+ and [Ollama](https://ollama.com) are installed.
2. Ensure Ollama is running and has models downloaded (`ollama pull llama3`, `ollama pull nomic-embed-text`).
3. Double-click `run.bat` or run:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
make install
make run
```
