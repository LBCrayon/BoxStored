import evdev
from evdev import InputDevice
import time
import RPi.GPIO as GPIO
from threading import Thread
import threading


def unlock_door1():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    try:
        GPIO.output(21, GPIO.HIGH)
        time.sleep(5)  # Wait for 1 second to allow the servo to move
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()  # Clean up GPIO configuration


def unlock_door2():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    try:
        GPIO.output(20, GPIO.HIGH)
        time.sleep(5)  # Wait for 1 second to allow the servo to move
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()


def unlock_doorAll():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    try:
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(5)  # Wait for 1 second to allow the servo to move
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()


device = evdev.InputDevice('/dev/input/event5')


def main():
    qr_code_data = ''
    key = ''
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == key_event.key_up:
                if key_event.keycode == 'KEY_ENTER':
                    if qr_code_data:
                        data = qr_code_data.split("LEFTSHIFT")
                        print("data", data)
                        dataDecode_ver1 = "".join(data)
                        dataDecode_ver2 = dataDecode_ver1.split("MINUS")
                        dataDecode_ver3 = "-".join(dataDecode_ver2)
                        dataDecode_ver4 = dataDecode_ver3.split("DOT")
                        dataDecode_ver5 = ".".join(dataDecode_ver4)
                        print("dataDecode_ver5", dataDecode_ver5)
                        dataDecode_ver6 = dataDecode_ver5.split("COMMA")
                        dataDecode_ver7 = "".join(dataDecode_ver6)
                        value_qrcode1 = dataDecode_ver7[11:47]
                        value_qrcode2 = dataDecode_ver7[58:]
                        value_key = dataDecode_ver7[0:6]
                        box1 = "44D26E21-58E5-40A6-961D-34DA1D0EDF27"
                        box2 = "5D2D4E6E-1E25-4B38-B803-6FC661AE9EF3"
                        if value_qrcode1 == box1 and value_qrcode2 == '' and key == value_key:
                            unlock_door1()
                            print("Box 1 Unlocked")
                            qr_code_data = ''
                            key = ''
                        elif value_qrcode1 == box2 and value_qrcode2 == '' and key == value_key:
                            unlock_door2()
                            print("Box 2 unlocked")
                            qr_code_data = ''
                            key = ''
                        if value_qrcode1 == box1 and value_qrcode2 == box2:
                            unlock_doorAll()
                            qr_code_data = ''
                            print("All Box Unlocked")
                        else:
                            print("Unlock failed")
                else:
                    qr_code_data += key_event.keycode[4:]


if __name__ == "__main__":
    main()
