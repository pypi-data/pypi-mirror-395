from typing import Dict, Any, Callable, Optional

ConnectionState = str  # 'connecting' | 'connected' | 'disconnected'

EventCallback = Callable[..., None]

RealtimeXOptions = Dict[str, Any]

ChannelData = Dict[str, Any]
