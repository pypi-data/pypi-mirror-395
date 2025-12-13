from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel

from openreward.api.rollouts.serializers.models import NormalizedType


class RolloutConfig(BaseModel):
    run_name: str
    rollout_name: Optional[str] = None
    environment: Optional[str] = None
    split: Optional[str] = None
    metadata: Optional[dict] = None
    task_spec: Optional[Dict[str, Any]] = None


@dataclass
class Config:
    process_name: str
    shutdown_timeout: float
    send_loop_config: "SendLoopConfig"


@dataclass
class SendLoopConfig:
    max_items: int # max item threshold
    max_bytes: int # max byte threshold
    max_age: float # max age
    jitter: float # % jitter of the flush interval

    ring_capacity: int # max items, at which the ring buffer will be flushed

    max_batch_items: int # max number of items to flush at once
    max_batch_bytes: int # max number of bytes to flush at once

    max_retries: int # max number of retries
    backoff_base: float # base time of the backoff
    backoff_factor: float # factor of the backoff
    backoff_cap: float # cap time of the backoff

    max_upload_concurrency: int

    api_key: str | None
    base_url: str

@dataclass
class LogMessageEvent:
    # rollout info
    eventId: str
    timestamp: int
    index: int

    rolloutEventId: str

    # normalized event info
    type: NormalizedType
    content: Optional[str] = None # visible text or JSON string for tools
    contentReference: Optional[str] = None # only for hidden reasoning
    summary: Optional[str] = None # reasoning-only
    name: Optional[str] = None # tool name (tool_call only)
    callId: Optional[str] = None # join key for tool_call/result

    # extra info
    reward: Optional[float] = None
    is_finished: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

    eventType: Literal["message"] = "message"


@dataclass # Do we want this to be on the background process?
class RolloutStartedEvent:
    # rollout info
    eventId: str
    timestamp: int

    # rollout info
    runName: str
    step: Optional[int] = None
    environment: Optional[str] = None
    rolloutName: Optional[str] = None
    split: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    task_spec: Optional[Dict[str, Any]] = None

    eventType: Literal["rollout"] = "rollout"

    @classmethod
    def from_config(cls, event_id: str, timestamp: int, config: RolloutConfig, step: Optional[int] = None):
        return cls(
            eventId=event_id,
            timestamp=timestamp,
            runName=config.run_name,
            rolloutName=config.rollout_name,
            environment=config.environment,
            split=config.split,
            metadata=config.metadata,
            task_spec=config.task_spec,
            step=step
        )

@dataclass
class FlushEvent:
    event_type: Literal["flush"] = "flush"

@dataclass
class ShutdownEvent:
    event_type: Literal["shutdown"] = "shutdown"

InputEvent = Union[LogMessageEvent, RolloutStartedEvent, FlushEvent, ShutdownEvent]

@dataclass
class ShutdownResponse:
    success: bool
    timestamp: datetime
    event_type: Literal["shutdown_response"] = "shutdown_response"

OutputEvent = ShutdownResponse