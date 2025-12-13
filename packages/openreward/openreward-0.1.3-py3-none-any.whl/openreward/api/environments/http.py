import asyncio, aiohttp
import json as json_lib
from typing import Any, Optional, AsyncGenerator, Tuple, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from logging import getLogger

logger = getLogger("matrix-client")

def _is_retryable_http_error(exception: BaseException) -> bool:
    if isinstance(exception, (aiohttp.ClientError, asyncio.TimeoutError)):
        return True
    if isinstance(exception, aiohttp.ClientResponseError):
        return exception.status >= 500
    return False

@retry(
    retry=retry_if_exception(_is_retryable_http_error),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def request_retryable(
    client: aiohttp.ClientSession,
    method: str,
    path: str,
    expect_json: bool,
    token: str | None,
    json: dict[str, Any] | None = None,
    sid: str | None = None,
    deployment: str | None = None,
) -> Any:
    headers: dict[str, str] = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-API-Key"] = token
    if sid:
        headers["X-Session-ID"] = sid
    if deployment:
        headers["X-Deployment"] = deployment

    async with client.request(method, path, headers=headers, json=json) as response:
        text = await response.text()  # read body first
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise aiohttp.ClientResponseError(
                request_info=e.request_info,
                history=e.history,
                status=e.status,
                message=text,
                headers=e.headers,
            )
        return await response.json() if expect_json else None

class HeartbeatTimeoutError(Exception):
    pass

class MaxRetriesError(Exception):
    pass

async def _parse_sse_events(
    response: aiohttp.ClientResponse,
) -> AsyncGenerator[Tuple[str, str], None]:
    """Parses an aiohttp response stream and yields SSE events."""
    event = None
    data_lines: list[str] = []
    async for raw_line in response.content:
        line = raw_line.decode("utf-8", "ignore").rstrip("\r\n")

        if not line:
            if event:
                yield event, "\n".join(data_lines)
            event = None
            data_lines = []
            continue

        if line.startswith(":"):
            continue

        field, value = line.split(":", 1)
        value = value.lstrip()

        if field == "event":
            event = value
        elif field == "data":
            data_lines.append(value)

# The simplified main function
async def resumable_sse(
    client: aiohttp.ClientSession,
    path: str,
    token: str | None,
    *,
    json: Optional[Dict[str, Any]] = None,
    sid: Optional[str] = None,
    deployment: Optional[str] = None,
    task_id: Optional[str] = None,
    max_retries: Optional[int] = None,
    backoff_base: float = 0.5,
    backoff_max: float = 10.0,
    timeout: Optional[float] = None,
    heartbeat_timeout: int = 30
) -> Any:

    client_timeout = aiohttp.ClientTimeout(total=None, sock_read=heartbeat_timeout)
    payload = dict(json or {})
    headers: dict[str, str] = {
        "Accept": "text/event-stream"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if sid:
        headers["X-Session-ID"] = sid
    if deployment:
        headers["X-Deployment"] = deployment

    async def _execute_with_retries():
        nonlocal task_id, payload
        attempt = 0
        while True:
            if task_id:
                payload["task_id"] = task_id

            try:
                async with client.post(path, headers=headers, json=payload, timeout=client_timeout) as resp:
                    resp.raise_for_status()
                    attempt = 0

                    chunks = []
                    async for event, data in _parse_sse_events(resp):
                        if event == "task_id":
                            task_id = data.strip()
                        elif event == "chunk":
                            chunks.append(data)
                        elif event == "end":
                            chunks.append(data)
                            final_result = "".join(chunks)
                            return json_lib.loads(final_result)
                        elif event == "error":
                            raise RuntimeError(data or "Unknown SSE error")

                    raise aiohttp.ClientPayloadError("Stream ended unexpectedly")

            except aiohttp.ClientResponseError as e:
                if e.status < 500:
                    raise e

            except aiohttp.ClientError as e:
                logger.warning(f"Client error: {e}")
                pass

            except RuntimeError as e:
                raise e

            except asyncio.TimeoutError:
                raise HeartbeatTimeoutError()

            attempt += 1
            if max_retries is not None and attempt > max_retries:
                raise MaxRetriesError("Exceeded max retries for a retryable error.")

            delay = min(backoff_max, backoff_base * (2 ** (attempt - 1)))
            await asyncio.sleep(delay)


    try:
        return await asyncio.wait_for(_execute_with_retries(), timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Total operation timed out after {timeout} seconds.") from None