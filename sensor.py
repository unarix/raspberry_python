# Install dependence: $ sudo apt-get install python-rpi.gpio python3-rpi.gpio
# reference: https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/ + https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")