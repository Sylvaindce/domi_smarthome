#!/usr/bin/env python3

import os, sys, argparse

__proj_base_path = os.path.dirname(os.path.realpath(__file__))
None if __proj_base_path in sys.path else sys.path.insert(0, __proj_base_path)

## FIX because of the dash in the folder name
sys.path.insert(0, os.path.realpath("lib/rpi-rf/"))
import rpi_rf.rpi_rf as rpi_rf
import zmq

class domi_smarthome(object):

    def __init__(self):
        zmq_context = zmq.Context()
        self.__domi_zmq_pub = zmq_context.socket(zmq.PUB)
        self.__domi_zmq_pub.bind("ipc://@domi_smarthome/pub")
        while True:
            self.__domi_zmq_pub.send_json({"code" : 8665554})
        
        #self.__rf_receiver = rpi_rf.RFDevice(11)
        
if __name__ == "__main__":
    domi_smarthome()