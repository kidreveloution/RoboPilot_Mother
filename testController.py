import pygame

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Detect the first joystick (assuming the T16XS is connected as the first device)
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    exit()

joystick = pygame.joystick.Joystick(0)  # Get the first joystick
joystick.init()

# Print joystick information
print(f"Joystick: {joystick.get_name()}")
print(f"Number of Axes: {joystick.get_numaxes()}")
print(f"Number of Buttons: {joystick.get_numbuttons()}")
print(f"Number of Hats: {joystick.get_numhats()}")

# Main loop
running = True
while running:
    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for joystick button press
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")

        if event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")

        # Check for joystick movement on any axis
        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            value = joystick.get_axis(axis)
            print(f"Axis {axis} moved to {value:.2f}")

        # Check for hat (D-pad) movement
        if event.type == pygame.JOYHATMOTION:
            hat = event.hat
            value = joystick.get_hat(hat)
            print(f"Hat {hat} moved to {value}")

# Quit Pygame
pygame.quit()
