import inspect
from logging import getLogger
from typing import Any, Awaitable, Callable, Sequence, TypeVar, get_type_hints
from pydantic import BaseModel, ValidationError

from .types import (
    JSONObject,
    GetToolsOutput,
    RunToolError,
    RunToolOutput,
    RunToolSuccess,
    ToolOutput,
    ToolSpec,
    Blocks,
)
from .utils import maybe_await

T = TypeVar("T")

logger = getLogger(__file__)


def tool(fn: Callable[..., Any]) -> Callable[..., Any]:
    setattr(fn, "_env_tool", True)
    return fn

class Environment:
    """
    An environment is an interface to computation that may be stateful. Clients interface with the
    environment through a persistent connection to perform actions. Environments have _tasks_, which
    are JSON objects describing a particular setup and goal state. For example, inside of an Ubuntu
    environment, a task could be to download a file from the internet and save its contents to a csv
    file.
    """
    def __init__(self, task_spec: JSONObject = {}) -> None:
        self.task_spec = task_spec

    def setup(self) -> None | Awaitable[None]:
        """
        Setup the environment. This is called upon the first tool call by a connected client.
        """
        ...
    
    def teardown(self) -> None | Awaitable[None]:
        """
        Teardown the environment. This is called upon client disconnect.
        """
        ...

    def get_prompt(self) -> Blocks | Awaitable[Blocks]:
        """
        Get a default prompt for the current task. For example, if the task is a question-answer pair,
        returning the question would be a sensible choice here.
        """
        return []

    @classmethod
    def get_tasks(cls, split: str) -> Sequence[JSONObject]:
        """
        Get a list of tasks for the given split. Default is the empty list.
        """
        return []
    
    @classmethod
    def get_splits(cls) -> list[str]:
        """
        Get a list of splits for the environment. Default is the empty list.
        """
        return []

    @staticmethod
    def _is_tool(fn: Callable[..., Any]) -> bool:
        if not callable(fn) or not getattr(fn, "_env_tool", False):
            return False
        real = inspect.unwrap(fn)
        hints = get_type_hints(real, include_extras=True)
        params = [p for p in inspect.signature(real).parameters.values() if p.name != "self"]
        ret = hints.get("return")
        if len(params) == 0:
            return ret == ToolOutput
        if len(params) == 1:
            pt = hints.get(params[0].name)
            return (
                pt is not None and ret is not None and inspect.isclass(pt)
                and issubclass(pt, BaseModel) and ret == ToolOutput
            )
        return False

    @classmethod
    def get_tools(cls) -> GetToolsOutput:
        out: list[ToolSpec] = []
        for name in dir(cls):
            fn = getattr(cls, name)
            if not cls._is_tool(fn):
                continue
            real = inspect.unwrap(fn)
            hints = get_type_hints(real, include_extras=True)
            params = [p for p in inspect.signature(real).parameters.values() if p.name != "self"]
            schema = None
            if params:
                mdl: type[BaseModel] = hints[params[0].name]  # type: ignore[assignment]
                schema = mdl.model_json_schema() if hasattr(mdl, "model_json_schema") else mdl.schema()  # type: ignore[attr-defined]
            out.append(ToolSpec(name=name, description=(fn.__doc__ or "").strip(), input_schema=schema))
        return GetToolsOutput(tools=out)

    async def _call_tool(self, name: str, input: JSONObject) -> RunToolOutput:
        fn = getattr(self, name, None)
        if fn is None or not self._is_tool(fn):
            return RunToolError(error=f"{name!r} is not a valid tool")
        real = inspect.unwrap(fn)
        hints = get_type_hints(real, include_extras=True)
        params = [p for p in inspect.signature(real).parameters.values() if p.name != "self"]
        if not params:
            res = await maybe_await(fn())
        else:
            mdl: type[BaseModel] = hints[params[0].name]  # type: ignore[assignment]
            try:
                inp = mdl(**input)
            except ValidationError as e:
                return RunToolError(error=f"Tool input validation error: {str(e.errors())}")
            res = await maybe_await(fn(inp))
        if not isinstance(res, ToolOutput):
            raise TypeError(f"{name!r} returned {type(res).__name__}; expected ToolOutput")
        return RunToolSuccess(output=res)
