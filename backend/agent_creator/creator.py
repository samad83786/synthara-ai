from .llm import llm
from .agent_registry import save_agent
from .config import WORKER_MODEL

def generate_agent_system_prompt(name, description):
    prompt = f"""Create a system prompt for an AI agent with these specifications:

Name: {name}
Purpose: {description}

The system prompt should:
1. Define the agent's role clearly
2. Specify its expertise and capabilities
3. Set behavioral guidelines
4. Include output format preferences if relevant

Return ONLY the system prompt text, nothing else."""

    system_prompt = llm.ask_orchestrator(
        prompt,
        system="You are an expert at crafting effective AI system prompts."
    )
    return system_prompt.strip()

def create_agent(name, description=None, system_prompt=None, model=None):
    if not system_prompt and description:
        system_prompt = generate_agent_system_prompt(name, description)
    if not model:
        model = WORKER_MODEL
    return save_agent(name, system_prompt, model)
