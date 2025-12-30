from fastapi import FastAPI
import json
import os
from app.models import Target
from app.checks import check_all

app = FastAPI(title="Status Ping Server")

TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", 3))

BASE_DIR = os.path.dirname(__file__)
TARGETS_FILE = os.path.join(BASE_DIR, "../targets.json")

def load_targets(category: str) -> list[Target]:
    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        all_targets = [Target(**t) for t in json.load(f)]
    return [t for t in all_targets if t.category == category]

@app.get("/status/vApp")
async def get_vApp_status():
    targets = load_targets("vApp")
    results = await check_all(targets, TIMEOUT)
    return results

@app.get("/status/fApp")
async def get_fApp_status():
    targets = load_targets("fApp")
    results = await check_all(targets, TIMEOUT)
    return results
