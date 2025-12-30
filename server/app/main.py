import json
import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from app.models import Target
from app.checks import check_target

load_dotenv()

app = FastAPI(title="Status Ping Server")

TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", 3))

BASE_DIR = os.path.dirname(__file__)
TARGETS_FILE = os.path.join(BASE_DIR, "../targets.json")

@app.get("/status")
async def get_status():
    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets = [Target(**t) for t in json.load(f)]

    # הרץ את הבדיקות במקביל לכל ה-targets
    results = await asyncio.gather(*(check_target(t, TIMEOUT) for t in targets))

    return results
