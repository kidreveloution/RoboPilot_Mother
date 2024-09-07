import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
import pygame
import sys
import common.messageBuilder as messageBuilder

RX_ID = None
zmqObj = None

def handleMessage(var):
    print(var)

class GLOBAL:
    zmqObj = zmqHeader.ZMQ_CONNECTION(TX_ID="MOTHER",RX_ID="ROUTER",SERVER_IP="tcp://3.22.90.156:5555",message_handler=handleMessage)

def startTransmission(bot_id):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value

                if axis == 3:
                    value = 0.05 * (value + 1) + 0.1
                    value = format(float(value), ".2f")
                    zmqObj.sendMessage(RX_ID=bot_id,msg_name="steering",content=value)
                    print(f"Axis {event.axis} moved to {value}")

                if axis == 1:
                    value = (value * 100)
                    if value >= -1 and value <= 1:
                        value = 0.00
                    else:
                        value = format(float(value), ".2f")
                    print(f"Axis {event.axis} moved to {value}")
                    zmqObj.sendMessage(RX_ID=bot_id,msg_name="power",content=value)

                #if statement for button to abort transmission

def selectBot(bot):
    print("Selected Bot: ",bot)
    RX_ID = bot
    print("======= Hit Abort on Controller to End Transmission =======")
    startTransmission()
    # Start message stream to bot 

def connectRouter():
    try:
        GLOBAL.zmqObj.connectZMQ()
        print("======= Connected to Router =======")
    except:
        print("======= Connection Failed =======")

def startListen():
    try:
        GLOBAL.zmqObj.startListenThread()
        print("======= Started Listen =======")
    except:
        print("======= Listen Failed =======")

def getBots():
    GLOBAL.zmqObj.sendMessage(RX_ID="ROUTER",msg_name="getRegister",content=None)

if __name__ == "__main__":
    print("======= Auto Pilot RC =======")
    print("======= Connecting to Router =======")
    connectRouter()
    print("======= Starting Listen =======")
    startListen()
    print("======= Getting Bots... =======")
    getBots()






