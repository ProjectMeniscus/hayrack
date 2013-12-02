"""
The transport module defines the classes that serve as the transport layer for
Portal when sending parsed syslog messages downstream.
"""

import zmq


class ZeroMQCaster(object):
    """
    ZeroMQCaster allows for messages to be sent downstream by pushing
    messages over a zmq socket to downstream clients.  If multiple clients
    connect to this PUSH socket the messages will be load balanced evenly
    across the clients.
    """

    def __init__(self, bind_host_tuple):
        """
        Creates an instance of the ZeroMQCaster.  A zmq PUSH socket is
        created and is bound to the specified host:port.

        :param bind_host_tuple: (host, port), for example ('127.0.0.1', '5000')
        """

        self.socket_type = zmq.PUSH
        self.bind_host = 'tcp://{0}:{1}'.format(*bind_host_tuple)
        self.context = None
        self.socket = None
        self.bound = False

    def bind(self):
        """
        Bind the ZeroMQCaster to a host:port to push out messages.
        Create a zmq.Context and a zmq.PUSH socket, and bind the
        socket to the specified host:port
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(self.socket_type)
        self.socket.bind(self.bind_host)
        self.bound = True

    def cast(self, msg):
        """
        Sends a message over the zmq PUSH socket
        """
        if not self.bound:
            raise zmq.error.ZMQError(
                "ZeroMQCaster is not bound to a socket")
        self.socket.send(msg)

    def close(self):
        """
        Close the zmq socket
        """
        if self.bound:
            self.socket.close()
            self.context.destroy()
            self.socket = None
            self.context = None
            self.bound = False
