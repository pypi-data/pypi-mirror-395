import unittest
from unittest.mock import Mock, patch, MagicMock
from src.realtimex import RealtimeX


class TestRealtimeX(unittest.TestCase):
    @patch('src.realtimex.Connection')
    def test_initialization(self, mock_connection):
        client = RealtimeX('test-api-key')
        
        self.assertEqual(client.api_key, 'test-api-key')
        self.assertEqual(client.options['cluster'], 'eu')
        mock_connection.return_value.connect.assert_called_once()

    @patch('src.realtimex.Connection')
    def test_custom_options(self, mock_connection):
        client = RealtimeX('test-api-key', {
            'ws_host': 'localhost',
            'ws_port': 3001,
            'encrypted': False
        })
        
        self.assertEqual(client.options['ws_host'], 'localhost')
        self.assertEqual(client.options['ws_port'], 3001)
        self.assertFalse(client.options['encrypted'])

    @patch('src.realtimex.Connection')
    def test_build_url_encrypted(self, mock_connection):
        client = RealtimeX('my-key', {'encrypted': True, 'ws_host': 'test.com', 'ws_port': 443})
        url = client._build_url()
        
        self.assertEqual(url, 'https://test.com:443?api_key=my-key')

    @patch('src.realtimex.Connection')
    def test_build_url_unencrypted(self, mock_connection):
        client = RealtimeX('my-key', {'encrypted': False, 'ws_host': 'localhost', 'ws_port': 3001})
        url = client._build_url()
        
        self.assertEqual(url, 'http://localhost:3001?api_key=my-key')

    @patch('src.realtimex.Connection')
    def test_subscribe(self, mock_connection):
        client = RealtimeX('test-api-key')
        channel = client.subscribe('test-channel')
        
        self.assertEqual(channel.name, 'test-channel')
        self.assertIn('test-channel', client.channels)
        mock_connection.return_value.send.assert_called_with({'event': 'subscribe', 'data': {'channel': 'test-channel'}})

    @patch('src.realtimex.Connection')
    def test_subscribe_existing_channel(self, mock_connection):
        client = RealtimeX('test-api-key')
        channel1 = client.subscribe('test-channel')
        channel2 = client.subscribe('test-channel')
        
        self.assertIs(channel1, channel2)

    @patch('src.realtimex.Connection')
    def test_unsubscribe(self, mock_connection):
        client = RealtimeX('test-api-key')
        client.subscribe('test-channel')
        client.unsubscribe('test-channel')
        
        self.assertNotIn('test-channel', client.channels)

    @patch('src.realtimex.Connection')
    def test_route_to_channel(self, mock_connection):
        client = RealtimeX('test-api-key')
        channel = client.subscribe('test-channel')
        
        called = []
        channel.bind('my-event', lambda data: called.append(data))
        
        client._route_to_channel({
            'channel': 'test-channel',
            'event': 'my-event',
            'data': {'msg': 'hello'}
        })
        
        self.assertEqual(called, [{'msg': 'hello'}])

    @patch('src.realtimex.Connection')
    def test_disconnect(self, mock_connection):
        client = RealtimeX('test-api-key')
        client.subscribe('test-channel')
        client.disconnect()
        
        self.assertEqual(len(client.channels), 0)
        mock_connection.return_value.disconnect.assert_called_once()


if __name__ == '__main__':
    unittest.main()
