import cv2
import numpy as np
from scipy.signal import find_peaks
import time

# Function to extract the average green channel value from a frame
def extract_green_channel(frame):
    green_channel = frame[:, :, 1]
    return np.mean(green_channel)

# Function to estimate the heart rate
def estimate_heart_rate(frames, frame_rate):
    green_channel_values = []
    
    for frame in frames:
        green_channel_value = extract_green_channel(frame)
        green_channel_values.append(green_channel_value)
    
    # Perform peak detection to find the heart rate
    peaks, _ = find_peaks(green_channel_values, height=10)
    time_per_frame = 1 / frame_rate
    heart_rate = 60 / (np.mean(np.diff(peaks)) * time_per_frame)
    
    return heart_rate

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the frame rate and initialize variables
frame_rate = 30  # Adjust based on your webcam's frame rate
frames_to_capture = 300  # You can adjust this number
frames = []

# Capture frames
for i in range(frames_to_capture):
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Estimate the heart rate
heart_rate = estimate_heart_rate(frames, frame_rate)
print(f"Estimated Heart Rate: {heart_rate} BPM")

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
