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

# Inject custom CSS for a modern look
st.markdown(
    """
    <style>
    body {
         background-color: #f0f2f6;
         font-family: 'Helvetica Neue', sans-serif;
    }
    .main-title {
         text-align: center;
         color: #2c3e50;
         margin-top: 20px;
         font-size: 3rem;
    }
    .sub-title {
         text-align: center;
         color: #34495e;
         margin-bottom: 30px;
         font-size: 2rem;
    }
    .query-list {
         font-size: 1.1rem;
         color: #2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Updated Titles
st.markdown("<h1 class='main-title'>Welcome to Muhammad Ubaid Hussain’s CodeGen</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-title'>Python Code Generator Agent</h2>", unsafe_allow_html=True)

suggested_queries = [
    "Develop a web scraper that collects trending topics from Twitter",
    "Create a command-line tool that backs up files automatically",
    "Implement a data analysis pipeline for processing CSV files",
    "Build a REST API using Flask with proper error handling",
    "Design a GUI application using Tkinter for a to-do list",
]


st.write("### Suggested Queries:")
for query in suggested_queries:
    st.markdown(f"- <span class='query-list'>{query}</span>", unsafe_allow_html=True)

user_input = st.text_input("Enter the problem statement:", "")

if st.button("Generate Code"):
    if user_input.strip():
        with st.spinner("Generating code, please wait..."):
            response = DevCrew().crew().kickoff(inputs={"problem": user_input})
        if response:
            st.code(response, language='python')
            # Save the response as a file
            file_name = "response.py"
            with open(file_name, "w") as f:
                f.write(str(response))
            # Provide download button
            with open(file_name, "rb") as f:
                st.download_button(label="Download Generated Code",
                                   data=f,
                                   file_name=file_name,
                                   mime="text/x-python")
        else:
            st.error("No response generated. Please try again.")
    else:
        st.warning("Please enter a problem statement before generating code.")

# Updated Sidebar Content
st.sidebar.title("About Muhammad Ubaid Hussain")
st.sidebar.info(
    """
    Muhammad Ubaid Hussain is a passionate software developer known for blending innovative AI technology with creative problem solving. Welcome to his AI-powered Python Code Generator Agent—a state-of-the-art tool designed to simplify your coding tasks.

    🔹 **How It Works:**
    1. **Enter a Problem Statement:** Provide a coding challenge or requirement.
    2. **AI-Powered Code Generation:** Two specialized AI agents work together:
         - 👨‍💻 **Junior Developer** (5 years of experience) – Generates the initial code.
         - 👨‍🏫 **Senior Developer** (20 years of experience) – Reviews and refines the code.
    3. **Instant Output & Download:** View the generated code instantly and download it as a file.

    🚀 **Features:**
    - Supports Object-Oriented Programming & robust error handling.
    - Handles a variety of Python tasks—from simple functions to complex applications.
    - Provides suggested queries for quick inspiration.

    Start coding smarter with AI!
    """
)

