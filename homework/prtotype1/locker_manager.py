import cv2
import serial
import time
import json
import datetime
import requests
from cryptography.fernet import Fernet

# ----- Configuration -----

# Serial port settings: adjust device name and baud rate as needed.
# Common device names on Raspberry Pi 4 are '/dev/serial0' or '/dev/ttyS0'
SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 9600

# Read the encryption key from key.txt
with open('key.txt', 'rb') as key_file:
    KEY = key_file.read()
cipher = Fernet(KEY)

# API endpoint for logging data
API_ENDPOINT = "http://yourserver.com/api/log_data/"

# ----- Initialize Serial Port -----

try:
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)
    print("Opened serial port:", SERIAL_PORT)
except Exception as e:
    print("Error opening serial port:", e)
    raise

# ----- Initialize Camera -----

cap = cv2.VideoCapture(0)  # Adjust camera index if necessary
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Create a QR code detector instance
qrDecoder = cv2.QRCodeDetector()

def check_internet():
    """Check if the internet connection is available."""
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def log_to_server(data):
    """Log data to the server."""
    try:
        response = requests.post(API_ENDPOINT, json=data)
        response.raise_for_status()
        print("Data logged to server successfully")
        return True
    except requests.RequestException as e:
        print(f"Failed to log data to server: {e}")
        return False

def log_locally(data):
    """Log data locally to a file."""
    with open("local_log.txt", "a") as log_file:
        log_file.write(json.dumps(data) + "\n")
    print("Data logged locally")

def process_logs():
    """Process and send local logs to the server if internet is available."""
    if check_internet():
        try:
            with open("local_log.txt", "r") as log_file:
                logs = log_file.readlines()
            with open("local_log.txt", "w") as log_file:
                for log in logs:
                    data = json.loads(log.strip())
                    if not log_to_server(data):
                        log_file.write(log)
        except FileNotFoundError:
            pass

# ----- Main Loop -----

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    # Detect and decode any QR code in the frame
    data, bbox, _ = qrDecoder.detectAndDecode(frame)
    if data:
        print("QR Code detected:", data)
        try:
            # Decrypt the QR code data (which was encrypted as a JSON string)
            decrypted_bytes = cipher.decrypt(data.encode())
            decrypted_str = decrypted_bytes.decode()
            payload = json.loads(decrypted_str)
            print("Decrypted JSON:", payload)
           
            # Check validity based on time (if payload contains start_time and end_time)
            if "start_time" in payload and "end_time" in payload:
                start_time = datetime.datetime.fromisoformat(payload["start_time"])
                end_time = datetime.datetime.fromisoformat(payload["end_time"])
                now = datetime.datetime.now()
                if start_time <= now <= end_time:
                    command = "unlock"
                else:
                    command = "lock"
            else:
                # Default action if time validity is not provided
                command = "unlock"

            # Send the command over UART to the Pi Zero
            ser.write((command + "\n").encode())
            print("Sent command via UART:", command)

            # Log the action
            log_data = {
                "username": payload.get("username"),
                "locker_id": payload.get("locker_id"),
                "action": command,
                "timestamp": now.isoformat()
            }
            if check_internet():
                if not log_to_server(log_data):
                    log_locally(log_data)
            else:
                log_locally(log_data)

        except Exception as e:
            print("Error processing QR code:", e)

    # Optionally display the video stream for debugging purposes
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Process local logs
    process_logs()

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()