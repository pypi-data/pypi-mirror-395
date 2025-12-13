import socketio
import threading
from typing import Optional, Dict, Any
from .utils import EventEmitter
from .types import ConnectionState


class Connection(EventEmitter):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.state: ConnectionState = 'disconnected'
        self.sio: Optional[socketio.Client] = None
        self._reconnect_timer: Optional[threading.Timer] = None

    def connect(self) -> None:
        if self.state == 'connected' or self.state == 'connecting':
            return

        self.state = 'connecting'
        self.emit('connecting')

        self.sio = socketio.Client(reconnection=False)
        self._register_handlers()

        try:
            self.sio.connect(self.url, transports=['websocket'])
        except Exception:
            self.state = 'disconnected'
            self.emit('disconnected')
            self._schedule_reconnect()

    def _register_handlers(self) -> None:
        @self.sio.event
        def connect():
            self.state = 'connected'
            self.emit('connected')

        @self.sio.event
        def disconnect():
            self.state = 'disconnected'
            self.emit('disconnected')
            self._schedule_reconnect()

        self.sio.on('server-event', lambda data: self.emit('message', data))
        self.sio.on('realtimex_internal:subscription_succeeded', 
                    lambda data: self.emit('message', {'event': 'realtimex_internal:subscription_succeeded', 'data': data}))
        self.sio.on('realtimex_internal:subscription_error',
                    lambda data: self.emit('message', {'event': 'realtimex_internal:subscription_error', 'data': data}))
        self.sio.on('realtimex:pong',
                    lambda data: self.emit('message', {'event': 'realtimex:pong', 'data': data}))

    def disconnect(self) -> None:
        if self._reconnect_timer:
            self._reconnect_timer.cancel()
            self._reconnect_timer = None

        if self.sio and self.sio.connected:
            self.sio.disconnect()
        
        self.state = 'disconnected'

    def send(self, event: str, data: Dict[str, Any]) -> None:
        if self.sio and self.sio.connected:
            self.sio.emit(event, data)

    def ping(self) -> None:
        self.send('realtimex:ping', {})

    def _schedule_reconnect(self) -> None:
        if self._reconnect_timer:
            return

        def reconnect():
            self._reconnect_timer = None
            self.connect()

        self._reconnect_timer = threading.Timer(3.0, reconnect)
        self._reconnect_timer.start()
