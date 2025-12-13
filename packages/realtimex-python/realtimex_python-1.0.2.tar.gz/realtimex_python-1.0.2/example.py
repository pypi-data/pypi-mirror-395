from src.realtimex import RealtimeX
import time

# Create client
client = RealtimeX('YOUR_API_KEY', {
    'ws_host': 'localhost',
    'ws_port': 3001,
    'encrypted': False
})

# Connection events
client.connection.bind('connecting', lambda: print('🔄 Connecting...'))
client.connection.bind('connected', lambda: print('✅ Connected!'))
client.connection.bind('disconnected', lambda: print('❌ Disconnected'))

# Subscribe to channel
channel = client.subscribe('test-channel')

# Listen to events
channel.bind('my-event', lambda data: print(f'📨 Received event: {data}'))

# Listen to all events
channel.bind_global(lambda event, data: print(f'🌐 Global event {event}: {data}'))

# Subscription succeeded event
channel.bind('realtimex_internal:subscription_succeeded', lambda data: print(f'✅ Subscription succeeded: {data}'))

# Send client event after 2 seconds
def send_message():
    time.sleep(2)
    try:
        channel.trigger('client-test', {'message': 'Hello from Python SDK!'})
        print('📤 Sent client-test event')
    except Exception as e:
        print(f'❌ Error: {e}')

import threading
threading.Thread(target=send_message, daemon=True).start()

# Keep the program running
print('🚀 Client started. Press Ctrl+C to exit.')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\n👋 Disconnecting...')
    client.disconnect()
    print('✅ Disconnected')
