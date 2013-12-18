# Hayrack

A tool for capturing syslog messages from STDIN, such as when run as a program destination by Syslog-NG, and pushing messages over ZeroMQ to downstream hosts.

Example Hayrack Server:

```
from hayrack import server

#start the IO Loop to read from STDIN
server.start_io('127.0.0.1', '5000')
```

The IO Loop will block the current process.  The server binds to a ZeroMQ PUSH socket and forwards all messages received via STDIN.  The server has a signal handler that will properly close sockets of a sigterm is recevied.