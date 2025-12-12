import asyncio
import json
import logging
import threading
from collections import deque
from typing import Any
from typing import Deque
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from pyee.asyncio import AsyncIOEventEmitter
from waitress.server import BaseWSGIServer
from waitress.server import create_server
from waitress.server import MultiSocketServer

from runtime.types import CaptchaSolverSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CaptchaEvent = Literal[
    "CAPTCHA_EXTENSION_READY", "CAPTCHA_DETECTED", "CAPTCHA_SOLVED", "HIT_LIMIT", "MAX_RETRIES_EXHAUSTED", "ERROR"
]


class EventRequest(BaseModel):
    model_config = {"populate_by_name": True}
    event: CaptchaEvent
    # tab_id: str = Field(None, alias="tabId")
    session_id: Optional[str] = Field(None, alias="sessionId")
    payload: Optional[Any] = None


class EventQueues:
    queues: dict[CaptchaEvent, Deque[EventRequest]]

    def __init__(self):
        self.queues = {}


class TabEventQueue:
    events_queue: dict[str, EventQueues]
    last_detection_event: Optional[EventRequest]

    def __init__(self, tab_id: str):
        self.tab_id = tab_id
        self.events_queue = {}
        self.last_detection_event = None


class ExtensionServer:
    tabs: dict[str, TabEventQueue]
    is_healthy: bool = False
    _server: Optional[MultiSocketServer | BaseWSGIServer] = None
    _loop: Optional[asyncio.AbstractEventLoop] = None
    _thread: Optional[threading.Thread] = None

    def __init__(self):
        self.tabs = dict()

    def __call__(self, environ, start_response):
        """WSGI application"""
        path = environ.get("PATH_INFO", "")
        method = environ["REQUEST_METHOD"]

        if path == "/ingest" and method == "POST":
            return self._handle_ingest(environ, start_response)

        start_response("404 Not Found", [("Content-Type", "application/json")])
        return [json.dumps({"error": "Not found"}).encode()]

    def _handle_queue_event(self, event: EventRequest):
        queueable_events: list[CaptchaEvent] = [
            "CAPTCHA_DETECTED",
            "CAPTCHA_SOLVED",
            "HIT_LIMIT",
            "MAX_RETRIES_EXHAUSTED",
            "ERROR",
        ]

        if event.event not in queueable_events:
            return
        tab_id = "page-0"  # We will revisit on multi-tab support
        if event.session_id is None:
            return
        if tab_id not in self.tabs:
            self.tabs[tab_id] = TabEventQueue(tab_id=tab_id)
        tab_info = self.tabs[tab_id]
        if event.event == "CAPTCHA_DETECTED":
            logger.info(f"Setting last detection event to {event}")
            tab_info.last_detection_event = event
            return
        logger.info(f"Queueing Event: {event}")
        if event.session_id not in tab_info.events_queue:
            tab_info.events_queue[event.session_id] = EventQueues()

        event_queues = tab_info.events_queue[event.session_id]
        if event.event not in event_queues.queues:
            event_queues.queues[event.event] = deque(maxlen=5)

        event_queues.queues[event.event].append(event)

    def _handle_ingest(self, environ, start_response):
        try:
            global event_emitter
            if event_emitter is None:
                event_emitter = AsyncIOEventEmitter()
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            data = json.loads(body)
            event_data = EventRequest(**data)
            if event_data.event == "CAPTCHA_EXTENSION_READY":
                self.is_healthy = True
            self._handle_queue_event(event=event_data)
            if self._loop and not self._loop.is_closed():
                self._loop.call_soon_threadsafe(event_emitter.emit, event_data.event, {})
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps({}).encode()]

        except ValidationError as e:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": e.errors()}).encode()]
        except Exception as e:
            logger.error(f"Error: {e}")
            start_response("500 Internal Server Error", [("Content-Type", "application/json")])
            return [json.dumps({"error": "Internal server error"}).encode()]

    async def start(self, port: int = 3000, host: str = "0.0.0.0") -> None:
        """Start server using daemon thread"""
        self._loop = asyncio.get_running_loop()
        self._server = create_server(self.__call__, host=host, port=port)

        def _run_server():
            try:
                if self._server:
                    self._server.run()
            except OSError as err:
                if err.errno != 9:
                    raise

        self._thread = threading.Thread(target=_run_server, daemon=True)
        self._thread.start()

    async def stop(self):
        self._loop = None
        if self._server:
            self._server.close()

            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=5.0)


event_emitter: Optional[AsyncIOEventEmitter] = None
extension_server: Optional[ExtensionServer] = None


async def setup_intuned_extension_server(captcha_settings: Optional[CaptchaSolverSettings] = None):
    global event_emitter, extension_server
    if captcha_settings is None:
        captcha_settings = CaptchaSolverSettings()
    extension_server = ExtensionServer()
    event_emitter = AsyncIOEventEmitter()
    await extension_server.start(port=captcha_settings.port)


async def clean_intuned_extension_server():
    global event_emitter, extension_server
    if extension_server is not None:
        await extension_server.stop()
        extension_server = None

    if event_emitter is not None:
        event_emitter.remove_all_listeners()
        event_emitter = None


def get_event_from_event_queue(
    event: CaptchaEvent, tab_id: str = "page-0", session_id: str = ""
) -> Optional[EventRequest]:
    if extension_server is None:
        raise RuntimeError("Extension server is not initialized or healthy")

    tab_info = extension_server.tabs.get(tab_id)
    if tab_info is None:
        return None
    if event == "CAPTCHA_DETECTED":
        value = tab_info.last_detection_event
        tab_info.last_detection_event = None
        return value

    if session_id not in tab_info.events_queue:
        return None

    event_queues = tab_info.events_queue[session_id]
    if event not in event_queues.queues or len(event_queues.queues[event]) == 0:
        return None

    return event_queues.queues[event].popleft()


def get_intuned_event_emitter() -> AsyncIOEventEmitter:
    if event_emitter is None:
        raise RuntimeError("Event emitter is not initliazed")
    return event_emitter
