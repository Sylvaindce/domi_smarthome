import signal, time, zmq

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


class client_pub(object):

    def __init__(self, zmq_addr = "tcp://127.0.0.1:5000",  code="0"):
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)

        context = zmq.Context()
        self.__socket = context.socket(zmq.PUB)
        self.__socket.connect(zmq_addr)

        while True:
            self.__socket.send_json({"code" : code, "pulse_length" : 318})
            time.sleep(5)

    def service_shutdown(self, signum, frame):
        print("Caught signal %d" % signum)
        self.__socket.close()
        raise ServiceExit

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--zmq_addr", type=str, help="ZMQ addr")
    parser.add_argument("--code", type=int, help="Code to send")

    args = parser.parse_args()
    if args.code and args.zmq_addr:
        client_pub(zmq_addr = args.zmq_addr, code = args.code)
    elif args.code and not args.zmq_addr:
        client_pub(code = args.code)
