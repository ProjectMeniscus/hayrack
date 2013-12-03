import unittest

from mock import MagicMock, patch
from hayrack import transport


class WhenTestingZeroMqCaster(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.port = '5000'
        self.msg = '{"key": "value"}'
        self.zmq_mock = MagicMock()
        self.zmq_mock.PUSH = transport.zmq.PUSH

        #set up the mock of the socket object
        self.socket_mock = MagicMock()
        #create a mock for the zmq context object
        self.context_mock = MagicMock()
        #have the mock context object return the mock socket
        # when the context.socket() method is called
        self.context_mock.socket.return_value = self.socket_mock
        #have the mock zmq module return the mocked context object
        # when the Context() constructor is called
        self.zmq_mock.Context.return_value = self.context_mock

        self.caster = transport.ZeroMQCaster(self.host, self.port)

    def test_constructor(self):
        self.assertEqual(self.caster.socket_type, transport.zmq.PUSH)
        self.assertEqual(
            self.caster.bind_host,
            'tcp://{0}:{1}'.format(self.host, self.port))
        self.assertIsNone(self.caster.context)
        self.assertIsNone(self.caster.socket)
        self.assertFalse(self.caster.bound)

    def test_bind(self):
        with patch('hayrack.transport.zmq', self.zmq_mock):
            self.caster.bind()
        self.context_mock.socket.assert_called_once_with(
            transport.zmq.PUSH)
        self.socket_mock.bind.assert_called_once_with(
            'tcp://{0}:{1}'.format(self.host, self.port))
        self.assertTrue(self.caster.bound)

    def test_cast(self):
        with patch('hayrack.transport.zmq', self.zmq_mock):
            self.caster.bind()
        self.caster.cast(self.msg)
        self.socket_mock.send.assert_called_once_with(self.msg)

        self.caster.close()
        with self.assertRaises(transport.zmq.error.ZMQError):
            self.caster.cast(self.msg)

    def test_close(self):
        with patch('hayrack.transport.zmq', self.zmq_mock):
            self.caster.bind()
        self.caster.close()
        self.socket_mock.close.assert_called_once_with()
        self.context_mock.destroy.assert_called_once_with()
        self.assertIsNone(self.caster.context)
        self.assertIsNone(self.caster.socket)
        self.assertFalse(self.caster.bound)


if __name__ == '__main__':
    unittest.main()
