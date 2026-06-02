# AI Resume Builder — Usage Examples

Complete examples for all features.

---

## 🚀 Quick Start Example

### 1. Start the Server

```bash
python app.py
```

### 2. Check Health Status

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "ollama": "connected",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 📝 Generate Professional Summary

### Request

```bash
curl -X POST http://localhost:5000/api/generate/summary \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "target_role": "Senior Data Scientist",
    "years_experience": "7+ years",
    "skills": [
      "Python",
      "Machine Learning",
      "TensorFlow",
      "PyTorch",
      "AWS",
      "SQL",
      "Statistics"
    ],
    "achievements": [
      "Led ML team of 6 engineers",
      "Improved model accuracy by 35%",
      "Reduced inference time by 60%"
    ]
  }'
```

### Response

```json
{
  "success": true,
  "summary": "Results-driven Senior Data Scientist with 7+ years of experience building production ML systems. Proven track record of leading cross-functional teams and delivering measurable business impact through advanced analytics and machine learning. Expert in Python, TensorFlow, and AWS with demonstrated success in improving model accuracy by 35% and reducing inference time by 60%. Skilled at translating complex data insights into actionable business strategies."
}
```

---

## 💼 Generate Cover Letter

### Request

```bash
curl -X POST http://localhost:5000/api/generate/cover-letter \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Chen",
    "position": "Full Stack Developer",
    "company": "TechCorp Inc.",
    "job_description": "We are seeking a talented Full Stack Developer with experience in React, Node.js, and cloud platforms. You will work on building scalable web applications that serve millions of users. The ideal candidate has 5+ years of experience and a passion for creating excellent user experiences.",
    "skills": [
      "React",
      "Node.js",
      "TypeScript",
      "AWS",
      "Docker",
      "PostgreSQL"
    ],
    "experience_summary": "5 years building full-stack web applications with React and Node.js",
    "achievements": [
      "Built e-commerce platform serving 2M users",
      "Reduced page load time by 45%",
      "Led migration to microservices architecture"
    ]
  }'
```

### Response

```json
{
  "success": true,
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Full Stack Developer position at TechCorp Inc. With 5 years of experience building scalable web applications and a proven track record of delivering high-impact results, I am excited about the opportunity to contribute to your engineering team.\n\nIn my current role, I have built an e-commerce platform that serves 2 million users daily, leveraging React and Node.js to create seamless user experiences. I reduced page load times by 45% through performance optimization and successfully led our team's migration to a microservices architecture, improving system reliability and scalability.\n\nMy technical expertise in React, Node.js, TypeScript, and AWS aligns perfectly with your requirements. I am particularly drawn to TechCorp's commitment to innovation and would welcome the opportunity to bring my skills in building performant, user-centric applications to your team.\n\nI would love to discuss how my experience can contribute to TechCorp's continued success. Thank you for considering my application.\n\nSincerely,\nAlex Chen"
}
```

---

## 🔍 ATS Analysis

### Request

```bash
curl -X POST http://localhost:5000/api/analyze/ats \
  -H "Content-Type: application/json" \
  -d '{
    "resume": {
      "personal_info": {
        "full_name": "Maria Garcia",
        "email": "maria.garcia@email.com",
        "phone": "555-0123",
        "location": "Austin, TX",
        "linkedin": "linkedin.com/in/mariagarcia",
        "summary": "Software engineer with 6 years experience"
      },
      "skills": [
        "Python",
        "JavaScript",
        "React",
        "Django",
        "PostgreSQL",
        "AWS",
        "Docker"
      ],
      "experience": [
        {
          "company": "Tech Startup",
          "position": "Senior Software Engineer",
          "location": "Austin, TX",
          "start_date": "2020-03",
          "end_date": "Present",
          "responsibilities": [
            "Led development of microservices architecture",
            "Implemented CI/CD pipeline reducing deployment time by 60%",
            "Mentored junior developers"
          ],
          "achievements": [
            "Increased system performance by 40%",
            "Reduced bug count by 35%"
          ]
        }
      ],
      "education": [
        {
          "institution": "University of Texas",
          "degree": "BS",
          "field": "Computer Science",
          "start_date": "2014-09",
          "end_date": "2018-05",
          "gpa": "3.7"
        }
      ],
      "projects": [],
      "certifications": [],
      "achievements": []
    },
    "job_description": "We are looking for a Senior Software Engineer with strong Python and AWS experience. You will design and build scalable microservices, implement CI/CD pipelines, and mentor junior team members. 5+ years of experience required."
  }'
```

