import tkinter as tk
import cv2
from PIL import Image, ImageTk

class UserInterface:
    def __init__(self, frame):
        self.root = tk.Tk()
        self.root.title("User Interface")

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
        self.frame = frame
        self.bpm = 0
        self.hand_position = "N/A"

        # Schedule the update method to run periodically
        self.update()

    def update(self):
        # Display the video frame in the canvas
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.photo = photo

        # Update the labels for heart rate and hand position
        self.label_heart_rate.config(text="Heart Rate (BPM): " + str(round(self.bpm, 2)))
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
        self.root.destroy()

if __name__ == "__main__":
    # If you run user_interface.py as a standalone script for testing
    vid = cv2.VideoCapture(0)
   
    ret, frame = vid.read()
    
    ui = UserInterface(frame)
    
    def update_ui():
        # Capture the current frame
        ret, frame = vid.read()
        if ret:
            # Update the UI with the latest frame, heart rate, and hand position
            ui.update_interface(frame, 0, "N/A")

            # Check for user input or exit conditions
            if ui.check_for_exit():
                ui.cleanup()
                return
        ui.root.after(10, update_ui)  # Schedule the update_ui function to run periodically

    update_ui()  # Start the update_ui function

    ui.root.mainloop()  # Start the tkinter main event loop

    # Release the video capture object
    vid.release()
