import asyncio
import atexit
import multiprocessing as mp
import time
import uuid
from queue import Empty
from typing import Any, Dict, Optional

from anthropic.types import MessageParam as AnthropicMessageParam
from google.genai import types as gdm_types
from openai.types.responses import ResponseInputItemParam

from openreward.models import (
    InputEvent,
    LogMessageEvent,
    OutputEvent,
    RolloutConfig,
    RolloutStartedEvent,
    SendLoopConfig,
    ShutdownEvent,
)
from .background import worker_loop
from .serializers.ant import serialize_anthropic_message
from .serializers.base import UploadType, base_to_normalized
from .serializers.gdm import serialize_gdm_message
from .serializers.models import NormalizedEvent
from .serializers.oai_completions import (
    OpenAIChatMessage,
    openai_completions_to_normalized,
)
from .serializers.oai_responses import serialize_openai_response


class RolloutAPI:
    def __init__(self, 
        send_loop_config: SendLoopConfig,
        shutdown_timeout: float = 10.0,
        process_name: str = "openreward_rollout_api"
    ):
        self.send_loop_config = send_loop_config
        self.shutdown_timeout = shutdown_timeout
        self.process_name = process_name

        self._in: mp.Queue[InputEvent] = mp.Queue()
        self._out: mp.Queue[OutputEvent] = mp.Queue()

        self._p = mp.Process(
            target=worker_loop, 
            args=(self._in, self._out, self.send_loop_config),
            name=self.process_name,
            daemon=True
        )
        self._p.start()
        self.closed = asyncio.Event()

        atexit.register(self._atexit_handler)

    def create(
        self, 
        run_name: str, 
        rollout_name: Optional[str] = None, 
        environment: Optional[str] = None, 
        split: Optional[str] = None, 
        metadata: Optional[dict] = None, 
        task_spec: Optional[Dict[str, Any]] = None
    ) -> "Rollout":
        config = RolloutConfig(
            run_name=run_name,
            rollout_name=rollout_name,
            environment=environment,
            split=split,
            metadata=metadata,
            task_spec=task_spec
        )
        return Rollout(config=config, _in=self._in)

    def close(self):
        # check if we have the rollout api
        if self.closed.is_set():
            return
        self._in.put(ShutdownEvent())
        try:
            response = self._out.get(timeout=self.shutdown_timeout)
        except Empty:
            pass

        self._p.join(timeout=self.shutdown_timeout)
        if self._p.is_alive():
            self._p.terminate()
            print("Warning: terminating upload process while alive, some requests may not have been processed!")
        self.closed.set()

    def __del__(self):
        self.close()

    def _atexit_handler(self):
        # Best effort if user forgot
        try:
            self.close()
        except Exception:
            pass

class Rollout:
    def __init__(self, config: RolloutConfig, _in: mp.Queue):
        self.config = config
        self.event_id = str(uuid.uuid4())
        self._in = _in
        self._in.put(RolloutStartedEvent.from_config(
            event_id=self.event_id,
            timestamp=int(time.time() * 1000),
            config=config
        ))
        self.logged_messages = 0

    def _log_message(self, normalized_event: NormalizedEvent, reward: Optional[float] = None, is_finished: Optional[bool] = False, metadata: Optional[dict] = None):
        
        if is_finished is None:
            is_finished = False
        
        self._in.put(LogMessageEvent(
            eventId = str(uuid.uuid4()),
            timestamp=int(time.time() * 1000),
            index=self.logged_messages,
            rolloutEventId=self.event_id,
            type=normalized_event.type,
            content=normalized_event.content,
            contentReference=normalized_event.content_reference,
            summary=normalized_event.summary,
            name=normalized_event.name,
            callId=normalized_event.call_id,
            reward=reward,
            is_finished=is_finished,
            metadata=metadata or {},
        ))
        self.logged_messages += 1

    def log(
        self, 
        message: UploadType,
        reward: Optional[float] = None,
        is_finished: Optional[bool] = False,
        metadata: Optional[dict] = None,
    ):
        normalized_event = base_to_normalized([message])[0]
        self._log_message(normalized_event, reward, is_finished, metadata)

    def log_openai_completions(
        self,
        message: OpenAIChatMessage,
        reward: Optional[float] = None,
        is_finished: Optional[bool] = False,
        metadata: Optional[dict] = None,
    ):
        normalized_event = openai_completions_to_normalized([message])[0]
        self._log_message(normalized_event, reward, is_finished, metadata)

    def log_openai_response(
        self,
        message: ResponseInputItemParam,
        reward: Optional[float] = None,
        is_finished: Optional[bool] = False,
        metadata: Optional[dict] = None,
    ):
        event = serialize_openai_response(message)
        self._log_message(event, reward, is_finished, metadata)

    def log_anthropic_message(
        self,
        message: AnthropicMessageParam,
        reward: Optional[float] = None,
        is_finished: Optional[bool] = False,
        metadata: Optional[dict] = None,
    ):
        for event in serialize_anthropic_message(message):
            self._log_message(event, reward, is_finished, metadata)

    def log_gdm_message(
        self,
        message: gdm_types.Content,
        reward: Optional[float] = None,
        is_finished: Optional[bool] = False,
        metadata: Optional[dict] = None,
    ):
        for event in serialize_gdm_message(message):
            self._log_message(event, reward, is_finished, metadata)
