from crewai import Agent, Task

def create_hse_analyst(llm):
    agent = Agent(
        role="HSE Incident Analyst",
        goal="Analyze detected vision events and categorize the exact safety violation.",
        backstory="You are a certified Health, Safety, and Environment specialist with 15 years of industrial site expertise.",
        llm=llm,
        verbose=False
    )
    return agent

def create_hse_analysis_task(agent, event_data):
    return Task(
        description=(
            f"Analyze the following potential HSE violation raw data:\n"
            f"- Camera: {event_data['camera']}\n"
            f"- Location: {event_data['location']}\n"
            f"- Rule Violated: {event_data['raw_violation']}\n"
            f"- Description: {event_data['description']}\n\n"
            f"Determine:\n"
            f"1. Exact Violation Category (e.g., PPE Non-Compliance, Unsafe Zone Entry, Mechanical Hazard)\n"
            f"2. Primary Workplace Hazard\n"
            f"Respond concisely in 2 sentences."
        ),
        expected_output="Concise summary of violation category and main workplace hazard.",
        agent=agent
    )
