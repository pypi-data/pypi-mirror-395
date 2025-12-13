import unittest
from src.utils import EventEmitter


class TestEventEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = EventEmitter()

    def test_bind_and_emit(self):
        called = []
        
        def callback(data):
            called.append(data)
        
        self.emitter.bind('test', callback)
        self.emitter.emit('test', 'hello')
        
        self.assertEqual(called, ['hello'])

    def test_unbind_specific_callback(self):
        called = []
        
        def callback1(data):
            called.append(f'cb1:{data}')
        
        def callback2(data):
            called.append(f'cb2:{data}')
        
        self.emitter.bind('test', callback1)
        self.emitter.bind('test', callback2)
        self.emitter.unbind('test', callback1)
        self.emitter.emit('test', 'hello')
        
        self.assertEqual(called, ['cb2:hello'])

    def test_unbind_all_callbacks(self):
        called = []
        
        def callback(data):
            called.append(data)
        
        self.emitter.bind('test', callback)
        self.emitter.unbind('test')
        self.emitter.emit('test', 'hello')
        
        self.assertEqual(called, [])

    def test_multiple_events(self):
        called = []
        
        self.emitter.bind('event1', lambda: called.append('e1'))
        self.emitter.bind('event2', lambda: called.append('e2'))
        
        self.emitter.emit('event1')
        self.emitter.emit('event2')
        
        self.assertEqual(called, ['e1', 'e2'])


if __name__ == '__main__':
    unittest.main()
