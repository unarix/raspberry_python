# Raspberry_Python (boarding access control)

## Use of DS9208 Zebra scanner on Raspberry PI 1

Este proyecto permite el uso del scanner zebra symbol DS9208 con un raspberry pi1 (sobre debian linux). Ante el evento del barcodereader dispara los siguientes checks:

_This project allows the use of the zebra symbol DS9208 scanner with a raspberry pi1 (on debian linux). In the event of the barcodereader it triggers the following checks:_

- if occupancy sensor == 'False'
- Validate lenght code > 16
- Validate code type (M1/M2/M3)
- Validate code with API
- Response OK allow enter
- others

### Features:
- Barcode Zebra scanner PDF417 support -> OK
- Decode barcode ascii -> OK 
- Suppont for GPIO interface IN/OUT -> OK
- Obtain status sensro occupancy -> OK
- Open door -> OK
- Call api REST -> OK

## GPIO Connections:
- To the gate:
- >N: PIN 6
- >P: PIN 11

- To the occupancy sensor:
- >N: PIN 1
- >P: PIN 10

## Connectors Reference:

![alt text](https://raspberrypihq.com/wp-content/uploads/2018/01/a-and-b-physical-pin-numbers.png)

## How to use:

>$ python fotoread.py

## Initialization script:

**Create the script and add to the file:**

>$ nano launcher.sh
```
    #!/bin/sh
    # launcher.sh
    cd /
    cd home/pi/
    python fotoread.py
    cd/
```

**Allow it to be executable:**

>$ chmod 755 launcher.sh

**Launch at startup**

>$ sudo nano /home/pi/.bashrc

```
    echo Iniciando fotopoc
    sh /home/pi/launcher.sh
```

## Links / Doc:

    Gpio:
    https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins

    Scanner model:
    https://www.zebra.com/content/dam/zebra_new_ia/en-us/manuals/barcode-scanners/ds9208-prg-en.pdf

    BarcodeReader:
    https://github.com/vpatron/barcode_scanner_python
