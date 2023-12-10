import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class GifPlayerApp:
    def __init__(self, root, gif_path):
        self.root = root
        self.gif_path = gif_path

        # Load GIF
        self.gif = Image.open(gif_path)
        self.gif_frames = []
        self.current_frame = 0

        # Initialize GUI
        self.init_gui()

        # Start background processing
        self.background_thread = threading.Thread(target=self.background_process)
        self.background_thread.start()

    def init_gui(self):
        # Set up the main window
        self.root.title("GIF Player with Background Processing")

        # Create label to display GIF
        self.gif_label = tk.Label(self.root)
        self.gif_label.pack()

        self.quit_button = tk.Button(root, text="Quit", command=root.destroy)
        self.quit_button.pack() #button to close the window

        # Load frames from the GIF
        try:
            while True:
                frame = self.gif.copy()
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            pass

        # Display the first frame
        self.show_frame()

    def show_frame(self):
        self.gif_label.config(image=self.gif_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.root.after(100, self.show_frame)  # Update every 100 milliseconds

    def background_process(self):
        while True:
            # Your background processing logic goes here
            # For example, simulate some processing by sleeping for 1 second
            time.sleep(1)
            print("Bg process exiting..")
            break

if __name__ == "__main__":
    root = tk.Tk()
    gif_path = "gifs/loading-doge.gif"  # Replace with the path to your GIF file
    app = GifPlayerApp(root, gif_path)
    root.mainloop()