### Response

```json
{
  "success": true,
  "result": {
    "score": 78,
    "rating": "Good",
    "keywords_found": [
      "aws",
      "cicd",
      "django",
      "docker",
      "engineer",
      "microservices",
      "pipeline",
      "python",
      "senior",
      "software"
    ],
    "keywords_missing": [
      "design",
      "experience",
      "implement",
      "mentor",
      "required",
      "scalable",
      "team"
    ],
    "recommendations": [
      "Add more keywords from the job description to your resume",
      "Include 2-3 relevant projects to demonstrate hands-on experience"
    ],
    "strengths": [
      "Experience quality",
      "Skills relevance"
    ],
    "weaknesses": []
  }
}
```

---

## 📄 Export to PDF

### Request

```bash
curl -X POST http://localhost:5000/api/export/pdf \
  -H "Content-Type: application/json" \
  -d @resume.json \
  --output my_resume.pdf
```

**Where `resume.json` contains:**
```json
{
  "resume": {
    "personal_info": {
      "full_name": "John Doe",
      "email": "john.doe@email.com",
      "phone": "555-0100",
      "location": "San Francisco, CA",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe",
      "summary": "Passionate software engineer with 8 years of experience building scalable web applications."
    },
    "skills": [
      "Python",
      "JavaScript",
      "React",
      "Node.js",
      "AWS",
      "Docker",
      "PostgreSQL",
      "Git"
    ],
    "experience": [
      {
        "company": "Tech Giant",
        "position": "Senior Software Engineer",
        "location": "San Francisco, CA",
        "start_date": "2020-01",
        "end_date": "Present",
        "responsibilities": [
          "Led backend development for user authentication system serving 10M users",
          "Designed and implemented RESTful APIs using Python and Django"
        ],
        "achievements": [
          "Reduced API response time by 50%",
          "Improved system uptime to 99.9%"
        ]
      },
      {
        "company": "Startup Inc",
        "position": "Software Engineer",
        "location": "San Francisco, CA",
        "start_date": "2016-06",
        "end_date": "2019-12",
        "responsibilities": [
          "Built front-end features using React and Redux",
          "Collaborated with design team on UX improvements"
        ],
        "achievements": [
          "Increased user engagement by 30%"
        ]
      }
    ],
    "education": [
      {
        "institution": "Stanford University",
        "degree": "BS",
        "field": "Computer Science",
        "start_date": "2012-09",
        "end_date": "2016-05",
        "gpa": "3.8",
        "achievements": [
          "Dean's List all semesters",
          "CS Department Award for Outstanding Senior Project"
        ]
      }
    ],
    "projects": [
      {
        "title": "Open Source Contribution - Django REST Framework",
        "description": "Contributed bug fixes and features to popular Python REST framework",
        "technologies": ["Python", "Django"],
        "link": "github.com/encode/django-rest-framework",
        "highlights": [
          "10+ merged pull requests",
          "500+ stars on contributed features"
        ]
      }
    ],
    "certifications": [
      {
        "name": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "date": "2022-08",
        "credential_id": "ABC123XYZ"
      }
    ],
    "achievements": [
      "Speaker at PyCon 2023",
      "Hackathon winner - Best AI Application 2021"
    ]
  }
}
```

### Result

Downloads `my_resume.pdf` with professional formatting.

---

## 📝 Generate LinkedIn About

### Request

```bash
curl -X POST http://localhost:5000/api/generate/linkedin-about \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Emily Rodriguez",
    "title": "Product Manager",
    "industry": "SaaS / B2B Technology",
    "years_experience": "6 years",
    "skills": [
      "Product Strategy",
      "User Research",
      "Roadmap Planning",
      "Agile/Scrum",
      "Data Analysis",
      "Stakeholder Management"
    ],
    "achievements": [
      "Launched 3 successful products with $5M+ ARR",
      "Increased user retention by 45%",
      "Led cross-functional teams of 15+"
    ],
    "career_goals": "Looking to join a high-growth startup where I can drive product strategy and make a meaningful impact"
  }'
```

### Response

