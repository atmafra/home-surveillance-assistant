import cv2
from .camera_discovery import discover_cameras


def run_surveillance(ip_prefix: str = "192.168.15."):
    print("Starting Home Surveillance Assistant...")

    print("Discovering cameras on the local network...")
    potential_cameras = discover_cameras(ip_prefix=ip_prefix)
    if potential_cameras:
        print("Potential cameras found:")
        for camera in potential_cameras:
            print(f"IP: {camera['ip']}, Port: {camera['port']}")
    else:
        print("No potential cameras found on the network via basic port scan.")

    # Attempt to open the default camera (usually webcam, index 0)
    # If you have an IP camera, you can replace 0 with its RTSP or HTTP stream URL
    # e.g., "rtsp://username:password@ip_address:port/stream_path"
    # or "http://ip_address/video.mjpg"
    print("\nAttempting to open the default camera (index 0)...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Camera opened successfully. Press 'q' to stop the surveillance.")

    while True:
        # Only process frames if the camera was successfully opened
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break
        else:  # If default camera failed, maybe we just wait or handle network cameras
            if not potential_cameras:  # If no cameras at all, then break
                print("No cameras available to stream.")
                break
            # Add a small delay or a different logic if only network cameras are expected
            cv2.waitKey(100)  # Wait a bit before next loop iteration
            continue  # Skip frame processing if cap is not opened

        cv2.imshow("Live Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    print("Surveillance stopped.")


if __name__ == "__main__":
    run_surveillance()
