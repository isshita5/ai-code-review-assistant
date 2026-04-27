import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Code Review Assistant")
st.write("Paste your code and get instant AI-powered review!")

# ── Groq client ───────────────────────────────────────────────────────────────
client = Groq()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Review Settings")

    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "TypeScript",
         "C++", "SQL", "PowerShell", "Other"]
    )

    review_type = st.multiselect(
        "What to review?",
        ["Bugs & Errors", "Security Issues",
         "Performance", "Best Practices",
         "Code Quality", "Documentation"],
        default=["Bugs & Errors", "Security Issues", "Best Practices"]
    )

    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("🤖 Groq LLM API (Llama 3.3)")
    st.markdown("🐍 Python + Streamlit")

# ── Main UI ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Your Code")
    code_input = st.text_area(
        "Paste your code here:",
        height=400,
        placeholder="""# Paste your code here
# Example:
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)"""
    )

    st.markdown("**Try sample code:**")
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🐍 Python Sample"):
            st.session_state.sample = """import pickle

def load_user_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def get_user_info(user_id):
    password = "admin123"
    query = f"SELECT * FROM users WHERE id={user_id}"
    result = db.execute(query)
    return result

def process_data(items):
    result = []
    for i in range(len(items)):
        result = result + [items[i] * 2]
    return result"""

    with col_b:
        if st.button("⚡ JS Sample"):
            st.session_state.sample = """function getUserData(userId) {
    var query = "SELECT * FROM users WHERE id=" + userId;
    var result = db.query(query);

    for (var i = 0; i < result.length; i++) {
        console.log(result[i].password);
    }

    eval(result[0].userScript);
    return result;
}"""

with col2:
    st.subheader("🤖 AI Review")

    if st.button("🔍 Review My Code", type="primary", use_container_width=True):

        code_to_review = (
            st.session_state.get('sample', code_input)
            if not code_input.strip()
            else code_input
        )

        if not code_to_review.strip():
            st.error("Please paste some code first!")
        else:
            with st.spinner("AI is reviewing your code..."):

                review_focus = ", ".join(review_type) if review_type else "general quality"

                prompt = f"""You are an expert {language} code reviewer.

Review this code focusing on: {review_focus}

Code to review:
```{language.lower()}
{code_to_review}
```

Provide a structured review with these exact sections:

## 🔴 Critical Issues
[List any bugs, security vulnerabilities, or critical problems with line numbers]

## 🟡 Warnings
[List performance issues, bad practices, or potential problems]

## 🟢 Good Practices
[List what the developer did well]

## 💡 Suggestions
[Specific improvements with corrected code examples]

## 📊 Overall Score
[Rate the code X/10 and explain why]

Be specific, actionable, and include corrected code snippets where helpful."""

                # Call Groq API
                message = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=2000
                )

                review = message.choices[0].message.content
                st.markdown(review)

                # Download button
                st.download_button(
                    label="📥 Download Review",
                    data=review,
                    file_name="code_review.md",
                    mime="text/markdown"
                )

# ── Show sample if button clicked ─────────────────────────────────────────────
if 'sample' in st.session_state and not code_input.strip():
    with col1:
        st.code(st.session_state.sample, language="python")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with ❤️ using **Groq LLM API** | "
    "AI Code Review Assistant by Isshita Pandita"
)