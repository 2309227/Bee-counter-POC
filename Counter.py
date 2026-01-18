# POC to count trigger events and save time stamped data to CSV file

# Import necessary libraries
import time
import os

# Import and set up relevent GPIO pins on Pi
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Paths for system calls to control built in LED
ledTrigger = "/sys/class/leds/ACT/trigger"
ledBrightness = "/sys/class/leds/ACT/brightness"


def TurnLEDOn():
    with open(ledBrightness, "w") as f:
        f.write("1")


def TurnLEDOff():
    with open(ledBrightness, "w") as f:
        f.write("0")


# Wait until the pin is HIGH before starting
os.system(f"echo none | sudo tee {ledTrigger} > /dev/null")

# Loop until pin 11 is high
while GPIO.input(11) != GPIO.HIGH:
    TurnLEDOff()
    time.sleep(0.05)

TurnLEDOn()

prev_state = GPIO.input(11)


# Trigger function
def CheckTrigger():
    global prev_state

    current_state = GPIO.input(11)
    triggered = False

    # Trigger only once when pin goes from HIGH to LOW
    if prev_state == GPIO.HIGH and current_state == GPIO.LOW:
        TurnLEDOff()
        triggered = True

    # If voltage is detected turn on LED
    elif current_state == GPIO.HIGH:
        TurnLEDOn()

    prev_state = current_state
    return triggered


# Function to save passed in string to CSV file
def SaveToFile(Savedstring):
    with open("log.csv", "a") as f:
        f.write(Savedstring + "\n")


# Function to get current timestamp (Will need modification for RTC use)
def GetTimestamp():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# Main driver function
def main():

    # Infanitie loop
    while True:
        # Check if IR has been tripped
        run = CheckTrigger()
        if run:
            Currtime = GetTimestamp()  # Get time stamp
            SaveToFile(Currtime)  # Save time stamp to csv file


# Call main function
if __name__ == "__main__":
    main()
