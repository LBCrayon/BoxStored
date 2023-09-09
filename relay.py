
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.OUT)
while True:     
        GPIO.output(21, True)
        time.sleep(2)  # Wait for 1 second to allow the servo to move
      
        GPIO.output(21, False)
        time.sleep(2)  # Wait for 1 second
        
# Clean up GPIO configuration

