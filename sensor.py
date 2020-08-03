# Install dependence: $ sudo apt-get install python-rpi.gpio python3-rpi.gpio
# Reference: https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/ + https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input of fotopoc sensor, if pin 10 is HIGH a person is located between the way
GPIO.setup(11, GPIO.OUT) # Set pin 11 to be an output, this is only for test, turn on a led.


while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        GPIO.output(11,GPIO.HIGH)
        print "HAY UNA PERSONA EN EL MEDIO"
    if GPIO.input(10) == GPIO.LOW:
        GPIO.output(11,GPIO.LOW)
        print "NO HAY NADIE, SE PUEDE OPERAR"