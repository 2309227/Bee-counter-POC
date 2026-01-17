# POC to count trigger events and save time stamped data to CSV file

# Import necessary libraries
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ledTrigger = "/sys/class/leds/ACT/trigger"
ledBrightness = "/sys/class/leds/ACT/brightness"

# Wait until the pin is HIGH before starting
os.system(f"echo none | sudo tee {ledTrigger}")

print("Waiting for pin 11 to go HIGH to start...")

while GPIO.input(11) != GPIO.HIGH:
    os.system(f"echo 0 | sudo tee {ledBrightness}")
    time.sleep(0.05)
print("Pin is HIGH, starting detection...")

os.system(f"echo 1 | sudo tee {ledBrightness}")
prev_state = GPIO.input(11)


# Main driver function
def main():

    # Infanitie loop
    while True:

        run = CheckTrigger()
        if run:
            Currtime = GetTimestamp()
            start = time.time_ns()
            SaveToFile(Currtime)
            end = time.time_ns()

            print(end - start)


# Trigger function (Button)
def CheckTrigger():
    global prev_state  # allow modifying the global variable

    current_state = GPIO.input(11)
    triggered = False

    # Trigger only once when pin goes from HIGH to LOW
    if prev_state == GPIO.HIGH and current_state == GPIO.LOW:
        os.system(f"echo 0 | sudo tee {ledBrightness}")
        triggered = True
        print("Contact lost!")  # single output

    elif current_state == GPIO.HIGH:
        os.system(f"echo 1 | sudo tee {ledBrightness}")

    prev_state = current_state
    return triggered


# Function to save last 10 items in q to file (CSV or TXT)
def SaveToFile(Savedstring):

    with open("log.csv", "a") as f:
        f.write(Savedstring + "\n")

    # with open("log.txt", "a") as f:
    # for each item in que or just passed in value
    #    f.write(Savedstring)


# Function to get current timestamp (Will need modification for RTC use)
def GetTimestamp():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# Call main function
main()
