import RPi.GPIO as GPIO
import time
import smbus
# Set the GPIO mode and specify the pin number


# Set up the GPIO pin as output
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On
ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
bus = smbus.SMBus(1)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

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
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


# Function to unlock the door (rotate the servo)
def unlock_door():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    try:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(1)  # Wait for 1 second to allow the servo to move
        GPIO.output(17, GPIO.LOW)
        time.sleep(1)  # Wait for 1 second
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()  # Clean up GPIO configuration

def get_user_input():
    # Prompt the user for the password
    user_input = input("Enter the password to unlock the door: ")
    return user_input

if __name__ == "__main__":
    try:
        # Replace "your_password" with your actual password
        correct_password = "123"
        lcd_init()
        while True:
            user_password = "123"

            if user_password == correct_password:
                lcd_string("Password correct",LCD_LINE_1)
                lcd_string("Unlocking door...",LCD_LINE_2)
                unlock_door()
                time.sleep(3)
                lcd_string("Unlocked", LCD_LINE_2)
            else:
                lcd_string("Password incorrect. Access denied.",LCD_LINE_1)
    except KeyboardInterrupt:
        pass

