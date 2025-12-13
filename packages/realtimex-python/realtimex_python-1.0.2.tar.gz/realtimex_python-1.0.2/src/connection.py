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

        # Handle server-event - emit as 'message' with full structure
        self.sio.on('server-event', lambda data: self.emit('message', data))
        
        # Handle subscription events - emit directly on connection
        self.sio.on('realtimex_internal:subscription_succeeded', 
                    lambda data: self.emit('subscription_succeeded', data))
        self.sio.on('realtimex_internal:subscription_error',
                    lambda data: self.emit('subscription_error', data))
        
        # Handle pong
        self.sio.on('realtimex:pong', lambda data: self.emit('pong', data))

    def disconnect(self) -> None:
        if self._reconnect_timer:
            self._reconnect_timer.cancel()
            self._reconnect_timer = None

        if self.sio and self.sio.connected:
            self.sio.disconnect()
        
        self.state = 'disconnected'

    def send(self, data: Dict[str, Any]) -> None:
        """Send data through socket. Handles protocol translation like JS SDK."""
        if not self.sio or not self.sio.connected:
            return
        
        event = data.get('event')
        
        if event == 'subscribe':
            # Send realtimex:subscribe with channel data
            self.sio.emit('realtimex:subscribe', {
                'channel': data.get('data', {}).get('channel')
            })
        elif event == 'unsubscribe':
            # Send realtimex:unsubscribe with channel data
            self.sio.emit('realtimex:unsubscribe', {
                'channel': data.get('data', {}).get('channel')
            })
        elif event and event.startswith('client-'):
            # Send client-event with channel, event, and data
            self.sio.emit('client-event', {
                'channel': data.get('channel'),
                'event': event,
                'data': data.get('data')
            })

    def ping(self) -> None:
        if self.sio and self.sio.connected:
            self.sio.emit('realtimex:ping', {})

    def _schedule_reconnect(self) -> None:
        if self._reconnect_timer:
            return

        def reconnect():
            self._reconnect_timer = None
            self.connect()

        self._reconnect_timer = threading.Timer(3.0, reconnect)
        self._reconnect_timer.start()
