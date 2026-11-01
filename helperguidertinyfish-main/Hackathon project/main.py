import os
import uuid
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
KEY = os.getenv("TINYFISH_API_KEY")
if not KEY:
    raise RuntimeError(
        "TINYFISH_API_KEY is missing. Set it in Hackathon project\\.env."
    )
BASE = "https://agent.tinyfish.ai/v1"
H = {"X-API-Key": KEY, "Content-Type": "application/json"}
FRONTEND = Path(__file__).with_name("frontend.html")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
MISSIONS = {}  # swap for a database later

class Mission(BaseModel):
    name: str
    url: str
    goal: str
    output_schema: dict | None = None

@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(FRONTEND)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/missions")
async def launch(m: Mission):
    payload = {"url": m.url, "goal": m.goal}
    if m.output_schema:
        payload["output_schema"] = m.output_schema
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(f"{BASE}/automation/run-async", headers=H, json=payload)
        r.raise_for_status()
        data = r.json()
    mid = str(uuid.uuid4())
    MISSIONS[mid] = {**m.model_dump(), "id": mid,
                     "run_id": data.get("run_id"), "status": "running"}
    return MISSIONS[mid]

@app.get("/missions")
def list_missions():
    return list(MISSIONS.values())

@app.get("/missions/{mid}")
async def status(mid: str):
    m = MISSIONS.get(mid)
    if m is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(f"{BASE}/runs/{m['run_id']}", headers=H)
        r.raise_for_status()
        run = r.json()
    m["status"] = run.get("status", m["status"])
    m["result"] = run.get("result")
    return m

@app.post("/missions/{mid}/abort")
async def abort(mid: str):
    m = MISSIONS.get(mid)
    if m is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(f"{BASE}/runs/{m['run_id']}/cancel", headers=H)
        r.raise_for_status()
    m["status"] = "cancelled"
    return m

@app.post("/missions/stream")
async def live(m: Mission):
    """Proxy TinyFish's SSE stream to the dashboard."""
    async def gen():
        async with httpx.AsyncClient(timeout=None) as c:
            async with c.stream("POST", f"{BASE}/automation/run-sse",
                                headers=H, json={"url": m.url, "goal": m.goal}) as r:
                async for line in r.aiter_lines():
                    if line:
                        yield line + "\n"
    return StreamingResponse(gen(), media_type="text/event-stream")