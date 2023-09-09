import evdev

# Replace '/dev/input/eventX' with the actual event path of your QR code scanner
device = evdev.InputDevice('/dev/input/event5')

qr_code_data = ''

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)
        if key_event.keystate == key_event.key_up:
            if key_event.keycode == 'KEY_ENTER':
                if qr_code_data:  # Ignore empty scans
                    data = qr_code_data.split("LEFTSHIFT")
                    data1 = "".join(data)
                    data2 = data1.split("MINUS")
                    data3 = "-".join(data2)
                    data4 = data3.split("DOT")
                    data5 = ".".join(data4)
                    print("Scanned QR Code:", data5)
                qr_code_data = ''
            else:
                qr_code_data += key_event.keycode[4:]

