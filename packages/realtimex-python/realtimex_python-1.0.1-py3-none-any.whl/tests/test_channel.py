import unittest
from unittest.mock import Mock, MagicMock
from src.channel import Channel


class TestChannel(unittest.TestCase):
    def setUp(self):
        self.realtimex_mock = Mock()
        self.realtimex_mock.connection = Mock()
        self.channel = Channel('test-channel', self.realtimex_mock)

    def test_bind_event(self):
        called = []
        
        def callback(data):
            called.append(data)
        
        self.channel.bind('my-event', callback)
        self.channel._handle_event('my-event', {'msg': 'hello'})
        
        self.assertEqual(len(called), 1)
        self.assertEqual(called[0], {'msg': 'hello'})

    def test_bind_global(self):
        called = []
        
        def callback(event, data):
            called.append((event, data))
        
        self.channel.bind_global(callback)
        self.channel._handle_event('event1', 'data1')
        self.channel._handle_event('event2', 'data2')
        
        self.assertEqual(called, [('event1', 'data1'), ('event2', 'data2')])

    def test_trigger_client_event(self):
        self.channel.trigger('client-test', {'message': 'hello'})
        
        self.realtimex_mock.connection.send.assert_called_once_with('client-event', {
            'channel': 'test-channel',
            'event': 'client-test',
            'data': {'message': 'hello'}
        })

    def test_trigger_non_client_event_raises(self):
        with self.assertRaises(ValueError):
            self.channel.trigger('invalid-event', {})

    def test_unsubscribe(self):
        self.channel.unsubscribe()
        self.realtimex_mock.unsubscribe.assert_called_once_with('test-channel')


if __name__ == '__main__':
    unittest.main()
