import Jetson.GPIO as GPIO
import time

# Setup
output_pin = 5  # Select the appropriate pin number
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

# Send a signal
try:
    while True:
        GPIO.output(output_pin, GPIO.HIGH)  # Signal on
        time.sleep(1)
        GPIO.output(output_pin, GPIO.LOW)  # Signal off
        time.sleep(1)
finally:
    GPIO.cleanup()  # Clean up
