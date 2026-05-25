from .llm import llm
from .agent_registry import load_agent

def call_agent(agent_name, task, model_override=None):
    agent = load_agent(agent_name)
    if not agent:
        return f"[Error] Agent '{agent_name}' not found."
    model = model_override or agent["model"]
    return llm.generate(model, task, system=agent["system_prompt"])

def call_with_prompt(model, system_prompt, task):
    return llm.generate(model, task, system=system_prompt)
