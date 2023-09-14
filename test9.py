import evdev
import RPi.GPIO as GPIO
import time


def unlock_door(door_number=None):
    GPIO.setmode(GPIO.BCM)
    try:
        if door_number == 1:
            GPIO.setup(21, GPIO.OUT)
            GPIO.output(21, GPIO.HIGH)
        elif door_number == 2:
            GPIO.setup(20, GPIO.OUT)
            GPIO.output(20, GPIO.HIGH)
        elif door_number is None or door_number == "all":
            GPIO.setup(20, GPIO.OUT)
            GPIO.setup(21, GPIO.OUT)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.HIGH)
        else:
            print("Door number is not valid.")
            return
        time.sleep(5)  # Wait for 5 seconds to allow the servo to move
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Clean up GPIO configuration


def process_qr_code(qr_code_data):
    key1 = ''
    key2 = ''
    key3 = ''
    role1 = "1"
    role2 = '2'
    box1 = "FCFC113E-69F6-423D-A456-AFF04D6F4AFF"
    box2 = "56518C02-55CD-446C-AC92-0825F7997485"
    data = qr_code_data.split("LEFTSHIFT")
    data = "".join(data).split("MINUS")
    data = "-".join(data).split("DOT")
    data = ".".join(data).split("COMMA")
    data = "".join(data)
    value_qrcode1 = data[24:60]
    print("value_qrcode1", value_qrcode1)
    value_qrcode2 = data[60:]
    print("value_qrcode2", value_qrcode2)
    key1 = data[2:12]
    print("value_key1", key1)
    key2 = data[2:12]
    print("value_key2", key2)
    key3 = data[0:1]
    print("value_key3", key3)
    if value_qrcode1 == box1 and value_qrcode2 == '' and key1 == key2 and key3 == role1:
        unlock_door(1)
        print("Box 1 Unlocked")
    elif value_qrcode1 == box2 and value_qrcode2 == '' and key1 == key2 and key3 == role1:
        unlock_door(2)
        print("Box 2 Unlocked")
    elif value_qrcode1 == box1 and value_qrcode2 == box2 and key3 == role2:
        unlock_door("all")
        print("All Boxes Unlocked")
        key2 = ''
        key3 = ''
    else:
        print("Unlock failed")


def main():
    device = evdev.InputDevice('/dev/input/event6')
    qr_code_data = ''

    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == key_event.key_up:
                if key_event.keycode == 'KEY_ENTER':
                    if qr_code_data:
                        process_qr_code(qr_code_data)
                    qr_code_data = ''
                else:
                    qr_code_data += key_event.keycode[4:]


if __name__ == "__main__":
    main()
