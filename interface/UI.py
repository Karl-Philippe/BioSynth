import tkinter as tk
import cv2
from PIL import Image, ImageTk
import multiprocessing

class UserInterface:
    def __init__(self, video_source=0):
        self.root = tk.Tk()
        self.root.title("User Interface")

        # Create an OpenCV video capture object
        self.vid = cv2.VideoCapture(video_source)

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        # Create labels for heart rate (BPM) and hand position
        self.label_heart_rate = tk.Label(self.root, text="Heart Rate (BPM): 0")
        self.label_heart_rate.pack()

        self.label_hand_position = tk.Label(self.root, text="Hand Position: N/A")
        self.label_hand_position.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.cleanup)
        self.quit_button.pack()

        # Initialize variables to store the frame, heart rate, and hand positions
        self.frame = None
        self.bpm = 0
        self.hand_position = "N/A"

        # Schedule the update method to run periodically
        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Display the video frame in the canvas
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.photo = photo

            # Update the labels for heart rate and hand position
            self.label_heart_rate.config(text="Heart Rate (BPM): " + str(self.bpm))
            self.label_hand_position.config(text="Hand Position: " + str(self.hand_position))

        # Schedule the update method to run periodically
        self.root.after(10, self.update)

    def update_interface(self, frame, bpm, hand_position):
        # Update the frame, BPM, and hand position values
        self.frame = frame
        self.bpm = bpm
        self.hand_position = hand_position

    def check_for_exit(self):
        # Implement your exit logic here, e.g., based on a button press
        return False

    def cleanup(self):
        self.vid.release()
        self.root.destroy()

if __name__ == "__main__":
    # If you run user_interface.py as a standalone script for testing
    ui = UserInterface()
    ui.root.mainloop()
