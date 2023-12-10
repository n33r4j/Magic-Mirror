import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class GifPlayerApp:
    def __init__(self, root, gif_path, trigger_variable):
        self.root = root
        self.gif_path = gif_path
        self.trigger_variable = trigger_variable
        self.gif_frames = []
        self.current_frame = 0

        # Initialize GUI
        self.init_gui()

        # Start background processing (playing the GIF)
        self.background_thread = threading.Thread(target=self.play_gif)
        self.background_thread.start()

    def init_gui(self):
        # Set up the main window
        self.root.title("GIF Player with Background Processing")

        # Create label to display GIF
        self.gif_label = tk.Label(self.root)

        # Load frames from the GIF
        try:
            while True:
                frame = Image.open(self.gif_path)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                frame.seek(frame.tell() + 1)
        except EOFError:
            pass

    def show_frame(self):
        self.gif_label.config(image=self.gif_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.root.after(100, self.show_frame)  # Update every 100 milliseconds

    def play_gif(self):
        while True:
            if self.trigger_variable.get():
                self.show_frame()
                time.sleep(0)  # Adjust the delay as needed
            else:
                time.sleep(1)  # Sleep when the trigger is False to reduce CPU usage

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    trigger_variable = tk.BooleanVar(value=True)  # Set the initial value to True
    
    gif_path = "gifs/loading-doge.gif"  # Replace with the path to your GIF file
    app = GifPlayerApp(root, gif_path, trigger_variable)
    
    # You can change the trigger variable value to open or close the window
    trigger_variable.set(False)  # Set the trigger variable to False to close the window
    
    root.mainloop()
