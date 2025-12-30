from fastapi import FastAPI
import json
import os
from app.models import Target
from app.checks import check_all_targets

app = FastAPI(title="Status Ping Server")

TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", 3))

BASE_DIR = os.path.dirname(__file__)

def load_targets_from_file(filename: str) -> list[Target]:
    with open(filename, "r", encoding="utf-8") as f:
        return [Target(**t) for t in json.load(f)]

@app.get("/status/vapp")
async def get_vapp_status():
    targets = load_targets_from_file(
        os.path.join(BASE_DIR, "../targets/vapp.json")
    )
    return await check_all_targets(targets, TIMEOUT)

@app.get("/status/fapp")
async def get_fapp_status():
    targets = load_targets_from_file(
        os.path.join(BASE_DIR, "../targets/fapp.json")
    )
    return await check_all_targets(targets, TIMEOUT)
