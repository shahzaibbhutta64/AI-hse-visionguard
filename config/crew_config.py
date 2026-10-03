import os
import streamlit as st
from crewai import Crew, Process
from langchain_groq import ChatGroq
from agents.hse_analyst import create_hse_analyst, create_hse_analysis_task
from agents.risk_action import create_risk_action_agent, create_risk_task
from agents.security_alert import create_security_alert_agent, create_alert_task

def get_groq_llm():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API Key missing! Please add GROQ_API_KEY to Streamlit Secrets.")
        st.stop()
        
    # Directly initialize ChatGroq using developer plan model
    return ChatGroq(
        api_key=api_key,
        model_name="openai/gpt-oss-20b",
        temperature=0.2
    )

def run_hse_crew(event_data):
    """Executes 3 CrewAI agents in sequence for event analysis."""
    llm = get_groq_llm()
    
    # 1. Instantiate Agents
    analyst = create_hse_analyst(llm)
    risk_agent = create_risk_action_agent(llm)
    alert_agent = create_security_alert_agent(llm)
    
    # 2. Instantiate Tasks
    task1 = create_hse_analysis_task(analyst, event_data)
    task2 = create_risk_task(risk_agent, event_data)
    task3 = create_alert_task(alert_agent, event_data["camera"], event_data["location"], event_data["timestamp"])
    
    # 3. Execute Crew
    crew = Crew(
        agents=[analyst, risk_agent, alert_agent],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=False
    )
    
    result = crew.kickoff()
    raw_output = str(result)
    
    severity = "High" if "High" in raw_output else ("Medium" if "Medium" in raw_output else "Low")
    
    return {
        "analysis_summary": raw_output,
        "severity": severity,
        "action": "Security to verify evidence and dispatch floor supervisor if confirmed."
    }
