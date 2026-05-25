import secrets
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from agent_creator.creator import create_agent as create_agent_file
from agent_creator.agent_registry import list_agents as list_agent_files, delete_agent as delete_agent_file
from agent_creator.subagent import call_agent
from agent_creator.config import ADMIN_API_KEY, ADMIN_EMAIL
from database import (
    create_user, get_user_by_api_key, get_user, save_agent_to_db,
    get_user_agents, get_agent, record_usage, deduct_credits, add_credits,
    get_all_users, get_all_agents, get_all_usage, get_all_payments, get_total_stats
)

router = APIRouter()

class CreateAgentRequest(BaseModel):
    name: str
    description: str = ""
    system_prompt: str = ""
    model: str = ""

class ChatRequest(BaseModel):
    message: str
    agent_id: int

class SignupRequest(BaseModel):
    email: str

class TopUpRequest(BaseModel):
    amount: float
    tx_signature: str = ""

async def require_user(x_api_key: str = Header(...)):
    user = get_user_by_api_key(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user

@router.post("/auth/signup")
def signup(req: SignupRequest):
    existing = get_user(req.email)
    if existing:
        return {"api_key": existing["api_key"], "credits": existing["credits"]}
    api_key = f"sk-{secrets.token_hex(24)}"
    user_id = create_user(req.email, api_key)
    if not user_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"api_key": api_key, "credits": 1.0}

@router.post("/agents")
def create_agent_route(req: CreateAgentRequest, user=Depends(require_user)):
    if not req.system_prompt and not req.description:
        raise HTTPException(status_code=400, detail="description or system_prompt required")
    result = create_agent_file(req.name, req.description, req.system_prompt, req.model or None)
    agent_id = save_agent_to_db(
        user["id"], result["name"], req.description,
        result["system_prompt"], result["model"]
    )
    return {"id": agent_id, **result}

@router.get("/agents")
def list_agents_route(user=Depends(require_user)):
    agents = get_user_agents(user["id"])
    return {"agents": agents}

@router.post("/agents/{agent_id}/chat")
def chat_with_agent(agent_id: int, req: ChatRequest, user=Depends(require_user)):
    agent = get_agent(agent_id)
    if not agent or agent["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits. Top up with SOL.")
    response = call_agent(agent["name"], req.message, agent["model"])
    cost = 0.01
    record_usage(user["id"], agent_id, 0, 0, cost)
    deduct_credits(user["id"], cost)
    return {"response": response}

@router.get("/usage")
def get_usage(user=Depends(require_user)):
    from database import get_db
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM usage WHERE user_id = ? ORDER BY created_at DESC LIMIT 100",
        (user["id"],)
    ).fetchall()
    conn.close()
    return {"usage": [dict(r) for r in rows]}

@router.get("/credits")
def get_credits(user=Depends(require_user)):
    return {"credits": user["credits"]}

@router.post("/credits/topup")
def top_up_credits(req: TopUpRequest, user=Depends(require_user)):
    add_credits(user["id"], req.amount, req.tx_signature or None)
    return {"credits": user["credits"] + req.amount}

@router.get("/wallet")
def get_wallet():
    from agent_creator.config import SYNTHARA_WALLET
    return {"wallet": SYNTHARA_WALLET}

@router.post("/credits/verify-deposit")
def verify_deposit(req: TopUpRequest, user=Depends(require_user)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    add_credits(user["id"], req.amount, req.tx_signature or None)
    from database import get_user_by_id
    u = get_user_by_id(user["id"])
    return {"credits": u["credits"], "message": f"{req.amount} credits added"}

# --- Admin Routes ---
def require_admin(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return True

@router.get("/admin/stats")
def admin_stats(_=Depends(require_admin)):
    return get_total_stats()

@router.get("/admin/users")
def admin_users(_=Depends(require_admin)):
    return {"users": get_all_users()}

@router.get("/admin/agents")
def admin_agents(_=Depends(require_admin)):
    return {"agents": get_all_agents()}

@router.get("/admin/usage")
def admin_usage(_=Depends(require_admin)):
    return {"usage": get_all_usage()}

@router.get("/admin/payments")
def admin_payments(_=Depends(require_admin)):
    return {"payments": get_all_payments()}

@router.post("/admin/credits/set")
def admin_set_credits(user_id: int, credits: float, _=Depends(require_admin)):
    from database import get_db
    conn = get_db()
    conn.execute("UPDATE users SET credits = ? WHERE id = ?", (credits, user_id))
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} credits set to {credits}"}
