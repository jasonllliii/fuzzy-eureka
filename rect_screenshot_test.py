import tkinter as tk
from PIL import ImageGrab, ImageTk
from screeninfo import get_monitors

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        print("rect_screenshot_test.py")
        # self.root.title("Screenshot Tool")
        # self.button = tk.Button(root, text="Take Screenshot", command=self.take_screenshot)
        # self.button.pack(pady=10)
        
        # Initialize variables
        self.rect_id = None
        self.selection_windows = []
#         self.take_screenshot()
# 
#     def take_screenshot(self):
        """Capture screenshots of all monitors and create selection windows."""
        # self.root.withdraw()  # Hide the main window
        self.selection_windows = []  # Reset selection windows list
        monitors = get_monitors()  # Get list of all monitors
        
        for monitor in monitors:
            # Define the bounding box for the current monitor
            bbox = (monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height)
            screenshot = ImageGrab.grab(bbox=bbox,all_screens=True)  # Capture screenshot for this monitor
            # Create a Toplevel window for this monitor
            selection_window = tk.Toplevel()
            selection_window.overrideredirect(True)  # Remove window borders
            selection_window.attributes('-topmost', True)  # Keep window on top
            selection_window.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            
            # Create a canvas to display the screenshot
            canvas = tk.Canvas(selection_window, width=monitor.width, height=monitor.height)
            canvas.pack()
            photo = ImageTk.PhotoImage(screenshot)
            canvas.create_image(0, 0, image=photo, anchor='nw')
            canvas.image = photo  # Keep reference to prevent garbage collection
            canvas.config(cursor='crosshair')  # Set cursor to crosshair
            
            # Store monitor and screenshot as canvas attributes
            canvas.monitor = monitor
            canvas.screenshot = screenshot
            
            # Bind mouse events for selection
            canvas.bind('<Button-1>', self.start_selection)
            canvas.bind('<B1-Motion>', self.update_selection)
            canvas.bind('<ButtonRelease-1>', self.end_selection)
            
            # Bind cancel options
            selection_window.bind('<Escape>', lambda event: self.close_all_selection_windows())
            canvas.bind('<Button-3>', lambda event: self.close_all_selection_windows())
            
            # Store window details
            self.selection_windows.append({
                'window': selection_window,
                'canvas': canvas,
                'monitor': monitor,
                'screenshot': screenshot,
                'photo': photo
            })

    def start_selection(self, event):
        """Start the selection process on the clicked canvas."""
        self.current_canvas = event.widget
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.current_canvas.delete(self.rect_id)
            self.rect_id = None

    def update_selection(self, event):
        """Update the selection rectangle as the mouse moves."""
        canvas = event.widget
        if self.rect_id:
            canvas.delete(self.rect_id)
        self.rect_id = canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )

    def end_selection(self, event):
        """End the selection, crop the screenshot, and save it."""
        canvas = event.widget
        end_x = event.x
        end_y = event.y
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)
        if right > left and bottom > top:
            screenshot = canvas.screenshot
            cropped_image = screenshot.crop((left, top, right, bottom))
            cropped_image.save('tmp.jpg')
        self.close_all_selection_windows()

    def close_all_selection_windows(self):
        """Close all selection windows and show the main window."""
        for sw in self.selection_windows:
            sw['window'].destroy()
        # self.root.deiconify()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.iconify   ()
    app = ScreenshotApp(root)
    root.mainloop()