#!/usr/bin/env python3

import os, sys, argparse, signal, time

__proj_base_path = os.path.dirname(os.path.realpath(__file__))
None if __proj_base_path in sys.path else sys.path.insert(0, __proj_base_path)

import rf_module.receiver as receiver
import rf_module.transmitter as transmitter


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


class domi_smarthome(object):

    def __init__(self):
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)

        self.__canals = [receiver.receiver(callback=self.callback), transmitter.transmitter(callback=self.callback)]

        try:
            for canal in self.__canals:
                canal.start()
            #while self.__canals[0].is_alive():
            #    pass
        except ServiceExit:
            print("Stop Thread")
            for canal in self.__canals:
                canal.stop()
                canal.join()

    def service_shutdown(self, signum, frame):
        print("Caught signal %d" % signum)
        raise ServiceExit

    def callback(self, data):
        print(data)

if __name__ == "__main__":
    domi_smarthome()
