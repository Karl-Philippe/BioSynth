import cv2
from collections import deque
from data_processing import heart_rate_extraction, hand_pose_estimation
from audio import synth
from interface import user_interface
from time import sleep

def main():
    # Initialize the video capture object
    vid = cv2.VideoCapture(0)  # You can change the video source as needed

    # Initialize the heart rate extraction module
    frame_rate = 10
    hr_extractor = heart_rate_extraction.HeartRateExtractor(frame_rate)

    # Initialize the hand pose estimation module
    pose_estimator = hand_pose_estimation.HandPoseEstimator()

    # Initialize the SuperCollider controller
    sc_controller = synth.Synth()
    
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)

    # Initialize the user interface
    ui = user_interface.UserInterface(frame)

    def update_ui():
        # Capture the current frame
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)

        # Append the current frame to the buffer
        #frame_buffer.append(frame)

        # Capture and process the frame for heart rate extraction
        heart_rate = hr_extractor.estimate_heart_rate(frame)

        # Capture and process the frame for hand pose estimation
        hand_positions, hand_landmarks = pose_estimator.estimate_hand_pose(frame)
        
        if hand_positions is not None:
            frame, bbox_center, bbox_area = pose_estimator.compute_bounding_box(frame, hand_landmarks)
            hand_positions = bbox_center
        
        # Update the UI with the latest frame, heart rate, and hand position
        ui.update_interface(frame, heart_rate, hand_positions)

        # Update the SuperCollider audio based on the data received
        sc_controller.update_sound(heart_rate, hand_positions)

        # Check for user input or exit conditions
        if ui.check_for_exit():
            ui.cleanup()
            return

        ui.root.after(100, update_ui)  # Schedule the function to run again
        
    # Create a deque to store the last 100 frames
    #sframe_buffer = deque(maxlen=20)

    #ret, frame = vid.read()
    #frame_buffer.append(frame)  # Initialize the frame_buffer with the first frame

    update_ui()  # Start the update_ui function

    ui.root.mainloop()  # Start the tkinter main event loop

    # Release the video capture object
    vid.release()

    # Cleanup and close other components
    hr_extractor.cleanup()
    pose_estimator.cleanup()
    sc_controller.cleanup()
    ui.cleanup()

if __name__ == "__main__":
    main()
