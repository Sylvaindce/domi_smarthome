import sys, os, time
from threading import Thread

__lib_path = os.path.realpath("../lib/rpi-rf/")
None if __lib_path in sys.path else sys.path.insert(0, __lib_path)

import rpi_rf.rpi_rf as rpi_rf
import zmq


class transmitter(Thread):

    def __init__(self, callback=None, gpio=17, zmq_addr="ipc://@domi_smarthome/sub"):
        Thread.__init__(self)
        self.__init_rf(gpio)
        self.__init_zmq(zmq_addr)
        self.__run = False
        self.__callback = callback

    def __init_rf(self, gpio):
        self.__rf_snd = rpi_rf.RFDevice(gpio)
        self.__rf_snd.enable_tx()
        self.__rf_snd.tx_repeat = 50

    def __init_zmq(self, zmq_addr):
        zmq_context = zmq.Context()
        self.__domi_zmq_sub = zmq_context.socket(zmq.SUB)
        self.__domi_zmq_sub.bind(zmq_addr)
        self.__domi_zmq_sub.subscribe("")


    def __get_data(self):
        print("[Transmitter] Start")
        while self.__run:
            msg = self.__domi_zmq_sub.recv_json()
            print("[Transmitter]", msg)
            try:
                #self.__rf_snd.enable_tx()
                #self.__rf_snd.tx_repeat = 10
                self.__rf_snd.tx_code(msg.get("code", 0), msg.get("protocol", None), msg.get("pulse_length", None), msg.get("lenght", None))
                #self.__rf_snd.disable_tx()
            except Exception as ex:
                print(ex)
                pass
            time.sleep(0.01)

    def run(self):
        self.__run = True
        self.__get_data()

    def stop(self):
        self.__run = False
        self.__rf_snd.cleanup()
        print("[Transmitter] Stop")
