import cv2


def run_surveillance():
    print("Starting Home Surveillance Assistant...")

    # Attempt to open the default camera (usually webcam, index 0)
    # If you have an IP camera, you can replace 0 with its RTSP or HTTP stream URL
    # e.g., "rtsp://username:password@ip_address:port/stream_path"
    # or "http://ip_address/video.mjpg"
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Video stream opened. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        cv2.imshow("Live Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Surveillance stopped.")


if __name__ == "__main__":
    run_surveillance()
