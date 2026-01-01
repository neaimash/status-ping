import time
import httpx
import asyncio
from typing import List, Dict, Any
from .models import Target, Status

async def check_target(
    http_client: httpx.AsyncClient,
    target: Target,
    timeout: int,
    retries: int = 2,
) -> Status:
    for attempt in range(retries):
        start = time.time()
        try:
            response = await http_client.get(target.url, timeout=timeout)
            latency = int((time.time() - start) * 1000)
            if response.status_code < 500:
                return Status(
                    name=target.name,
                    url=target.url,
                    status="UP",
                    latency=latency,
                    critical=target.critical,
                )
        except httpx.RequestError:
            pass  
        if attempt < retries - 1:
            await asyncio.sleep(0.1)

    return Status(
        name=target.name,
        url=target.url,
        status="DOWN",
        latency=None,
        critical=target.critical,
    )

def summarize_results(results: List[Status]) -> Dict[str, Any]:
    failed_services = [r.name for r in results if r.status == "DOWN"]
    failed_critical_services = [r.name for r in results if r.status == "DOWN" and r.critical]
    up_services = [r.name for r in results if r.status == "UP"]
    avg_latency = (
        sum(r.latency for r in results if r.latency is not None) / len(results)
        if results else 0
    )

    if failed_critical_services:
        overall_status = "CRITICAL_FAILURE"
    elif failed_services:
        overall_status = "DEGRADED"
    else:
        overall_status = "ALL_SYSTEMS_OK"

    return {
        "overall_status": overall_status,
        "failed_services": failed_services,
        "failed_critical_services": failed_critical_services,
        "up_services": up_services,
        "average_latency_ms": avg_latency,
    }

async def run_health_checks(targets: List[Target], timeout: int) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *(check_target(client, t, timeout) for t in targets)
        )

    return {**summarize_results(results), "targets": results}
