from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")


model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)


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
    


   

st.title("Welcome to Muhammad Ubaid CODEGEN 🚀")
st.title("Python Code Generator Agent")

suggested_queries = [
    "Make a function who Get Me The Current Weather Of Karachi",
    "Make a Calculator Use if else for operations with complete error handling",
    "Make a function which will return me the current time",
    "Develop a complex Game Using Object Orinted Programming with complete Error Handling",
    "Make a python Function who get the latest news with the help of api key",
]

st.write("### Suggested Queries:")
for query in suggested_queries:
    st.write(f"- {query}")

user_input = st.text_input("Enter the problem statement:", "")

if st.button("Generate Code"):
    if user_input.strip():
        with st.spinner("Generating code Please Wait..."):
            response = DevCrew().crew().kickoff(inputs={"problem": user_input})

        if response:  # Move the check outside the spinner block
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




st.sidebar.title("Description:")
st.sidebar.info(
    """
    Welcome to Muhammad Ubaid CODEGEN – a cutting-edge AI-powered Python Code Generator Agent designed to simplify your coding needs. This intelligent agent leverages Crew AI with Gemini Flash 2.0 to generate high-quality Python code based on your problem statements.

🔹 How It Works:

1-Enter a Problem Statement – Provide a coding problem or requirement.

2-AI-Powered Code Generation – The system processes your request with two specialized AI agents:

    👨‍💻 Junior Developer 
    (5 years of experience)
    – Generates the initial 
      code.

    👨‍🏫 Senior Developer 
    (20 years of experience) 
    – Reviews and refines the
      code to ensure quality.

3-Instant Output & Download – View the generated code instantly and download it as a response.py file for further use.

🚀 Features:

✅ Supports Object-Oriented Programming & Error Handling

✅ Handles a variety of Python tasks – from basic functions to complex applications

✅ Includes Junior & Senior Developer AI Agents for writing and reviewing code

✅ Displays suggested queries for quick inspiration

Start coding smarter with AI! 🚀
    """
)

