import zmq
import time
import pygame
import sys
import common.messageBuilder as messageBuilder

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    sys.exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Initialized Joystick: {joystick.get_name()}")
print("Press joystick buttons or move axes. Press any button to exit.")

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://3.22.90.156:5555")
CLIENT_ID = "pc_1"
dealer.send_multipart([CLIENT_ID.encode('utf-8'), b""])

target_worker_id = "car_1"
message = f"Hello from  {CLIENT_ID},bitch".encode('utf-8')
dealer.send_multipart([target_worker_id.encode('utf-8'), message])



while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            value = event.value
            if axis == 3:
                value = 0.05 * (value + 1) + 0.1
                value = format(float(value), ".2f")
                #message = "steering,"+str(value)
                message = messageBuilder.MESSAGE_CLASS(
                    address=CLIENT_ID,
                    msg_name="steering",
                    dest=target_worker_id,
                    content=value
                )
                #dealer.send_multipart([target_worker_id.encode('utf-8'), message.encode('utf-8')])
                dealer.send_multipart([message.dest.encode('utf-8'), message.encode('utf-8')])

                print(f"Axis {event.axis} moved to {value}")
            if axis == 1:
                value = (value * 100)

                if value >= -1 and value <= 1:
                    value = 0.00
                else:
                    value = format(float(value), ".2f")
                
                #message = "power,"+str(value)
                print(f"Axis {event.axis} moved to {value}")

                message = messageBuilder.MESSAGE_CLASS(
                    address=CLIENT_ID,
                    msg_name="power",
                    dest=target_worker_id,
                    content=value
                )
                dealer.send_multipart([message.dest.encode('utf-8'), message.encode('utf-8')])

                #dealer.send_multipart([target_worker_id.encode('utf-8'), message.encode('utf-8')])

                #dealer.send_string("power,"+str(value))



