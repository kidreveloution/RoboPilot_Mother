import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
import time
import logging
import random
import json

logging.basicConfig(filename='fakeWorker.log', level=logging.DEBUG)

def handleMessage(val):
    logging.info(f"Received message: {val}")
    print(val)

def generate_fake_gps():
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    return lat, lon

# Create ZMQ_CONNECTION objects
zmqObj1 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_1", "ROUTER", "tcp://3.22.90.156:5555", handleMessage)
zmqObj2 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_2", "ROUTER", "tcp://3.22.90.156:5555", handleMessage)
zmqObj3 = zmqHeader.ZMQ_CONNECTION("FAKE_WORKER_3", "ROUTER", "tcp://3.22.90.156:5555", handleMessage)

workers = [zmqObj1, zmqObj2, zmqObj3]

for i, worker in enumerate(workers, 1):
    logging.info(f"Attempting to connect zmqObj{i}")
    if worker.connectZMQ():
        logging.info(f"zmqObj{i} connected successfully")
        worker.startListenThread()
        logging.info(f"zmqObj{i} listen thread started")
        
        # Test sending a message
        try:
            worker.sendMessage(RX_ID="MOTHER", msg_name="TEST", content=f'{{"test":"message from FAKE_WORKER_{i}"}}')
            logging.info(f"Test message sent from zmqObj{i}")
        except Exception as e:
            logging.error(f"Error sending test message from zmqObj{i}: {e}")
    else:
        logging.error(f"Failed to connect zmqObj{i}")

# Keep the script running
while True:
    for i, worker in enumerate(workers, 1):
        try:
            lat, lon = generate_fake_gps()
            content = json.dumps({
                "lat": str(lat),
                "lon": str(lon),
            })
            worker.sendMessage(RX_ID="MOTHER", msg_name="GPS", content=content)
            logging.info(f"GPS message sent from zmqObj{i}: {content}")
        except Exception as e:
            logging.error(f"Error sending GPS message from zmqObj{i}: {e}")
    
    time.sleep(3)
    logging.info("Script still running...")