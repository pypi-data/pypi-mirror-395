import pytest
import asyncio
import uvicorn
import aiohttp
from threading import Thread
from typing import Generator

from openreward import OpenReward
from openreward.environments import Environment, Server, tool, ToolOutput
from openreward.environments.types import Blocks, TextBlock, JSONObject


class Foo(Environment):
    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text=str(self.task_spec["foo"]))]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "train"
        return [{"foo": "bar"}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="baz")], reward=1.0, finished=True)


async def wait_for_server(base_url: str, timeout: float = 5.0):
    """Wait for server to be ready using aiohttp."""
    import time
    start = time.monotonic()
    async with aiohttp.ClientSession() as session:
        while time.monotonic() - start < timeout:
            try:
                async with session.get(f"{base_url}/health", timeout=aiohttp.ClientTimeout(total=0.5)) as resp:
                    if resp.status == 200:
                        return
            except Exception:
                pass
            await asyncio.sleep(0.1)
    pytest.fail("Server failed to start")


@pytest.fixture(scope="module")
def server() -> Generator[str, None, None]:
    """Start the server in a background thread and yield the base URL."""
    host = "localhost"
    port = 8080
    app = Server(environments=[Foo]).app
    
    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server_instance = uvicorn.Server(config)
    
    thread = Thread(target=server_instance.run, daemon=True)
    thread.start()
    
    base_url = f"http://{host}:{port}"
    asyncio.get_event_loop().run_until_complete(wait_for_server(base_url))
    
    yield base_url
    
    server_instance.should_exit = True


@pytest.fixture
def client(server: str) -> OpenReward:
    return OpenReward(base_url=server)

@pytest.mark.asyncio
async def test_splits(client: OpenReward):
    environment = client.environments.get("foo")
    splits = await environment.list_splits()
    assert splits == ["train"]

@pytest.mark.asyncio
async def test_tools(client: OpenReward):
    environment = client.environments.get("foo")
    tools = await environment.list_tools()
    tool_names = [t.name for t in tools]
    assert "submit" in tool_names

@pytest.mark.asyncio
async def test_list_tasks(client: OpenReward):
    environment = client.environments.get("foo")
    tasks = await environment.list_tasks(split="train")
    assert len(tasks) == 1
    assert tasks[0].task_spec == {"foo": "bar"}

@pytest.mark.asyncio
async def test_call_tool(client: OpenReward):
    environment = client.environments.get("foo")
    tasks = await environment.list_tasks(split="train")
    
    async with environment.session(tasks[0]) as session:
        res = await session.call_tool("submit")
        
        assert res.reward == 1.0
        assert res.finished is True
        assert len(res.blocks) == 1
        assert res.blocks[0].type == "text"
        assert res.blocks[0].text == "baz"