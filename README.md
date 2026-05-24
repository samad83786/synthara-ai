# Synthara

**Describe an AI agent. We build it. Deploy it. Pay with crypto.**

Synthara is an open-source AI agent platform. You describe what you want an agent to do in plain English, and Synthara generates the agent — complete with system prompt, model config, and a chat interface.

## ✨ Features

- **Create agents with natural language** — "Make an agent that researches competitors" → instant agent
- **Chat with your agents** — deployed and ready in seconds
- **6 pre-built agents** — Researcher, Investigator, Coder, Artist, Coach, ImageGen
- **Multi-provider AI** — Ollama (local) or any OpenAI-compatible API (Groq free tier, Together, etc.)
- **Credit system** — prepay with crypto, pay per API call
- **Solana payments** — no bank account needed

## 🚀 Quick Start

### 1. Run locally

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### 2. Get a free AI API key

```bash
# Get free key from Groq (30K requests/day)
# https://console.groq.com

# Set it as env var:
SYNTHARA_API_TYPE=openai
SYNTHARA_OPENAI_KEY=gsk_your_key
SYNTHARA_OPENAI_BASE=https://api.groq.com/openai/v1
SYNTHARA_ORCHESTRATOR_MODEL=mixtral-8x7b-32768
SYNTHARA_WORKER_MODEL=mixtral-8x7b-32768
```

### 3. Deploy to the cloud

```bash
# Push to GitHub → deploy to Railway in one command
.\deploy.ps1
```

## 🧠 Architecture

```
User describes agent  →  Synthara API generates system prompt  →  Agent deployed
                                                                    ↓
User chats with agent  ←  Synthara routes to best AI provider  ←  Agent ready
```

## 📦 API

```bash
# Sign up — get your API key
POST /api/v1/auth/signup
{"email": "user@example.com"}
→ {"api_key": "sk-...", "credits": 1.0}

# Create an agent
POST /api/v1/agents
{"name": "Researcher", "description": "Deep research agent"}

# Chat with your agent
POST /api/v1/agents/1/chat
{"message": "Research quantum computing"}

# Check credits
GET /api/v1/credits

# Get wallet address for top-up
GET /api/v1/wallet
```

## 💰 Revenue Model

| Plan | Price | Agents | Calls/mo |
|------|-------|--------|----------|
| Free | 1 SOL one-time | 3 | 100 |
| Pro | 5 SOL/mo | 50 | 10,000 |
| Unlimited | 20 SOL/mo | Unlimited | Unlimited |

(1 SOL ≈ $150 — prices adjust with market)

## 🔧 Configuration

See [CONFIG.md](CONFIG.md) for all options.

## 🗺️ Roadmap

- ✓ Agent creation from description
- ✓ Chat with agents
- ✓ Credit system
- ✓ Solana crypto payments
- ✓ 6 pre-built agent templates
- Multi-provider smart routing
- Agent marketplace
- Team collaboration
- One-click deploy templates

## 🏗️ Built With

- **Backend:** FastAPI, SQLite, httpx
- **Frontend:** React, Vite, TypeScript
- **AI:** Ollama, Groq, OpenAI-compatible APIs
- **Payments:** Solana blockchain
- **Infra:** Docker, Railway, GitHub Actions

## 📄 License

MIT
