import cv2
import numpy as np
from scipy.signal import find_peaks
import time
from collections import deque
import mediapipe as mp

class HeartRateExtractor:
    def __init__(self, duration=10):
        self.duration = duration
        self.frames = []
        self.heart_rate_buffer = deque(maxlen=10)
        self.heart_rate = 0
        self.heart_rate_text = "Estimated Heart Rate: - BPM"
        self.heart_rate_timer = time.time()
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    def extract_green_channel(self, frame):
        green_channel = frame[:, :, 1]
        return np.mean(green_channel)

    def estimate_heart_rate(self):
        if len(self.frames) < 2:
            return 0

        green_channel_values = [self.extract_green_channel(frame) for frame in self.frames]

        peaks, _ = find_peaks(green_channel_values, height=10)

        if len(peaks) < 2:
            return 0

        time_diff = time.time() - self.heart_rate_timer
        self.heart_rate = 60 / (np.mean(np.diff(peaks)) * time_diff)
        self.heart_rate_buffer.append(self.heart_rate)
        print(f"Estimated Heart Rate: {round(np.mean(self.heart_rate_buffer), 2)} BPM")
        self.heart_rate_timer = time.time()

    def extract_head_region(self, frame):
        results = self.face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                head_region = frame[y:y+h, x:x+w].copy()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Display the ROI in blue
                return head_region
        return None

    def cleanup(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    duration = 10
    hr_extractor = HeartRateExtractor(duration)
    
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        head_region = hr_extractor.extract_head_region(frame)
        if head_region is not None:
            hr_extractor.frames.append(head_region)
        hr_extractor.estimate_heart_rate()

        heart_rate_text = f"Estimated Heart Rate: {round(hr_extractor.heart_rate, 2)} BPM"
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, heart_rate_text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    hr_extractor.cleanup()
