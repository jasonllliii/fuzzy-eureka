import pystray
import tkinter as tk
import keyboard
from PIL import Image

# Function to trigger when hotkey is pressed
def on_hotkey():
    print("Hotkey pressed!")

# Create a simple blue square image for the tray icon
image = Image.new('RGB', (64, 64), color='blue')

# Function to quit the script when "Quit" is selected
def quit_function(icon):
    icon.stop()

# Create a menu with a "Quit" option
menu = pystray.Menu(pystray.MenuItem('Quit', quit_function))

# Register the hotkey (Ctrl+Shift+A)
keyboard.add_hotkey('ctrl+shift+a', on_hotkey)

# Set up and run the tray icon
icon = pystray.Icon('my_app', image, menu=menu)
icon.run()