from dataclasses import dataclass
from typing import Mapping, Sequence, Literal
from typing_extensions import TypeAliasType

JSONValue = TypeAliasType(
    "JSONValue",
    "Mapping[str, JSONValue] | Sequence[JSONValue] | str | int | float | bool | None",
)
JSONObject = Mapping[str, JSONValue]

@dataclass
class Server:
    name: str

@dataclass
class Environment:
    server_name: str
    environment_name: str
    namespace: str = "matrix"

    @property
    def deployment_name(self) -> str:
        """Get the full deployment identifier in namespace/server_name format."""
        if "/" in self.server_name:
            # Already contains namespace
            return self.server_name
        return f"{self.namespace}/{self.server_name}"

@dataclass
class Task:
    server_name: str
    environment_name: str
    task_spec: JSONObject
    namespace: str | None

    @property
    def deployment_name(self) -> str:
        """Get the full deployment identifier in namespace/server_name format."""
        if self.namespace is None:
            return self.server_name
        else:
            return f"{self.namespace}/{self.server_name}"

@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: JSONObject | None

@dataclass
class TextBlock:
    text: str
    detail: JSONObject | None = None
    type: Literal["text"] = "text"

@dataclass
class ImageBlock:
    data: str
    mimeType: str
    detail: JSONObject | None = None
    type: Literal["image"] = "image"


@dataclass
class ToolOutput:
    blocks: list[TextBlock | ImageBlock]
    metadata: JSONObject | None = None
    reward: float | None = None
    finished: bool = False

class ToolCallError(Exception):
    pass