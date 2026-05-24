import os
import json
from .config import AGENTS_DIR

os.makedirs(AGENTS_DIR, exist_ok=True)

def save_agent(name, system_prompt, model=None):
    filepath = os.path.join(AGENTS_DIR, f"{name}.json")
    agent_data = {
        "name": name,
        "system_prompt": system_prompt,
        "model": model or "qwen3:latest",
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(agent_data, f, indent=2)
    return {"name": name, "system_prompt": system_prompt, "model": model}

def load_agent(name):
    filepath = os.path.join(AGENTS_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def list_agents():
    os.makedirs(AGENTS_DIR, exist_ok=True)
    agents = []
    for f in os.listdir(AGENTS_DIR):
        if f.endswith(".json"):
            with open(os.path.join(AGENTS_DIR, f), "r", encoding="utf-8") as fh:
                agents.append(json.load(fh))
    return agents

def delete_agent(name):
    filepath = os.path.join(AGENTS_DIR, f"{name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
