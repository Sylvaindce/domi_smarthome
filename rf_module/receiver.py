import sys, os, time
from threading import Thread

__lib_path = os.path.realpath("../lib/rpi-rf/")
None if __lib_path in sys.path else sys.path.insert(0, __lib_path)

import rpi_rf.rpi_rf as rpi_rf
import zmq


class receiver(Thread):

    def __init__(self, callback=None, gpio=27, zmq_addr="ipc://@domi_smarthome/pub"):
        Thread.__init__(self)
        self.__init_rf(gpio)
        self.__init_zmq(zmq_addr)
        self.__run = False
        self.__callback = callback

    def __init_rf(self, gpio):
        self.__rf_recv = rpi_rf.RFDevice(gpio)
        self.__rf_recv.enable_rx()

    def __init_zmq(self, zmq_addr):
        zmq_context = zmq.Context()
        self.__domi_zmq_pub = zmq_context.socket(zmq.PUB)
        self.__domi_zmq_pub.bind(zmq_addr)

    def __get_data(self):
        timestamp = None
        while self.__run:
            if self.__rf_recv.rx_code_timestamp != timestamp:
                timestamp = self.__rf_recv.rx_code_timestamp
                self.__domi_zmq_pub.send_json({
                    "code" : self.__rf_recv.rx_code,
                    "pulse_length" : self.__rf_recv.rx_pulselength,
                    "protocol" : self.__rf_recv.rx_proto
                    })
            time.sleep(0.01)

    def run(self):
        self.__run = True
        self.__get_data()

    def stop(self):
        self.__run = False
        self.__rf_recv.cleanup()