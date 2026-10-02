from crewai import Agent, Task

def create_security_alert_agent(llm):
    agent = Agent(
        role="Security Control Room Alert Dispatcher",
        goal="Synthesize analysis into a clear, standardized Control Room alert.",
        backstory="You format critical safety alerts for rapid decision-making by human operators.",
        llm=llm,
        verbose=False
    )
    return agent

def create_alert_task(agent, camera, location, timestamp):
    return Task(
        description=(
            f"Synthesize the prior agent outputs into a standardized Security Alert for:\n"
            f"Camera: {camera} | Location: {location} | Time: {timestamp}\n\n"
            f"Format response explicitly as:\n"
            f"Violation: <Short Summary>\n"
            f"Severity: <Low/Medium/High>\n"
            f"Action: <Immediate Step>"
        ),
        expected_output="Formatted summary containing Violation, Severity, and Action.",
        agent=agent
    )
