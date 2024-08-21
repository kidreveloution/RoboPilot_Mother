import zmq
import keyboard
import sys
import time
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
# Set up ZMQ

# Initial values
power = 0.00
steering = 0.15
power_step = 5.00  # Amount to increase/decrease per step
steering_step = 0.01  # Amount to increase/decrease per step

def messagePrint(msg):
    print(msg)

zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="MOTHER",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=messagePrint
)

print(zmqObj.connectZMQ())
zmqObj.startListenThread()

zmqObj.sendMessage(RX_ID="ROUTER",msg_name="getRegister",content=None)
#zmqObj.stopListenThread()




# Main loop
RX_ID = "fake_worker_1"
zmqObj.sendMessage(RX_ID=RX_ID,msg_name="steering",content=0.15)
# try:
#     while True:
#         if keyboard.is_pressed('w'):
#             power = min(100.00, power + power_step)  # Increase power, max 100
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="power",content=power)
#             #zmqObj.sendMessage("power", power)
#         elif keyboard.is_pressed('s'):
#             power = max(-100.00, power - power_step)  # Decrease power, min -100
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="power",content=power)

#             #zmqObj.sendMessage("power", power)
#         else:
#             power = 0.00  # Stop power when neither W nor S is pressed
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="power",content=power)

#             #zmqObj.sendMessage("power", power)

#         if keyboard.is_pressed('a'):
#             steering = max(0.10, steering - steering_step)  # Decrease steering, min 0.10
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="steering",content=steering)

#             #zmqObj.sendMessage("steering", steering)
#         elif keyboard.is_pressed('d'):
#             steering = min(0.20, steering + steering_step)  # Increase steering, max 0.20
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="steering",content=steering)
#         else:
#             steering = 0.15  # Reset steering to default when neither A nor D is pressed
#             zmqObj.sendMessage(RX_ID=RX_ID,msg_name="steering",content=steering)

#         time.sleep(0.1)  # Small delay to control the rate of change

# except KeyboardInterrupt:
#     print("Program interrupted")
#     sys.exit()
