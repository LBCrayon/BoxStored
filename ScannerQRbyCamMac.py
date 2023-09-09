import cv2
from pyzbar.pyzbar import decode


def scan_qr_code(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", obj.data.decode("utf-8"))
        print()


def main():
    cap = cv2.VideoCapture(0)  # Open the default camera (camera index 0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame (optional, comment out if not needed)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

        # Convert the frame to grayscale for decoding
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Scan QR codes in the frame
        scan_qr_code(gray)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
