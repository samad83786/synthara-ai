import os
import json
import httpx
from .config import ORCHESTRATOR_MODEL, WORKER_MODEL

API_TYPE = os.environ.get("SYNTHARA_API_TYPE", "ollama")
OPENAI_BASE = os.environ.get("SYNTHARA_OPENAI_BASE", "https://api.groq.com/openai/v1")
OPENAI_KEY = os.environ.get("SYNTHARA_OPENAI_KEY", "")

class LLMClient:
    def __init__(self):
        self.api_type = API_TYPE
        self.ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")

    def generate(self, model, prompt, system=None):
        try:
            if self.api_type == "openai":
                return self._generate_openai(model, prompt, system)
            return self._generate_ollama(model, prompt, system)
        except Exception as e:
            return f"[Error: {e}]"

    def _generate_ollama(self, model, prompt, system=None):
        payload = {"model": model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        resp = httpx.post(
            f"{self.ollama_url}/api/generate",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"]

    def _generate_openai(self, model, prompt, system=None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = httpx.post(
            f"{OPENAI_BASE}/chat/completions",
            json={"model": model, "messages": messages},
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json",
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def ask_orchestrator(self, prompt, system=None):
        return self.generate(ORCHESTRATOR_MODEL, prompt, system)

    def ask_worker(self, prompt, system=None):
        return self.generate(WORKER_MODEL, prompt, system)

llm = LLMClient()
