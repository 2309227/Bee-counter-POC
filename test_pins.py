import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Default LOW

prev_state = GPIO.input(11)  # initial state

while True:
    current_state = GPIO.input(11)

    # Trigger only when it changes from HIGH to LOW
    if prev_state == GPIO.HIGH and current_state == GPIO.LOW:
        print("Contact lost!")  # or whatever you want to do

    prev_state = current_state
    time.sleep(0.05)  # small delay to reduce CPU usage
