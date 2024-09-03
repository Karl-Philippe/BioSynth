import cv2
import mediapipe as mp

class HandPoseEstimator:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def estimate_hand_pose(self, frame):
        # Process the provided frame for hand pose estimation
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            # Assuming you want to track the position of the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]
            # Extract hand positions from hand_landmarks
            hand_positions = [landmark.x for landmark in hand_landmarks.landmark]  # Modify as needed

            return hand_positions, hand_landmarks
        else:
            return None, None

    def compute_bounding_box(self, frame, hand_landmarks):
        bbox_center = None
        bbox_area = None

        if hand_landmarks is not None:
            min_x = min(landmark.x for landmark in hand_landmarks.landmark)
            max_x = max(landmark.x for landmark in hand_landmarks.landmark)
            min_y = min(landmark.y for landmark in hand_landmarks.landmark)
            max_y = max(landmark.y for landmark in hand_landmarks.landmark)
            min_x, max_x, min_y, max_y = int(min_x * frame.shape[1]), int(max_x * frame.shape[1]), int(min_y * frame.shape[0]), int(max_y * frame.shape[0])
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)  # Green bounding box

            # Compute the center of the bounding box
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red circle at the center

            # Compute the area of the bounding box
            bbox_area = (max_x - min_x) * (max_y - min_y)

            # Set bbox_center to be a tuple of center_x and center_y
            bbox_center = (center_x, center_y)

        return frame, bbox_center, bbox_area

    def cleanup(self):
        pass

if __name__ == "__main__":
    hand_estimator = HandPoseEstimator()

    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 for the default camera

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            break

        hand_positions, hand_landmarks = hand_estimator.estimate_hand_pose(frame)
        if hand_positions is not None:
            frame, bbox_center, bbox_area = hand_estimator.compute_bounding_box(frame, hand_landmarks)
            #print(f"Hand Positions: {hand_positions}")

            if bbox_center is not None:
                print(f"Bounding Box Center: {bbox_center}")
            if bbox_area is not None:
                print(f"Bounding Box Area: {bbox_area}")

        frame = cv2.flip(frame, 1)
        cv2.imshow("Hand Pose Estimation", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
