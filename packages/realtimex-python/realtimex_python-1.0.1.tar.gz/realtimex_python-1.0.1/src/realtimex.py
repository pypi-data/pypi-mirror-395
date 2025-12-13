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
        
        self.connection.bind('message', self._handle_message)
        self.connection.connect()

    def subscribe(self, channel_name: str) -> Channel:
        if channel_name in self.channels:
            return self.channels[channel_name]

        channel = Channel(channel_name, self)
        self.channels[channel_name] = channel

        self.connection.send('realtimex:subscribe', {'channel': channel_name})
        
        return channel

    def unsubscribe(self, channel_name: str) -> None:
        if channel_name not in self.channels:
            return

        self.connection.send('realtimex:unsubscribe', {'channel': channel_name})
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

    def _handle_message(self, message: Dict) -> None:
        event = message.get('event')
        data = message.get('data', {})
        
        if event == 'server-event':
            channel_name = data.get('channel')
            event_name = data.get('event')
            event_data = data.get('data')
            
            if channel_name in self.channels:
                self.channels[channel_name]._handle_event(event_name, event_data)
        
        elif event == 'realtimex_internal:subscription_succeeded':
            channel_name = data.get('channel')
            # Emit on connection (like JS SDK)
            self.connection.emit('subscription_succeeded', data)
            # Also emit on channel
            if channel_name in self.channels:
                self.channels[channel_name].emit('realtimex_internal:subscription_succeeded', data)
        
        elif event == 'realtimex_internal:subscription_error':
            channel_name = data.get('channel')
            # Emit on connection (like JS SDK)
            self.connection.emit('subscription_error', data)
            # Also emit on channel
            if channel_name in self.channels:
                self.channels[channel_name].emit('realtimex_internal:subscription_error', data)
