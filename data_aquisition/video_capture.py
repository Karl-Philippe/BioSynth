import cv2
import multiprocessing



def capture_frames(shared_queue, video_source=0):
    # Create a video capture object
    vid = cv2.VideoCapture(video_source)

    while True:
        ret, frame = vid.read()
        if not ret:
            # If there's an issue with capturing frames, you can handle it here
            break

        # Put the frame in the shared queue for other processes to access
        shared_queue.put(frame)

    # Release the video capture object when done
    vid.release()

if __name__ == "__main__":
    # If you run video_capture.py as a standalone script for testing
    frame_queue = multiprocessing.Queue()
    capture_process = multiprocessing.Process(target=capture_frames, args=(frame_queue,))
    capture_process.start()

    while True:
        try:
            frame = frame_queue.get()
            # Do something with the captured frame (for testing purposes)
            cv2.imshow("Captured Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    capture_process.terminate()
    cv2.destroyAllWindows()
