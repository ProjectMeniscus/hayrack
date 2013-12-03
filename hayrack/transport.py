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

    def __init__(self, bind_host, bind_port,
                 high_water_mark=0, socket_linger=-1):
        """
        Creates an instance of the ZeroMQCaster.  A zmq PUSH socket is
        created and is bound to the specified host:port.

        :param bind_host: ip address to bind to
        :param bind_port: port to bind to
        :param high_water_mark: messages buffered before ZMQ socket.send blocks
        :param socket_linger: time to wait for unsent messages to process on
        socket.close (milliseconds)
        """

        self.socket_type = zmq.PUSH
        self.bind_host = 'tcp://{0}:{1}'.format(bind_host, bind_port)
        self.high_water_mark = int(high_water_mark)
        self.socket_linger = int(socket_linger)
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
        self.socket.set_hwm(self.high_water_mark)
        self.socket.setsockopt(zmq.LINGER, self.socket_linger)
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
