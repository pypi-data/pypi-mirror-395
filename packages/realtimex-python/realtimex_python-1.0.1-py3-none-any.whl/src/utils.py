from typing import Dict, List, Callable, Optional, Any


class EventEmitter:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}

    def bind(self, event: str, callback: Callable) -> None:
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(callback)

    def unbind(self, event: str, callback: Optional[Callable] = None) -> None:
        if event not in self._events:
            return
        
        if callback is None:
            del self._events[event]
        else:
            self._events[event] = [cb for cb in self._events[event] if cb != callback]
            if not self._events[event]:
                del self._events[event]

    def emit(self, event: str, *args: Any) -> None:
        if event in self._events:
            for callback in self._events[event][:]:
                callback(*args)
