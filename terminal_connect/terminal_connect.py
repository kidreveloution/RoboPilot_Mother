import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
import pygame
import sys
import json
import common.messageBuilder as messageBuilder

RX_ID = None
zmqObj = None
connectedToRouter = False
worker_objects = {}

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    pass
    #print("No joystick detected.")
    #exit()
else:
    joystick = pygame.joystick.Joystick(0)  # Get the first joystick
    joystick.init()

class workerObject:
    def __init__(self, worker_id=None, gps=None, ip=None):
        self.worker_id = worker_id
        self.ip = ip
        self.gps = gps

def handleMessage(var):
    """Write the received message to a text file."""
    try:
        var = var.replace("'", '"')
        python_dict = json.loads(var)
        if python_dict["msg_name"] == "register_list":
            #print(python_dict["content"])
            for worker in python_dict["content"]:
                worker_id = worker
                ip = python_dict["content"][worker]
                if worker_id not in worker_objects:
                    worker_obj = workerObject(worker_id=worker_id, ip=ip)
                    worker_objects[worker_id] = worker_obj
            print("\n")
            for worker_id, obj in worker_objects.items():
                print(f"Worker ID: {obj.worker_id}, IP: {obj.ip}, GPS: {obj.gps}")
        if python_dict["msg_name"] == "GPS":
            worker_id = python_dict["tx_id"]
            worker_objects[worker_id].gps = python_dict["content"]
    except:
        pass
    # with open("messages_log.txt", "a") as file:
    #     file.write(f"{var}\n")


class GLOBAL:
    zmqObj = zmqHeader.ZMQ_CONNECTION(TX_ID="MOTHER",RX_ID="ROUTER",SERVER_IP="tcp://3.22.90.156:5555",message_handler=handleMessage)

def startTransmission(bot_id):
    running = True  # Flag to control the while loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value

                if axis == 3:
                    value = 0.05 * (value + 1) + 0.1
                    value = format(float(value), ".2f")
                    GLOBAL.zmqObj.sendMessage(RX_ID=bot_id, msg_name="steering", content=value)
                    print(f"Axis {event.axis} moved to {value}")

                if axis == 1:
                    value = (value * 100)
                    if -1 <= value <= 1:
                        value = 0.00
                    else:
                        value = format(float(value), ".2f")
                    print(f"Axis {event.axis} moved to {value}")
                    GLOBAL.zmqObj.sendMessage(RX_ID=bot_id, msg_name="power", content=value)

            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                print("====== QUIT COMMAND, EXITING ======")
                running = False  # Set running to False to exit the while loop
                break  # Exit the for loop

                #if statement for button to abort transmission

def selectBot():
    print("====== Choose Bot ======")
    # Display available worker bots
    for worker_id, obj in worker_objects.items():
        print(f"Worker ID: {obj.worker_id}, IP: {obj.ip}, GPS: {obj.gps}")

    while True:
        # Get user input
        bot_name = input("Choose a bot (by Worker ID): ").strip()

        # Check if the input matches a valid bot ID
        if bot_name in worker_objects:
            print("\nValid Name")
            startTransmission(bot_name)
            break  # Exit the loop after successfully starting the transmission
        else:
            print("\nInvalid Name. Please try again.")

# Example call (ensure worker_objects is defined beforehand)
# selectBot()


def connectRouter():
    try:
        GLOBAL.zmqObj.connectZMQ()
        print("======= Connected to Router =======")
        connectedToRouter = True
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

def clearScreen():
    """Clear the terminal screen."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and Mac
        os.system('clear')

while True:
        clearScreen()  # Clear the screen before showing the menu
        print("\n======= Auto Pilot RC Menu =======")
        print("1. Connect to Router")
        print("2. Start Listening")
        print("3. Get Available Bots")
        print("4. Select Bot to Control")
        print("5. Exit")

        choice = input("Select an option: ")

        clearScreen()  # Clear the screen after making a selection

        if choice == '1':
            connectRouter()
        elif choice == '2':
            startListen()
        elif choice == '3':
            getBots()
        elif choice == '4':
            selectBot()
        elif choice == '5':
            print("Exiting program...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")
        input("\nPress Enter to continue...")  # Wait for user before clearing screen again





