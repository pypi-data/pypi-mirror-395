from typing import Literal, Mapping, Sequence, Union
from typing_extensions import TypeAliasType
from pydantic import BaseModel, RootModel, Field

JSONValue = TypeAliasType(
    "JSONValue",
    "Mapping[str, JSONValue] | Sequence[JSONValue] | str | int | float | bool | None",
)
JSONObject = Mapping[str, JSONValue]


class TextBlock(BaseModel, extra="forbid"):
    text: str
    detail: JSONObject | None = None
    type: Literal["text"] = "text"

class ImageBlock(BaseModel, extra="forbid"):
    data: str
    mimeType: str
    detail: JSONObject | None = None
    type: Literal["image"] = "image"

Blocks = TypeAliasType("Blocks", "list[TextBlock | ImageBlock]")

class ToolOutput(BaseModel, extra="forbid"):
    blocks: Blocks
    metadata: JSONObject | None = None
    reward: float | None = None
    finished: bool = False

class RunToolSuccess(BaseModel, extra="forbid"):
    ok: Literal[True] = True
    output: ToolOutput

class RunToolError(BaseModel, extra="forbid"):
    ok: Literal[False] = False
    error: str

class RunToolOutput(RootModel[Union[RunToolSuccess, RunToolError]]):
    root: Union[RunToolSuccess, RunToolError] = Field(discriminator="ok")

class ToolSpec(BaseModel, extra="forbid"):
    name: str
    description: str
    input_schema: JSONObject | None

class GetToolsOutput(BaseModel, extra="forbid"):
    tools: list[ToolSpec]

class ToolCall(BaseModel, extra="forbid"):
    name: str
    input: JSONObject
    task_id: str | None = None

class CreateSession(BaseModel, extra="forbid"):
    env_name: str
    task_spec: JSONObject