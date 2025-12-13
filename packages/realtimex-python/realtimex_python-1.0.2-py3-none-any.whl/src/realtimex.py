from typing import Dict, Optional
from .connection import Connection
from .channel import Channel
from .types import RealtimeXOptions


class RealtimeX:
    def __init__(self, api_key: str, options: Optional[RealtimeXOptions] = None):
        self.api_key = api_key
        self.options = self._merge_options(options or {})
        self.channels: Dict[str, Channel] = {}
        
        url = self._build_url()
        self.connection = Connection(url)
        self._setup_connection_handlers()
        self.connection.connect()

    def _setup_connection_handlers(self) -> None:
        # Route server-event messages to channels
        self.connection.bind('message', self._route_to_channel)

    def subscribe(self, channel_name: str) -> Channel:
        if channel_name in self.channels:
            return self.channels[channel_name]

        channel = Channel(channel_name, self)
        self.channels[channel_name] = channel

        # Send subscribe event like JS SDK
        self.connection.send({
            'event': 'subscribe',
            'data': {'channel': channel_name}
        })
        
        return channel

    def unsubscribe(self, channel_name: str) -> None:
        if channel_name not in self.channels:
            return

        # Send unsubscribe event like JS SDK
        self.connection.send({
            'event': 'unsubscribe',
            'data': {'channel': channel_name}
        })
        del self.channels[channel_name]

    def disconnect(self) -> None:
        self.connection.disconnect()
        self.channels.clear()

    def _merge_options(self, options: RealtimeXOptions) -> RealtimeXOptions:
        defaults = {
            'cluster': 'eu',
            'ws_host': 'ws.realtimex.net',
            'ws_port': 443,
            'encrypted': True
        }
        return {**defaults, **options}

    def _build_url(self) -> str:
        protocol = 'https' if self.options['encrypted'] else 'http'
        host = self.options['ws_host']
        port = self.options['ws_port']
        
        return f"{protocol}://{host}:{port}?api_key={self.api_key}"

    def _route_to_channel(self, message: Dict) -> None:
        # Route server-event to appropriate channel
        channel_name = message.get('channel')
        event_name = message.get('event')
        event_data = message.get('data')
        
        if channel_name and channel_name in self.channels:
            self.channels[channel_name]._handle_event(event_name, event_data)
