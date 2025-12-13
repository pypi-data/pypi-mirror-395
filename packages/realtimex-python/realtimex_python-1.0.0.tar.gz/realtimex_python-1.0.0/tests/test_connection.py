import unittest
from unittest.mock import Mock, patch, MagicMock
from src.connection import Connection


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:3001?api_key=test'
        self.connection = Connection(self.url)

    def test_initial_state(self):
        self.assertEqual(self.connection.state, 'disconnected')
        self.assertEqual(self.connection.url, self.url)
        self.assertIsNone(self.connection.sio)

    @patch('src.connection.socketio.Client')
    def test_connect_changes_state(self, mock_client):
        mock_sio = Mock()
        mock_client.return_value = mock_sio
        
        self.connection.connect()
        
        self.assertEqual(self.connection.state, 'connecting')
        mock_client.assert_called_once_with(reconnection=False)

    @patch('src.connection.socketio.Client')
    def test_connect_already_connected(self, mock_client):
        self.connection.state = 'connected'
        self.connection.connect()
        
        mock_client.assert_not_called()

    @patch('src.connection.socketio.Client')
    def test_send_when_connected(self, mock_client):
        mock_sio = Mock()
        mock_sio.connected = True
        mock_client.return_value = mock_sio
        
        self.connection.connect()
        self.connection.sio = mock_sio
        self.connection.send('test-event', {'data': 'test'})
        
        mock_sio.emit.assert_called_once_with('test-event', {'data': 'test'})

    def test_send_when_not_connected(self):
        self.connection.send('test-event', {'data': 'test'})
        # Should not raise error, just do nothing

    def test_ping(self):
        self.connection.send = Mock()
        self.connection.ping()
        
        self.connection.send.assert_called_once_with('realtimex:ping', {})

    @patch('src.connection.socketio.Client')
    def test_disconnect(self, mock_client):
        mock_sio = Mock()
        mock_sio.connected = True
        mock_client.return_value = mock_sio
        
        self.connection.connect()
        self.connection.sio = mock_sio
        self.connection.disconnect()
        
        mock_sio.disconnect.assert_called_once()
        self.assertEqual(self.connection.state, 'disconnected')

    def test_event_emitter_integration(self):
        called = []
        
        self.connection.bind('connecting', lambda: called.append('connecting'))
        self.connection.bind('connected', lambda: called.append('connected'))
        
        self.connection.emit('connecting')
        self.connection.emit('connected')
        
        self.assertEqual(called, ['connecting', 'connected'])


if __name__ == '__main__':
    unittest.main()
