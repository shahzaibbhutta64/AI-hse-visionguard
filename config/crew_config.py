import os
import time
import functools

# Turn off CrewAI telemetry (avoids slow start-up / network noise on Streamlit Cloud)
os.environ["OTEL_SDK_DISABLED"] = "true"

# ---------------------------------------------------------------------------
# GROQ COMPATIBILITY PATCH
# Some CrewAI versions add a hidden field called "cache_breakpoint" to every
# message. Groq does not know this field and rejects the request.
# This patch removes the field just before the request is sent to Groq.
# It must run BEFORE crewai is imported, so it lives at the top of the file.
# ---------------------------------------------------------------------------
_BAD_KEY = "cache_breakpoint"


def _strip_bad_key(messages):
    """Returns a copy of the message list without the unsupported field."""
    if not isinstance(messages, list):
        return messages
    cleaned = []
    for m in messages:
        if isinstance(m, dict) and _BAD_KEY in m:
            m = {k: v for k, v in m.items() if k != _BAD_KEY}
        cleaned.append(m)
    return cleaned


def _wrap_litellm_function(fn):
    if getattr(fn, "_hse_patched", False):
        return fn  # already patched (Streamlit re-runs the script often)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if "messages" in kwargs:
            kwargs["messages"] = _strip_bad_key(kwargs["messages"])
        elif len(args) > 1:
            args = (args[0], _strip_bad_key(args[1])) + tuple(args[2:])
        return fn(*args, **kwargs)

    wrapper._hse_patched = True
    return wrapper


try:
    import litellm

    litellm.completion = _wrap_litellm_function(litellm.completion)
    if hasattr(litellm, "acompletion"):
        litellm.acompletion = _wrap_litellm_function(litellm.acompletion)
except Exception:
    pass  # if litellm is missing, the normal error message will explain it
# ---------------------------------------------------------------------------

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


def _is_temporary_error(error):
    """True for network / access / timeout problems that are worth retrying."""
    msg = str(error)
    markers = (
        "Access denied",
        "network settings",
        "APIError",
        "Connection",
        "Timeout",
        "timed out",
        "RateLimit",
        "ServiceUnavailable",
    )
    return any(m in msg for m in markers)


def _run_crew_once(llm, event_data):
    """Builds the 3 agents + 3 tasks and runs the crew one time."""
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
    return crew.kickoff()


def run_hse_crew(event_data):
    """Executes 3 CrewAI agents in sequence (same Groq key + same model, with auto-retry)."""
    llm = get_groq_llm()

    MAX_TRIES = 5          # total number of attempts
    WAIT_STEP = 5          # waits 5s, 10s, 15s, 20s between attempts
    last_error = None
    result = None

    for attempt in range(1, MAX_TRIES + 1):
        try:
            result = _run_crew_once(llm, event_data)
            break  # success -> stop retrying
        except Exception as e:
            last_error = e
            if _is_temporary_error(e) and attempt < MAX_TRIES:
                time.sleep(WAIT_STEP * attempt)
                continue
            raise  # different kind of error, or out of tries

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
