/**
 * app.js - Frontend logic for AI Resume Builder
 */

document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        personal_info: {
            full_name: '', email: '', phone: '', location: '', linkedin: '', github: '', summary: ''
        },
        experience: [],
        education: [],
        skills: [],
        projects: []
    };

    // DOM Elements
    const elements = {
        navItems: document.querySelectorAll('.nav-item'),
        tabContents: document.querySelectorAll('.tab-content'),
        overlay: document.getElementById('loading-overlay'),
        loadingText: document.getElementById('loading-text'),
        previewSheet: document.getElementById('resume-preview'),
        
        // Form Inputs
        inputs: {
            personal: {
                full_name: document.getElementById('personal-name'),
                email: document.getElementById('personal-email'),
                phone: document.getElementById('personal-phone'),
                location: document.getElementById('personal-location'),
                linkedin: document.getElementById('personal-linkedin'),
                github: document.getElementById('personal-github'),
                summary: document.getElementById('personal-summary')
            },
            skills: document.getElementById('skills-input')
        },
        
        // Lists
        expList: document.getElementById('experience-list'),
        eduList: document.getElementById('education-list'),
        
        // Buttons
        btnAddExp: document.getElementById('btn-add-experience'),
        btnAddEdu: document.getElementById('btn-add-education'),
        btnLoadSample: document.getElementById('btn-load-sample'),
        btnExportPdf: document.getElementById('btn-export-pdf'),
        btnExportDocx: document.getElementById('btn-export-docx'),
        btnExportTxt: document.getElementById('btn-export-txt'),
        
        // AI Buttons
        btnAiSummary: document.getElementById('btn-ai-summary'),
        btnGenerateCl: document.getElementById('btn-generate-cl'),
        btnGenerateLi: document.getElementById('btn-generate-li'),
        btnAnalyzeAts: document.getElementById('btn-analyze-ats'),
    };

    // Check backend health
    checkHealth();

    // ─────────────────────────────────────────────────────────
    // UI Interactions
    // ─────────────────────────────────────────────────────────

    // Tab Switching
    elements.navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.currentTarget.getAttribute('data-tab');
            
            // Update active nav
            elements.navItems.forEach(nav => nav.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            // Update active tab content
            elements.tabContents.forEach(tab => tab.classList.remove('active'));
            document.getElementById(`tab-${target}`).classList.add('active');
        });
    });

    // Auto-update Preview on input changes
    Object.values(elements.inputs.personal).forEach(input => {
        input.addEventListener('input', () => {
            updateStateFromForms();
            renderPreview();
        });
    });
    
    elements.inputs.skills.addEventListener('input', () => {
        updateStateFromForms();
        renderPreview();
    });

    // Dynamic Lists (Experience & Education)
    let idCounter = 1;

    elements.btnAddExp.addEventListener('click', () => {
        const template = document.getElementById('tpl-experience').innerHTML;
        const html = template.replace(/{id}/g, idCounter++);
        elements.expList.insertAdjacentHTML('beforeend', html);
        attachDynamicListeners(elements.expList.lastElementChild);
        updateStateFromForms();
        renderPreview();
    });

    elements.btnAddEdu.addEventListener('click', () => {
        const template = document.getElementById('tpl-education').innerHTML;
        const html = template.replace(/{id}/g, idCounter++);
        elements.eduList.insertAdjacentHTML('beforeend', html);
        attachDynamicListeners(elements.eduList.lastElementChild);
        updateStateFromForms();
        renderPreview();
    });

    function attachDynamicListeners(container) {
        // Delete button
        const delBtn = container.querySelector('.btn-delete');
        if (delBtn) {
            delBtn.addEventListener('click', () => {
                container.remove();
                updateStateFromForms();
                renderPreview();
            });
        }
        
        // Input changes
        const inputs = container.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                updateStateFromForms();
                renderPreview();
            });
        });
    }

    // ─────────────────────────────────────────────────────────
    // State Management & Preview
    // ─────────────────────────────────────────────────────────

    function updateStateFromForms() {
        // Personal Info
        state.personal_info.full_name = elements.inputs.personal.full_name.value;
        state.personal_info.email = elements.inputs.personal.email.value;
        state.personal_info.phone = elements.inputs.personal.phone.value;
        state.personal_info.location = elements.inputs.personal.location.value;
        state.personal_info.linkedin = elements.inputs.personal.linkedin.value;
        state.personal_info.github = elements.inputs.personal.github.value;
        state.personal_info.summary = elements.inputs.personal.summary.value;

        // Skills
        const skillsRaw = elements.inputs.skills.value;
        state.skills = skillsRaw ? skillsRaw.split(',').map(s => s.trim()).filter(s => s) : [];

        // Experience
        state.experience = [];
        document.querySelectorAll('.experience-item').forEach(item => {
            const responsibilities = item.querySelector('.exp-resp').value.split('\n').filter(s => s.trim());
            const achievements = item.querySelector('.exp-achiev').value.split('\n').filter(s => s.trim());
            
            state.experience.push({
                company: item.querySelector('.exp-company').value,
                position: item.querySelector('.exp-position').value,
                location: item.querySelector('.exp-location').value,
                start_date: item.querySelector('.exp-start').value,
                end_date: item.querySelector('.exp-end').value,
                responsibilities,
                achievements
            });
        });

        // Education
        state.education = [];
        document.querySelectorAll('.education-item').forEach(item => {
            state.education.push({
                institution: item.querySelector('.edu-inst').value,
                degree: item.querySelector('.edu-degree').value,
                field: item.querySelector('.edu-field').value,
                start_date: item.querySelector('.edu-start').value,
                end_date: item.querySelector('.edu-end').value,
                gpa: item.querySelector('.edu-gpa').value
            });
        });
    }

    function renderPreview() {
        const { personal_info, experience, education, skills } = state;
        
        let html = `
            <h1>${personal_info.full_name || 'Your Name'}</h1>
            <div class="contact-info">
                ${[personal_info.email, personal_info.phone, personal_info.location, personal_info.linkedin, personal_info.github].filter(Boolean).join(' | ')}
            </div>
        `;
        
        if (personal_info.summary) {
            html += `
                <h2>Professional Summary</h2>
                <p>${personal_info.summary}</p>
            `;
        }
        
        if (experience.length > 0) {
            html += `<h2>Experience</h2>`;
            experience.forEach(exp => {
                html += `
                    <div style="margin-bottom: 12px;">
                        <div class="item-meta">
                            <span class="item-title">${exp.position}</span>
                            <span class="item-date">${exp.start_date} - ${exp.end_date}</span>
                        </div>
                        <div class="item-meta">
                            <span class="item-subtitle">${exp.company}${exp.location ? `, ${exp.location}` : ''}</span>
                        </div>
                        <ul>
                            ${exp.responsibilities.map(r => `<li>${r}</li>`).join('')}
                            ${exp.achievements.map(a => `<li>${a}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
        }
        
        if (education.length > 0) {
            html += `<h2>Education</h2>`;
            education.forEach(edu => {
                html += `
                    <div style="margin-bottom: 12px;">
                        <div class="item-meta">
                            <span class="item-title">${edu.institution}</span>
                            <span class="item-date">${edu.start_date} - ${edu.end_date}</span>
                        </div>
                        <div>${edu.degree} in ${edu.field}${edu.gpa ? `, GPA: ${edu.gpa}` : ''}</div>
                    </div>
                `;
            });
        }
        
        if (skills.length > 0) {
            html += `
                <h2>Skills</h2>
                <p>${skills.join(', ')}</p>
            `;
        }
        
        elements.previewSheet.innerHTML = html;
    }

    // ─────────────────────────────────────────────────────────
    // Sample Data
    // ─────────────────────────────────────────────────────────
    
    elements.btnLoadSample.addEventListener('click', () => {
        elements.inputs.personal.full_name.value = "Alex Developer";
        elements.inputs.personal.email.value = "alex@example.com";
        elements.inputs.personal.phone.value = "(555) 987-6543";
        elements.inputs.personal.location.value = "San Francisco, CA";
        elements.inputs.skills.value = "Python, JavaScript, React, Node.js, Docker, AWS";
        
        elements.btnAddExp.click();
        const expItem = elements.expList.lastElementChild;
        expItem.querySelector('.exp-company').value = "Tech Solutions Inc";
        expItem.querySelector('.exp-position').value = "Senior Software Engineer";
        expItem.querySelector('.exp-location').value = "San Francisco, CA";
        expItem.querySelector('.exp-start').value = "Jan 2020";
        expItem.querySelector('.exp-end').value = "Present";
        expItem.querySelector('.exp-resp').value = "Led backend team of 5 developers.\nArchitected microservices infrastructure.";
        expItem.querySelector('.exp-achiev').value = "Improved API latency by 40%.\nReduced cloud costs by $20k/yr.";
        
        elements.btnAddEdu.click();
        const eduItem = elements.eduList.lastElementChild;
        eduItem.querySelector('.edu-inst').value = "State University";
        eduItem.querySelector('.edu-degree').value = "B.S.";
        eduItem.querySelector('.edu-field').value = "Computer Science";
        eduItem.querySelector('.edu-start').value = "2015";
        eduItem.querySelector('.edu-end').value = "2019";
        
        updateStateFromForms();
        renderPreview();
    });

    // ─────────────────────────────────────────────────────────
    // API & AI Integration
    // ─────────────────────────────────────────────────────────

    function showLoading(text) {
        elements.loadingText.textContent = text;
        elements.overlay.classList.remove('hidden');
    }
    
    function hideLoading() {
        elements.overlay.classList.add('hidden');
    }

    async function checkHealth() {
        try {
            const res = await fetch('/health');
            const data = await res.json();
            const dot = document.getElementById('system-status-dot');
            const text = document.getElementById('system-status-text');
            
            if (data.ollama === 'connected') {
                dot.className = 'dot online';
                text.textContent = 'System Ready';
            } else {
                dot.className = 'dot offline';
                text.textContent = 'Ollama Offline';
            }
        } catch (e) {
            console.error(e);
        }
    }

    // AI Summary
    elements.btnAiSummary.addEventListener('click', async () => {
        if (!state.personal_info.full_name) return alert("Please enter your name first");
        
        showLoading('Generating Summary...');
        try {
            const res = await fetch('/api/generate/summary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: state.personal_info.full_name,
                    target_role: "Professional", // Could be a field
                    years_experience: "Various",
                    skills: state.skills,
                    achievements: state.experience.flatMap(e => e.achievements)
                })
            });
            const data = await res.json();
            if (data.success) {
                elements.inputs.personal.summary.value = data.summary;
                updateStateFromForms();
                renderPreview();
            } else {
                alert("Error: " + data.error);
            }
        } catch (e) {
            alert("Connection error");
        }
        hideLoading();
    });

    // AI Cover Letter
    elements.btnGenerateCl.addEventListener('click', async () => {
        showLoading('Generating Cover Letter...');
        const company = document.getElementById('ai-cl-company').value;
        const position = document.getElementById('ai-cl-position').value;
        const jd = document.getElementById('ai-cl-jd').value;
        
        try {
            const res = await fetch('/api/generate/cover-letter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: state.personal_info.full_name || "Applicant",
                    company, position, job_description: jd,
                    skills: state.skills,
                    experience_summary: state.personal_info.summary || "Experienced professional",
                    achievements: state.experience.flatMap(e => e.achievements)
                })
            });
            const data = await res.json();
            if (data.success) {
                const resultBox = document.getElementById('cl-result');
                document.getElementById('cl-result-text').value = data.cover_letter;
                resultBox.classList.remove('hidden');
            } else {
                alert("Error: " + data.error);
            }
        } catch (e) {
            alert("Connection error");
        }
        hideLoading();
    });

    // AI LinkedIn
    elements.btnGenerateLi.addEventListener('click', async () => {
        showLoading('Generating LinkedIn About...');
        const title = document.getElementById('ai-li-title').value;
        const goals = document.getElementById('ai-li-goals').value;
        
        try {
            const res = await fetch('/api/generate/linkedin-about', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: state.personal_info.full_name || "Professional",
                    title: title || "Professional",
                    industry: "Tech", 
                    years_experience: "Multiple",
                    skills: state.skills,
                    achievements: state.experience.flatMap(e => e.achievements),
                    career_goals: goals
                })
            });
            const data = await res.json();
            if (data.success) {
                const resultBox = document.getElementById('li-result');
                document.getElementById('li-result-text').value = data.about;
                resultBox.classList.remove('hidden');
            } else {
                alert("Error: " + data.error);
            }
        } catch (e) {
            alert("Connection error");
        }
        hideLoading();
    });

    // ATS Analysis
    elements.btnAnalyzeAts.addEventListener('click', async () => {
        showLoading('Analyzing ATS Match...');
        const jd = document.getElementById('ats-jd').value;
        
        try {
            const res = await fetch('/api/analyze/ats', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume: state,
                    job_description: jd
                })
            });
            const data = await res.json();
            if (data.success) {
                document.getElementById('ats-results').classList.remove('hidden');
                
                // Update Score
                const score = data.result.score;
                document.getElementById('ats-score-value').textContent = Math.round(score) + "%";
                document.getElementById('ats-rating').textContent = data.result.rating;
                
                // Animate Circle
                const circle = document.getElementById('ats-score-path');
                circle.setAttribute('stroke-dasharray', `${score}, 100`);
                if(score > 80) circle.style.stroke = 'var(--secondary)';
                else if(score > 60) circle.style.stroke = '#F59E0B'; // Amber
                else circle.style.stroke = 'var(--danger)';
                
                // Recommendations
                const recsContainer = document.getElementById('ats-recommendations');
                recsContainer.innerHTML = data.result.recommendations.map(r => `<li>${r}</li>`).join('');
                
                // Keywords
                const foundContainer = document.getElementById('ats-keywords-found');
                const missingContainer = document.getElementById('ats-keywords-missing');
                
                document.getElementById('count-found').textContent = data.result.keyword_analysis.found.length;
                document.getElementById('count-missing').textContent = data.result.keyword_analysis.missing.length;
                
                foundContainer.innerHTML = data.result.keyword_analysis.found.map(k => `<span class="tag tag-found">${k}</span>`).join('');
                missingContainer.innerHTML = data.result.keyword_analysis.missing.map(k => `<span class="tag tag-missing">${k}</span>`).join('');
            }
        } catch (e) {
            alert("Connection error");
        }
        hideLoading();
    });

    // Copy Buttons
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetId = e.currentTarget.getAttribute('data-target');
            const textarea = document.getElementById(targetId);
            textarea.select();
            document.execCommand('copy');
            
            const originalHTML = e.currentTarget.innerHTML;
            e.currentTarget.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            setTimeout(() => e.currentTarget.innerHTML = originalHTML, 2000);
        });
    });

    // ─────────────────────────────────────────────────────────
    // Export Functions
    // ─────────────────────────────────────────────────────────

    async function exportResume(format) {
        showLoading(`Exporting to ${format.toUpperCase()}...`);
        try {
            const res = await fetch(`/api/export/${format}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume: state })
            });
            
            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // Try to get filename from header
                const disposition = res.headers.get('Content-Disposition');
                let filename = `resume.${format}`;
                if (disposition && disposition.includes('filename=')) {
                    filename = disposition.split('filename=')[1].replace(/["']/g, '');
                }
                
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                alert("Export failed");
            }
        } catch (e) {
            alert("Connection error during export");
        }
        hideLoading();
    }

    elements.btnExportPdf.addEventListener('click', () => exportResume('pdf'));
    elements.btnExportDocx.addEventListener('click', () => exportResume('docx'));
    elements.btnExportTxt.addEventListener('click', () => exportResume('txt'));
});
