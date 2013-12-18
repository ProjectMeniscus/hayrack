# Hayrack

A tool for capturing syslog messages from STDIN, such as when run as a program destination by Syslog-NG, and pushing messages over ZeroMQ to downstream hosts.

### Example Hayrack Server:

```
from hayrack import server

#start the IO Loop to read from STDIN
server.start_io('127.0.0.1', '5000')
```

The IO Loop will block the current process.  The server binds to a ZeroMQ PUSH socket and forwards all messages received via STDIN.  Messages sent over a PUSH socket are load balanced acorss all connected ZeroMQ PULL sockets.  The server has a signal handler that will properly close sockets of a sigterm is recevied.


### Example Client Side:

```
from hayrack import transport

#create a receiver
rcvr = transport.ZeroMQReceiver(connect_host_tuples=[('127.0.0.1', '5000')])
rcvr.connect()

#receive a single message
message = rcvr.get()

rcvr.close()
```

The client side receiver creates a ZeroMQ PULL socket that can connect to 1 or more ZeroMQ sockets, and pull messages across the socket.

### Installing and running Hayrack.

Hayrack can be used as a library as shown above or run as an application.  To build a debian package for Hayrack you can run [make_deb.sh](https://github.com/ProjectMeniscus/hayrack/blob/master/make_deb.sh) file included in the repo.  This will create a configuration file at [/etc/hayrack/hayrack.conf](https://github.com/ProjectMeniscus/hayrack/blob/master/pkg/layout/etc/hayrack/hayrack.conf) that will allow you to configure the Hayrack server.  When installed the server can be run using [/usr/share/hayrack/bin/run.py](https://github.com/ProjectMeniscus/hayrack/blob/master/pkg/layout/usr/share/hayrack/bin/run.py).

The initial intended use for this application is to serve as a transport mechanism for logging-as-a-service. Hayrack is used to receive messages from a local Syslog-NG server on STDIN and then load balance these messages over ZeroMQ to downstream worker nodes for processing.

The Chef cookbook [syslogng-transport](https://github.com/ProjectMeniscus/chef-cookbooks/tree/master/cookbooks/syslogng-transport) can be used for deploying Hayrack with Syslog-NG.