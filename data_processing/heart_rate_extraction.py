import cv2
import numpy as np
from scipy.signal import find_peaks
import time
from collections import deque

class HeartRateExtractor:
    def __init__(self, duration=10, frame_rate=30):
        self.duration = duration
        self.frame_rate = frame_rate
        self.frames = deque(maxlen=int(duration * frame_rate))
        self.heart_rate_buffer = deque(maxlen=10)
        self.heart_rate = 0
        self.heart_rate_text = "Estimated Heart Rate: - BPM"
        self.heart_rate_timer = time.time()

    def extract_green_channel(self, frame):
        green_channel = frame[:, :, 1]
        return np.mean(green_channel)

    def estimate_heart_rate(self, frame):
        self.frames.append(frame)
        time_diff = time.time() - self.heart_rate_timer
            
        if time.time() - self.heart_rate_timer >= 1:
            green_channel_values = []
    
            for frame in self.frames:
                green_channel_value = self.extract_green_channel(frame)
                green_channel_values.append(green_channel_value)
            
            peaks, _ = find_peaks(green_channel_values, height=10)
            
            if len(peaks) < 2:
                print("Not enough peaks")
            else:
                time_per_frame = 1 / self.frame_rate
                self.heart_rate = 60 / (np.mean(np.diff(peaks)) * time_per_frame)
                self.heart_rate_buffer.append(self.heart_rate)
                print(f"Estimated Heart Rate: {round(np.mean(self.heart_rate_buffer), 2)} BPM")
                
            self.heart_rate_timer = time.time()

    def cleanup(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    duration = 10
    frame_rate = 30
    hr_extractor = HeartRateExtractor(duration, frame_rate)
    
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hr_extractor.estimate_heart_rate(frame)
        heart_rate_text = f"Estimated Heart Rate: {round(hr_extractor.heart_rate, 2)} BPM"
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, heart_rate_text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    hr_extractor.cleanup()
