import asyncio
import logging
from multiprocessing.managers import DictProxy
from queue import Empty
import time
from dataclasses import dataclass
import multiprocessing as mp
import traceback
from typing import Callable, Literal

import aiohttp
from .http import request_retryable

@dataclass
class StartPingRequest:
    type: Literal["start_ping"]
    task_id: str
    url: str
    deployment: str
    session_id: str
    api_key: str | None
    sleep_time: float

@dataclass
class StartPingResponse:
    type: Literal["start_ping"]

@dataclass
class StopPingRequest:
    type: Literal["stop_ping"]
    task_id: str

@dataclass
class StopPingResponse:
    type: Literal["stop_ping"]

@dataclass
class ShutdownRequest:
    type: Literal["shutdown"]
    id: str

@dataclass
class ErrorResponse:
    type: Literal["error"]
    message: str

Request = (
    StartPingRequest |
    StopPingRequest |
    ShutdownRequest
)

Response = (
    StartPingResponse |
    StopPingResponse |
    ErrorResponse
)

async def ping(url: str, deployment: str, session_id: str, api_key: str | None, sleep_time: float, client: aiohttp.ClientSession) -> None:
    while True:
        start = time.monotonic()
        await request_retryable(
            client,
            "POST",
            url,
            deployment=deployment,
            sid=session_id,
            expect_json=False,
            token=api_key,
        )
        elapsed = time.monotonic() - start
        delay = max(0, sleep_time - elapsed)
        await asyncio.sleep(delay)

async def ping_worker_loop_(request_queue: mp.Queue, response_dict: DictProxy) -> None:

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("matrix:ping_worker_loop")

    ping_tasks: dict[str, asyncio.Task[None]] = {}
    connector = aiohttp.TCPConnector(limit=1_000_000)
    
    async with aiohttp.ClientSession(connector=connector) as client:
        while True:
            try:
                try:
                    req: Request = request_queue.get_nowait()
                except Empty:
                    await asyncio.sleep(0.01)
                    continue

                if req.type == "start_ping":
                    if req.task_id in ping_tasks:
                        logger.warning(f"Received duplicate task {req.task_id} for ping")
                    else:
                        ping_tasks[req.task_id] = asyncio.create_task(ping(req.url, req.deployment, req.session_id, req.api_key, req.sleep_time, client))
                    response_dict[req.task_id] = StartPingResponse(type="start_ping")
                
                elif req.type == "stop_ping":
                    if req.task_id not in ping_tasks:
                        error_str = f"Cannot delete task {req.task_id}: Unknown ID"
                        logger.error(error_str)
                        response_dict[req.task_id] = ErrorResponse(type="error", message=error_str)
                    else:
                        t = ping_tasks.pop(req.task_id)
                        t.cancel()
                        response_dict[req.task_id] = StopPingResponse(type="stop_ping")
                
                elif req.type == "shutdown":
                    ts = []
                    for k in list(ping_tasks.keys()):
                        t = ping_tasks.pop(k)
                        t.cancel()
                        ts.append(t)
                    await asyncio.gather(*ts)
                    break

            except:
                tb = traceback.format_exc()
                logger.error(f"Unhandled exception in worker loop:\n{tb}")

def ping_worker_loop(request_queue: mp.Queue, response_dict: DictProxy) -> None:
    asyncio.run(ping_worker_loop_(request_queue, response_dict))

class PingManager:

    def __init__(self) -> None:

        self.request_queue = mp.Queue()
        self.response_dict = mp.Manager().dict()
        self.proc = mp.Process(target=ping_worker_loop, args=(self.request_queue, self.response_dict), daemon=True)
        self.proc.start()

    async def get_response(self, req_id: str, timeout: float | None = None, sleep_interval: float = 0.01) -> Response:
        t0 = time.perf_counter()
        while True:
            elapsed = time.perf_counter() - t0
            if timeout is not None and elapsed >= timeout:
                break

            if req_id in self.response_dict:
                return self.response_dict.pop(req_id)
            
            await asyncio.sleep(sleep_interval)

        return ErrorResponse(type="error", message=f"Request {req_id} timed out waiting for response")

    async def start_ping(
        self, 
        task_id: str,
        url: str,
        deployment: str,
        session_id: str,
        api_key: str | None,
        sleep_time: float, 
        on_error: Callable[[ErrorResponse], None], 
    ) -> None:
        
        if not self.proc.is_alive(): # restart process if it has terminated
            self.proc = mp.Process(target=ping_worker_loop, args=(self.request_queue, self.response_dict))
            self.proc.start()

        self.request_queue.put_nowait(StartPingRequest(type="start_ping", task_id=task_id, url=url, deployment=deployment, session_id=session_id, api_key=api_key, sleep_time=sleep_time))
        res = await self.get_response(req_id=task_id, timeout=10.0)
        if res.type == "error":
            on_error(res)
        else:
            assert res.type == "start_ping"

    async def stop_ping(self, task_id: str) -> None:
        self.request_queue.put_nowait(StopPingRequest(type="stop_ping", task_id=task_id))
        res = await self.get_response(req_id=task_id, timeout=10.0)
        if res.type == "error":
            raise RuntimeError(f"Failed to stop ping: {res.message}")
        else:
            assert res.type == "stop_ping"

    def shutdown(self) -> None:
        self.request_queue.put(ShutdownRequest(type="shutdown", id="_shutdown"))
        self.proc.join(timeout=1.0)
