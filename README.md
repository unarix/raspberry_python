# raspberry_python

## Uso de ds9208 zebra scanner en Raspberry PI 1
Este proyecto permite el uso del scanner zebra symbol DS9208 con un raspberry pi1 (sobre debian linux). Ante el evento del barcodereader dispara los siguientes checks:

_This project allows the use of the zebra symbol DS9208 scanner with a raspberry pi1 (on debian linux). In the event of the barcodereader it triggers the following checks:_

- Si sensor de ocupación == 'False'
- Validar largo del código leído > 16
- Validar que sea un código (M1/M2/M3)
- Validar contra API
- Respuesta OK permitir el paso
- Otros

### Features:
- Barcode Zebra scanner PDF417 support -> OK
- Decode barcode ascii -> OK 
- Suppont for GPIO interface IN/OUT -> OK
- Obtain status sensro occupancy -> OK
- Permitir el paso _open the door_ -> OK
- Call api REST -> OK

## GPIO Connections:
- Puerta / Gate:
- >N: PIN 6
- >P: PIN 11

- Ocupación / Sensor:
- >N: PIN 1
- >P: PIN 10

## Referencia de conectores _Connectors Reference_:

![alt text](https://raspberrypihq.com/wp-content/uploads/2018/01/a-and-b-physical-pin-numbers.png)

## Uso _Use_:

>$ python fotoread.py

## Script de inicializaion _Initialization script_:

**Crear el script y agregar al archivo:**
_Create the script and add to the file:_

>$ nano launcher.sh
```
    #!/bin/sh
    # launcher.sh
    cd /
    cd home/pi/
    python fotoread.py
    cd/
```
**Permitir que sea ejecutable:**
_Allow it to be executable:_

>$ chmod 755 launcher.sh

**Iniciar en el startup:**
_Launch at startup_

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
