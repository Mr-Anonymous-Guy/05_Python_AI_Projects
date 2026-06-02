# 🐍 05_Python_AI_Projects

A comprehensive collection of professional Python projects demonstrating software engineering, machine learning, and AI engineering skills. Each project is built with production-grade code quality, comprehensive testing, and detailed documentation.

---

## 📚 Projects Overview

### **Project 01: Rock Paper Scissors** 🎮
**Category:** Python Fundamentals  
**Difficulty:** Beginner  
**Tech:** Pure Python

A terminal-based game demonstrating core Python concepts:
- Variables, Functions, Loops, Conditionals
- Input Validation & Random Module
- Modular Programming
- 45 unit tests with 100% coverage

**Key Features:**
- 4 game modes (Single, Best of 3/5, Unlimited)
- Live statistics tracking
- Cross-platform (Windows/Linux/macOS)

📂 [View Project](./Rock_Paper_Scissors/)

---

### **Project 02: Password Generator** 🔐
**Category:** Python Fundamentals + Security  
**Difficulty:** Intermediate  
**Tech:** Python, `secrets` module

A cryptographically secure password generator with strength analysis:
- CSPRNG-based generation (not pseudo-random)
- ATS-style strength scoring (0-100)
- Clipboard integration
- 89 unit tests

**Key Features:**
- Custom length (4-512 characters)
- Character category control
- Bulk generation (1-1000 passwords)
- Export to TXT with metadata
- Real-time strength analysis

📂 [View Project](./Password_Generator/)

---

### **Project 03: Student Marks Predictor** 📊
**Category:** Machine Learning  
**Difficulty:** Intermediate  
**Tech:** Python, scikit-learn, pandas, matplotlib

A complete ML engineering project for student performance prediction:
- 3 regression algorithms (Linear, Decision Tree, Random Forest)
- Automatic best-model selection
- Model persistence (pickle)
- 21 comprehensive tests

**Key Features:**
- Multi-model training pipeline
- Automated hyperparameter tuning
- 5 visualization types (heatmaps, scatter, residuals)
- Interactive CLI for predictions
- Full evaluation metrics (MAE, MSE, RMSE, R²)

📂 [View Project](./Student_Marks_Predictor/)

---

### **Project 04: AI Resume Builder** 🤖
**Category:** AI Engineering / Full Stack  
**Difficulty:** Advanced  
**Tech:** Flask, Ollama, ReportLab, python-docx

A production-grade AI-powered resume platform rivaling commercial SaaS:
- Local LLM integration (Ollama)
- ATS optimization engine
- Professional document export
- REST API + Web UI
- 20+ unit tests

**Key Features:**
- **AI Generation:** Professional summaries, cover letters, LinkedIn profiles
- **ATS Analysis:** Weighted scoring (0-100), keyword extraction, recommendations
- **Export Formats:** PDF, DOCX, TXT
- **Career Tools:** Resume tailoring, interview prep suggestions
- **Privacy:** 100% local processing, zero external API calls

📂 [View Project](./AI_Resume_Builder/)

---

## 📊 Repository Statistics

```
Total Projects:       4
Total Files:         ~100
Lines of Code:      ~10,000
Test Coverage:       85%+
Languages:           Python, HTML, CSS, JavaScript
Frameworks:          Flask, scikit-learn, ReportLab
```

---

## 🎯 Skills Demonstrated

### **Python Fundamentals**
- ✅ Variables, Functions, Loops, Conditionals
- ✅ Data Structures (lists, dicts, sets, tuples)
- ✅ Object-Oriented Programming
- ✅ File I/O and Path handling
- ✅ Error Handling and Logging
- ✅ Type Hints and Dataclasses

### **Software Engineering**
- ✅ Modular Design
- ✅ Clean Architecture
- ✅ Unit Testing (pytest, unittest)
- ✅ Configuration Management
- ✅ Version Control (Git)
- ✅ Documentation (README, API docs)

### **Data Science & ML**
- ✅ Data Processing (pandas, numpy)
- ✅ Machine Learning (scikit-learn)
- ✅ Model Training & Evaluation
- ✅ Visualization (matplotlib, seaborn)
- ✅ Feature Engineering
- ✅ Model Persistence

### **AI Engineering**
- ✅ LLM Integration (Ollama)
- ✅ Prompt Engineering
- ✅ REST API Development (Flask)
- ✅ Document Generation (PDF/DOCX)
- ✅ NLP (keyword extraction, text analysis)

### **Security & Cryptography**
- ✅ CSPRNG Usage (`secrets` module)
- ✅ Input Validation
- ✅ Secure Random Generation
- ✅ Privacy-First Design

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Ollama for AI Resume Builder

### **Running Any Project**

