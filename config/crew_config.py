import os

# Turn off CrewAI telemetry (avoids slow start-up / network noise on Streamlit Cloud)
os.environ["OTEL_SDK_DISABLED"] = "true"

import streamlit as st
from crewai import Crew, Process, LLM
from agents.hse_analyst import create_hse_analyst, create_hse_analysis_task
from agents.risk_action import create_risk_action_agent, create_risk_task
from agents.security_alert import create_security_alert_agent, create_alert_task


def get_groq_llm():
    """Reads the Groq API key from Streamlit Secrets and returns a CrewAI LLM."""
    api_key = None
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        # No secrets file or key not found -> try environment variable instead
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API Key missing! Please add GROQ_API_KEY to Streamlit Secrets.")
        st.stop()

    # LiteLLM (used by CrewAI for Groq) reads the key from this environment variable
    os.environ["GROQ_API_KEY"] = api_key

    return LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0.2,
    )


def run_hse_crew(event_data):
    """Executes 3 CrewAI agents in sequence for event analysis."""
    llm = get_groq_llm()

    # 1. Create the agents
    analyst = create_hse_analyst(llm)
    risk_agent = create_risk_action_agent(llm)
    alert_agent = create_security_alert_agent(llm)

    # 2. Create the tasks
    task1 = create_hse_analysis_task(analyst, event_data)
    task2 = create_risk_task(risk_agent, event_data)
    task3 = create_alert_task(
        alert_agent,
        event_data["camera"],
        event_data["location"],
        event_data["timestamp"],
    )

    # 3. Run the crew
    crew = Crew(
        agents=[analyst, risk_agent, alert_agent],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    raw_output = str(result)

    if "High" in raw_output:
        severity = "High"
    elif "Medium" in raw_output:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "analysis_summary": raw_output,
        "severity": severity,
        "action": "Security to verify evidence and dispatch floor supervisor if confirmed.",
    }
