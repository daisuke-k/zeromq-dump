import argparse
import logging
import time

import msgpack
import zmq

LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connect", help="host to connect",
            required=True, action="store", type=str, metavar="URL")
    args = parser.parse_args()

    lognum = getattr(logging, "INFO")
    logging.basicConfig(format='{asctime} {levelname} {module} {message}',
            style='{', level=lognum)

    context = zmq.Context()
    
    sock = context.socket(zmq.REQ)
    sock.connect(args.connect)
    req_msg = {"key1": "val1", "key2": 2}

    while True:
        try:
            sock.send(msgpack.packb(req_msg))
            LOG.info("Sent as REQ: %s", req_msg)

            recv_msg = msgpack.unpackb(sock.recv(), encoding='utf-8')
            LOG.info("Received as REP: %s", recv_msg)

            time.sleep(1)
        except KeyboardInterrupt:
            break
