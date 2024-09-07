import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
import time

def handleMessage(val):
    print(val)

zmqObj1 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_1","ROUTER","tcp://3.22.90.156:5555",handleMessage)
zmqObj2 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_2","ROUTER","tcp://3.22.90.156:5555",handleMessage)
zmqObj3 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_3","ROUTER","tcp://3.22.90.156:5555",handleMessage)

zmqObj1.connectZMQ()
zmqObj2.connectZMQ()
zmqObj3.connectZMQ()

workers = [zmqObj1,zmqObj2,zmqObj3]

while True:
    for worker in workers:
        worker.sendMessage(RX_ID="MOTHER",msg_name="GPS",content='{"lat":"42.33","lon":"46.33"}')
        print(worker, " sent message")
        time.sleep(3)