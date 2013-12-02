import os
import sys

for path in os.walk('/usr/share/hayrack/lib/python'):
    sys.path.append(path[0])

from hayrack import config
from hayrack import log

cfg = config.get_config()
log.configure_logging(cfg)

from hayrack import server


if __name__ == '__main__':
    server.start_io(cfg.core.zmq_bind_host, cfg.core.zmq_bind_port)
