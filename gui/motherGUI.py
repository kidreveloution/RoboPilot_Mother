import zmq
import json
import os
import sys
import tkinter as tk
from tkinter import ttk
import time
import tkinter_Test

# Add the common directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader

def messageDigst(msg):
    try:
        msg = json.loads(msg)
        print("Turned into Json")
    except:
        try:
            msg = eval(msg)
            print("Turned into Dict")
        except Exception as e:
            if isinstance(msg,str):
                return
            print("Neither dict or Json: ",e)
    if msg["msg_name"] == "register":
        createWorker(msg)
    elif msg["msg_name"] == "register_list":
        createWorkers(msg)

# Initialize the ZMQ connection
zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="MOTHER",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=messageDigst
)

zmqObj.connectZMQ()

# Start listening to messages
zmqObj.startListenThread()


def getRegisteredWorkers():
    zmqObj.sendMessage(RX_ID="ROUTER",msg_name="getRegister",content=None)

def createWorker(msg):
    print("Making Worker")

def createWorkers(msg):
    print("Making Workers!")
    print(msg)
    for worker in msg:
        if worker == "msg_name":
            pass
        else:
            tkinter_Test.createButton(worker)

            print(str(worker))

getRegisteredWorkers()


