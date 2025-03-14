from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

@CrewBase
class DevCrew:
    """Dev Crew"""
    agents_config = "src/pythonuv/config/agents.yaml"
    tasks_config = "src/pythonuv/config/tasks.yaml"

    @agent
    def junior_developer(self) -> Agent:
        return Agent(config=self.agents_config.get("junior_developer", {}))

    @agent
    def senior_developer(self) -> Agent:
        return Agent(config=self.agents_config.get("senior_developer", {}))

    @task
    def write_code(self) -> Task:
        return Task(config=self.tasks_config.get("write_code", {}))

    @task
    def review_code(self) -> Task:
        return Task(config=self.tasks_config.get("review_code", {}))

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

# UI Configuration
st.set_page_config(page_title="CODEGEN", page_icon="💻", layout="wide")

# Main Content
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🚀 Muhammad Ubaid CODEGEN</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2d3436; margin-top: 0;'>AI-Powered Python Code Generator</h3>", unsafe_allow_html=True)

# Initialize session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

# Problem Input
with st.container():
    user_input = st.text_input(
        "**Describe your coding challenge:**",
        value=st.session_state.user_input,
        placeholder="Enter your problem statement here...",
        key="problem_input"
    )
    st.divider()

# Suggested Queries Grid
st.markdown("#### 💡 Try these example queries:")
suggested_queries = [
    "Develop a web scraper that collects trending topics from Twitter",
    "Create a command-line tool that backs up files automatically",
    "Implement a data analysis pipeline for processing CSV files",
    "Build a REST API using Flask with proper error handling",
    "Design a GUI application using Tkinter for a to-do list",
]

# Create 2 columns for the grid
cols = st.columns(2)
for i, query in enumerate(suggested_queries):
    with cols[i % 2]:  # Alternate between columns
        if st.button(
            f"💡 {query}",
            use_container_width=True,
            help="Click to auto-fill prompt"
        ):
            st.session_state.user_input = query

st.divider()

# Generation Section
if st.button("🚀 Generate Code", type="primary", use_container_width=True):
    if user_input.strip():
        with st.spinner("🔍 Senior developers are reviewing the code..."):
            try:
                response = DevCrew().crew().kickoff(inputs={"problem": user_input})
                
                st.success("✅ Code Generated Successfully!")
                with st.expander("**Generated Code**", expanded=True):
                    st.code(response, language='python')

                # Download functionality
                with open("generated_code.py", "w") as f:
                    f.write(str(response))
                
                st.download_button(
                    label="📥 Download Code",
                    data=open("generated_code.py", "rb").read(),
                    file_name="generated_code.py",
                    mime="text/x-python",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error generating code: {str(e)}")
    else:
        st.warning("⚠️ Please enter a problem statement before generating code.")

# Sidebar Description
with st.sidebar:
    st.markdown("""
    ## 📝 About CODEGEN
    
    **Your AI-Powered Coding Partner**  
    Leverage cutting-edge AI to transform your ideas into production-ready Python code.
    
    ### 🛠️ How It Works
    1. **Describe** your coding challenge
    2. **Junior Developer** (5 yrs exp) drafts initial solution
    3. **Senior Developer** (30 yrs exp) reviews and refines code
    4. **Get** polished, production-ready code
    
    ### 🌟 Key Features
    - Dual AI Agent System
    - Full Error Handling
    - OOP Best Practices
    - Real-world Code Standards
    - One-click Download
    
    ### 🚨 Limitations
    - Python-only support
    - Requires clear problem statements
    - May require API keys for web services
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>🚀 Powered by CrewAI & Gemini Flash 2.0 | 🛡️ Enterprise Grade Code Generation</div>", unsafe_allow_html=True)