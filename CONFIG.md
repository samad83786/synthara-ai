# Configuration

## Using a Free AI Provider (Groq)
Get a free API key from https://console.groq.com

```
SYNTHARA_API_TYPE=openai
SYNTHARA_OPENAI_KEY=gsk_your_groq_key
SYNTHARA_OPENAI_BASE=https://api.groq.com/openai/v1
SYNTHARA_ORCHESTRATOR_MODEL=mixtral-8x7b-32768
SYNTHARA_WORKER_MODEL=mixtral-8x7b-32768
```

## Using Local Ollama
```bash
ollama pull qwen3
ollama serve
```

```
SYNTHARA_API_TYPE=ollama
OLLAMA_URL=http://localhost:11434
```

## Using Together AI
```
SYNTHARA_API_TYPE=openai
SYNTHARA_OPENAI_KEY=together_your_key
SYNTHARA_OPENAI_BASE=https://api.together.xyz/v1
SYNTHARA_ORCHESTRATOR_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
```

## Solana Wallet
Set your Solana wallet address in the env var to receive payments:
```
SYNTHARA_WALLET=YourSolanaWalletAddressHere
```
