import argparse
import logging
import time

import zmq
import msgpack

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen", help="listen", required=True,
            action="store", type=str, metavar="URL")
    args = parser.parse_args()

    lognum = getattr(logging, "INFO")
    logging.basicConfig(format='{asctime} {levelname} {module} {message}',
            style='{', level=lognum)

    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind(args.listen)
    send_msg = {"key1": "val1", "key2": 2}
    send_bin = msgpack.packb(send_msg)

    while True:
        try:
            recv_msg = msgpack.unpackb(sock.recv(), encoding='utf-8')
            LOG.info("Received as REQ: %s", recv_msg)

            sock.send(send_bin)
            LOG.info("Sent as REP: %s", send_msg)

        except KeyboardInterrupt:
            break
