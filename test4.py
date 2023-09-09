import evdev
from evdev import InputDevice
import smbus
import time
import RPi.GPIO as GPIO
import requests
import re
# Barcode scanner setup

# Set up the GPIO pin as output
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
bus = smbus.SMBus(1)


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Function to unlock the door (rotate the servo)


def unlock_door():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    try:
        GPIO.output(21, GPIO.HIGH)
        time.sleep(1)  # Wait for 1 second to allow the servo to move
        GPIO.output(21, GPIO.LOW)
        time.sleep(1)  # Wait for 1 second
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()  # Clean up GPI


# Replace '/dev/input/eventX' with the actual event path of your QR code scanner
device = evdev.InputDevice('/dev/input/event5')
qr_code_data = ''


def scan_QR_code(qr_code_data):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == key_event.key_up:
                if key_event.keycode == 'KEY_ENTER':
                    print("Scanned QR Code:", qr_code_data)
                    qr_code_data = ''
                else:
                    qr_code_data += key_event.keycode[4:]


base_api_url = "https://dev.fine-api.smjle.vn/api/admin/box"


def main():
    global bus
    bus = smbus.SMBus(1)

    lcd_init()
    lcd_string("Scanning...", LCD_LINE_1)
    response = requests.post(base_api_url, json=qr_code_data)
    print("response", response)
    if response.status_code == 200:
        print("Barcode sent to API successfully!")
        unlock_door()
        lcd_string("Unlocking door...", LCD_LINE_1)
        lcd_string("Waiting for check your barcode...", LCD_LINE_2)
        time.sleep(2)
        lcd_string("Unlocked", LCD_LINE_2)
    else:
        print("Failed to send barcode to API.")
        lcd_string("Access denied.", LCD_LINE_1)
        bus.close()
        time.sleep(2)


if __name__ == "__main__":
    main()
