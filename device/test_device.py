import signal, zmq, json


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


class test_device(object):

    __slots__ = ["__socket", "__addr", "__codes"]

    def __init__(self, config=None):
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)
        with open(config) as json_data:
            data = json.load(json_data)
        self.__codes = list(data["codes"].values())
        self.__addr = "ipc://@domi_smarthome/pub"
        context = zmq.Context()
        self.__socket = context.socket(zmq.SUB) #(PUB / PUSH)
        self.__socket.connect(self.__addr)
        self.__socket.subscribe("")

        while True:
            try:
                message = self.__socket.recv_json(flags = 1)
                for codes in self.__codes:
                    if message["code"] in codes:
                        print(message)
            except:
                continue
           
    def service_shutdown(self, signum, frame):
        print("Caught signal %d" % signum)
        #self.__socket.unsubscribe("")
        self.__socket.close()
        raise ServiceExit


if __name__ == "__main__":
    path = "config/kerui_w18.config"
    test_device(config=path)
