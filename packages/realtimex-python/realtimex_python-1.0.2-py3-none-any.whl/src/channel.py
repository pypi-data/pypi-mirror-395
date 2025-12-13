from typing import Callable, Optional, Dict, Any
from .utils import EventEmitter


class Channel(EventEmitter):
    def __init__(self, name: str, realtimex):
        super().__init__()
        self.name = name
        self._realtimex = realtimex
        self._global_callbacks = []

    def bind_global(self, callback: Callable) -> None:
        self._global_callbacks.append(callback)

    def trigger(self, event: str, data: Dict[str, Any]) -> None:
        if not event.startswith('client-'):
            raise ValueError("Client events must start with 'client-'")
        
        # Send like JS SDK: {event, channel, data}
        self._realtimex.connection.send({
            'event': event,
            'channel': self.name,
            'data': data
        })

    def unsubscribe(self) -> None:
        self._realtimex.unsubscribe(self.name)

    def _handle_event(self, event: str, data: Any) -> None:
        self.emit(event, data)
        
        for callback in self._global_callbacks[:]:
            callback(event, data)
