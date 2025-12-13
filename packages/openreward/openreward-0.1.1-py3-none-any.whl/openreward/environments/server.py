import inspect, traceback, logging, uvicorn, asyncio, time, base64
from typing import Union, cast
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.routing import APIRoute
from sse_starlette import EventSourceResponse
from contextlib import asynccontextmanager, suppress

from .environment import Environment
from .utils import maybe_await
from .types import CreateSession, JSONValue, RunToolError, RunToolOutput, RunToolSuccess, ToolCall, Blocks
from .reconnect import sse_task_stream

def _get_env_map(environments: list[type[Environment]]) -> dict[str, type[Environment]]:
    env_map = {}
    for env in environments:
        cls = env if inspect.isclass(env) else env.__class__
        if not issubclass(cls, Environment):
            raise TypeError(f"{cls!r} is not Environment")
        key = cls.__name__.lower()
        if key in env_map:
            raise ValueError(f"duplicate env {key}")
        env_map[key] = cls
    return env_map

def _get_env_cls(env_map: dict[str, type[Environment]], env_name: str) -> type[Environment]:
    env_cls = env_map.get(env_name.lower())
    if env_cls is None:
        raise HTTPException(404, f"unknown environment {env_name!r}")
    return env_cls

async def extract_sid(request: Request) -> str:
    x_session_id = request.headers.get("X-Session-ID")
    if not x_session_id:
        raise HTTPException(400, "X-Session-ID header is required")
    return x_session_id.strip()

class _LoggingRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()
        async def handler(request: Request):
            try:
                return await original(request)
            except Exception as exc:
                logging.exception(f"{request.method} {str(request.url)}", exc_info=exc)
                raise
        return handler

async def _delete_session(
    sid: str,
    active_envs: dict[str, Environment | None],
    last_ping: dict[str, float],
    setup_tasks: dict[str, asyncio.Task],
    ready: dict[str, asyncio.Event],
    setup_errors: dict[str, Exception],
):
    last_ping.pop(sid, None) # stop TTL

    task = setup_tasks.pop(sid, None) # cancel setup if it's running
    if task and not task.done():
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    evt = ready.get(sid) # set error for waiters
    if evt and not evt.is_set():
        setup_errors[sid] = HTTPException(410, "Session deleted")
        evt.set()
    ready.pop(sid, None)

    env = active_envs.pop(sid, None) # teardown env
    if env:
        try:
            await maybe_await(env.teardown())
        except Exception:
            logging.exception("teardown failed for %s", sid)

    setup_errors.pop(sid, None) # clear error for waiters

