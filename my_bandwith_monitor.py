# Written by Jacob Clouse

# Original Idea Inspired by -> https://github.com/karan/Projects#networking
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import psutil
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables & Setup
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Create a Tkinter window
root = tk.Tk()
root.title("Bandwidth Monitor")

# Create a Figure object to display the graph
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlabel('Time')
ax.set_ylabel('Data Usage (Bytes)')

# Create a Canvas widget to display the graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initialize variables for tracking data usage
prev_down = psutil.net_io_counters().bytes_recv
prev_up = psutil.net_io_counters().bytes_sent

# Create labels for displaying current upload and download data
download_label = tk.Label(root, text="Download: 0 bytes")
download_label.pack(side=tk.BOTTOM, pady=5)
upload_label = tk.Label(root, text="Upload: 0 bytes")
upload_label.pack(side=tk.BOTTOM, pady=5)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to print out my Logo ---
def myLogo():
    theDateTime = defang_datetime()
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Jackie Caldwell-Firstiun and Jesse Firstiun")
    print(f"Current datetime: {theDateTime}")


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

# --- Function to update the graph with current data usage ---
def update_graph():
    global prev_down, prev_up
    # Get current data usage
    current_down = psutil.net_io_counters().bytes_recv
    current_up = psutil.net_io_counters().bytes_sent
    # Calculate data usage since last update
    down = current_down - prev_down
    up = current_up - prev_up
    prev_down = current_down
    prev_up = current_up
    # Add data usage to graph
    ax.plot([time.time()], [down+up], 'bo')

    # Update labels with current data usage
    download_label.config(text="Download: {} bytes".format(current_down))
    upload_label.config(text="Upload: {} bytes".format(current_up))
    
    # Refresh the graph
    canvas.draw()
    # Schedule the function to run again in 1 second
    root.after(1000, update_graph)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

myLogo()

# Schedule the function to run in 1 second
root.after(1000, update_graph)

# Run the Tkinter event loop
root.mainloop()