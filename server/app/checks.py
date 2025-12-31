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
                status="UP" if response.status_code < 499 else "DOWN",
                latency=latency,
                critical=target.critical
            )

    except Exception:
        return Status(
            name=target.name,
            url=target.url,
            status="DOWN",
            latency=None,
            critical=target.critical
        )

async def check_all_targets(targets: list[Target], timeout: int):
    results: list[Status] = await asyncio.gather(
        *(check_target(t, timeout) for t in targets)
    )

    has_critical_down = any(
        r.status == "DOWN" and r.critical
        for r in results
    )

    overall_status = (
        "CRITICAL_FAILURE"
        if has_critical_down
        else "ALL_SYSTEMS_OK"
    )

    return {
        "overall_status": overall_status,
        "targets": results
    }
