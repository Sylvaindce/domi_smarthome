#!/usr/bin/env python3

import os, sys, argparse, signal, time

__proj_base_path = os.path.dirname(os.path.realpath(__file__))
None if __proj_base_path in sys.path else sys.path.insert(0, __proj_base_path)

## FIX because of the dash in the folder name
sys.path.insert(0, os.path.realpath("lib/rpi-rf/"))
import rpi_rf.rpi_rf as rpi_rf
import zmq


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

        self.__rf_recv = rpi_rf.RFDevice(27)
        self.__rf_recv.enable_rx()
        timestamp = None

        zmq_context = zmq.Context()
        self.__domi_zmq_pub = zmq_context.socket(zmq.PUB)
        self.__domi_zmq_pub.bind("ipc://@domi_smarthome/pub")

        while True:
            if self.__rf_recv.rx_code_timestamp != timestamp:
                timestamp = self.__rf_recv.rx_code_timestamp
                self.__domi_zmq_pub.send_json({
                    "code" : self.__rf_recv.rx_code,
                    "pulse_length" : self.__rf_recv.rx_pulselength,
                    "protocol" : self.__rf_recv.rx_proto
                    })
            time.sleep(0.01)
            
    def service_shutdown(self, signum, frame):
        print("Caught signal %d" % signum)
        self.__rf_recv.cleanup()
        raise ServiceExit


if __name__ == "__main__":
    domi_smarthome()