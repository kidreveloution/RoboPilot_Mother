import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Workers Panel")

# Set the size of the window to be mid-sized
root.geometry("400x300")  # Width x Height in pixels

# Create a frame to represent the "Workers" panel
workers_frame = tk.Frame(root, bg="lightgray")
workers_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add a label to the workers panel
label = tk.Label(workers_frame, text="Workers Panel", font=("Arial", 16))
label.grid(row=0, column=0, columnspan=4, pady=20)

# Variable to keep track of the currently selected button
selected_button = None

# Variable to keep track of the current position for new buttons
button_count = 0

def on_button_click(button):
    global selected_button
    
    # Deselect the previously selected button
    if selected_button:
        selected_button.config(relief="raised", bg="SystemButtonFace")
    
    # Select the new button
    button.config(relief="sunken", bg="lightblue")
    selected_button = button

# Function to create a new button dynamically
def createButton(name):
    global button_count
    
    row = button_count // 4 + 1  # Calculate row based on button count
    col = button_count % 4  # Calculate column based on button count
    
    button = tk.Button(workers_frame, text=name, font=("Arial", 14))
    button.config(command=lambda b=button: on_button_click(b))
    button.grid(row=row, column=col, padx=5, pady=5)
    
    button_count += 1  # Increment button count

# Run the application
root.mainloop()
