import time
import httpx
import asyncio      
from .models import Target, Status

async def check_target(target: Target, timeout: int) -> Status:
    start = time.time()

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(target.url)
            latency = int((time.time() - start) * 1000)

            return Status(
                name=target.name,
                url=target.url,
                status="UP" if response.status_code < 400 else "DOWN",
                latency=latency
            )
    except Exception:
        return Status(
            name=target.name,
            url=target.url,
            status="DOWN",
            latency=None
        )

async def check_all(targets: list[Target], timeout: int):
    return await asyncio.gather(*(check_target(t, timeout) for t in targets))
