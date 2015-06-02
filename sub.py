import argparse
import logging
import msgpack
import zmq

LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connect", help="host to connect for subscribe",
            required=True, action="append", type=str, metavar="URL")
    args = parser.parse_args()

    lognum = getattr(logging, "INFO")
    logging.basicConfig(format='{asctime} {levelname} {module} {message}',
            style='{', level=lognum)

    context = zmq.Context()
    poller = zmq.Poller()

    for host in args.connect:
        sock = context.socket(zmq.SUB)
        sock.connect(host)
        sock.setsockopt(zmq.SUBSCRIBE, b'')
        poller.register(sock, zmq.POLLIN)

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        for sock in socks:
            recv_msg = msgpack.unpackb(sock.recv(), encoding='utf-8')
            LOG.info("Received: %s", recv_msg)

