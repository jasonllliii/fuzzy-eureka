import pystray
import keyboard
from PIL import Image
import tkinter as tk
from rect_screenshot_test import ScreenshotApp

# Function to trigger when "Ctrl+Shift+A" is pressed
def on_hotkey_a():
    print("Hotkey pressed!\ta")
    # Create a new toplevel window instead of a new root
    ScreenshotApp(root)
    # top = tk.Toplevel(root)
    # top.title("Tkinter Window")
    # top.geometry("300x200")
    # tk.Label(top, text="This is a Tkinter window").pack()
    # top.deiconify()

# Function to trigger when "Ctrl+Shift+Q" is pressed
def on_hotkey_q():
    print("Hotkey pressed!\tq")
    # Optional: Add quit functionality
    # icon.stop()
    # root.quit()

# Function to quit the script when "Quit" is selected from the tray menu
def quit_function(icon, item):
    icon.stop()
    # root.quit()  # Also stop the Tkinter event loop

# Create a simple blue square image for the tray icon
image = Image.new("RGB", (64, 64), color="blue")

# Create a menu with a "Quit" option
menu = pystray.Menu(pystray.MenuItem("Quit", quit_function))

# Run the application
if __name__ == "__main__":
    # Set up the Tkinter root window once and hide it initially
    root = tk.Tk()
    root.withdraw()  # Hide the root window until needed

    # Register the hotkeys
    keyboard.add_hotkey("ctrl+shift+a", on_hotkey_a)
    keyboard.add_hotkey("ctrl+shift+q", on_hotkey_q)

    # Set up and run the tray icon in a separate thread
    icon = pystray.Icon("my_app", image, menu=menu)
    icon.run_detached()  # Runs pystray in a separate thread

    # Start the Tkinter event loop in the main thread
    root.mainloop()