class Server:
    def __init__(self, environments: list[type[Environment]]) -> None:
        self._env_classes: dict[str, type[Environment]] = _get_env_map(environments)
        self._active_envs: dict[str, Environment | None] = {}
        self._last_ping: dict[str, float] = {}
        
        self._setup_tasks: dict[str, asyncio.Task] = {}
        self._ready: dict[str, asyncio.Event] = {}
        self._setup_errors: dict[str, Exception] = {}

        self._reaper_task: asyncio.Task | None = None

        async def await_environment_ready(sid: str) -> Environment:
            evt = self._ready.get(sid)
            if evt is None:
                raise HTTPException(404, "Active environment not found")

            if evt.is_set(): # fast path
                err = self._setup_errors.get(sid)
                if err:
                    raise err
                env = self._active_envs.get(sid)
                if env is None:
                    raise HTTPException(410, "Session deleted")
                return env

            await evt.wait()
            err = self._setup_errors.get(sid, None)
            if err:
                raise err
            env = self._active_envs.get(sid)
            if env is None:
                raise HTTPException(410, "Session deleted")
            return env

        async def reaper_coro(reaper_interval: float=5, stale_threshold: float=900):
            while True:
                await asyncio.sleep(reaper_interval)
                now = time.monotonic()
                stale = [sid for sid, ts in list(self._last_ping.items()) if now - ts > stale_threshold]
                for sid in stale:
                    await _delete_session(
                        sid,
                        self._active_envs,
                        self._last_ping,
                        self._setup_tasks,
                        self._ready,
                        self._setup_errors,
                    )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            self._reaper_task = asyncio.create_task(reaper_coro())
            yield
            if self._reaper_task:
                self._reaper_task.cancel()
                try:
                    await self._reaper_task
                except asyncio.CancelledError:
                    pass

        app = FastAPI(lifespan=lifespan)
        app.router.route_class = _LoggingRoute

        @app.exception_handler(Exception)
        async def unhandled_exception_handler(request: Request, exc: Exception):
            logging.exception(traceback.format_exc())
            raise HTTPException(500, "Internal server error")

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        @app.post("/ping")
        async def ping(sid: str = Depends(extract_sid)):
            if sid not in self._active_envs:
                raise HTTPException(404, "Active environment not found")
            self._last_ping[sid] = time.monotonic()
            return {"status": "ok"}

        @app.get("/list_environments")
        async def get_envs():
            return list(self._env_classes.keys())

        @app.get("/{env_name}/tools")
        async def get_tools(env_name: str):
            env_cls = _get_env_cls(self._env_classes, env_name)
            return env_cls.get_tools().model_dump()

        @app.get("/{env_name}/splits")
        async def get_splits(env_name: str):
            env_cls = _get_env_cls(self._env_classes, env_name)
            return env_cls.get_splits()

        @app.post("/{env_name}/tasks")
        async def get_tasks(env_name: str, request: Request):
            env_cls = _get_env_cls(self._env_classes, env_name)
            body = await request.json()
            split = body.get("split", "")
            return {"tasks": env_cls.get_tasks(split)}
        
        @app.post("/create")
        async def create_environment(create_session: CreateSession, sid: str = Depends(extract_sid)):
            if sid in self._active_envs:
                raise HTTPException(status_code=400, detail="Session already exists")

            self._active_envs[sid] = None
            self._last_ping[sid] = time.monotonic()
            self._ready[sid] = asyncio.Event()

            async def perform_setup():
                try:
                    env_cls = _get_env_cls(self._env_classes, create_session.env_name)
                    env = env_cls(task_spec=create_session.task_spec)
                    await maybe_await(env.setup())
                    self._active_envs[sid] = env
                except Exception as e:
                    self._setup_errors[sid] = e
                finally:
                    self._ready[sid].set()

            if sid not in self._setup_tasks:
                self._setup_tasks[sid] = asyncio.create_task(perform_setup())

            return {"sid": sid}

        async def require_existing_session(
            sid: str = Depends(extract_sid),
        ):
            self._last_ping[sid] = time.monotonic()
            return await await_environment_ready(sid)


        @app.post("/delete")
        async def delete_environment(sid: str = Depends(extract_sid)):
            if sid not in self._setup_tasks:
                raise HTTPException(404, "Active environment not found")
            await _delete_session(
                sid, 
                self._active_envs, 
                self._last_ping,
                self._setup_tasks,
                self._ready,
                self._setup_errors,
            )
            return {"sid": sid}

        @app.post("/{env_name}/call")
        async def call_tool(request: Request, tool_call: ToolCall, env: Environment = Depends(require_existing_session)):
            async def call_tool_coro():
                res = await env._call_tool(tool_call.name, tool_call.input)
                return res.model_dump_json(indent=None)
            
            return EventSourceResponse(
                sse_task_stream(
                    lambda: call_tool_coro(),
                    request,
                    task_id=tool_call.task_id,
                ),
                ping=10,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )

        @app.get("/{env_name}/prompt")
        async def get_prompt(request: Request, env: Environment = Depends(require_existing_session)) -> Blocks:
            return (await maybe_await(env.get_prompt()))

        self.app = app

    def run(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        uvicorn.run(self.app, host=host, port=port)