```bash
# Clone the repository
git clone <repository-url>
cd 05_Python_AI_Projects

# Navigate to a project
cd Rock_Paper_Scissors

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py

# Or use the provided launchers
./run.sh      # Linux/macOS
run.bat       # Windows
```

### **Running Tests**

```bash
# All projects support pytest
cd <project-directory>
python -m pytest tests/ -v

# Or use unittest
python -m unittest discover tests/ -v
```

---

## 📖 Learning Path

### **Recommended Order**

1. **Start Here:** Rock Paper Scissors
   - Learn Python basics
   - Understand project structure
   - Get comfortable with testing

2. **Next:** Password Generator
   - Security concepts
   - String manipulation
   - Advanced validation

3. **Then:** Student Marks Predictor
   - Data science workflow
   - Machine learning fundamentals
   - Visualization techniques

4. **Finally:** AI Resume Builder
   - Full-stack development
   - AI integration
   - Production deployment

---

## 🛠️ Tech Stack Overview

### **Core Technologies**

| Technology | Used In | Purpose |
|---|---|---|
| **Python 3.8+** | All projects | Core language |
| **pytest** | All projects | Unit testing |
| **pandas** | ML, AI | Data manipulation |
| **scikit-learn** | ML | Machine learning |
| **Flask** | AI Builder | Web framework |
| **Ollama** | AI Builder | Local LLM inference |
| **ReportLab** | AI Builder | PDF generation |
| **matplotlib** | ML | Data visualization |

### **Development Tools**

- **Makefile** — Build automation
- **pytest** — Testing framework
- **Type Hints** — Static type checking
- **Logging** — Debugging and monitoring

---

## 📚 Documentation

Each project includes:
- ✅ **README.md** — Project overview, setup, usage
- ✅ **requirements.txt** — Python dependencies
- ✅ **run.sh / run.bat** — Cross-platform launchers
- ✅ **tests/** — Comprehensive test suite
- ✅ **.gitignore** — Clean repository

Some projects also include:
- 📘 **EXAMPLES.md** — Usage examples and patterns
- 📊 **PROJECT_SUMMARY.md** — Architecture and design decisions
- 🔧 **Makefile** — Build and deployment commands

---

## 🎓 Educational Value

### **For Beginners**
- Start with Rock Paper Scissors
- Learn Python syntax and control flow
- Understand testing and project structure

### **For Intermediate Developers**
- Password Generator teaches security
- Student Marks Predictor introduces ML
- Focus on clean code and architecture

### **For Advanced Developers**
- AI Resume Builder shows production patterns
- Full-stack integration
- AI/ML engineering practices

---

## 🔄 Project Evolution

### **Phase 1: Fundamentals** ✅ COMPLETE
- [x] Rock Paper Scissors
- [x] Password Generator

### **Phase 2: Data Science** ✅ COMPLETE
- [x] Student Marks Predictor

### **Phase 3: AI Engineering** ✅ COMPLETE
- [x] AI Resume Builder

### **Phase 4: Advanced (Future)**
- [ ] Natural Language Processing Project
- [ ] Computer Vision Application
- [ ] Real-time Data Processing
- [ ] Distributed Systems

---

## 🤝 Contributing

Contributions are welcome! Each project is self-contained:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

---

## 📄 License

MIT License — free to use, modify, and distribute.

Each project is standalone and can be used independently.

---

## 🎯 Project Highlights

### **Code Quality**
- ✅ PEP 8 compliant
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Clean architecture
- ✅ Error handling

### **Testing**
- ✅ Unit tests
- ✅ Integration tests
- ✅ 80%+ code coverage
- ✅ Edge case handling

### **Documentation**
- ✅ Clear README files
- ✅ API documentation
- ✅ Usage examples
- ✅ Architecture diagrams

### **Deployment**
- ✅ Cross-platform support
- ✅ Easy installation
- ✅ Production-ready
- ✅ Docker support (where applicable)

---

## 🌟 Why This Repository?

### **Portfolio Quality**
Every project demonstrates:
- Professional coding standards
- Real-world problem solving
- Production-ready architecture
- Comprehensive testing

### **Learning Journey**
Structured progression from:
- Python basics → Security → ML → AI
- Simple CLIs → Full-stack web apps
- Local processing → API integration

### **Career Ready**
Projects showcase:
- Software engineering best practices
- Modern tech stack (Flask, ML, AI)
- Problem-solving abilities
- Documentation skills

---

## 📞 Contact & Support

**Questions?** Open an issue in the repository.

**Found a bug?** Submit a pull request with a fix.

**Want to contribute?** Check individual project READMEs for contribution guidelines.

---

**Built with ❤️ to demonstrate that learning projects can be production-grade.**

*Showing that open-source educational content can compete with commercial tutorials.*
