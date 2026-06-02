"""
main.py - Streamlit entry point for EduSense.
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path so 'src' imports work
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.storage.database import init_db, get_db
from src.storage.faiss_manager import FaissManager
from src.ai.llm_manager import LLMManager
from src.ai.embed_manager import EmbedManager
from src.retrieval.rag_engine import RAGEngine
from src.services.subject_service import SubjectService
from src.services.tutor_service import TutorService
from src.services.assessment_service import AssessmentService
from src.services.planning_service import PlanningService

# Page Config
st.set_page_config(page_title="EduSense", page_icon="🧠", layout="wide")

def load_css():
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize singletons in st.session_state
if 'initialized' not in st.session_state:
    init_db()
    
    # DB session
    db_gen = get_db()
    db_session = next(db_gen)
    st.session_state.db = db_session
    
    # Managers
    llm = LLMManager()
    embed = EmbedManager()
    faiss = FaissManager(embed.get_embeddings())
    rag = RAGEngine(llm, faiss)
    
    # Services
    st.session_state.subject_svc = SubjectService(db_session, faiss)
    st.session_state.tutor_svc = TutorService(db_session, rag)
    st.session_state.assessment_svc = AssessmentService(db_session, llm, faiss)
    st.session_state.planning_svc = PlanningService(db_session, llm, faiss)
    
    st.session_state.initialized = True
    st.session_state.current_subject_id = None

def render_sidebar():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3389/3389081.png", width=50)
    st.sidebar.title("EduSense")
    
    subjects = st.session_state.subject_svc.get_subjects()
    if not subjects:
        st.sidebar.info("Create a Subject to get started.")
    else:
        subject_names = {s.name: s.id for s in subjects}
        selected = st.sidebar.selectbox("Active Subject", list(subject_names.keys()))
        st.session_state.current_subject_id = subject_names[selected]
        
    st.sidebar.markdown("---")
    return st.sidebar.radio("Navigation", ["Dashboard", "AI Tutor", "Study Planner", "Assessments", "Analytics"])

def render_dashboard():
    st.header("Workspace Dashboard")
    
    with st.expander("➕ Create New Subject", expanded=(not st.session_state.current_subject_id)):
        with st.form("new_subject"):
            name = st.text_input("Subject Name")
            desc = st.text_area("Description")
            if st.form_submit_button("Create"):
                if name:
                    st.session_state.subject_svc.create_subject(name, desc)
                    st.success(f"Subject '{name}' created!")
                    st.rerun()
                else:
                    st.error("Name required.")
                    
    if st.session_state.current_subject_id:
        subject = st.session_state.subject_svc.get_subject(st.session_state.current_subject_id)
        st.subheader(f"Subject: {subject.name}")
        st.write(subject.description)
        
        st.markdown("### Upload Study Materials")
        uploaded_files = st.file_uploader("Upload PDFs, DOCX, TXT", accept_multiple_files=True)
        if st.button("Process Documents"):
            for f in uploaded_files:
                with st.spinner(f"Processing {f.name}..."):
                    success = st.session_state.subject_svc.add_document(subject.id, f.read(), f.name)
                    if success:
                        st.success(f"Added {f.name} successfully.")
                    else:
                        st.error(f"Failed to add {f.name}.")

def render_tutor():
    if not st.session_state.current_subject_id:
        st.warning("Please select a subject first.")
        return
        
    st.header("🤖 AI Tutor")
    subject_id = st.session_state.current_subject_id
    
    # Display History
    history = st.session_state.tutor_svc.get_chat_history(subject_id)
    for msg in history:
        with st.chat_message(msg.role):
            st.write(msg.content)
            
    # Chat Input
    if prompt := st.chat_input("Ask a question about your study materials..."):
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.tutor_svc.ask_tutor(subject_id, prompt)
                st.write(response['answer'])
                if response['citations']:
                    with st.expander("View Sources"):
                        for c in response['citations']:
                            st.caption(f"Source: {c['source']}\n\n{c['snippet']}")
        st.rerun()

def render_assessments():
    if not st.session_state.current_subject_id:
        st.warning("Please select a subject first.")
        return
        
    st.header("📝 Assessments & Flashcards")
    subject_id = st.session_state.current_subject_id
    
    tab1, tab2 = st.tabs(["Flashcards", "Quiz"])
    
    with tab1:
        if st.button("Generate Flashcards"):
            with st.spinner("Generating..."):
                cards = st.session_state.assessment_svc.generate_flashcards(subject_id)
                st.markdown(cards)
                
    with tab2:
        if st.button("Generate Quiz"):
            with st.spinner("Generating..."):
                quiz = st.session_state.assessment_svc.generate_quiz(subject_id)
                st.markdown(quiz)
                
        st.markdown("---")
        st.subheader("Record Quiz Result")
        with st.form("quiz_result"):
            score = st.slider("Score (%)", 0, 100, 80)
            feedback = st.text_area("Feedback or what you struggled with:")
            if st.form_submit_button("Save Result"):
                st.session_state.assessment_svc.record_quiz_score(subject_id, score, feedback)
                st.success("Result saved!")

def render_planner():
    if not st.session_state.current_subject_id:
        st.warning("Please select a subject first.")
        return
        
    st.header("📅 Study Planner")
    subject_id = st.session_state.current_subject_id
    
    with st.form("planner_form"):
        plan_type = st.selectbox("Plan Type", ["Daily", "Weekly", "Exam Cram"])
        time_avail = st.text_input("Time Available (e.g., '2 hours/day for 3 days')")
        
        if st.form_submit_button("Generate Plan"):
            with st.spinner("Creating your personalized schedule..."):
                plan = st.session_state.planning_svc.generate_plan(subject_id, plan_type, time_avail)
                st.markdown(plan)

def render_analytics():
    if not st.session_state.current_subject_id:
        st.warning("Please select a subject first.")
        return
        
    st.header("📊 Learning Analytics")
    subject_id = st.session_state.current_subject_id
    
    analytics = st.session_state.assessment_svc.get_subject_analytics(subject_id)
    
    col1, col2 = st.columns(2)
    col1.metric("Average Quiz Score", f"{analytics['average_score']}%")
    col2.metric("Quizzes Taken", analytics['quizzes_taken'])
    
    st.subheader("Areas for Improvement (Weak Topics)")
    if analytics['weak_areas']:
        for topic in analytics['weak_areas']:
            st.error(topic)
    else:
        st.info("No weak topics identified yet. Take some quizzes and record feedback!")

def main():
    load_css()
    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "AI Tutor":
        render_tutor()
    elif page == "Study Planner":
        render_planner()
    elif page == "Assessments":
        render_assessments()
    elif page == "Analytics":
        render_analytics()

if __name__ == "__main__":
    main()
