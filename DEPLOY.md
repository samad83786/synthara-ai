# Deploy Synthara to Railway

## Prerequisites
1. A [Railway](https://railway.app) account
2. [Railway CLI](https://docs.railway.app/develop/cli) installed
3. A free LLM API key (Groq gives 30K requests/day free)
4. A [GitHub](https://github.com) account

## One-Command Deploy

```bash
# 1. Clone and set up
git add .
git commit -m "Initial commit"
git push origin main

# 2. Deploy backend
cd backend
railway up

# 3. Set environment variables in Railway dashboard:
#    SYNTHARA_API_TYPE=openai
#    SYNTHARA_OPENAI_KEY=gsk_your_key
#    SYNTHARA_OPENAI_BASE=https://api.groq.com/openai/v1
#    SYNTHARA_ORCHESTRATOR_MODEL=mixtral-8x7b-32768
#    SYNTHARA_WORKER_MODEL=mixtral-8x7b-32768
#    SYNTHARA_WALLET=your_solana_wallet

# 4. Deploy frontend
cd ../frontend
railway up
```

## Or Deploy with the Deploy Script

```powershell
# Windows
.\deploy.ps1
```
