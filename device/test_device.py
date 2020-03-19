import signal, zmq


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


class test_device(object):

    __slots__ = ["__socket", "__addr"]

    def __init__(self):
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)

        self.__addr = "ipc://@domi_smarthome/pub"
        context = zmq.Context()
        self.__socket = context.socket(zmq.SUB) #(PUB / PUSH)
        self.__socket.connect(self.__addr)
        self.__socket.subscribe("")

        while True:
            try:
                message = self.__socket.recv_json()
            except:
                continue
            print(message)

    def service_shutdown(self, signum, frame):
        print("Caught signal %d" % signum)
        self.__socket.unsubscribe("")
        self.__socket.close()
        raise ServiceExit
        

if __name__ == "__main__":
    server = test_device()