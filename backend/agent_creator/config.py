import os

ORCHESTRATOR_MODEL = os.environ.get("SYNTHARA_ORCHESTRATOR_MODEL", "qwen3:4b")
WORKER_MODEL = os.environ.get("SYNTHARA_WORKER_MODEL", "qwen3:4b")
AGENTS_DIR = os.environ.get("SYNTHARA_AGENTS_DIR", "workspace")
DATABASE_URL = os.environ.get("SYNTHARA_DATABASE_URL", "sqlite:///synthara.db")
SECRET_KEY = os.environ.get("SYNTHARA_SECRET_KEY", "change-me-in-production")
API_KEY = os.environ.get("SYNTHARA_API_KEY", "sk-synthara-dev")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
SYNTHARA_WALLET = os.environ.get("SYNTHARA_WALLET", "Af1RxSsw14AocinFTa4T3PkY9nm5MiK5trZ5ZtgfMLaV")
ADMIN_API_KEY = os.environ.get("SYNTHARA_ADMIN_KEY", "sk-admin-synthara-root")
ADMIN_EMAIL = os.environ.get("SYNTHARA_ADMIN_EMAIL", "admin@synthara.ai")
