import streamlit as st
import requests
import streamlit.components.v1 as components
from export_pdf import create_quiz_pdf

st.set_page_config(
    page_title="Assessly",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div {
            overflow-y: hidden !important;
        }
        section[data-testid="stSidebar"] > div:hover {
            overflow-y: auto !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"
ENDPOINT = "/upload-n-generate/"

if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

def generate_quiz(uploaded_file, num_questions, difficulty_level):
    st.session_state.quiz_generated = False
    st.session_state.quiz_submitted = False
    st.session_state.quiz_data = None

    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    data = {"num_questions": str(num_questions), "difficulty": difficulty_level}

    try:
        response = requests.post(f"{BACKEND_URL}{ENDPOINT}", files=files, data=data, timeout=300)

        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                st.error(f"Quiz Generation Failed: {result['error']}")
                return

            quiz_data = result.get('quiz_data', [])
            
            if not isinstance(quiz_data, list):
                st.error("Invalid quiz data format received from backend")
                return
                
            st.session_state.quiz_data = quiz_data
            st.session_state.quiz_generated = True
            
            if not st.session_state.quiz_data:
                st.error("Quiz generated but no questions were returned")
                return
                
            st.success("Quiz generated successfully! Start the assessment.")
        else:
            error_detail = response.json().get("detail", f"Server responded with status {response.status_code}")
            st.error(f"Backend Error: {error_detail}")

    except requests.exceptions.ConnectionError:
        st.error(f"Connection Error: Could not connect to backend at {BACKEND_URL}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

uploaded_file = st.sidebar.file_uploader(
    "Upload Document (PDF or DOCX)",
    type=['pdf', 'docx'],
    accept_multiple_files=False
)


st.sidebar.markdown("---")
st.sidebar.subheader("Quiz Parameters")

num_questions = st.sidebar.number_input(
    "No. of MCQs to generate:",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

difficulty_level = st.sidebar.selectbox(
    "Select Difficulty Level:",
    options=['easy', 'medium', 'hard'],
    index=1
)

if st.sidebar.button("Generate Quiz", use_container_width=True, type="primary"):
    if uploaded_file:
        st.session_state.quiz_submitted = False
        st.session_state.score = 0
        with st.spinner("Processing document and generating quiz..."):
            generate_quiz(uploaded_file, num_questions, difficulty_level)
    else:
        st.sidebar.error("Please upload a **PDF or DOCX** file to generate a quiz.")

col1, col2 = st.columns([6, 1])

with col1:
    st.title("Assessly: PDF to Quiz Generator")
    st.caption("Turn your PDFs into smart multiple-choice quizzes instantly!")

with col2:
    if st.session_state.quiz_generated and st.session_state.quiz_data:
        pdf_buffer = create_quiz_pdf(st.session_state.quiz_data)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="quiz.pdf",
            mime="application/pdf"
        )

st.markdown("---")

st.subheader("Generated Multiple-Choice Quiz")

if st.session_state.quiz_generated and st.session_state.quiz_data and not st.session_state.quiz_submitted:
    quiz_form = st.form(key="quiz_submission_form")
    with quiz_form:
        st.markdown(f"**Quiz Details:** {len(st.session_state.quiz_data)} **{difficulty_level.upper()}** MCQs generated.")
        st.warning("⚠️ **Note:** There is negative marking of **-0.25** for each incorrect answer.")
        st.markdown("---")
        
        for i, q in enumerate(st.session_state.quiz_data):
            if not isinstance(q, dict):
                st.error(f"Data Error: Question {i+1} is corrupted.")
                continue
                
            question_text = q.get('question', f"Error: Q{i+1} text missing.")
            marks = q.get('marks', 1)
            options = q.get('options', [])
            
            st.markdown(f"**Q{i+1}:** {question_text} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **({marks} Marks)**", unsafe_allow_html=True)
            
            if options and isinstance(options, list) and len(options) == 4:
                st.session_state.user_answers[i] = st.radio(
                    "Select your answer:", 
                    options, 
                    key=f"q_{i}_ans", 
                    index=None
                )
            else:
                st.error(f"Q{i+1} options are corrupted or missing.")
            
            st.markdown("---")
        
        if st.form_submit_button("Submit Quiz & Review", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()

elif st.session_state.quiz_submitted and st.session_state.quiz_data:
    components.html(
        """
            <script>
                var body = window.parent.document.querySelector(".main");
                body.scrollTop = 0;
            </script>
        """,
        height=0
    )
    st.subheader("Quiz Results & Review")
    
    obtained_marks = 0
    total_marks = 0
    questions = st.session_state.quiz_data
    
    for i, q in enumerate(questions):
        if isinstance(q, dict):
            user_answer = st.session_state.user_answers.get(i)
            correct_answer = q.get('correct_answer')
            marks = q.get('marks', 1)
            total_marks += marks
            
            if correct_answer and user_answer:
                if str(user_answer).strip() == str(correct_answer).strip():
                    obtained_marks += marks
                else:
                    obtained_marks -= 0.25
    
    st.session_state.score = max(0, obtained_marks) 
    st.session_state.score = obtained_marks
    
    score_col1, score_col2, reload_col = st.columns(3)
    
    with score_col1:
        st.metric("Your Score", f"{st.session_state.score}/{total_marks}")
    
    with score_col2:
        percentage = round((st.session_state.score / total_marks) * 100) if total_marks > 0 else 0
        st.metric("Percentage", f"{percentage}%")
    
    with reload_col:
        if st.button("Take Quiz Again", use_container_width=True):
            st.session_state.quiz_submitted = False
            st.session_state.score = 0
            st.session_state.user_answers = {}
            st.rerun()
    
    st.markdown("---")
    
    for i, q in enumerate(questions):
        if isinstance(q, dict):
            user_answer = st.session_state.user_answers.get(i, "No Answer Given")
            correct_answer = q.get('correct_answer')
            
            is_correct = correct_answer and str(user_answer).strip() == str(correct_answer).strip()
            
            if is_correct:
                st.success(f"**Q{i+1} (Correct):** {q.get('question', 'N/A')}")
                st.markdown(f"**Your Answer:** *{user_answer}*")
            else:
                
                st.error(f"**Q{i+1} (Incorrect):** {q.get('question', 'N/A')}")
                st.markdown(f"**Your Answer:** *{user_answer}*")
                st.markdown(f"**Correct Answer:** **{correct_answer or 'Missing'}**")
            
            st.markdown("---")

else:
    st.info("Upload a PDF or DOCX file, set the number of questions and difficulty, and hit 'Generate Quiz'.")