import sys
import requests
import json


# if __name__ == '__main__':
#     try:
#             response = requests.get("https://prod.fine-api.smjle.vn/api/product")
#             print(response.text)
#     except KeyboardInterrupt:
#         pass

# import evdev
# from evdev import InputDevice
# import smbus
# import time
# import requests  # Import the requests library

# # Barcode scanner setup
# scanner_path = "/dev/input/eventX"  # Replace X with the appropriate event number

# # API endpoint URL
# api_url = "https://your-api-url.com/barcode"

# def listen_for_scan(scanner_path):
#     scanner = InputDevice(scanner_path)
#     barcode_data = ""

#     try:
#         for event in scanner.read_loop():
#             if event.type == evdev.ecodes.EV_KEY:
#                 key_event = evdev.categorize(event)
#                 if key_event.keystate == key_event.key_down:
#                     if key_event.keycode == 'KEY_ENTER':
#                         if barcode_data:
#                             return barcode_data
#                     else:
#                         barcode_data += key_event.keycode
#     except KeyboardInterrupt:
#         pass

# def send_to_api():
#     data = {"code": 7191100001}
#     response = requests.post("https://prod.fine-api.smjle.vn/api/product", json = data)
#     if response.status_code == 200:
#         print("Barcode sent to API successfully!")
#     else:
#         print("Failed to send barcode to API.")

# def main():
#     # Send the scanned barcode to the API
#     send_to_api()

# if __name__ == "__main__":
#     main()


# # URL to which you want to send the POST request
# if __name__ == '__main__':

#     url = "https://localhost:7058/api/box"

# # Data to send in the POST request (if needed)
# data = {
#     "code": "7191100001"
# }
# headers = {
#     "Content-Type": "application/json"  # Or the appropriate content type
# }
# # Sending the POST request
# response = requests.post(url, data=data, headers=headers)

# # Checking the response
# if response.status_code == 200:
#     print("Request was successful")
#     print("Response content:", response.text)
# else:
#     print("Request failed with status code:", response.status_code)

url = "https://dev.fine-api.smjle.vn/api/admin/box"  # Example API endpoint

data = {
    "code": "719100001"
}

response = requests.post(url, json=data)

if response.status_code == 200:  # 201 Created status code
    print("Post created successfully!")
    # print("Response content:", response.json())
    print("Response :", response.text)
else:
    print("Request failed with status code:", response.status_code)