```json
{
  "success": true,
  "about": "I'm a product leader who thrives at the intersection of technology and user experience. Over the past 6 years in B2B SaaS, I've learned that the best products come from deeply understanding customer pain points and translating them into elegant solutions.\n\nMy proudest accomplishment? Leading the development of three products that now generate over $5M in annual recurring revenue. But what really drives me is seeing how our solutions help businesses work smarter—like when we increased user retention by 45% through data-driven feature prioritization.\n\nI believe great product management is about balance: listening to users while staying focused on the vision, moving fast while building sustainably, and empowering teams while maintaining accountability.\n\nCurrently looking for my next challenge with a high-growth startup where I can leverage my experience in product strategy, user research, and cross-functional leadership to drive meaningful impact.\n\nLet's connect if you're building something interesting or want to talk product strategy over coffee!"
}
```

---

## 🎯 Complete Python Example

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

# Create resume data
resume_data = {
    "personal_info": {
        "full_name": "David Kim",
        "email": "david.kim@email.com",
        "phone": "555-0200",
        "location": "Seattle, WA",
        "linkedin": "linkedin.com/in/davidkim"
    },
    "skills": ["Python", "AWS", "Docker", "Kubernetes"],
    "experience": [{
        "company": "Cloud Corp",
        "position": "DevOps Engineer",
        "location": "Seattle, WA",
        "start_date": "2019-01",
        "end_date": "Present",
        "responsibilities": ["Managed AWS infrastructure"],
        "achievements": ["Reduced costs by 30%"]
    }],
    "education": [{
        "institution": "UW",
        "degree": "BS",
        "field": "CS",
        "start_date": "2015",
        "end_date": "2019"
    }]
}

# 1. Generate professional summary
summary_response = requests.post(
    f"{BASE_URL}/api/generate/summary",
    json={
        "name": "David Kim",
        "target_role": "Senior DevOps Engineer",
        "years_experience": "5+ years",
        "skills": resume_data["skills"],
        "achievements": ["Reduced cloud costs by 30%"]
    }
)
print("Generated Summary:")
print(summary_response.json()["summary"])
print("\n" + "="*60 + "\n")

# 2. Analyze ATS score
ats_response = requests.post(
    f"{BASE_URL}/api/analyze/ats",
    json={
        "resume": resume_data,
        "job_description": "Looking for DevOps Engineer with AWS and Kubernetes experience"
    }
)
ats_result = ats_response.json()["result"]
print(f"ATS Score: {ats_result['score']}/100 ({ats_result['rating']})")
print(f"Keywords Found: {', '.join(ats_result['keywords_found'][:5])}")
print("\n" + "="*60 + "\n")

# 3. Export to PDF
pdf_response = requests.post(
    f"{BASE_URL}/api/export/pdf",
    json={"resume": resume_data}
)
with open("david_kim_resume.pdf", "wb") as f:
    f.write(pdf_response.content)
print("✅ Resume exported to david_kim_resume.pdf")
```

---

## 🧪 Testing with curl

### Test All Endpoints

```bash
#!/bin/bash

echo "Testing AI Resume Builder API..."
echo ""

# Health check
echo "1. Health Check"
curl -s http://localhost:5000/health | jq
echo ""

# Generate summary
echo "2. Generate Summary"
curl -s -X POST http://localhost:5000/api/generate/summary \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "target_role": "Software Engineer",
    "years_experience": "3 years",
    "skills": ["Python", "JavaScript"],
    "achievements": ["Built scalable systems"]
  }' | jq
echo ""

# ATS analysis
echo "3. ATS Analysis"
curl -s -X POST http://localhost:5000/api/analyze/ats \
  -H "Content-Type: application/json" \
  -d '{
    "resume": {
      "personal_info": {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "555-0000",
        "location": "City, State"
      },
      "skills": ["Python"],
      "experience": [],
      "education": []
    },
    "job_description": "Python developer needed"
  }' | jq
echo ""

echo "✅ All tests completed!"
```

---

## 🔧 Troubleshooting Common Issues

### Issue: "Ollama connection failed"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve

# Pull a model if needed
ollama pull llama3
```

### Issue: "Model not found"

**Solution:**
```bash
# List available models
ollama list

# Pull the missing model
ollama pull llama3
```

### Issue: "PDF export fails"

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade reportlab python-docx
```

---

**Happy Resume Building! 🎉**
