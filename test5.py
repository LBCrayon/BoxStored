import evdev
from evdev import InputDevice
import smbus
import time
import RPi.GPIO as GPIO
import requests

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
        time.sleep()  # Wait for 1 second to allow the servo to move
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()  # Clean up GPIO configuration


# Replace '/dev/input/eventX' with the actual event path of your QR code scanner
device = evdev.InputDevice('/dev/input/event5')


def main():
    Box1 = "44D26E21-58E5-40A6-961D-34DA1D0EDF27"
    global bus
    bus = smbus.SMBus(1)
    lcd_init()
    lcd_string("Scanning...", LCD_LINE_1)
    qr_code_data = ''
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == key_event.key_up:
                if key_event.keycode == 'KEY_ENTER':
                    if qr_code_data:  # Ignore empty scans
                        print("Scanned QR Code:", qr_code_data)
                        data = qr_code_data.split("LEFTSHIFT")
                        data1 = "".join(data)
                        data2 = data1.split("MINUS")
                        data3 = "-".join(data2)
                        data4 = data3.split("DOT")
                        data5 = ".".join(data4)
                        data6 = data5[11:]
                        qr_code_data == Box1
                    print("Scanned QR Code:", data6)
                    if qr_code_data == Box1:
                        print("Box unlocked successfully!")
                        lcd_string("Unlocked", LCD_LINE_1)
                        time.sleep(1)
                        unlock_door()
                        lcd_string("Locked", LCD_LINE_1)
                    else:
                        print("Box unlock failed")
                        lcd_string("Access denied.", LCD_LINE_1)
                        bus.close()
                        time.sleep(1)
                else:

                    qr_code_data += key_event.keycode[4:]


if __name__ == "__main__":
    main()
