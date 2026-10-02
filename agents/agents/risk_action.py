from crewai import Agent, Task

def create_risk_action_agent(llm):
    agent = Agent(
        role="HSE Risk & Action Specialist",
        goal="Assess severity and define mandatory immediate corrective actions.",
        backstory="You are an emergency response supervisor who rapidly triages site risks.",
        llm=llm,
        verbose=False
    )
    return agent

def create_risk_task(agent, event_data):
    return Task(
        description=(
            f"Based on the camera event at '{event_data['location']}' involving rule '{event_data['raw_violation']}', determine:\n"
            f"1. Severity Level: Low, Medium, or High\n"
            f"2. Potential Consequence/Risk\n"
            f"3. Immediate Action required by Security or HSE floor supervisor.\n"
            f"Keep output under 30 words."
        ),
        expected_output="Severity level, main potential risk, and immediate action.",
        agent=agent
    )
